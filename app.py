from flask import Flask, render_template, request, redirect, url_for
from config import setings
from models import Dataset, db
from flask_migrate import Migrate
import os
from excel_grafick import *

# Создание экземпляра Flask приложения
app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = setings.SQLALCHEMY  # URI для подключения к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания модификаций

# Инициализация базы данных с приложением
db.init_app(app)

# Инициализация миграций
migrate = Migrate(app, db)


# Маршрут для главной страницы
@app.route('/')
def index():
    # Получение всех наборов данных из базы
    datasets = Dataset.query.all()
    # Рендеринг шаблона с передачей списка наборов данных
    return render_template('index.html', datasets=datasets)


# Маршрут для добавления нового набора данных (принимает GET и POST запросы)
@app.route('/add_dataset', methods=['GET', 'POST'])
def add_dataset():
    # Если метод POST (отправка формы)
    if request.method == 'POST':
        # Проверка наличия файла в запросе
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Проверка, что файл был выбран
        if file.filename == '':
            return redirect(request.url)
        # Проверка расширения файла
        if file and '.' in file.filename and file.filename.rsplit('.')[-1].lower() in setings.ALLOWED_EXTENSIONS:
            filename = file.filename
            # Создание папки для загрузки, если она не существует
            if not os.path.exists(setings.UPLOAD_FOLDER):
                os.mkdir(setings.UPLOAD_FOLDER)
            # Сохранение файла
            file_path = os.path.join(setings.UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Получение имени набора данных из формы (или использование имени файла по умолчанию)
            dataset_name = request.form.get('name', filename)

            # Создание новой записи в базе данных
            new_dataset = Dataset(name=dataset_name, file_path=file_path)
            db.session.add(new_dataset)
            db.session.commit()

            # Перенаправление на главную страницу после успешного добавления
            return redirect('/')

    # Рендеринг шаблона формы добавления набора данных (для GET запроса)
    return render_template('add_dataset.html')


# Маршрут для просмотра конкретного набора данных
@app.route('/view_dataset/<int:dataset_id>')
def view_dataset(dataset_id):
    # Получение набора данных по ID или возврат 404 ошибки, если не найден
    dataset = Dataset.query.get_or_404(dataset_id)
    # Чтение данных из Excel файла
    df = read_xlsx_data(dataset.file_path)
    # Если данные не прочитаны - возвращаем ошибку сервера
    if df is None:
        return 'Ошибка при чтении данных', 500
    # Получение статистики по данным
    stats = get_dataset_stats(df)
    # Создание графика
    plot = create_plot(df)

    # Рендеринг шаблона с передачей данных, статистики и графика
    return render_template('dataset.html', dataset=dataset, stats=stats, plot=plot, data=df.to_dict('records'))


# Точка входа - запуск приложения
if __name__ == '__main__':
    app.run(host=setings.ALLOWED_HOSTS, debug=setings.DEBUG)
