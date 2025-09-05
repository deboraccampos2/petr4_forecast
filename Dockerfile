# Base image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Evitar prompts do apt
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema necessárias para Prophet e matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libcurl4-openssl-dev \
    libssl-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt se tiver ou instalar direto
# Aqui instalamos direto os pacotes necessários
RUN pip install --upgrade pip
RUN pip install \
    pandas \
    numpy \
    matplotlib \
    scikit-learn \
    yfinance \
    prophet \
    mlflow \
    fastapi \
    uvicorn[standard]

# Copiar todo o código para dentro do container
COPY . /app

# Dar permissão de execução para o script de espera
RUN chmod +x wait_and_start.sh

# Default command (não usado no training, será sobrescrito no doc