# Импорт необходимых модулей Flask
from flask import render_template, redirect, request, url_for
from models import Dataset
from app_one import db
from config import setings
import os
from excel_grafick import read_xlsx_data, get_dataset_stats, create_plot


def view_dataset(dataset_id):
    """
    Функция для просмотра набора данных и визуализации графиков
    :param dataset_id: ID набора данных в базе
    :return: отображает шаблон dataset.html с данными
    """
    # Создаем контекст для передачи в шаблон
    context = {
        'title': 'Графики данных',  # Заголовок страницы
        'EMGStatistics': 'Статистика EMG',  # Заголовок для статистики EMG
        'AngleStatistics': 'Статистика угла',  # Заголовок для статистики угла
        'Records': 'Первые 10 записей'  # Заголовок для таблицы записей
    }

    # Получаем набор данных из базы или возвращаем 404
    dataset = Dataset.query.get_or_404(dataset_id)
    # Читаем данные из Excel файла
    df = read_xlsx_data(dataset.file_path)

    # Если данные не прочитаны, возвращаем ошибку
    if df is None:
        return 'Ошибка при чтении данных', 500
    # Получаем статистику по данным
    stats = get_dataset_stats(df)
    # Создаем графики
    plot = create_plot(df)
    # Рендерим шаблон с передачей всех данных
    return render_template('dataset.html', dataset=dataset, stats=stats, plot=plot,
                           data=df.to_dict('records'), **context)


def update_dataset(dataset_id):
    """
    Функция для обновления набора данных
    :param dataset_id: ID набора данных для обновления
    :return: перенаправляет на страницу просмотра или показывает форму обновления
    """
    # Создаем контекст для передачи в шаблон
    context = {
        'title_name': 'Обновить новый набор данных',
        'New_set': 'Новое название набора',
        'New_data_file': 'Новый файл данных (XLSX)'
    }

    # Получаем набор данных из базы или возвращаем 404
    dataset = Dataset.query.get_or_404(dataset_id)

    # Обработка POST-запроса (отправка формы)
    if request.method == 'POST':
        # Проверяем наличие файла в запросе
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # Проверяем, что файл был выбран
        if file.filename == '':
            return redirect(request.url)
        # Проверяем расширение файла
        if file and '.' in file.filename and file.filename.rsplit('.')[-1].lower() in setings.ALLOWED_EXTENSIONS:
            # Сохраняем файл
            filename = file.filename
            file_path = os.path.join(setings.UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Пробуем прочитать данные из файла
            df = read_xlsx_data(file_path)
            # Если данные не читаются, удаляем файл и возвращаем ошибку
            if df is None:
                os.remove(file_path)
                return 'Неверный формат файла', 400

            # Обновляем данные в базе
            dataset.file_path = file_path
            dataset.name = request.form.get('name')
            db.session.commit()
            # Перенаправляем на страницу просмотра
            return redirect(url_for('view_dataset', dataset_id=dataset_id))

    # Если метод GET, показываем форму обновления
    return render_template('update_dataset.html', dataset=dataset, **context)
