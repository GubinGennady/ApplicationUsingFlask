from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import setings
from urls import register_routes

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Импортируем настройки после создания app, чтобы избежать циклических импортов
    app.config['SQLALCHEMY_DATABASE_URI'] = setings.SQLALCHEMY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Регистрируем маршруты
    register_routes(app)

    return app
