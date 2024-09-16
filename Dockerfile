# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файли залежностей
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо решту файлів проекту
COPY bizmodelai /app/bizmodelai
COPY static /app/static

# Відкриваємо порт 8000
EXPOSE 8000

# Запускаємо додаток
CMD ["python", "-m", "bizmodelai.main"]