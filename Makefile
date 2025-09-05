.PHONY: build train api mlflow up down logs restart

# Constrói todas as imagens
build:
	docker-compose build

# Executa o treinamento
train:
	docker-compose run --rm training

# Sobe apenas a API em background
api:
	docker-compose up -d api

# Sobe apenas o MLflow em background
mlflow:
	docker-compose up -d mlflow

# Sobe API + MLflow em background
up:
	docker-compose up -d api mlflow

# Derruba todos os serviços e remove volumes
down:
	docker-compose down -v

# Mostra os logs em tempo real
logs:
	docker-compose logs -f

# Reinicia todo o ambiente (API + MLflow)
restart: down up
