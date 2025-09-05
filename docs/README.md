## Previsão de fechamento PETR4-SA

## Pós Tech -  MACHINE LEARNING ENGINEERING

Prova Substitutiva Fase 5 - FIAP

## Introdução
Este projeto implementa um pipeline de **previsão de séries temporais** para a ação **PETR4.SA** utilizando o modelo **Prophet**, com deploy via **FastAPI** e monitoramento com **MLflow**.  

## Tecnologias
- [Prophet](https://facebook.github.io/prophet/) - modelo de séries temporais
- [FastAPI](https://fastapi.tiangolo.com/) - API de produção
- [MLflow](https://mlflow.org/) - rastreamento e registro de modelos
- [Docker + docker-compose](https://docs.docker.com/) - ambientes isolados
- [Makefile](https://www.gnu.org/software/make/manual/make.html) - automação de comandos

## Etapas:

1. Construir os containers

```bash 
make build
```

2. Treinar o modelo
```bash
make train
```
- Baixa dados de PETR4.SA via yfinance
- Treina um modelo Prophet
- Avalia no conjunto de teste 
- Registra modelo e métricas no MLflow

3. Deploy da API
```bash
make api
```
- URL: http://localhost:8000/docs

4. Deploy MLflow UI
```bash
make mlflow
```
- URL: http://localhost:5000

5. Endpoints
- POST /predict
Recebe um número de dias e retorna previsões.
**Exemplo:**
```bash
curl -X POST "http://localhost:8000/predict?days=30"
```
**Resposta:**
```json
[
  {"ds": "2025-09-01", "yhat": 32.54},
  {"ds": "2025-09-02", "yhat": 32.61},
]
```
- GET /health
Verifica status da API.

6. Monitoramento
- **Treinamento:** métricas (MAE, RMSE, MAPE) registradas no MLflow (petr4_forecast)
- **API:** logs de uso e previsões armazenados em predictions.log e também no MLflow (petr4_forecast_api)
