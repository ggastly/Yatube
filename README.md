# Yatube
## Описание
Yatube - соц.сеть для публикации дневников.
Разработан по MVT архитектуре. Используется пагинация постов и кэширование. Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту. Написаны тесты, проверяющие работу сервиса.
## Технологии
- Python 3.9.7
- Django 2.2.19
### Установка
Склонировать репозиторий себе:
```
git clone https://github.com/Lulufox/api_yamdb.git
```
Зайти в папку с проектом:
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создать в проекте файл .env, в нем указать SECRET_KEY="любой плейсхолдер".

Зайти в папку с файлом manage.py:
```
cd api_yamdb
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
Наполнить БД:
```
python3 manage.py load_db_from_static_data
```

