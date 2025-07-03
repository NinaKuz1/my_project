from typing import List, Tuple, Optional
from junction import Junction, Signal, Color

def simulate_trip(junctions: List[Junction], speed_kmh: float) -> List[float]:
    
    # переводит скорости из км в м
    speed_ms = speed_kmh / 3.6
    # инициализируем список времен ожидания нулями
    wait_times = [0.0] * len(junctions)
    # начальное время - 0 секунд
    current_time = 0.0

    # проходим по всем парам соседних перекрестков
    for i in range(len(junctions) - 1):
    # текущий перекресток
        j1 = junctions[i]  
     # следующий перекресток
        j2 = junctions[i + 1]
        
        # вычисляем расстояние между перекрестками по координатам
        distance = ((j2.x - j1.x) ** 2 + (j2.y - j1.y) ** 2) ** 0.5
        # вычисляем время в пути между перекрестками
        travel_time = distance / speed_ms
        # вычисляем время прибытия на следующий перекресток
        arrival_time = current_time + travel_time

        # получаем текущий сигнал светофора на следующем перекрестке
        signal_data = get_current_signal_with_offset(j2, arrival_time)
        if signal_data is None:
            # если сигнал не найден, время ожидания 0
            wait_times[i + 1] = 0.0
            continue

        # распаковываем данные сигнала
        signal, signal_start, signal_end = signal_data
        
        # проверяем цвет сигнала
        if signal.color == Color.GREEN:
            # если зеленый - время ожидания 0
            wait_times[i + 1] = 0.0
        else:
            # если красный - находим время начала следующего зеленого
            next_green_time = find_next_green_time(j2, arrival_time)
            # вычисляем время ожидания
            wait_time = next_green_time - arrival_time
            # сохраняем время ожидания (не меньше 0)
            wait_times[i + 1] = max(0, wait_time)
            # обновляем текущее время с учетом ожидания
            arrival_time += wait_time

        # обновляем текущее время для следующей итерации
        current_time = arrival_time
    
    return wait_times


def get_current_signal_with_offset(
    junction: Junction, 
    absolute_time: float
) -> Optional[Tuple[Signal, float, float]]:
    # вычисляем время в цикле светофора с учетом смещения
    cycle_time = (absolute_time - junction.cycle_offset_seconds) % junction.full_cycle_seconds
    current_time_in_cycle = 0.0  # текущее время внутри цикла

    # проходим по всем фазам светофора
    for phase in junction.full_cycle:
        # проходим по всем сигналам в фазе
        for signal in phase.signals:
            # вычисляем время окончания текущего сигнала
            signal_end_in_cycle = current_time_in_cycle + signal.duration_seconds
            
            # проверяем, попадает ли текущее время в интервал сигнала
            if current_time_in_cycle <= cycle_time < signal_end_in_cycle:
                # вычисляем абсолютное время начала и конца сигнала
                signal_start_abs = junction.cycle_offset_seconds + current_time_in_cycle
                signal_end_abs = junction.cycle_offset_seconds + signal_end_in_cycle
                return signal, signal_start_abs, signal_end_abs
            
            # переходим к следующему сигналу
            current_time_in_cycle = signal_end_in_cycle
    
    # если сигнал не найден
    return None


def find_next_green_time(junction: Junction, absolute_time: float) -> float:

    # вычисляем время в цикле светофора с учетом смещения
    cycle_time = (absolute_time - junction.cycle_offset_seconds) % junction.full_cycle_seconds
    next_green_in_cycle = None  # время следующего зеленого в цикле
    current_time_in_cycle = 0.0  # текущее время в цикле

    # первый проход: ищем зеленый сигнал после текущего времени
    for phase in junction.full_cycle:
        for signal in phase.signals:
            # если сигнал зеленый и его время >= текущего
            if signal.color == Color.GREEN and current_time_in_cycle >= cycle_time:
                next_green_in_cycle = current_time_in_cycle
                break
            current_time_in_cycle += signal.duration_seconds
        if next_green_in_cycle is not None:
            break

    # если не нашли - ищем с начала цикла
    if next_green_in_cycle is None:
        current_time_in_cycle = 0.0
        for phase in junction.full_cycle:
            for signal in phase.signals:
                if signal.color == Color.GREEN:
                    next_green_in_cycle = current_time_in_cycle
                    break
                current_time_in_cycle += signal.duration_seconds
            if next_green_in_cycle is not None:
                break

    # вычисляем абсолютное время следующего зеленого
    if next_green_in_cycle is not None:
        # количество полных циклов
        full_cycles = (absolute_time - junction.cycle_offset_seconds) // junction.full_cycle_seconds
        # если текущее время в цикле больше времени зеленого - добавляем цикл
        if cycle_time > next_green_in_cycle:
            full_cycles += 1
        return junction.cycle_offset_seconds + full_cycles * junction.full_cycle_seconds + next_green_in_cycle
    
    # если зеленый не найден (не должно происходить)
    return absolute_time