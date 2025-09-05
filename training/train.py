import yfinance as yf
import pandas as pd
import mlflow
import mlflow.pyfunc
from prophet import Prophet
from prophet.serialize import model_to_json
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

mlflow.set_experiment("petr4_forecast")

def download_data(symbol="PETR4.SA", start="2018-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    print(f"Baixando dados de {symbol} de {start} até {end}...")
    data = yf.download(symbol, start=start, end=end, multi_level_index=False)
    if data.empty:
        raise ValueError(f"Nenhum dado retornado para {symbol}. "
                         f"Verifique o ticker ou o período.")

    data.reset_index(inplace=True)
    df = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    df['ds'] = pd.to_datetime(df['ds'], utc=True).dt.tz_localize(None)
    print(f"Dados baixados: {len(df)} linhas")

    if df.empty:
        raise ValueError("Dataset ficou vazio após limpeza.")

    return df

def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return mae, rmse, mape

def plot_forecast(train, test, forecast, output_path):
    plt.figure(figsize=(10, 6))
    plt.plot(train['ds'], train['y'], label="Treino")
    plt.plot(test['ds'], test['y'], label="Teste", color="orange")
    plt.plot(forecast['ds'], forecast['yhat'], label="Previsão", color="green")
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'],
                     color="lightgreen", alpha=0.4)
    plt.legend()
    plt.title("Previsão Prophet - PETR4")
    plt.xlabel("Data")
    plt.ylabel("Preço de Fechamento")
    plt.savefig(output_path)
    plt.close()

def main():
    df = download_data()

    print(f"Dataset baixado: {len(df)} linhas")
    print(df.head())
    print(df.dtypes)

    if len(df) < 100:
        raise ValueError(f"Poucos dados ({len(df)}) disponíveis.")

    # Split
    train = df.iloc[:-60].copy()
    test = df.iloc[-60:].copy()

    # Garantir Series numérica
    train['y'] = pd.to_numeric(train['y'], errors='coerce')
    test['y'] = pd.to_numeric(test['y'], errors='coerce')

    train = train.dropna(subset=['y'])
    test = test.dropna(subset=['y'])

    print("=== Train sample ===")
    print(train.head())
    print(train.dtypes)
    print(train.shape)

    if train.empty or test.empty:
        raise ValueError("Treino ou teste ficaram vazios.")

    with mlflow.start_run(run_name="prophet_train"):
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        model.add_country_holidays(country_name='BR')

        print("Chamando model.fit(train)...")
        model.fit(train)

        future = model.make_future_dataframe(periods=len(test))
        forecast = model.predict(future)
        forecast_test = forecast.tail(len(test))

        # Avaliação
        mae, rmse, mape = evaluate_model(test['y'].values, forecast_test['yhat'].values)
        print(f"Métricas -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")

        # Log no MLflow
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)
        mlflow.log_param("changepoint_prior_scale", 0.05)

        # Salvar gráfico
        os.makedirs("plots", exist_ok=True)
        plot_path = "plots/forecast.png"
        plot_forecast(train, test, forecast, plot_path)
        mlflow.log_artifact(plot_path)

        # Serializar modelo Prophet
        os.makedirs("models", exist_ok=True)
        model_path = "models/prophet_model.json"
        with open(model_path, "w") as f:
            json.dump(model_to_json(model), f)
        mlflow.log_artifact(model_path)

        print("Treinamento concluído e artefatos salvos com sucesso.")

if __name__ == "__main__":
    main()