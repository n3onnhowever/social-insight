# Используем базовый образ Python
FROM python:3.11

# Устанавливаем зависимости
RUN pip install streamlit pandas transformers torch matplotlib seaborn datetime

# Копируем исходный код в контейнер
COPY . /app

COPY model /app/model

# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем приложение
CMD ["streamlit", "run", "web.py"]