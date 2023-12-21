import numpy as np
import matplotlib.pyplot as plt

def square_wave(t, T):
    return np.where(np.mod(t, T) < T / 2, 1, 0)

def square_wave_non_periodic(t, T):
    return np.where(np.abs(t) < T / 2, 1, 0)

def triangle_wave(t, T):
    return np.abs((t / (T / 2)) % 2 - 1)

def triangle_wave_non_periodic(t, T):
    return np.where(np.abs(t)< T / 2, np.abs((t / (T / 2)) % 2 - 1), 0)

def exponential_wave(t, tau):
    return np.where(t>0, np.exp(-t / tau), 0)

def unit_step(t):
    return np.heaviside(t, 1)

def sinusoidal_wave(t, A, f):
    return A * np.sin(2 * np.pi * f * t)

def cosinusoidal_wave(t, A, f):
    return A * np.cos(2 * np.pi * f * t)

def convolution(signal1, signal2, dt):
    dt = dt/2
    result = np.convolve(signal1, signal2, mode='full') * dt
    t_conv = np.arange(-10, -10 + len(result) * dt, dt)
    return t_conv, result

def plot_signals(t, signals, labels, title):
    plt.figure(figsize=(12, 8))
    for signal, label in zip(signals, labels):
        plt.plot(t, signal, label=label)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    dt = 0.01
    t = np.arange(-10, 10, dt)

    print("Select signals for convolution:")
    print("1. Square Wave")
    print("2. Triangle Wave")
    print("3. Exponential Wave")
    print("4. Unit Step")
    print("5. Sinusoidal Wave")
    print("6. Cosinusoidal Wave")
    print("7. Square Wave (non periodic)")
    print("8. Triangle Wave (non periodic)")

    selected_signals = []
    labels = []

    while len(selected_signals) < 2:
        choice = int(input("Enter the number of the signal (1-6): "))
        if choice == 1:
            selected_signals.append(square_wave(t, T=2))
            labels.append('Square Wave')
        elif choice == 2:
            selected_signals.append(triangle_wave(t, T=2))
            labels.append('Triangle Wave')
        elif choice == 3:
            selected_signals.append(exponential_wave(t, tau=1))
            labels.append('Exponential Wave')
        elif choice == 4:
            selected_signals.append(unit_step(t))
            labels.append('Unit Step')
        elif choice == 5:
            selected_signals.append(sinusoidal_wave(t, A=1, f=1))
            labels.append('Sinusoidal Wave')
        elif choice == 6:
            selected_signals.append(cosinusoidal_wave(t, A=1, f=1))
            labels.append('Cosinusoidal Wave')
        elif choice == 7:
            selected_signals.append(square_wave_non_periodic(t, T=2))
            labels.append('Square Wave')
        elif choice == 8:
            selected_signals.append(triangle_wave_non_periodic(t, T=2))
            labels.append('Triangle Wave')
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

    # Obliczenie splotu
    t_conv, result = convolution(selected_signals[0], selected_signals[1], dt)

    # Wyświetlenie wykresów
    print(result[2000])
    print(t_conv[0])
    plot_signals(t, selected_signals, labels, 'Selected Signals')
    plot_signals(t_conv, [result], ['Convolution Result'], 'Convolution Result')


if __name__ == "__main__":
    main()
