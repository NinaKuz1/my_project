from typing import List, Dict
from junction import Junction, GreenInterval
from green_wave import GreenWave, GreenWavesResult, GreenWaveInterval, GreenWavesChain, ThroughGreenWave

"""
Функции для поиска зеленых волн между двумя перекретками, представлленными наборами зеленых интервалов
"""
def find_green_waves(green_intervals_j1: List[GreenInterval], green_intervals_j2: List[GreenInterval], distance_meters: float, time_drive_seconds: float) -> List[GreenWave]:
    green_waves = []

    # Перебираем все возможные комбинации зеленых интервалов между первым и вторым перекрестками
    for green_interval_j1 in green_intervals_j1:
        start1, end1 = green_interval_j1.start_seconds, green_interval_j1.end_seconds
        # Расчёт "окна" времени прибытия первой выехавшей машины и последней машины, которая успевает проехать до конца зеленого сигнала
        first_arrival_j2 = start1 + time_drive_seconds
        last_arrival_j2 = end1 + time_drive_seconds
        for green_interval_j2 in green_intervals_j2:
            start2, end2 = green_interval_j2.start_seconds, green_interval_j2.end_seconds
            overlap_start = max(first_arrival_j2, start2)
            overlap_end = min(last_arrival_j2, end2)
            if overlap_start >= overlap_end:
                # Зелёная волна невозможна
                continue
            # Корректириуем времена выезда с первого перекрестка
            # Моменты времени, когда АТС должен выехать с первого перекрестка
            # чтобы прибыть на второй перекресток в "окно" зеленого сигнала (в найденном пересечении интервалов)
            adjusted_start_j1 = overlap_start - time_drive_seconds
            adjusted_end_j1 = overlap_end - time_drive_seconds

            # adjusted_start_j1 >= start1 - выезд не раньше начала зеленого
            # adjusted_end_j1 <= end1 - выезд не позже конца зеленого
            # adjusted_start_j1 < adjusted_end_j1 - интервал имеет положительную длительность
            if (adjusted_start_j1 >= start1 and adjusted_end_j1 <= end1 and adjusted_start_j1 < adjusted_end_j1):
                # Создаем зеленую волну
                green_wave = GreenWave(
                    GreenWaveInterval(green_interval_j1.phase_idx, adjusted_start_j1, adjusted_end_j1),
                    GreenWaveInterval(green_interval_j2.phase_idx, overlap_start, overlap_end),
                    distance_meters,
                    time_drive_seconds
                )
                green_waves.append(green_wave)
    return green_waves

