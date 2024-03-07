import streamlit as st
import pandas as pd

df_social_media = pd.read_csv("final_verse.csv")

# Функции для получения уникальных значений
def get_unique_seasons(df_data):
    unique_seasons = pd.to_datetime(df_data['Data']).dt.year.unique().tolist()
    seasons_modified = []
    for s, season in enumerate(unique_seasons):
        if s == 0:
            season = "Season " + str(season)
        seasons_modified.append(season)
    return seasons_modified

def get_unique_days(df_data):
    return df_data['Time'].dt.date.unique().tolist()

def get_unique_resources(df_data):
    return df_data['Resource_Name'].unique().tolist()

# Параметры страницы
st.set_page_config(layout="wide")

# Верхняя часть страницы
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Social Insight - анализ данных социальных медиа')
with row0_2:
    st.text("")
    st.subheader('сделано n3onN и ScreamProx')

# Введение
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Привет! Это интерактивное приложение позволяет анализировать данные социальных медиа. Вы можете исследовать статистику по различным аспектам вашего контента и ваших аудиторий.")
    st.markdown("Исходный код приложения доступен в [n3onN GitHub Repository](https://github.com/n3onnhowever/)")
    st.markdown("Если вас интересует, как это приложение было разработано, посмотрите [статью на Medium](https://tim-denzler.medium.com/is-bayern-m%C3%BCnchen-the-laziest-team-in-the-german-bundesliga-770cfbd989c7)")

# Сайдбар для фильтров
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

# Фильтры
st.sidebar.markdown("**Сначала выберите диапазон данных для анализа:** 👇")
unique_seasons = get_unique_seasons(df_social_media)
start_season, end_season = st.sidebar.select_slider('Выберите диапазон сезонов для анализа', unique_seasons, value=["Season 13/14", "Season 19/20"])
df_data_filtered_season = df_social_media[(df_social_media['Data'] >= start_season.replace("Season ", "")) & (df_social_media['Data'] <= end_season.replace("Season ", ""))]

unique_days = get_unique_days(df_data_filtered_season)
selected_days = st.sidebar.select_slider('Выберите диапазон дней для анализа', unique_days, value=[min(unique_days), max(unique_days)])

unique_resources = get_unique_resources(df_data_filtered_season)
all_resources_selected = st.sidebar.selectbox('Хотите ли вы включить только определенные ресурсы? Если да, выберите опцию и ресурсы в поле ниже.', ['Включить все ресурсы', 'Выбрать ресурсы вручную'])
if all_resources_selected == 'Выбрать ресурсы вручную':
    selected_resources = st.sidebar.multiselect("Выберите и снимите отметку с ресурсов, которые вы хотите включить в анализ.", unique_resources, default=unique_resources)
df_data_filtered = filter_teams(df_data_filtered_matchday)

### SEE DATA ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader("Выбранные данные в настоящее время:")

# Статистика о выбранных данных
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5 = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row2_1:
    unique_games_in_df = df_data_filtered.shape[0]
    str_games = "🏟️ " + str(unique_games_in_df) + " Matches"
    st.markdown(str_games)
with row2_2:
    unique_teams_in_df = df_data_filtered['Resource_Name'].nunique()
    t = " Resources"
    if unique_teams_in_df == 1:
        t = " Resource"
    str_teams = "🏃‍♂️ " + str(unique_teams_in_df) + t
    st.markdown(str_teams)
with row2_3:
    total_comments_count = df_data_filtered['Comments_Count'].sum()
    str_comments = "💬 " + str(total_comments_count) + " Comments"
    st.markdown(str_comments)
with row2_4:
    total_views = df_data_filtered['Views'].sum()
    str_views = "👀 " + str(total_views) + " Views"
    st.markdown(str_views)

# Вывод данных
row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    see_data = st.expander('Нажмите сюда, чтобы посмотреть сырые данные 👉')
    with see_data:
        st.dataframe(data=df_data_filtered.reset_index(drop=True))
st.text('')
