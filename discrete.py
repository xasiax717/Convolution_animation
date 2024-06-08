import numpy as np
import tkinter as tk

colors = ['#FFC0CB', '#40f4cd', '#faa009', '#d20057', '#135bb9', '#ffd700']

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, fill='black'):
    canvas.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, style=tk.ARC, outline=fill)
    canvas.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, style=tk.ARC, outline=fill)
    canvas.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, style=tk.ARC, outline=fill)
    canvas.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, style=tk.ARC, outline=fill)
    canvas.create_line(x1 + radius, y1, x2 - radius, y1, fill=fill)
    canvas.create_line(x1 + radius, y2, x2 - radius, y2, fill=fill)
    canvas.create_line(x1, y1 + radius, x1, y2 - radius, fill=fill)
    canvas.create_line(x2, y1 + radius, x2, y2 - radius, fill=fill)

def draw_array(canvas, array, start_x, start_y, label, current=None):
    cell_width = 38
    cell_height = 38
    for i, value in enumerate(array):
        x0 = start_x + i * cell_width
        y0 = start_y
        x1 = x0 + cell_width
        y1 = y0 + cell_height
        if i == current:
            canvas.create_rectangle(x0, y0, x1, y1, fill="pink")
        else:
            canvas.create_rectangle(x0, y0, x1, y1, fill="white")
        canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value))
    canvas.create_text(start_x - 20, start_y + cell_height / 2, text=label, anchor=tk.E)

def init_animation(canvas, x, h, x_start_x, x_start_y, h_start_x, h_start_y):
    canvas.delete("all")
    draw_array(canvas, x, x_start_x + (len(h)) * 38, x_start_y, 'x[n]')
    draw_array(canvas, h, h_start_x, h_start_y, 'h[n]')

def update_animation(canvas, k, x, h, x_start_x, x_start_y, h_start_x, h_start_y, y_start_x, y_start_y, colors, y):
    cell_width = 38
    cell_height = 38
    n = len(x) + len(h) - 1
    x_padded = np.pad(x, (0, len(h) - 1), 'constant')
    h_padded = np.pad(h, (0, len(x) - 1), 'constant')

    canvas.delete("all")
    draw_array(canvas, x, x_start_x + (len(h)) * cell_width, x_start_y, 'x[n]')
    h_shifted = [0] * k + list(h) + [0] * (len(x_padded) - k - len(h))
    draw_array(canvas, h, h_start_x + (k + 1) * cell_width, h_start_y, 'h[n]')

    equations = []

    for i in range(min(k + 1, len(x))):
        if k - i < len(h):
            color = colors[i % len(colors)]
            create_rounded_rectangle(canvas, x_start_x + 5 + i * cell_width + (len(h)) * cell_width, x_start_y + 5,
                                     x_start_x + cell_width - 5 + i * cell_width + (len(h)) * cell_width,
                                     h_start_y + cell_height - 5, radius=15, fill=color)
            equation = f"{x[i]}*{h[k - i]}"
            equations.append(equation)
            canvas.create_text(x_start_x + (i + 0.5) * cell_width + (len(h)) * cell_width, h_start_y - 15,
                               text=equation, fill=color)

    result_equation = " + ".join(equations)
    result_text = f"y[{k}] = {result_equation}"

    text_bbox = canvas.create_text(x_start_x + (k + 1) * cell_width + (len(h)) * cell_width,
                                   x_start_y - 25, text=result_text, fill="black")
    bbox = canvas.bbox(text_bbox)
    padding = 5
    canvas.create_rectangle(bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding,
                            fill="pink", outline="black")

    canvas.create_text(x_start_x + (k + 1) * cell_width + (len(h)) * cell_width, x_start_y - 25,
                       text=result_text, fill="black")

    y_el = 0
    for i in range(min(k + 1, len(x))):
        if k - i < len(h):
            y_el += x[i] * h[k - i]

    y.append(y_el)

    draw_array(canvas, y, y_start_x + (len(h)) * cell_width, y_start_y, 'y[n]', current=k)
    if k < n - 1:
        canvas.after(500, update_animation, canvas, k + 1, x, h, x_start_x, x_start_y, h_start_x, h_start_y, y_start_x, y_start_y, colors, y)
