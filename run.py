# Импорт функции создания Flask-приложения
from app import create_app
from config import settings

# Создание экземпляра Flask-приложения
app = create_app()

# Стандартная проверка для запуска приложения
if __name__ == '__main__':
    app.run(host=settings.ALLOWED_HOSTS, debug=settings.DEBUG)
