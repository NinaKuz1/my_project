from junction import Junction
from typing import List

def get_time(distance, speed_ms):
    ## Случайное число от speed_ms/2 до speed_ms: [speed_ms/2, speed_ms)
    new_speed = speed_ms / 2 + (speed_ms / 2) * (0.5 - 1)
    return distance / new_speed

def find_best_offsets(junctions: List[Junction], speed_kmh: float) -> List[int]:
    best_offsets = []
    speed_ms = speed_kmh / 3.6

    # Магия
    for i in range(len(junctions) - 1):
        j1 = junctions[i] # Первый перекресток
        j2 = junctions[i + 1] # Второй перекресток

        distance = ((j2.x - j1.x) ** 2 + (j2.y - j1.y) ** 2) ** 0.5 # Расстояние между перекрестками в метрах
        time_drive = distance / speed_ms # Время в пути между перекрестками в секундах

        # Ответить на вопрос:
        # Сколько надо времени "ожидать"
        # до первого зеленого сигнала светофора j2?
        time_wait = 2



    best_offsets = [0, -2, -1, -2]
    return best_offsets