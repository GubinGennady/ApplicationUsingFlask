from flask import render_template, redirect, request, url_for
from models import Dataset
from app_one import db
from config import setings
import os
from excel_grafick import read_xlsx_data, get_dataset_stats, create_plot


def index():
    datasets = Dataset.query.all()
    context = {
        'title': 'Главная',
        'dataset': 'Наборы данных'
    }
    return render_template('index.html', datasets=datasets, **context)


def add_dataset():
    # Создаем контекст для передачи в шаблон
    context = {
        'title_new': 'Добавить новый набор данных',
        'Set_name': 'Название набора',
        'Data_file': 'Файл данных (XLSX)'
    }

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and '.' in file.filename and file.filename.rsplit('.')[-1].lower() in setings.ALLOWED_EXTENSIONS:
            filename = file.filename
            if not os.path.exists(setings.UPLOAD_FOLDER):
                os.mkdir(setings.UPLOAD_FOLDER)
            file_path = os.path.join(setings.UPLOAD_FOLDER, filename)
            file.save(file_path)

            dataset_name = request.form.get('name', filename)
            new_dataset = Dataset(name=dataset_name, file_path=file_path)
            db.session.add(new_dataset)
            db.session.commit()
            return redirect('/')

    return render_template('add_dataset.html', **context)
