# Social Insight 

![version](https://img.shields.io/badge/version-0.1.0-blue)
![built-with](https://img.shields.io/badge/built%20with-Python%20%2B%20Streamlit-blue)

## ✨ Возможности  

- 📂 Агрегация постов из соцсетей (**VK**, **Telegram**)  
- 🤖 Классификация новостей по категориям с помощью дообученной **BERT**-модели  
- 📊 Расчёт рейтинга новостей (просмотры, лайки, комментарии, репосты)  
- 🔍 Фильтрация по категории и источнику  
- 📈 Сортировка новостей по метрикам: просмотры, лайки, комментарии, репосты, рейтинг  
- 🎨 Визуализации: средний рейтинг категорий по источникам  
- 🌐 Веб-интерфейс на **Streamlit** с кастомным оформлением  

---

## 🚀 Быстрый старт  

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/social-insight.git
cd social-insight

# 2. Собрать Docker-образ
docker build -t social-insight .

# 3. Запустить контейнер
docker run -p 8501:8501 social-insight

# 4. Открыть в браузере
http://localhost:8501
```

---

## 📂 Структура проекта

```
social-insight/
│
├── web.py                   # Streamlit-приложение
├── train_model.ipynb        # Jupyter Notebook для обучения модели
├── final_verse.csv          # Датасет с собранными постами
├── Dockerfile               # Конфигурация Docker-образа
├── background.png           # Фон веб-интерфейса
├── logo_white.png           # Логотип проекта
└── README.md                # Документация
```
