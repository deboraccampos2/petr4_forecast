from fastapi import FastAPI, HTTPException
import pandas as pd
import mlflow
import mlflow.pyfunc
import logging
from datetime import datetime
from prophet import Prophet
from prophet.serialize import model_from_json
import json
import os
import time

app = FastAPI()

logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Caminho local do modelo no container
MODEL_PATH = "/app/models/prophet_model.json"

# Espera pelo arquivo do modelo (até 30 segundos)
wait_time = 0
while not os.path.exists(MODEL_PATH) and wait_time < 30:
    logging.info(f"Aguardando modelo em {MODEL_PATH}...")
    time.sleep(2)
    wait_time += 2

try:
    # Carrega diretamente o Prophet
    with open(MODEL_PATH, "r") as f:
        model = model_from_json(json.load(f))
    logging.info("Modelo carregado com sucesso.")
except Exception as e:
    logging.error(f"Erro ao carregar modelo: {e}")
    raise RuntimeError("Falha ao carregar modelo.")

@app.post("/predict")
async def predict(days: int = 30):
    if days <= 0:
        raise HTTPException(status_code=400, detail="Número de dias deve ser maior que zero.")

    try:
        last_date = datetime.today()
        future_dates = pd.date_range(start=last_date, periods=days, freq="D")
        future_df = pd.DataFrame({"ds": future_dates})

        forecast = model.predict(future_df)
        predictions = forecast[['ds', 'yhat']].to_dict(orient="records")

        logging.info(f"Previsão realizada para {days} dias.")

        # Registrar no MLflow
        mlflow.set_experiment("petr4_forecast_api")
        with mlflow.start_run(run_name="api_prediction"):
            mlflow.log_param("request_days", days)
            mlflow.log_param("timestamp", datetime.now().isoformat())
            mlflow.log_metric("n_predictions", len(predictions))
            if predictions:
                mlflow.log_metric("yhat_first", predictions[0]['yhat'])
                mlflow.log_metric("yhat_last", predictions[-1]['yhat'])

        return predictions

    except Exception as e:
        logging.error(f"Erro na previsão: {e}")
        raise HTTPException(status_code=500, detail="Erro ao realizar previsão.")

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}