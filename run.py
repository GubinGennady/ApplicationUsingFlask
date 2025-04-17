# Импорт функции создания Flask-приложения
from app import create_app
from config import setings
from models import db

# Создание экземпляра Flask-приложения
app = create_app()

# Инициализация базы данных для созданного приложения
# Это связывает SQLAlchemy с нашим Flask-приложением
db.init_app(app)

# Стандартная проверка для запуска приложения
if __name__ == '__main__':
    app.run(host=setings.ALLOWED_HOSTS, debug=setings.DEBUG)
