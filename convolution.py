import numpy as np
import matplotlib.pyplot as plt
from numpy import convolve


# "Rectangle": ["amplitude", "shift", "width"],
# "Triangle": ["amplitude", "shift", "width"],
# "Sinus": ["amplitude", "frequency", "phase"],
# "Cosinus": ["amplitude", "frequency", "phase"],
# "Exponential": ["amplitude", "rate"]

def square_wave(t, amplitude, shift, width):
    return np.where(np.abs(t + shift) < width / 2, amplitude, 0)

def triangle_wave(t, amplitude, shift, width):
    return np.where(np.abs(t + shift) < width / 2, amplitude * np.abs(((t - shift) / (width / 2)) % 2 - 1), 0)

def exponential_wave(t, amp, tau):
    base = np.exp(1)
    return amp * np.power(base, t / tau)

def sinusoidal_wave(t, A, f, φ):
    return A * np.sin(2 * np.pi * f * t + φ)

def cosinusoidal_wave(t, A, f, phase):
    return A * np.cos(2 * np.pi * f * t + phase)

def convolution(signal1, signal2, dt):
    result = convolve(signal1, signal2, mode='full') * dt
    t_conv = np.linspace(-0.5 * len(result) * dt, 0.5 * len(result) * dt, len(result))
    x_lim_conv = (t_conv[0], t_conv[-1])
    x_values = []
    # print(result)
    for t_val, r_val in zip(t_conv, result):
        if x_lim_conv[0] <= t_val <= x_lim_conv[1]:
            if round(r_val, 5) == 0:
                continue
            else:
                x_values.append(t_val)
    x_lim = (min(x_values), max(x_values))
    # print(min(x_values))
    # print(max(x_values))
    return t_conv, result, x_lim


def get_convolution_data(signal1_choice, signal2_choice, dt):
    t = np.arange(-10, 10, dt)

    if signal1_choice == 1:
        signal1 = square_wave(t, T=2)
    elif signal1_choice == 2:
        signal1 = triangle_wave(t, T=2)
    elif signal1_choice == 3:
        signal1 = exponential_wave(t, tau=1)
    elif signal1_choice == 5:
        signal1 = sinusoidal_wave(t, A=1, f=1)
    elif signal1_choice == 6:
        signal1 = cosinusoidal_wave(t, A=1, f=1)
    else:
        raise ValueError("Invalid choice for signal 1.")

    if signal2_choice == 1:
        signal2 = square_wave(t, T=2)
    elif signal2_choice == 2:
        signal2 = triangle_wave(t, T=2)
    elif signal2_choice == 3:
        signal2 = exponential_wave(t, tau=1)
    elif signal2_choice == 5:
        signal2 = sinusoidal_wave(t, A=1, f=1)
    elif signal2_choice == 6:
        signal2 = cosinusoidal_wave(t, A=1, f=1)
    else:
        raise ValueError("Invalid choice for signal 2.")

    t_conv, result = convolution(signal1, signal2, dt)
    return t, signal1, signal2, t_conv, result

def plot_signals(t, signals, labels, title, ylim=None):
    plt.figure(figsize=(12, 8))
    for signal, label in zip(signals, labels):
        plt.plot(t, signal, label=label)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    if ylim:
        plt.ylim(0, ylim)  # Adjust the upper limit of the y-axis as needed
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
            selected_signals.append(square_wave(t, amplitude=1, shift=1, width=1))
            labels.append('Square Wave')
        elif choice == 2:
            selected_signals.append(triangle_wave(t, shift=1, amplitude=1, width=1))
            labels.append('Triangle Wave')
        elif choice == 3:
            selected_signals.append(exponential_wave(t, amp=1, tau=1))
            labels.append('Exponential Wave')
        elif choice == 5:
            selected_signals.append(sinusoidal_wave(t, A=2, f=0.5, φ=0))
            labels.append('Sinusoidal Wave')
        elif choice == 6:
            selected_signals.append(cosinusoidal_wave(t, A=3, f=0.1, phase=0))
            labels.append('Cosinusoidal Wave')
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

    # Obliczenie splotu
    t_conv, result, x = convolution(selected_signals[0], selected_signals[1], dt)

    # Finding the maximum value of the convolution result
    max_result = np.max(result)

    # Setting the y-axis limit for the convolution plot
    ylim_convolution = min(4, max_result * 1.1)  # Set the maximum y-axis limit as 4 or 110% of the max result, whichever is smaller

    # Displaying the plots
    plot_signals(t, selected_signals, labels, 'Selected Signals')
    plot_signals(t_conv, [result], ['Convolution Result'], 'Convolution Result', ylim=ylim_convolution)


if __name__ == "__main__":
    main()
