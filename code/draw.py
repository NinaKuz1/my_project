import matplotlib.pyplot as plt
from junction import Junction
from typing import List

dpi = 150
plt.rcParams['figure.dpi'] = dpi  
plt.rcParams["figure.figsize"] = (12, 9) # Дюймы
plt.ioff()

def plot_time_space_diagram(junctions: List[Junction]):
    fig, ax = plt.subplots(figsize=(6, 4))
    #
    # Реализовать построение диаграммы лент времени
    #
    plt.xlabel("Time (seconds)", fontsize=12, fontweight='bold')
    return plt