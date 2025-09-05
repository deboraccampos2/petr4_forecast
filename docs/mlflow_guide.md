# Guia do MLflow - PETR4 Forecast

Este documento explica como utilizar o **MLflow** no projeto **PETR4 Forecast**, tanto para rastrear experimentos de treinamento quanto para gerenciar modelos em produção.

---

## Acessando o MLflow UI

Após subir o container:

```bash
make mlflow
```

URL: [mlflow](http://localhost:5000)

## Estrutura no MLflow

No projeto, foi utilizado dois experimentos principais:

1. `petr4_forecast`
- Contém todos os treinamentos feitos em training/train.py
- Registra:
  - Hiperparâmetros (ex: changepoint_prior_scale)
  - Métricas de avaliação (MAE, RMSE, MAPE)
  - Artefatos (modelo Prophet serializado, gráficos de previsão)

2. `petr4_forecast_api`
- Contém os logs de previsões realizadas pela API em produção
- Útil para monitorar o desempenho do modelo em ambiente real

**Fluxo de Treinamento**

1. Executar:
```bash
make train
```

2. O script `training/train.py`:
- Baixa os dados do Yahoo Finance
- Divide em treino/teste
- Treina modelo Prophet
- Avalia métricas
- Salva no MLflow Tracking
- Registra o modelo no **MLflow Model Registry**

**Visualizando Métricas**
- Na UI do MLflow:
- Vá até o experimento `petr4_forecast`
- Clique em uma execução
- Verifique:
  - `metrics:` MAE, RMSE, MAPE
  - `params:` hiperparâmetros usados
  - `artifacts:` arquivos gerados (modelo .json, gráficos)

**Gerenciamento de Modelos**
O **Model Registry** permite controlar versões e estados do modelo:
- Stages disponíveis:
  - `None:` modelo ainda não avaliado
  - `Staging:` modelo em testes
  - `Production:` modelo ativo em produção
  - `Archived:` modelo antigo desativado

**Promover um modelo para produção:**
1. Acesse a aba **Models** no MLflow UI
2. Escolha o modelo `ProphetModel`
3. Clique na versão desejada
4. Defina o stage como **Production**

**API em Produção**
- A API (`api/main.py`) está configurada para sempre carregar o modelo mais recente do **stage** `Production` no MLflow.
- Isso garante que a atualização do modelo seja **sem downtime**: basta promover no MLflow.