"""
Находит все возможные зеленые волные между всеми сосденими парами перекрестков.
"""
def get_green_waves(junctions: List[Junction], speed_kmh: float) -> List[List[GreenWave]]:
    speed_ms = speed_kmh / 3.6
    waves = []
    
    # Обрабатываем каждую пару соседних перекрестков
    for i in range(len(junctions) - 1):
        j1 = junctions[i] # Первый перекресток
        j2 = junctions[i + 1] # Второй перекресток
        green_intervals_j1 = j1.get_green_intervals() # Зеленые интервалы первого перекрестка
        green_intervals_j2 = j2.get_green_intervals() # Зеленые интервалы второго перекрестка

        offset_j1 = j1.get_offset() # Смещение ленты времени первого перекрестка
        offset_j2 = j2.get_offset() # Смещение ленты времени второго перекрестка

        adjusted_intervals_j1 = []
        for interval in green_intervals_j1:
            # Надо сдвинуть начало и конец интервала на величину offset_j1
            start = (interval.start_seconds + offset_j1) % j1.full_cycle_seconds
            end = (interval.end_seconds + offset_j1) % j1.full_cycle_seconds
            if end < start:
                # От СДВИНУТОГО start до конца цикла
                adjusted_intervals_j1.append(GreenInterval(
                    interval.phase_idx, 
                    start, 
                    j1.full_cycle_seconds
                ))
                # От начала цикла до СДВИНУТОГО end
                adjusted_intervals_j1.append(GreenInterval(
                    interval.phase_idx,
                    0,
                    end
                ))
            else:
                # Обычный случай, когда конец интервала больше начала
                adjusted_intervals_j1.append(GreenInterval(interval.phase_idx, start, end))

        adjusted_intervals_j2 = []
        for interval in green_intervals_j2:
            # Надо сдвинуть начало и конец интервала на величину offset_j2
            start = (interval.start_seconds + offset_j2) % j2.full_cycle_seconds
            end = (interval.end_seconds + offset_j2) % j2.full_cycle_seconds
            if end < start:
                adjusted_intervals_j2.append(GreenInterval(
                    interval.phase_idx,
                    start,
                    j2.full_cycle_seconds
                ))
                adjusted_intervals_j2.append(GreenInterval(
                    interval.phase_idx,
                    0,
                    end
                ))
            else:
                # Обычный случай, когда конец интервала больше начала
                adjusted_intervals_j2.append(GreenInterval(interval.phase_idx, start, end))

        distance = ((j2.x - j1.x) ** 2 + (j2.y - j1.y) ** 2) ** 0.5 # Расстояние между перекрестками в метрах
        time_drive = distance / speed_ms # Время в пути между перекрестками в секундах

        segment_waves = find_green_waves(adjusted_intervals_j1, adjusted_intervals_j2, distance, time_drive)
        waves.append(segment_waves)
    return waves

def build_chain(wave: GreenWave, current_chain: List[GreenWave], waves_connections: Dict[GreenWave, List[GreenWave]], possible_chains: List[GreenWavesChain]) -> None:
    """
    Рекурсивно строит цепочки зеленых волн на основе связей между волнами
    """
    if wave not in waves_connections:
        # Создаем финальную цепочку из текущего пути
        possible_chains.append(GreenWavesChain(current_chain))
        return
    
    # Перебор всех волн, к которым может "подключиться" текущая волна
    for next_wave in waves_connections[wave]:
        # Рекурсивно строим цепочку для следующей волны
        # Примечание: создаем новый список current_chain + [next_wave], чтобы не изменять оригинальный список для других ветвей
        build_chain(next_wave, current_chain + [next_wave], waves_connections, possible_chains)
    
def extract_chains(segments_waves: List[List[GreenWave]]) -> List[GreenWavesChain]:
    """
    Извлекаем цепочки связанных зеленых волн
    """
    # Копии 
    segment_waves_clone: List[List[GreenWave]] = []
    for segment_waves in segments_waves:
        segment_clone: List[GreenWave] = []
        for wave in segment_waves:
            segment_clone.append(wave.clone())
        segment_waves_clone.append(segment_clone)
    
    waves_connections: Dict[GreenWave, List[GreenWave]] = {}
    current_segment = segment_waves_clone[0]
    for i in range(len(segment_waves_clone) - 1):
        next_segment = segment_waves_clone[i + 1]
        adjusted_next_segment: List[GreenWave] = []
        for wave_from in current_segment:
            connections = []
            for wave_to in next_segment:
                # Волны могут быть связаны, только если они относятся к одной фазе.
                # Примечание: МОЖНО спорить
                if wave_from.interval_j2.phase_idx != wave_to.interval_j1.phase_idx:
                    continue

                # Проверим, что пересечения интервалов валидны
                intervals_intersection = can_waves_connect(wave_from.interval_j2, wave_to.interval_j1)
                if not intervals_intersection:
                    continue

                adjusted_wave_to = wave_to.clone()
                delta_start = intervals_intersection.start - wave_to.interval_j1.start
                delta_end = intervals_intersection.end - wave_to.interval_j1.end

                # Применим корректировки
                # Заменим первый интервал второй волны на пересечение
                adjusted_wave_to.interval_j1 = intervals_intersection
                # Сдвинем второй интервал второй волны на delta_start и delta_end
                adjusted_wave_to.interval_j2.start += delta_start
                adjusted_wave_to.interval_j2.end += delta_end

                # Пересчитываем ширину зеленой волны
                adjusted_wave_to.band_size = adjusted_wave_to.interval_j2.end - adjusted_wave_to.interval_j2.start

                # Добавляем волну (скорректированную) в список связей
                connections.append(adjusted_wave_to)
                
                adjusted_next_segment.append(adjusted_wave_to)
            
            if connections:
                # Если есть связи, то добавляем их в словарь
                waves_connections[wave_from] = connections

        # Скорректированные волные становятся текущим сегментом для следующей итерации
        current_segment = adjusted_next_segment
        segment_waves_clone[i + 1] = adjusted_next_segment

    possible_chains: List[GreenWavesChain] = []
    for wave in segment_waves_clone[0]:
        # Начинаем строить цепочки с каждой волны из первого сегмента
        build_chain(wave, [wave], waves_connections, possible_chains)
    
    return possible_chains

