import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import subprocess

# Загрузка библиотек из файла requirements.txt
with open('requirements.txt') as f:
    requirements = f.readlines()
requirements = [x.strip() for x in requirements]

# Установка библиотек
for requirement in requirements:
    st.write(f'Установка {requirement}')
    subprocess.run(['pip', 'install', requirement])

# Симулируем данные
data = pd.DataFrame({
    'Category': np.random.choice(['Technology', 'Science', 'Art'], 100),
    'Date': pd.date_range(start='2024-01-01', end='2024-03-07', periods=100),
    'Likes': np.random.randint(0, 100, 100),
    'Reposts': np.random.randint(0, 50, 100),
    'Views': np.random.randint(0, 500, 100),
    'Comments': np.random.randint(0, 30, 100)
})

# Страница "Дашборд"
def dashboard():
    st.header("Дашборд")
    
    # Выбор категории
    category = st.sidebar.selectbox("Выберите категорию", data['Category'].unique())
    
    # Фильтрация данных по выбранной категории и дате
    filtered_data = data[(data['Category'] == category) & (data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    # Графики
    st.subheader("Статистика постов")
    st.write(filtered_data)
    
    # Графики
    fig = px.bar(filtered_data, x='Date', y=['Likes', 'Reposts', 'Views', 'Comments'], title='Статистика постов')
    st.plotly_chart(fig)
    
    # График категорий
    st.subheader("Общее количество просмотров по категориям")
    views_by_category = data.groupby('Category')['Views'].sum()
    st.bar_chart(views_by_category)

# Страница "Проверка модели"
def model_check():
    st.header("Проверка модели")
    
    # Текстовое поле для ввода текста
    text_input = st.text_input("Введите текст")
    
    # Кнопка отправки
    if st.button("Отправить"):
        # Здесь должен быть код для предсказания категории по тексту
        predicted_category = np.random.choice(['Technology', 'Science', 'Art'])
        st.write("Предсказанная категория:", predicted_category)

# Навигационное меню
page = st.sidebar.radio("Переход к страницам", ("Дашборд", "Проверка модели"))

if page == "Дашборд":
    st.title("Дашборд")
    start_date = st.sidebar.date_input("Выберите начальную дату", min_value=pd.to_datetime('2024-01-01'), max_value=pd.to_datetime('2024-03-06'))
    end_date = st.sidebar.date_input("Выберите конечную дату", min_value=pd.to_datetime('2024-01-02'), max_value=pd.to_datetime('2024-03-07'), value=pd.to_datetime('2024-03-07'))
    dashboard()
elif page == "Проверка модели":
    st.title("Проверка модели")
    model_check()
