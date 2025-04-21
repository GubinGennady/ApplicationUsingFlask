# Импорт необходимых модулей и компонентов Flask
from flask import render_template, redirect, request, url_for
from models import Dataset
from app_one import db
from config import setings
import os


def index():
    """
    Обработчик главной страницы приложения.
    Отображает список всех наборов данных из базы данных.

    Returns:
        Ответ Flask с отрендеренным шаблоном index.html, содержащим список наборов данных
    """

    # Получаем все наборы данных из базы данных
    datasets = Dataset.query.all()

    # Создаем контекст для передачи данных в шаблон
    context = {
        'title': 'Главная',
        'dataset': 'Наборы данных'
    }

    # Рендерим шаблон index.html с передачей:
    # - списка наборов данных (datasets)
    # - дополнительного контекста (context)
    return render_template('index.html', datasets=datasets, **context)


def add_dataset():
    """
    Обрабатывает добавление нового набора данных через веб-интерфейс.
    Поддерживает два типа запросов:
    - GET: Отображает форму добавления набора данных
    - POST: Принимает и сохраняет загруженный файл и данные формы
    """
    # Создаем контекст для передачи в шаблон
    context = {
        'title_new': 'Добавить новый набор данных',
        'Set_name': 'Название набора',
        'Data_file': 'Файл данных (XLSX)'
    }

    # Обработка POST-запроса (отправка формы)
    if request.method == 'POST':
        # Проверяем наличие файла в запросе
        if 'file' not in request.files:
            # Если файла нет - перенаправляем обратно на ту же страницу
            return redirect(request.url)

        # Получаем объект файла из запроса
        file = request.files['file']

        # Проверяем что файл был выбран
        if file.filename == '':
            # Если имя файла пустое - перенаправляем обратно
            return redirect(request.url)

        # Проверяем что файл есть и его расширение разрешено
        if file and '.' in file.filename and file.filename.rsplit('.')[-1].lower() in setings.ALLOWED_EXTENSIONS:
            # Сохраняем оригинальное имя файла
            filename = file.filename

            # Создаем папку для загрузок, если она не существует
            if not os.path.exists(setings.UPLOAD_FOLDER):
                os.mkdir(setings.UPLOAD_FOLDER)

            # Формируем полный путь для сохранения файла
            file_path = os.path.join(setings.UPLOAD_FOLDER, filename)

            # Сохраняем файл на сервер
            file.save(file_path)

            # Получаем имя набора из формы (используем имя файла как значение по умолчанию)
            dataset_name = request.form.get('name', filename)

            # Создаем новый объект Dataset
            new_dataset = Dataset(name=dataset_name, file_path=file_path)

            # Добавляем в сессию и сохраняем в БД
            db.session.add(new_dataset)
            db.session.commit()

            # Перенаправляем на главную страницу после успешного сохранения
            return redirect('/')

    # Для GET-запроса или если POST-запрос не прошел валидацию
    # Отображаем шаблон формы с переданным контекстом
    return render_template('add_dataset.html', **context)
