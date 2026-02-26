FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем зависимости
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY app/ .

# Команда запуска
CMD ["python", "main.py"]