# Импорт необходимых модулей Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import setings
from urls import register_routes

# Инициализация расширений без привязки к конкретному приложению
# (паттерн "Application Factory")
db = SQLAlchemy()  # Создаем экземпляр SQLAlchemy для работы с БД
migrate = Migrate()  # Создаем экземпляр Migrate для управления миграциями


def create_app():
    """
    Фабрика для создания экземпляра Flask-приложения (Application Factory Pattern)
    Returns:
        Flask: Экземпляр Flask-приложения с настроенными расширениями и маршрутами
    """

    # Создаем экземпляр Flask-приложения
    app = Flask(__name__)

    # Конфигурация приложения из файла настроек
    # Подключаемся к базе данных (URI берем из настроек)
    app.config['SQLALCHEMY_DATABASE_URI'] = setings.SQLALCHEMY

    # Отключаем отслеживание модификаций (для экономии памяти)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Регистрируем все маршруты (URL-адреса) приложения
    register_routes(app)

    return app  # Возвращаем готовое приложение
