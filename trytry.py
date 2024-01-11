import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from convolution import plot_signals
from convolution import convolution
from convolution import square_wave_non_periodic
from convolution import triangle_wave_non_periodic

# def rect_plot():
#     x_values = np.linspace(-0.5, 0.5, 400)
#     y_values = 0*x_values + 1
#     ax1.plot(x_values, y_values, color='blue')
#     ax1.set_title("$y=rect(x)$")
#     ax1.set_xlabel("X")
#     ax1.set_ylabel("Y")
#
def tri_plot():
    fig_tri = Figure(figsize=(5, 3), tight_layout=True)
    ax2 = fig_tri.add_subplot(111)
    x_values = np.linspace(-1, 0, 400)
    y_values = x_values + 1

    x_values2 = np.linspace(0, 1, 400)
    y_values2 = -x_values2 + 1
    ax2.plot(x_values, y_values, color='blue')
    ax2.plot(x_values2, y_values2, color='blue')
    ax2.set_title("$y = tri(x)$")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")

    return fig_tri

def conv_plot():
    fig_conv = Figure(figsize=(5, 3), tight_layout=True)
    ax3 = fig_conv.add_subplot(111)
    dt = 0.01
    t = np.arange(-10, 10, dt)
    selected_signals = [square_wave_non_periodic(t, T=2), triangle_wave_non_periodic(t, T=2)]
    t_conv, result = convolution(selected_signals[0], selected_signals[1], dt)
    ax3.plot(t_conv, result)
    ax3.set_title("$y = conv(rect(x),tri(x))")
    ax3.set_xlabel("X")
    ax3.set_ylabel("Y")

    return fig_conv