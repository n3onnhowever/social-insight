import streamlit as st
import pandas as pd

# Загрузка датасета из CSV файла
@st.cache
def load_data(filename):
    df = pd.read_csv(filename)
    return df

# Функция для анализа текста
def analyze_text(text):
    # Здесь должен быть ваш код для анализа текста
    # Например, если у вас есть модель машинного обучения, вы можете использовать ее здесь
    # Вернем просто заглушку
    return "Категория текста: Примерная"

# Главный код Streamlit
def main():
    st.title('Веб-сервис анализа данных и текстов')
    
    # Добавляем пользовательские стили для создания синего градиента
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(to right, #33ccff, #0077b3);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Опции для выбора вкладок
    options = ['Аналитика данных', 'Проверка модели']
    choice = st.sidebar.selectbox('Выберите вкладку', options)
    
    # Отображение соответствующей вкладки
    if choice == 'Аналитика данных':
        # Загрузка данных из CSV файла
        filename = st.file_uploader("Загрузите ваш файл CSV", type=['csv'])
        if filename is not None:
            df = load_data(filename)
            # Выводим датасет
            st.subheader('Датасет:')
            st.write(df)
            
            # Выводим статистику по датасету
            st.subheader('Статистика по датасету:')
            st.write(df.describe())
    elif choice == 'Проверка модели':
        st.subheader('Введите текст для анализа:')
        text_input = st.text_area('Введите текст сюда:')
        if st.button('Анализировать'):
            if text_input:
                category = analyze_text(text_input)
                st.write('Категория текста:', category)
            else:
                st.write('Пожалуйста, введите текст для анализа')

if __name__ == '__main__':
    main()
