import matplotlib.pyplot as plt
from junction import Junction
from typing import List
from junction import Color


dpi = 150 
plt.rcParams['figure.dpi'] = dpi 
plt.rcParams["figure.figsize"] = (0, 0) 

def plot_time_space_diagram(junctions: List[Junction]):
    # создаем фигуру и оси для графика
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # настройка оформления осей и заголовков
    # по х
    ax.set_xlabel("t, секунды", fontsize=12, fontweight='bold')
    #аналигично ток для y
    ax.set_ylabel("светофорные объекты, метры", fontsize=12, fontweight='bold')
    
    # подготовка данных для оси у
    # получаем позиции светофоров по оси у в метрах
    y_positions = [j.y for j in junctions]
    # создаем подписи для каждого светофора айдишник и расстояние
    y_labels = [f"tls #{j.id}\n{j.y}m" for j in junctions]
    
    # устанавливаем метки и позиции на оси у
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels)
    ax.grid(True, linestyle='--', alpha=0.1)

    # максимальное время отображения на графике в секах
    max_time = 85
    
    # сопоставление цветов сигналов с цветами на графике
    color_map = {
        Color.RED: 'red',     
        Color.GREEN: 'green', 
        Color.YELLOW: 'yellow'
    }
    
    # обработка каждого перекрестка (светофора)
    for i, junction in enumerate(junctions):
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
                        # позиция по оси Y
                            y=junction.y,
    
                            width=end - start,
                            left=start,
                        # высота полосы
                            height=20,
                        # цвет сигнала
                            color=color_map[signal.color]
            
                        )
                        
                        signal_start = end
                        # увеличиваем текущее время на длительность сигнала
                        current_time += end - start
                        break 
                    
        
                    accumulated_time += signal.duration_seconds
                else:
            
                    continue
                break
    
    # устанавливаем перделы осей
     # от 0 до max_time по x
    ax.set_xlim(0, max_time)
     # от 0 до 650 метров по y
    ax.set_ylim(0, 650) 

    # добавляем горизонтальные линии для каждого светофора
    for y in y_positions:
        ax.axhline(y=y, color='gray', linestyle='--', alpha=0.2)
    
    plt.tight_layout()
    return plt