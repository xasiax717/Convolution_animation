import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from convolution import convolution
from convolution import triangle_wave_non_periodic
from convolution import square_wave_non_periodic

def AnimatedPlot(root, signal1_name, signal2_name, param1, param2):
    dt = 0.01
    t = np.arange(-10, 10, dt)

    signal1 = triangle_wave_non_periodic(t, 2)
    signal2 = square_wave_non_periodic(t, 2)

    x, y = convolution(signal1, signal2, dt)

    # Inicjalizacja wykresu
    fig, ax = plt.subplots()
    line, = ax.plot(x, y)


    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    def update(frame):
        line.set_xdata(x[:frame*100])
        line.set_ydata(y[:frame*100])
        return line,

    # Inicjalizacja animacji
    anim = FuncAnimation(fig=fig, func=update, frames=50, init_func=init, blit=True)

    # Dodanie widżetu wykresu do interfejsu Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    AnimatedPlot(root, "tri", "sqr", 1, 2)
    root.mainloop()