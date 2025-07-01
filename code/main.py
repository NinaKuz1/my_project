from junction import Junction, Phase, Signal, Color
from draw import plot_time_space_diagram

def main():
    junctions = [
        Junction(
            0, "tls #0",
            0, 0,
            [
                Phase(1, [Signal(30, Color.GREEN, 25, 35), Signal(20, Color.RED, 20, 20)]),
                Phase(2, [Signal(20, Color.GREEN, 15, 25), Signal(15, Color.RED, 15, 15)])
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
    
    for junction in junctions:
        print("Длительность цикла", junction.full_cycle_seconds)

    plt = plot_time_space_diagram(junctions)
    plt.show()
       

if __name__ == "__main__":
    main()

