# Импорт необходимых модулей
from .extensions import db
from datetime import datetime


class Dataset(db.Model):
    """
    Модель для хранения информации о наборах данных
    Атрибуты:
        id - уникальный идентификатор набора (первичный ключ)
        name - название набора данных
        file_path - путь к файлу с данными
        upload_date - дата и время загрузки набора
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __str__(self):
        """
        Строковое представление объекта (для вывода в консоли, логах и т.д.)
        Возвращает: Строку с названием набора данных.
        """
        return f'Name dataset: {self.name}'