def merge_green_waves(segments_waves: List[List[GreenWave]]) -> List[ThroughGreenWave]:
    """
    Объединяет цепочки связанных зеленых волн в сквозные зеленые волны.
    """
    possible_chains = extract_chains(segments_waves)
    through_waves = []
    for chain in possible_chains:
        # Сквозная волная должна проходить минимум через 2 сегмента
        if len(chain.green_waves) < 2:
            continue
        # Подготовим скорректированные волны
        # Клонированные зеленые волны
        adjusted_waves = [wave.clone() for wave in chain.green_waves]
        for i in range(len(adjusted_waves)-1, 0, -1):
            current = adjusted_waves[i] # Текущая волна (более поздняя)
            previous = adjusted_waves[i - 1] # Предыдущая волна (более ранняя)
            intersection = can_waves_connect(previous.interval_j2, current.interval_j1)
            if not intersection:
                # Если волны не могут соединиться, то пропускаем
                continue
            # Заменяем начальный интервал текущей волны на найденное пересечение
            current.interval_j1.start = intersection.start
            current.interval_j1.end = intersection.end
            # Вычисляем изменения в пересечении относительно исходного интервала
            delta_start = intersection.start - previous.interval_j2.start
            delta_end = intersection.end - previous.interval_j2.end
            # Корректируем конечный интервал предыдущей волны
            previous.interval_j2.start = intersection.start
            previous.interval_j2.end = intersection.end
            # Пропорционально корректируем начальный интервал предыдущей волны
            previous.interval_j1.start += delta_start
            previous.interval_j1.end += delta_end
            # Пересчитываем ширину зеленой волны
            previous.band_size = previous.interval_j2.end - previous.interval_j2.start

        intervals = []
        intervals.append(adjusted_waves[0].interval_j1)
        for wave in adjusted_waves:
            intervals.append(wave.interval_j2)
        through_waves.append(ThroughGreenWave(intervals))
    return through_waves

def find_complete_green_waves(junctions: List[Junction], speed_kmh: float) -> GreenWavesResult:
    green_waves = get_green_waves(junctions, speed_kmh)
    chained_green_waves = merge_green_waves(green_waves)
    return GreenWavesResult(green_waves, chained_green_waves)

def can_waves_connect(interval_j1: GreenWaveInterval, interval_j2: GreenWaveInterval) -> GreenWaveInterval | None:
    """
    Проверка, что две идущие друг за другом зеленые волные могут соедениться в одну.
    Если могут, то возвращает интервал соединения, иначе None.
    """
    epsilon = 0.01  # Допустимая разница для сравнения с нулем
    overlap_start = max(interval_j1.start, interval_j2.start)
    overlap_end = min(interval_j1.end, interval_j2.end)
    if overlap_end - overlap_start > epsilon:
        return GreenWaveInterval(interval_j1.phase_idx, overlap_start, overlap_end)
    return None