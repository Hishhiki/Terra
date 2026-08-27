FROM python:3.11-slim-bookworm

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . .

# Порт для веб-интерфейса FastAPI
EXPOSE 8000

# Запуск FastAPI шлюза
CMD ["python", "-m", "services.api_gateway.main"]
