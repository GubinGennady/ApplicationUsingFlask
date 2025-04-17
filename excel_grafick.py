# Импорт необходимых библиотек
import pandas as pd  # Для работы с данными в табличной форме

import matplotlib

matplotlib.use('Agg')  # Устанавливаем бэкенд Agg до импорта plt

import matplotlib.pyplot as plt
from io import BytesIO
import base64


def read_xlsx_data(file_path):
    """
   Чтение данных из Excel-файла и проверка структуры данных
   :param file_path: путь к файлу Excel
   :return: DataFrame с данными или None, если произошла ошибка
   """
    try:
        # Чтение Excel-файла с использованием движка openpyxl
        df = pd.read_excel(file_path, engine='openpyxl')

        # Список обязательных колонок
        colums = ['timestamp', 'emg1', 'emg2', 'emg3', 'emg4', 'angle']

        # Проверка наличия всех обязательных колонок
        for col in colums:
            if not col in df.columns:
                raise ValueError('Файл не содержит всех необходимых колонок')
        return df
    except Exception as e:
        # Вывод ошибки в консоль
        print(e)
        return None


def count_peaks(angle_series, th=20):
    """
    Подсчет пиков в данных угла наклона
    :param angle_series: Series с данными угла наклона
    :param th: пороговое значение для определения пика (по умолчанию 20)
    :return: количество обнаруженных пиков
    """
    peaks = 0
    min_val = angle_series.iloc[0]  # Начальное минимальное значение

    for val in angle_series:
        if val < min_val:
            # Обновляем минимальное значение, если текущее значение меньше
            min_val = val
        elif val - min_val >= th:
            # Если разница между текущим значением и минимальным превышает порог, считаем это пиком
            peaks += 1
            min_val = val  # Обновляем минимальное значение
    return peaks


def get_dataset_stats(df):
    """
    Расчет статистических показателей для набора данных
    :param df: DataFrame с исходными данными
    :return: словарь с рассчитанной статистикой
    """
    stats = {
        'emg1': {'mean': df['emg1'].mean(), 'max': df['emg1'].max()},
        'emg2': {'mean': df['emg2'].mean(), 'max': df['emg2'].max()},
        'emg3': {'mean': df['emg3'].mean(), 'max': df['emg3'].max()},
        'emg4': {'mean': df['emg4'].mean(), 'max': df['emg4'].max()},
        'angle': {
            'mean': df['angle'].mean(),
            'max': df['angle'].max(),
            'peaks': count_peaks(df['angle'])},  # Подсчет пиков для угла
    }
    return stats


def create_plot(df):
    """
    Создание графиков по данным и возврат их в виде base64-encoded изображения
    :param df: DataFrame с исходными данными
    :return: строка с изображением в формате base64 для вставки в HTML
    """
    # Создаем фигуру с двумя субплогами
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # Увеличил высоту для лучшего отображения
    plt.subplots_adjust(hspace=0.5)  # Добавил больше пространства между графиками

    # Графики EMG-сигналов
    ax1.plot(df['timestamp'], df['emg1'], label='EMG1')
    ax1.plot(df['timestamp'], df['emg2'], label='EMG2')
    ax1.plot(df['timestamp'], df['emg3'], label='EMG3')
    ax1.plot(df['timestamp'], df['emg4'], label='EMG4')
    ax1.set_title('EMG Signals')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Amplitude')
    ax1.legend(loc='upper right')  # Оптимальное расположение легенды

    # График угла
    ax2.plot(df['timestamp'], df['angle'], color='red', label='Angle')
    ax2.set_title('Angle Variation')
    ax2.set_xlabel('Timestamp')
    ax2.set_ylabel('Degrees')
    ax2.legend(loc='upper right')
    ax2.grid(True)  # Добавил сетку для лучшей читаемости

    # Сохранение в буфер
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)  # Важно: закрываем фигуру

    # Подготовка base64 строки
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return f"data:image/png;base64,{image_base64}"
