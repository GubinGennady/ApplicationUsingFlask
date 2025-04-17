# Импорт view-функций из модулей представлений
from views.main_views import index, add_dataset
from views.dataset_views import view_dataset, update_dataset
from api.datasets import update_dataset_api


def register_routes(app):
    """
    Регистрирует все маршруты (URL-адреса) в Flask-приложении

    Параметры:
        app: Экземпляр Flask-приложения
    """
    # Регистрация маршрута для главной страницы
    # GET / - отображает индексную страницу
    app.route('/')(index)

    # Регистрация маршрута для добавления набора данных
    # GET /add_dataset - отображает форму добавления
    # POST /add_dataset - обрабатывает отправку формы
    app.route('/add_dataset', methods=['GET', 'POST'])(add_dataset)

    # Регистрация маршрута для просмотра набора данных
    # GET /view_dataset/<id> - отображает конкретный набор данных
    app.route('/view_dataset/<int:dataset_id>')(view_dataset)

    # Регистрация маршрута для обновления набора данных
    # GET /update_dataset/<id> - отображает форму редактирования
    # POST /update_dataset/<id> - обрабатывает отправку формы
    app.route('/update_dataset/<int:dataset_id>', methods=['GET', 'POST'])(update_dataset)

    # API routes
    # PUT /api/datasets/<id> - REST API для обновления набора данных
    app.route('/api/datasets/<int:dataset_id>', methods=['PUT'])(update_dataset_api)
