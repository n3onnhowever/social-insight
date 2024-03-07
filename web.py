import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка вашего набора данных
df = pd.read_csv("ваш_набор_данных.csv")

# Определение функций для анализа
def plot_topic_distribution(df, topic_column):
    """
    Визуализация распределения тем.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x=topic_column, data=df, palette='Set3')
    plt.title('Распределение тем')
    plt.xlabel('Тема')
    plt.ylabel('Количество')
    st.pyplot(plt)

def plot_sentiment_distribution(df, sentiment_column):
    """
    Визуализация распределения тональностей.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(x=sentiment_column, data=df, palette='Set2')
    plt.title('Распределение тональностей')
    plt.xlabel('Тональность')
    plt.ylabel('Количество')
    st.pyplot(plt)

# Отображение базовых статистических данных
st.title('Анализатор текстовых данных')
st.write(df.describe())

# Отображение первых нескольких строк набора данных
st.subheader('Первые несколько строк набора данных')
st.write(df.head())

# Визуализация распределения тем
st.subheader('Распределение тем')
plot_topic_distribution(df, 'Type')

# Визуализация распределения тональностей
st.subheader('Распределение тональностей')
plot_sentiment_distribution(df, 'Sentiment')

# Очистка
for variable in dir():
    if variable[0:2] != "__":
        del globals()[variable]
del variable
