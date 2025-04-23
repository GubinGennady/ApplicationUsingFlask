from flask import Flask
from .urls import register_routes
from .extensions import db, migrate
from config import settings


def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config.from_object(settings)

    # app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация маршрутов
    register_routes(app)

    return app
