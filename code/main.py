from junction import Junction, Phase, Signal, Color
from draw import plot_time_space_diagram, plot_green_waves, plot_through_wave_bands
from green_wave_finder import find_complete_green_waves
from modeling import simulate_trip
def main():
    junctions = [
        Junction(
            0, "tls #0",
            0, 0,
            [
                Phase(0, [Signal(30, Color.GREEN, 25, 35), Signal(20, Color.RED, 20, 20)]),
                Phase(1, [Signal(20, Color.GREEN, 15, 25), Signal(15, Color.RED, 15, 15)])
            ]
        ),
        Junction(
            1, "tls #1",
            0, 200,
            [
                Phase(10, [Signal(20, Color.RED, 20, 20), Signal(35, Color.GREEN, 30, 40), Signal(5, Color.YELLOW, 5, 5)]),
                Phase(11, [Signal(10, Color.RED, 10, 10), Signal(10, Color.GREEN, 5, 15), Signal(5, Color.YELLOW, 5, 5)])
            ]
        ),
        Junction(
            2, "tls #2",
            0, 450,
            [
                Phase(20, [Signal(45, Color.RED, 45, 45), Signal(10, Color.GREEN, 5, 15)]),
                Phase(21, [Signal(7, Color.RED, 7, 7), Signal(18, Color.GREEN, 18, 18), Signal(5, Color.YELLOW, 5, 5)])
            ]
        ),
        Junction(
            3, "tls #3",
            0, 600,
            [
                Phase(30, [Signal(40, Color.RED, 40, 40), Signal(15, Color.GREEN, 10, 20)]),
                Phase(31, [Signal(10, Color.RED, 10, 10), Signal(20, Color.GREEN, 20, 20)])
            ]
        )
    ]
    
# установка точных оффсетов
    offsets = [0, -2 ,-4.5, 0]
    for i, offset in enumerate(offsets):
        junctions[i].set_offset(offset)

    for junction in junctions:
        print(junction)
        print("Green intervals:", junction.get_green_intervals())

    complete_green_waves = find_complete_green_waves(junctions, speed_kmh=40)
    for wave in complete_green_waves.green_waves:
        print("Complete green wave:", wave)
    for through_wave in complete_green_waves.chained_green_waves:
        print("Through green wave:", through_wave, "CRITERIA", through_wave.band_size)
 
    wait_times = simulate_trip(junctions, speed_kmh=40)

    print("Время ожидания на перекрестках:", [f"{t:5f}" for t in wait_times])
    
    plt = plot_time_space_diagram(junctions)
    plt = plot_green_waves(plt, junctions, complete_green_waves.green_waves)
    plt = plot_through_wave_bands(plt, junctions, complete_green_waves.chained_green_waves)
    plt.show()

if __name__ == "__main__":
    main()

