# Импорт необходимых библиотек
import pandas as pd  # Для работы с данными в табличной форме
import matplotlib.pyplot as plt  # Для построения графиков
from io import BytesIO  # Для работы с бинарными данными в памяти
import base64  # Для кодирования изображения в base64


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
    :return: строка с изображением в формате base64
    """
    # Создаем фигуру с двумя субплогами (один под другим)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

    # Построение графиков EMG-сигналов на первом субплоте
    ax1.plot(df['timestamp'], df['emg1'], label='ENG1')
    ax1.plot(df['timestamp'], df['emg2'], label='ENG2')
    ax1.plot(df['timestamp'], df['emg3'], label='ENG3')
    ax1.plot(df['timestamp'], df['emg4'], label='ENG4')
    ax1.set_title('ENGS')
    ax1.set_xlabel('Timestamp')
    ax1.set_ylabel('Value')
    ax1.legend()

    # Построение графика угла на втором субплоте
    ax2.plot(df['timestamp'], df['angle'], label='Angle', color='red')
    ax2.set_title('Angle')  # Исправлено: было ax1 вместо ax2
    ax2.set_xlabel('Timestamp')  # Исправлено: было ax1 вместо ax2
    ax2.set_ylabel('Angle')  # Исправлено: было ax1 вместо ax2
    ax2.legend()  # Исправлено: было ax1 вместо ax2

    # Сохраняем график в бинарный буфер
    b = BytesIO()
    plt.savefig(b, format='png', dpi=100, bbox_inches='tight')
    b.seek(0)  # Перемещаем указатель в начало буфера
    plt.close()  # Закрываем фигуру, чтобы освободить память

    # Кодируем изображение в base64 и возвращаем как строку
    return base64.b64encode(b.read()).decode('utf-8')
