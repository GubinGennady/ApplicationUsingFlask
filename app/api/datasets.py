# Импорт необходимых модулей Flask
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os

from config import settings
from app.excel_grafick import read_xlsx_data
from app.models import Dataset, db


def update_dataset_api(dataset_id):
    """
    Обновляет набор данных через REST API
    PUT /api/datasets/<int:dataset_id> - обновление данных

    Параметры:
        dataset_id (int): ID набора данных для обновления

    Возвращает:
        JSON-ответ с результатом операции или ошибкой
    """
    # Получаем набор данных из базы или возвращаем 404 ошибку
    dataset = Dataset.query.get_or_404(dataset_id)

    # Обрабатываем только PUT-запросы
    if request.method == 'PUT':
        # Проверяем наличие файла в запросе
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']  # Получаем файл из запроса

        # Проверяем что файл был выбран
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Проверяем разрешенное расширение файла
        if file and allowed_file(file.filename):
            # Безопасно обрабатываем имя файла
            filename = secure_filename(file.filename)
            # Формируем полный путь для сохранения
            file_path = os.path.join(settings.UPLOAD_FOLDER, filename)

            try:
                # Сохраняем файл
                file.save(file_path)

                # Читаем данные из Excel-файла
                df = read_xlsx_data(file_path)
                if df is None:  # Если данные не прочитались
                    os.remove(file_path)  # Удаляем невалидный файл
                    return jsonify({'error': 'Invalid file format'}), 400

                # Обновляем данные в базе:
                # 1. Путь к файлу
                dataset.file_path = file_path
                # 2. Имя набора (если передано в форме)
                if 'name' in request.form:
                    dataset.name = request.form.get('name')

                # Сохраняем изменения в базе
                db.session.commit()

                # Возвращаем успешный ответ
                return jsonify({
                    'message': 'Набор данных успешно обновлен',
                    'dataset': {
                        'id': dataset.id,
                        'name': dataset.name,
                        'file_path': dataset.file_path
                    }
                }), 200

            except Exception as e:  # Обрабатываем любые исключения
                return jsonify({'error': str(e)}), 500

        # Если расширение файла не разрешено
        return jsonify({'error': 'Тип файла недопустим'}), 400

    # Если метод не PUT
    return jsonify({'error': 'Метод не разрешен'}), 405


def allowed_file(filename):
    """
    Проверяет разрешено ли расширение файла

    Параметры:
        filename (str): Имя файла для проверки

    Возвращает:
        bool: True если расширение разрешено, иначе False
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS
