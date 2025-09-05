#!/bin/sh

MODEL_PATH="/app/models/prophet_model.json"
WAIT_TIME=0
MAX_WAIT=60  # aguarda até 60 segundos

echo "Aguardando modelo em $MODEL_PATH..."

while [ ! -f "$MODEL_PATH" ] && [ $WAIT_TIME -lt $MAX_WAIT ]; do
    echo "Modelo não encontrado, esperando 2 segundos..."
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
done

if [ ! -f "$MODEL_PATH" ]; then
    echo "Modelo não encontrado após $MAX_WAIT segundos. Abortando."
    exit 1
fi

echo "Modelo encontrado! Iniciando API..."
exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload