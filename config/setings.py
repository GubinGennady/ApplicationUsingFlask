import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv('.env')

# Секретный ключ приложения - используется для защиты сессий и других функций безопасности
SECRET_KEY = os.getenv('SECRET_KEY')

# Режим отладки (True - включен, False - выключен)
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')

# Папка для загрузки файлов пользователями
UPLOAD_FOLDER = 'uploads'

# Разрешенные хосты - с каких адресов можно обращаться к приложению
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')  # Только локальные подключения

# ========= НАСТРОЙКИ БАЗЫ ДАННЫХ =========
DB_TYPE = os.getenv('DB_TYPE')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = (os.getenv('DB_PORT'))  # Преобразуем в число

# Разрешенные расширения файлов для загрузки (только Excel файлы)
ALLOWED_EXTENSIONS = {'xlsx'}

# Формирование строки подключения к базе данных в формате SQLAlchemy
# Формат: "тип_бд://пользователь:пароль@хост:порт/имя_бд"
# 1. Сначала пробуем взять готовую строку из DATABASE_URL
# 2. Если нет - собираем из отдельных компонентов
SQLALCHEMY = os.getenv('DATABASE_URL') or \
             f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
