# Documentação da API - PETR4 Forecast

A API foi construída em **FastAPI** e serve para gerar previsões de preço da ação **PETR4.SA** utilizando o modelo **Prophet**.  
O modelo carregado é registrado e versionado via **MLflow**.

---

## Base URL
http://localhost:8000

---

## Endpoints

### 1. `GET /health`

Verifica se a API está ativa.

**Requisição:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Resposta:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. `POST /predict`
Gera previsões de preço para os próximos **N dias.**

**Parâmetros**

- `days`: número de dias a prever.
- Deve ser **inteiro positivo.**

**Requisição**
```bash
curl -X POST "http://localhost:8000/predict?days=30"
```

**Resposta:**
```json
[
  {"ds": "2025-09-01", "yhat": 32.54},
  {"ds": "2025-09-02", "yhat": 32.61},
  {"ds": "2025-09-03", "yhat": 32.73},
]
```

3. **Exemplos de Uso**

**Python (requests)**
```python
import requests

BASE_URL = "http://localhost:8000"

# Checar status
health = requests.get(f"{BASE_URL}/health").json()
print("Status:", health)

# Fazer previsão de 15 dias
response = requests.post(f"{BASE_URL}/predict?days=15")
forecast = response.json()
print("Previsões:", forecast[:5])
```

**JavaScript (fetch)**
```javascript
const BASE_URL = "http://localhost:8000";

async function getPrediction(days = 10) {
  const response = await fetch(`${BASE_URL}/predict?days=${days}`, {
    method: "POST"
  });
  const data = await response.json();
  console.log("Previsões:", data);
}

getPrediction(10);
```

**Tratamento de Erros**
Exemplo: `days <= 0`

```bash
curl -X POST "http://localhost:8000/predict?days=-5"
```

**Resposta:**
```json
{
  "error": "Number of days must be positive"
}
```

**Exemplo: Modelo não encontrado**
Se o arquivo de modelo não for encontrado no container da API, será retornado:
```json
{
  "error": "Model file not found"
}
```

**Observações**
- O modelo usado é sempre o último **registrado no MLflow** e baixado para o container da API.
- Logs de previsões são armazenados em:
  - Arquivo: predictions.log
  - MLflow: experimento petr4_forecast_api