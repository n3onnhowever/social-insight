import streamlit as st
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from datetime import datetime
import base64
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data(filename):
    df = pd.read_csv(filename)
    return df

@st.cache_data
def image_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_string});
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

image_local('background.png')

def format_date_ru(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    month_names = {
        1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
        7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
    }
    formatted_date_time = date_obj.strftime(f"%d {month_names[date_obj.month]} %H:%M")
    return formatted_date_time

def plot_ratings_by_resource(df, category):
    filtered_df = df[df['Predicted'] == category]
    grouped_df = filtered_df.groupby('Resource_Name')['Rating'].mean().reset_index()

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Resource_Name', y='Rating', data=grouped_df, palette='viridis')
    plt.xlabel('')
    plt.ylabel('')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(True)
    plt.gca().spines['bottom'].set_visible(True)
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.savefig('rating_plot.png', bbox_inches='tight', transparent=True)
    st.image('rating_plot.png')
    plt.close()

def load_model_and_tokenizer(model_name_or_path):
    tokenizer = BertTokenizer.from_pretrained(model_name_or_path)
    model = BertForSequenceClassification.from_pretrained(model_name_or_path)
    return tokenizer, model

label_to_category = {
    0: 'Здравоохранение',
    1: 'ЖКХ',
    2: 'Образование',
    3: 'Инфраструктура',
    4: 'Культура',
    5: 'Экология',
    6: 'Социальное обеспечение',
    7: 'Политика',
    8: 'Безопасность',
    9: 'Доступность товаров и услуг',
    10: 'Официальные заявления',
    11: 'Туризм',
    12: 'Факты'
}

def predict_category(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_label = torch.argmax(outputs.logits).item()
    
    predicted_category = label_to_category[predicted_label]
    return predicted_category

def main():
    model_name_or_path = "/app/model"
    tokenizer, model = load_model_and_tokenizer(model_name_or_path)

    filename = 'final_verse.csv'
    df = load_data(filename)

    df['Predicted'] = df['Text'].apply(lambda text: predict_category(text, tokenizer, model))

    df['Rating'] = ((df['Count_Positive_Reactions'] + df['Comments_Count'] + df['Reposts']) / df['Views']) * 1000

    st.title('Агрегатор новостей - Social Insight')
    st.subheader('')

    st.sidebar.image('logo_white.png', use_column_width=True)

    st.sidebar.header('Фильтры')
    category = st.sidebar.selectbox('Выберите категорию:', df['Predicted'].unique())
    resource_type = st.sidebar.selectbox('Выберите тип ресурса:', df['Resource_Name'].unique())

    cols = st.columns(2)

    with cols[0]:
        st.subheader('Средний рейтинг категорий по новостным ресурсам')
        st.markdown('Новостные ресурсы ВК:')
        st.markdown('- Архангельск онлайн')
        st.markdown('- Архангельск life')
        st.markdown('Новостные ресурсы Telegram:')
        st.markdown('- 29.ru')
        st.markdown('- Жесть Архангельск')

    with cols[1]:
        plot_ratings_by_resource(df, category)

    st.sidebar.header('Сортировка')
    sort_by = st.sidebar.selectbox('Сортировать по:', ['Просмотрам', 'Лайкам', 'Комментариям', 'Репостам', 'Рейтингу'])

    st.subheader('🔥 Самые обсуждаемые новости:')
    filtered_df = df[(df['Predicted'] == category) & (df['Resource_Name'] == resource_type)]

    if sort_by == 'Просмотрам':
        filtered_df = filtered_df.sort_values(by='Views', ascending=False).head(10)
    elif sort_by == 'Лайкам':
        filtered_df = filtered_df.sort_values(by='Count_Positive_Reactions', ascending=False).head(10)
    elif sort_by == 'Комментариям':
        filtered_df = filtered_df.sort_values(by='Comments_Count', ascending=False).head(10)
    elif sort_by == 'Репостам':
        filtered_df = filtered_df.sort_values(by='Reposts', ascending=False).head(10)
    elif sort_by == 'Рейтингу':
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False).head(10)

    for index, row in filtered_df.iterrows():
        post_text = row['Text']
        post_date = row['Data'] + ' ' + row['Time']
        formatted_date = format_date_ru(post_date)
        post_views = row['Views']
        post_likes = row['Count_Positive_Reactions']
        post_reposts = row['Reposts']
        post_comments = row['Comments_Count']
        post_rating = row['Rating']

        if post_rating >= 40:
            rating_color = "#32CD32"
        elif post_rating >= 20:
            rating_color = "#FF8C00"
        else:
            rating_color = "#B22222"

        st.markdown(f'<div style="position: relative; padding: 10px; background-color: rgba(4,20,61, 0.5); margin-bottom: 10px; border-radius: 10px; box-sizing: border-box; color: white;">'
                    f'<div style="position: absolute; top: 0; right: 0; background-color: {rating_color}; padding: 5px; border-radius: 5px;">Рейтинг: {post_rating:.2f}</div>'
                    f'<span style="color: #A0AEC0;">{formatted_date}</span><br>'
                    f'{post_text}<br>'
                    f'❤️ Лайки: {post_likes}          💬 Комментарии: {post_comments}          🔁 Репосты: {post_reposts}          👁‍🗨 Просмотры: {post_views}<br>'                
                    '</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()