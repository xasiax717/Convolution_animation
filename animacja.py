import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots()
t = np.linspace(0, 3, 300)
rect_signal = np.where((t >= 0) & (t <= 1), 1, 0)  # Rectangular signal
tri_signal = np.maximum(0, 1 - np.abs(t - 1))  # Triangular signal
conv_result = np.convolve(rect_signal, tri_signal, mode='full')[:len(t)]

line1, = ax.plot(t, rect_signal, label='Rectangular Signal')
line2, = ax.plot(t, tri_signal, label='Triangular Signal')
line3, = ax.plot(t, conv_result, label='Convolution Result', linestyle='dashed', alpha=0.7)

ax.set(xlim=[0, 3], ylim=[-0.5, 2.5], xlabel='Time [s]', ylabel='Amplitude')
ax.legend()

def update(frame):
    line1.set_xdata(t[:frame])
    line1.set_ydata(rect_signal[:frame])

    line2.set_xdata(t[:frame])
    line2.set_ydata(tri_signal[:frame])

    line3.set_xdata(t[:frame])
    line3.set_ydata(conv_result[:frame])

ani = animation.FuncAnimation(fig=fig, func=update, frames=len(t), interval=30)
plt.show()
