import matplotlib.pyplot as plt

def plot_lap_times(laps, lap_times):
    plt.figure()
    plt.plot(laps, lap_times, marker='o')
    plt.xlabel("Lap")
    plt.ylabel("Lap Time (s)")
    plt.title("Lap Time Trend")
    plt.grid()
    plt.savefig("analysis/lap_time.png")
    plt.close()

def plot_degradation(laps, degradation):
    plt.figure()
    plt.plot(laps, degradation, marker='o')
    plt.xlabel("Lap")
    plt.ylabel("Tyre Degradation (s)")
    plt.title("Tyre Degradation Curve")
    plt.grid()
    plt.savefig("analysis/degradation.png")
    plt.close()

def generate_all_plots(data):
    laps = list(range(1, len(data["lap_times"]) + 1))

    plot_lap_times(laps, data["lap_times"])
    plot_degradation(laps, data["degradation"])