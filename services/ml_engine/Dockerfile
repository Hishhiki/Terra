FROM python:3.11-slim-bookworm

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Порт для gRPC
EXPOSE 50051

# Запуск ML gRPC сервера
CMD ["python", "-m", "services.ml_engine.main"]
