import matplotlib.pyplot as plt
from junction import Junction
from typing import List
from green_wave import GreenWave, ThroughGreenWave
from junction import Color

dpi = 150
plt.rcParams['figure.dpi'] = dpi  
plt.rcParams["figure.figsize"] = (12, 9) # Дюймы
plt.ioff()

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
    ax.set_yticklabels(y_labels, fontsize=6.5)
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
        #кружочки
        ax.plot(
            0.5,  # X-координата
            junction.y,  # Y-координата
            'o',  # Маркер
            markersize=8,  # Размер
            color="#0fd0eed2",  # Цвет
            clip_on=False
        )
        
        #переносла подпись над кружочками
        ax.text(
            0.5,  
            junction.y + 15, 
            f" tls#{junction.id}", 
            ha='center',  
            va='bottom',  
            fontsize=7  
        )
        
        # отрисовка лент времени
        prev_cycle_x = junction.get_offset()
        prev_cycle_y = junction.y
        
        for phases in junction.full_cycle:
            for signal in phases.signals:
                x_start = prev_cycle_x % junction.full_cycle_seconds
                x_end = (prev_cycle_x + signal.duration_seconds) % junction.full_cycle_seconds
                
                if x_end < x_start:
                     # рисуем горизонтальную полосу (сигнал светофора)  
                    ax.barh(
                        y=prev_cycle_y,
                        width=junction.full_cycle_seconds - x_start,
                        left=x_start,
                        height=12,
                        color=color_map[signal.color],
                        linewidth=0.5
                    )
                    # вторая часть
                    ax.barh(
                        y=prev_cycle_y,
                        width=x_end,
                        left=0,
                        height=12,
                        color=color_map[signal.color],
                        linewidth=0.5
                    )
                else:
                    ax.barh(
                        y=prev_cycle_y,
                        width=x_end - x_start,
                        left=x_start,
                        height=12,
                        color=color_map[signal.color],
                        linewidth=0.5
                    )
                
                prev_cycle_x += signal.duration_seconds
    
    # установка пределов осей
    indentation = max_time * 0.04
    ax.set_xlim(-indentation, max_time + indentation)
    ax.set_ylim(-20, 650)
    
    # добавление горизонтальных линий для каждого светофора
    for y in [j.y for j in junctions]:
        ax.axhline(y=y, color='gray', linestyle='--', alpha=0.5, linewidth=0.7)
    
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