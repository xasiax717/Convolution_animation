import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from convolution import plot_signals
from convolution import convolution
from convolution import square_wave_non_periodic
from convolution import triangle_wave_non_periodic


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Convolution")

        self.rect_fig = Figure(figsize=(5, 3), tight_layout=True)
        self.ax1 = self.rect_fig.add_subplot(111)
        self.rect_plot()

        self.tri_fig = Figure(figsize=(5, 3), tight_layout=True)
        self.ax2 = self.tri_fig.add_subplot(111)
        self.tri_plot()

        self.conv_fig = Figure(figsize=(5, 3), tight_layout=True)
        self.ax3 = self.conv_fig.add_subplot(111)
        self.conv_plot()

        self.rect_canvas = FigureCanvasTkAgg(self.rect_fig, master=self.master)
        self.rect_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.tri_canvas = FigureCanvasTkAgg(self.tri_fig, master=self.master)
        self.tri_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.conv_canvas = FigureCanvasTkAgg(self.conv_fig, master=self.master)
        self.conv_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def rect_plot(self):
        dt = 0.01
        t = np.arange(-10, 10, dt)
        rect = square_wave_non_periodic(t, T=2)
        #x_values = np.linspace(-0.5, 0.5, 400)
        #y_values = 0*x_values + 1
        self.ax1.plot(t, rect, color='blue')
        self.ax1.set_title("$y=rect(x)$")
        self.ax1.set_xlabel("X")
        self.ax1.set_ylabel("Y")


    def tri_plot(self):
        dt = 0.01
        t = np.arange(-10, 10, dt)
        tri = triangle_wave_non_periodic(t, T=2)

        #x_values = np.linspace(-1, 0, 400)
        #y_values = x_values + 1

        #x_values2 = np.linspace(0, 1, 400)
        #y_values2 = -x_values2 + 1
        self.ax2.plot(t, tri, color='blue')
        #self.ax2.plot(x_values2, y_values2, color='blue')
        self.ax2.set_title("$y = tri(x)$")
        self.ax2.set_xlabel("X")
        self.ax2.set_ylabel("Y")

    def conv_plot(self):
        #x_values = np.linspace(-1.5, 0, 400)
        #y_values = (x_values ** 2) / 2 + (3 * x_values) / 2 + 9 / 8
        #x_values2 = np.linspace(0, 1, 400)
        #y_values2 = (x_values2 ** 2) / 2 - x_values2 / 2 + 1 / 8

        dt = 0.01
        t = np.arange(-10, 10, dt)
        selected_signals = [square_wave_non_periodic(t, T=2), triangle_wave_non_periodic(t, T=2)]
        t_conv, result = convolution(selected_signals[0], selected_signals[1], dt)
        self.ax3.plot(t_conv, result)

        #self.ax3.plot(x_values, y_values, color='blue')
        #self.ax3.plot(x_values2, y_values2, color='blue')
        self.ax3.set_title("$y = conv(rect(x),tri(x))")
        self.ax3.set_xlabel("X")
        self.ax3.set_ylabel("Y")


root = tk.Tk()
app = App(root)
root.mainloop()
