from green_wave import GreenWave, ThroughGreenWave
import matplotlib.pyplot as plt
from junction import Junction
from typing import List
from junction import Color
from matplotlib.patches import Patch

dpi = 150 
plt.rcParams['figure.dpi'] = dpi 
plt.rcParams["figure.figsize"] = (10, 6)

def plot_time_space_diagram(junctions: List[Junction]):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # настройка оформления осей и заголовков
    # по х
    ax.set_xlabel("t, секунды", fontsize=10)
    #аналигично ток для y
    ax.set_ylabel("светофорные объекты, метры", fontsize=10)
    
    # подготовка данных для оси у
    # получаем позиции светофоров по оси у в метра
    y_positions = [j.y for j in junctions]
    # создаем подписи для каждого светофора айдишник и расстояние
    y_labels = [f"\n{j.y}" for j in junctions]
    
    # меточки
    additional_positions = [100, 300, 400, 500]
    y_positions.extend(additional_positions)
    y_labels.extend([f"\n{pos}" for pos in additional_positions])
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.grid(True, linestyle='--', alpha=0.1)

    # максимальное время отображения на графике в секах
    max_time = 85
    
    # сопоставление цветов сигналов с цветами на графике(сделала чуть ярче, чем в предыдущем)
    color_map = {
        Color.RED: "#ff2929",
        Color.GREEN: "#68ff68",
        Color.YELLOW: "#ffff40"
    }
    
    # обработка каждого перекрестка (светофора)
    for junction in junctions:
    # начальное время для текущего светофора
        current_time = junction.cycle_offset_seconds
        signal_start = 0
    # цикл продолжается пока не достигнем максимального времени    
        while signal_start < max_time:
    # вычисляем позицию в цикле светофора по моду 85 
            cycle_pos = current_time % junction.full_cycle_seconds
            accumulated_time = 0
    # перебираем все фазы цикла светофора        
            for phase in junction.full_cycle:
    # перебираем все сигналы в текущей фазе
                for signal in phase.signals:
                    if accumulated_time <= cycle_pos < accumulated_time + signal.duration_seconds:
                        start = signal_start
    # убеждаемся, что не выходим за пределы max_time
                        end = start + min(signal.duration_seconds, max_time - signal_start)
     # рисуем горизонтальную полосу (сигнал светофора)                    
                        ax.barh(
                        # позиция по оси у
                            y=junction.y,
                            width=end - start,
                            left=start,
                        # высота полосы
                            height=12, 
                        # цвет сигнала
                            color=color_map[signal.color],
                            linewidth=0.5
                        )
                        
                        signal_start = end
                    # увеличиваем текущее время на длительность сигнала
                        current_time += end - start
                        break
                    
                    accumulated_time += signal.duration_seconds
                else:
                    continue
                break
    

# устанавливаем пределы осей с отступами 
    
    indentation = max_time * 0.04
    ax.set_xlim(-indentation, max_time + indentation)
#чтобы было видно нормально нижнюю полосу
    ax.set_ylim(-20, 650)
    
    # добавляем горизонтальные линии для каждого светофора
    for y in [j.y for j in junctions]:
        ax.axhline(y=y, color='gray', linestyle='--', alpha=0.5, linewidth=0.7)
    
    #кружочки
    for junction in junctions:
        ax.plot(0.5, junction.y, 'o', markersize=8, color="#0fd0eed2", clip_on=False)
        #перенесла подпись над кружочками
        ax.text(0.5, junction.y + 15, f" tls#{junction.id}", 
                ha='center', va='bottom', fontsize=7)
    
    plt.tight_layout()
    return plt

def plot_green_waves(plt: plt, junctions: List[Junction], green_waves: list[list[GreenWave]]) -> plt:
    ax = plt.gca()
    wave_color = "#57B844"
    alpha = 0.3
    # Для каждого сегмента между перекрёстками
    for segment_idx, segment_waves in enumerate(green_waves):
        if segment_idx >= len(junctions) - 1:
            # Защита от несоответствия количества сегментов и перекрёстков
            break
        
        j1 = junctions[segment_idx]
        j2 = junctions[segment_idx + 1]
        y1 = j1.y
        y2 = j2.y
        # Для каждой зелёной волны в сегменте
        for wave in segment_waves:
            start_j1, end_j1 = wave.interval_j1.start, wave.interval_j1.end
            start_j2, end_j2 = wave.interval_j2.start, wave.interval_j2.end
            polygon = [
                (start_j1, y1),
                (start_j2, y2),
                (end_j2, y2),
                (end_j1, y1),
                (start_j1, y1)
            ]
            xs, ys = zip(*polygon)
            ax.fill(
                xs, ys,
                color=wave_color,
                alpha=alpha,
                edgecolor=wave_color,
                linewidth=0.5,
                zorder=2
            )
    return plt






def plot_through_wave_bands(plt: plt, junctions: List[Junction], through_waves: List[ThroughGreenWave]) -> plt:
    ax = plt.gca()
    wave_color = "#541FE4"
    alpha = 0.2
    for wave in through_waves:
        starts = []
        ends = []
        for j, interval in enumerate(wave.intervals):
            junction = junctions[j]
            y = junction.y
            starts.append((interval.start, y))
            ends.append((interval.end, y))
        ends.reverse()

        polygons = starts + ends
        xs, ys = zip(*polygons)
        ax.fill(xs, ys, color=wave_color, alpha=alpha, edgecolor=wave_color, linewidth=0.5, zorder=2)
    return plt