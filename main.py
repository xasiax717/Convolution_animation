import os
import tkinter as tk
from tkinter import ttk

import customtkinter
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from convolution import convolution, triangle_wave, square_wave, exponential_wave, sinusoidal_wave, cosinusoidal_wave
from discrete import create_rounded_rectangle, draw_array, init_animation, update_animation
from PIL import Image, ImageTk


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")  # ,"green", "dark-blue"

class AnimatedPlot:
    def __init__(self, root, signal1, signal2):
        self.signal1 = signal1
        self.signal2 = signal2
        self.dt = 0.01

        if signal1.get_type() != 'Exponential' and signal2.get_type() != 'Exponential':
            xmax = max(abs(float(signal1.get_shift())) + abs(float(signal1.get_width())) / 2, abs(float(signal2.get_shift())) + abs(float(signal2.get_width())) / 2)

            self.t = np.arange(-xmax, xmax, self.dt)
        else:
            xmax = abs(float(signal1.get_shift())) + abs(float(signal1.get_width())) / 2
            self.t = np.arange(-xmax*2.5, xmax*2.5, self.dt)

        if signal1.get_type() == "Rectangle":
            sig1 = square_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_shift()), float(self.signal1.get_width()))

        if signal1.get_type() == "Triangle":
            sig1 = triangle_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_shift()), float(self.signal1.get_width()))

        if signal1.get_type() == "Exponential":
            sig1 = exponential_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_rate()))

        if signal1.get_type() == "Sinus":
            sig1 = sinusoidal_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_frequency()), float(self.signal1.get_shift()))

        if signal1.get_type() == "Cosinus":
            sig1 = cosinusoidal_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_frequency()), float(self.signal1.get_shift()))


        if signal2.get_type() == "Rectangle":
            sig2 = square_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_shift()), float(self.signal2.get_width()))

        if signal2.get_type() == "Triangle":
            sig2 = triangle_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_shift()), float(self.signal2.get_width()))

        if signal2.get_type() == "Exponential":
            sig2 = exponential_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_rate()))

        if signal2.get_type() == "Sinus":
            sig2 = sinusoidal_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_frequency()), float(self.signal2.get_shift()))

        if signal2.get_type() == "Cosinus":
            sig2 = cosinusoidal_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_frequency()), float(self.signal2.get_shift()))

        self.x, self.y, self.xlim, self.ylimexp = convolution(sig1, sig2, self.dt)
        # self.x = self.x
        # self.y = self.y

        self.xmax = max(xmax, abs(self.xlim[0]), abs(self.xlim[1]))
        print(xmax)
        print(abs(self.xlim[0]))
        print(self.xmax)
        self.ylow = np.min(self.y)
        self.yhigh = np.max(self.y)
        if signal1.get_type() == 'Exponential' or signal2.get_type() == 'Exponential':
            self.xmax = xmax
            self.t = np.arange(self.x[0], self.x[-1], self.dt)
        else:
            self.t = np.arange(self.x[0], self.x[-1], self.dt)

        # Initialize the plot

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.line, = self.ax.plot(self.x, self.y)
        self.ax.set_xlim(-self.xmax-1, self.xmax+1)
        if signal1.get_type() == 'Exponential' or signal2.get_type() == 'Exponential':
            self.ax.set_ylim(self.ylow, self.ylimexp+self.ylimexp*0.5)

        self.fig2, self.ax2 = plt.subplots(figsize=(5, 3))
        self.line_moving, = self.ax2.plot([], [], lw=2)
        self.line_static, = self.ax2.plot([], [], lw=2)

        for axis in (self.ax, self.ax2):
            axis.spines['left'].set_position('zero')
            axis.spines['bottom'].set_position('zero')
            axis.spines['left'].set_color('black')
            axis.spines['right'].set_color('None')
            axis.spines['top'].set_color('None')

        self.ax2.set_xlim(-self.xmax, self.xmax)

        self.speed = 3
        self.frame_count = int(len(self.x)/200*self.speed**2)
        self.num_frames = len(self.x)/self.frame_count
        self.anim = FuncAnimation(self.fig, self.update, frames=int(self.num_frames), init_func=self.init, blit=True, interval=50)
        self.anim2 = FuncAnimation(self.fig2, self.animate, frames=int(self.num_frames), init_func=self.init, blit=True, interval=50)

        # Add the plot widget to the Tkinter interface using grid
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
        self.canvas.draw()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
        self.canvas2.draw()

        amp1 = float(self.signal1.get_amplitude())
        amp2 = float(self.signal2.get_amplitude())

        if amp1 > 0 and amp2 > 0:
            ylim1 = 0
            ylim2 = float(max(amp1, amp2)) + 0.2
        elif amp1 < 0 and amp2 < 0:
            ylim1 = float(min(amp1, amp2)) - 0.2
            ylim2 = 0
        elif amp1 < 0 < amp2:
            ylim1 = amp1 - 0.2
            ylim2 = amp2 + 0.2
        else:
            ylim1 = amp2 - 0.2
            ylim2 = amp1 + 0.2
        plt.ylim(ylim1, ylim2)

        plt.xlim(-self.xmax-1, self.xmax+1)

        self.anim_running = True

    def save_static_plot(self, directory):
        self.fig.canvas.draw()
        self.fig2.canvas.draw()

        # Save the first figure
        image1 = Image.frombuffer('RGBA', self.fig.canvas.get_width_height(), self.fig.canvas.buffer_rgba())
        image1.save(os.path.join(directory, "plot1.png"))

        # Save the second figure
        image2 = Image.frombuffer('RGBA', self.fig2.canvas.get_width_height(), self.fig2.canvas.buffer_rgba())
        image2.save(os.path.join(directory, "plot2.png"))

    # def save_animation_as_gif(self, filename, fps=20):
    #     frames = []
    #
    #     for i in range(100):  # Adjust the range based on your animation frames
    #         self.update(i)
    #         self.animate(i)
    #         self.fig.canvas.draw()
    #         self.fig2.canvas.draw()
    #
    #         image1 = Image.frombuffer('RGBA', self.fig.canvas.get_width_height(), self.fig.canvas.buffer_rgba())
    #         image2 = Image.frombuffer('RGBA', self.fig2.canvas.get_width_height(), self.fig2.canvas.buffer_rgba())
    #         combined_image = Image.new('RGBA', (image1.width + image2.width, max(image1.height, image2.height)))
    #         combined_image.paste(image1, (0, 0))
    #         combined_image.paste(image2, (image1.width, 0))
    #         frames.append(combined_image)
    #
    #     frames[0].save(filename, save_all=True, append_images=frames[1:], optimize=False, duration=1000 / fps, loop=1)

    def toggle_pause_animation(self):
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim2.event_source.stop()
        self.anim_running = not self.anim_running

    def toggle_start_animation(self):
        if not self.anim_running:
            self.anim.event_source.start()
            self.anim2.event_source.start()
        self.anim_running = not self.anim_running

    def init(self):
        self.line.set_data([], [])
        self.line_moving.set_data([], [])
        return self.line, self.line_moving

    def update(self, frame):
        frame_index = frame * self.frame_count
        self.line.set_xdata(self.x[:frame_index])
        self.line.set_ydata(self.y[:frame_index])
        return self.line,

    def animate(self, frame):

        # Compute the center of the moving function based on the frame number
        if self.signal1.get_type() != 'Exponential' and self.signal2.get_type() != 'Exponential':
            shift_caused_by_width = (self.xlim[1] - self.xlim[0] - float(self.signal2.get_width())) / 2
            shift_caused_by_shift = ((self.xlim[1] + self.xlim[0])/2 + float(self.signal2.get_shift())) / 2

        else:
            shift_caused_by_width = 0
            shift_caused_by_shift = 0
        moving_center = frame * self.dt * self.frame_count  - float(self.signal1.get_width())/2 + self.t[0] + shift_caused_by_width

        if self.signal1.get_type() == "Rectangle":
            self.y_moving = square_wave(self.t, float(self.signal1.get_amplitude()), moving_center, float(self.signal1.get_width()))

        if self.signal1.get_type() == "Triangle":
            self.y_moving = triangle_wave(self.t, float(self.signal1.get_amplitude()), moving_center, float(self.signal1.get_width()))

        if self.signal1.get_type() == "Exponential":
            self.y_moving = exponential_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_rate()))

        if self.signal1.get_type() == "Sinus":
            self.y_moving = sinusoidal_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_frequency()), moving_center)

        if self.signal1.get_type() == "Cosinus":
            self.y_moving = cosinusoidal_wave(self.t, float(self.signal1.get_amplitude()), float(self.signal1.get_frequency()), moving_center)

        if self.signal2.get_type() == "Rectangle":
            self.y_static = square_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_shift()), float(self.signal2.get_width()))

        if self.signal2.get_type() == "Triangle":
            self.y_static = triangle_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_shift()), float(self.signal2.get_width()))

        if self.signal2.get_type() == "Exponential":
            self.y_static = exponential_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_rate()))

        if self.signal2.get_type() == "Sinus":
            self.y_static = sinusoidal_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_frequency()), float(self.signal2.get_shift()))

        if self.signal2.get_type() == "Cosinus":
            self.y_static = cosinusoidal_wave(self.t, float(self.signal2.get_amplitude()), float(self.signal2.get_frequency()), float(self.signal2.get_shift()))


        # Update the data for the moving function
        self.line_moving.set_data(-self.t, self.y_moving)

        # Update the data for the static function
        self.line_static.set_data(self.t, self.y_static)

        # Update the convolution plot as well
        self.update(frame)

        return self.line_moving, self.line_static, self.line

    def destroy(self):
        # Stop animations
        if self.anim_running:
            self.anim.event_source.stop()
            self.anim2.event_source.stop()

        # Destroy Tkinter widgets
        self.canvas.get_tk_widget().destroy()
        self.canvas2.get_tk_widget().destroy()

        # Close matplotlib figures
        plt.close(self.fig)
        plt.close(self.fig2)

        # Clear any references to avoid memory leaks
        self.root = None
        self.signal1 = None
        self.signal2 = None
        self.fig = None
        self.fig2 = None
        self.canvas = None
        self.canvas2 = None

# Create signals classes
class Signal1:
    def __init__(self):
        self.type = "Rectangle"
        self.type = None
        self.amplitude = None
        self.frequency = None
        self.shift = None
        self.width = None
        self.rate = None

    def set_type(self, type):
        self.type = type

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude


    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_shift(self, shift):
        self.shift = shift

    def set_width(self, width):
        self.width = width

    def set_rate(self, rate):
        self.rate = rate

    def get_type(self):
        return self.type

    def get_amplitude(self):
        return self.amplitude

    def get_frequency(self):
        return self.frequency


    def get_shift(self):
        return self.shift

    def get_width(self):
        return self.width

    def get_rate(self):
        return self.rate


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.modifying_frames = []
        self.signal1 = Signal1()
        self.signal1.set_type("Rectangle")
        self.signal2 = Signal1()
        self.signal2.set_type("Rectangle")
        self.x_size = 5
        self.h_size = 5
        self.entries_x = []
        self.entries_h = []

        # application window, can change size if need
        self.title("convolution animation")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window's geometry to cover the full screen
        self.geometry(f"{screen_width}x{screen_height}")

        # todo: set the icon  of the app
        # configure grid layout (3x3)
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widget

        self.sidebar_frame = customtkinter.CTkFrame(self, width=110, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.main_button_event, text="Main")
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.about_button_event,
                                                        text="About")
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.help_button_event, text="Help")
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=10)
        self.toggle_discrete_button = customtkinter.CTkButton(self.sidebar_frame, command=self.discrete_button_event, text="Discrete", fg_color="red")
        self.toggle_discrete_button.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System","Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=10, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(10, 20))
        self.main_button_event()

        self.set_icon()

    def set_icon(self):
        # Load the image
        image_path = "resources/logo.png"
        image = Image.open(image_path)
        image = image.resize((90, 50), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, image=photo, text="")
        self.logo_label.image = photo  # keep a reference to the image to prevent garbage collection
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.iconphoto(False, photo)
    def add_title_label(self):
        title_label = tk.Label(self, text="Convolution animation", font=("Helvetica", 16))
        title_label.pack(pady=10)
    def change_appearance_mode_event(self, new_appearance_mode: str):  # change color scheme of app
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):  # change size of elements on the frame
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def choose_type_1_event(self, signalType: str):  # set type of the signal 1
        self.signal1.set_type(signalType)
        self.main_button_event()

    def choose_type_2_event(self, signalType: str):  # set type of the signal 2
        self.signal2.set_type(signalType)
        self.main_button_event()


    def choose_array_size1_event(self, array_size):
        self.x_size = int(array_size)
        self.discrete_button_event()

    def choose_array_size2_event(self, array_size):
        self.h_size = int(array_size)
        self.discrete_button_event()

    def start_animation(self):
        colors = ['#FFC0CB', '#40f4cd', '#faa009', '#d20057', '#135bb9', '#ffd700']
        x_values = [int(entry.get()) for entry in self.entries_x]
        h_values = [int(entry.get()) for entry in self.entries_h]
        global x, h, y, n, x_padded, h_padded
        x = np.array(x_values)
        h = np.array(h_values)
        y = []
        n = len(x) + len(h) - 1
        x_padded = np.pad(x, (0, len(h) - 1), 'constant')
        h_padded = np.pad(h, (0, len(x) - 1), 'constant')
        init_animation(self.canvas, x, h, 50, 150, 50, 250)
        self.canvas.after(1000, update_animation, self.canvas, 0, x, h, 50, 150, 50, 250, 50, 50, colors, y)


    def on_confirm_params_button_click(self):  # check do all the parameters have the required format and then set it into signals classes
        global valid_values
        valid_values = True
        values1 = []
        values2 = []
        if self.signal1.get_type() == "Rectangle" or self.signal1.get_type() == "Triangle":
            value_amp = self.entries_1[0]
            value_shift = self.entries_1[1]
            value_width = self.entries_1[2]
            if not (self.check_amplitude(value_amp.get())):
                value_amp.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid amplitude (max 2 decimal places, [-25, 25]).")

            else:
                value_amp.configure(fg_color=self.current_fg_color)
                values1.append(value_amp.get())

            if not (self.check_shift(value_shift.get())):
                value_shift.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid shift in time (max 2 decimal places, [-10^6, 10^6]).")

            else:
                value_shift.configure(fg_color=self.current_fg_color)
                values1.append(value_shift.get())

            if not (self.check_width(value_width.get())):
                value_width.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid width (max 2 decimal places, [-50, 50]).")

            else:
                value_width.configure(fg_color=self.current_fg_color)
                values1.append(value_width.get())
        if self.signal2.get_type() == "Rectangle" or self.signal2.get_type() == "Triangle":
            value_amp = self.entries_2[0]
            value_shift = self.entries_2[1]
            value_width = self.entries_2[2]
            if not (self.check_amplitude(value_amp.get())):
                value_amp.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid amplitude (max 2 decimal places, [-25, 25]).")

            else:
                value_amp.configure(fg_color=self.current_fg_color)
                values2.append(value_amp.get())

            if not (self.check_shift(value_shift.get())):
                value_shift.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid shift in time (max 2 decimal places, [-10^6, 10^6]).")

            else:
                value_shift.configure(fg_color=self.current_fg_color)
                values2.append(value_shift.get())

            if not (self.check_width(value_width.get())):
                value_width.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid width (max 2 decimal places, [-50, 50]).")

            else:
                value_width.configure(fg_color=self.current_fg_color)
                values2.append(value_width.get())
        if self.signal1.get_type() == "Exponential":
            value_amp = self.entries_1[0]
            value_width = self.entries_1[1]
            if not (self.check_amplitude(value_amp.get())):
                value_amp.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid amplitude (max 2 decimal places, [-25, 25]).")

            else:
                value_amp.configure(fg_color=self.current_fg_color)
                values1.append(value_amp.get())


            if not (self.check_width(value_width.get())):
                value_width.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid width (max 2 decimal places, [-50, 50]).")

            else:
                value_width.configure(fg_color=self.current_fg_color)
                values1.append(value_width.get())
        if self.signal2.get_type() == "Exponential":
            value_amp = self.entries_2[0]
            value_width = self.entries_2[1]
            if not (self.check_amplitude(value_amp.get())):
                value_amp.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid amplitude (max 2 decimal places, [-25, 25]).")

            else:
                value_amp.configure(fg_color=self.current_fg_color)
                values2.append(value_amp.get())

            if not (self.check_width(value_width.get())):
                value_width.configure(fg_color='red')
                valid_values = False
                self.show_message_box("Invalid Input",
                                      "Please enter valid width (max 2 decimal places, [-50, 50]).")

            else:
                value_width.configure(fg_color=self.current_fg_color)
                values2.append(value_width.get())


        # If all values fit the required format, proceed with further actions
        if valid_values:
            type_1 = self.signal1.get_type()
            type_2 = self.signal2.get_type()

            signal_attributes = {
                "Rectangle": ["amplitude", "shift", "width"],
                "Triangle": ["amplitude", "shift", "width"],
                "Sinus": ["amplitude", "frequency", "shift"],
                "Cosinus": ["amplitude", "frequency", "shift"],
                "Exponential": ["amplitude", "rate"]
            }

            # Set attributes for signal1
            for attribute, value in zip(signal_attributes.get(type_1, []), values1):
                setattr(self.signal1, attribute, value)
                getattr(self.signal1, f"set_{attribute}")(value)

            # Set attributes for signal2
            for attribute, value in zip(signal_attributes.get(type_2, []), values2):
                setattr(self.signal2, attribute, value)
                getattr(self.signal2, f"set_{attribute}")(value)

            default_attributes = {
                "Rectangle": {"frequency": None, "shift": None, "rate": None},
                "Triangle": {"frequency": None, "shift": None, "rate": None},
                "Sinus": {"shift": None, "width": None},
                "Cosinus": {"shift": None, "width": None},
                "Exponential": {"shift": None, "width": None}
            }
            # set default (None) values into the rest of attributes
            for attribute, default_value in default_attributes.get(type_1, {}).items():
                if attribute not in signal_attributes.get(type_1, []):
                    setattr(self.signal1, attribute, default_value)

            for attribute, default_value in default_attributes.get(type_2, {}).items():
                if attribute not in signal_attributes.get(type_2, []):
                    setattr(self.signal2, attribute, default_value)
            try:
                self.animated_plot.destroy()
                print("End")
            except:
                ...

            self.animated_plot = AnimatedPlot(self.simulation_frame, self.signal1, self.signal2)
            # self.animated_plot.save_static_plot(directory="C:/Users/Emilia/PycharmProjects/Convolution_animation")
            #self.animated_plot.save_animation_as_gif
            #self.animated_plot.save_animation_as_png_sequence(directory="C:/Users/Emilia/PycharmProjects/Convolution_animation")

        else:
            return

    def show_message_box(self, title, message):  # show the message box if values are not correct
        messagebox = tk.Toplevel()
        messagebox.title(title)
        label = tk.Label(messagebox, text=message)
        label.pack(padx=20, pady=10)
        ok_button = tk.Button(messagebox, text="OK", command=messagebox.destroy)
        ok_button.pack(pady=10)

        messagebox.update_idletasks()
        width = messagebox.winfo_width()
        height = messagebox.winfo_height()
        screen_width = messagebox.winfo_screenwidth()
        screen_height = messagebox.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        messagebox.geometry(f"+{x}+{y}")

        #  todo: change the required format

    def check_decimal(self, value):  # check do the values have the valid format
        try:
            float_value = float(value)

            # Check if the value is a decimal number with at most 2 decimal places and less than 1000000
            if 0 <= float_value < 1000000 and (
                    '{:.2f}'.format(float_value) == value or '{:.0f}'.format(float_value) == value or '{:.1f}'.format(
                float_value) == value):
                return True
            else:
                return False
        except ValueError:
            return False
    def check_amplitude(self, value):
        try:
            float_value = float(value)
            if -1000001 < float_value < 1000001 and ('{:.2f}'.format(float_value) == value
                                           or '{:.0f}'.format(float_value) == value
                                           or '{:.1f}'.format(float_value) == value):
                return True
            else:
                return False
        except ValueError:
            return False
    def check_shift(self, value):
        try:
            float_value = float(value)
            if -21 < float_value < 21 and ('{:.2f}'.format(float_value) == value
                                           or '{:.0f}'.format(float_value) == value
                                           or '{:.1f}'.format(float_value) == value):
                return True
            else:
                return False
        except ValueError:
            return False
    def check_width(self, value):
        try:
            float_value = float(value)
            if -51 < float_value < 51 and ('{:.2f}'.format(float_value) == value
                                           or '{:.0f}'.format(float_value) == value
                                           or '{:.1f}'.format(float_value) == value):
                return True
            else:
                return False
        except ValueError:
            return False
    def on_enter_continue(self, event):  # hover image continue button
        light_image = Image.open('resources/continue_hover_blue.png')
        photo_light_image = customtkinter.CTkImage(light_image)
        self.continueButton.configure(image=photo_light_image)
        self.continueButton.configure(fg_color='transparent')

    def on_leave_continue(self, event):
        image = Image.open('resources/continue_blue.png')
        photo_image = customtkinter.CTkImage(image)
        self.continueButton.configure(image=photo_image)
        self.continueButton.configure(fg_color='transparent')

    def on_enter_pause(self, event):  # hover image pause button
        pause_img = Image.open('resources/pause_hover_red.png')
        pause_photo_img = customtkinter.CTkImage(pause_img)
        self.pauseButton.configure(image=pause_photo_img)
        self.pauseButton.configure(fg_color='transparent')

    def on_leave_pause(self, event):
        pause_img = Image.open('resources/pause_50.png')
        pause_photo_img = customtkinter.CTkImage(pause_img)
        self.pauseButton.configure(image=pause_photo_img)
        self.pauseButton.configure(fg_color='transparent')

    def destroy(self):
        for frame in self.modifying_frames:
            frame.destroy()

    def toggle_pause_animation(self):
        self.animated_plot.toggle_pause_animation()

    def toggle_start_animation(self):
        self.animated_plot.toggle_start_animation()
    def discrete_button_event(self):
        # create frame of signals type choosing
        self.destroy()
        self.entries_x = []
        self.entries_h = []
        self.arrays_size_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.arrays_size_frame)
        self.arrays_size_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="nsew")
        # todo: change the font
        font = customtkinter.CTkFont(size=15)
        self.label_type_1 = customtkinter.CTkLabel(master=self.arrays_size_frame, text="Choose 1 array size", width=70,
                                                   height=10, font=font)
        self.label_type_1.grid(row=0, column=0, padx=20, pady=20)
        optionmenu_var_1 = customtkinter.StringVar(value=self.x_size)  # set initial value

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.arrays_size_frame, dynamic_resizing=False,
                                                        values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], width=100, height=20,
                                                        command=self.choose_array_size1_event, variable=optionmenu_var_1)

        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.label_type_2 = customtkinter.CTkLabel(master=self.arrays_size_frame, text="Choose 2 array size", width=70,
                                                   height=25, font=font)
        self.label_type_2.grid(row=0, column=1, padx=20, pady=10)
        optionmenu_var_2 = customtkinter.StringVar(value=self.h_size)  # set initial value

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.arrays_size_frame, dynamic_resizing=False,
                                                        values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], width=100, height=20,
                                                        command=self.choose_array_size2_event, variable=optionmenu_var_2)

        self.optionmenu_2.grid(row=1, column=1, padx=20, pady=(5, 10))

        # create frame of signals parameters choosing
        signal1 = self.signal1.get_type()
        signal2 = self.signal2.get_type()
        self.signals_parameters_frame = customtkinter.CTkFrame(self)
        self.separator2 = ttk.Separator(self.signals_parameters_frame, orient="horizontal")
        self.separator2.grid(row=3, column=0, columnspan=7, sticky="ew", pady=(10, 0))
        self.modifying_frames.append(self.signals_parameters_frame)
        self.signals_parameters_frame.grid(row=0, column=2, padx=(10, 0), pady=(20, 10), sticky="nsew")
        self.label1 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter array 1 parameters:",
                                             font=font)
        if self.x_size >= self.h_size:
            cs = self.x_size
        else:
            cs = self.h_size
        self.label1.grid(row=0, column=0, columnspan=cs, pady=(20, 0), padx=10)

        # create input for signal1
        # labels of inputs and its amount depends on the chosen type of signal
        for i in range(self.x_size):
            entry = customtkinter.CTkEntry(master=self.signals_parameters_frame, width=50, height=50)
            entry.grid(row=1, column=i, padx=1, pady=10)
            self.entries_x.append(entry)
        self.label2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter array 2 parameters:",
                                             font=font)
        self.label2.grid(row=3, column=0, columnspan=cs, pady=(20, 0))

        for i in range(self.h_size):
            entry = customtkinter.CTkEntry(master=self.signals_parameters_frame, width=50, height=50)
            entry.grid(row=4, column=i, padx=1, pady=10)
            self.entries_h.append(entry)

        self.start_button = customtkinter.CTkButton(master=self.signals_parameters_frame, text="Start Animation",
                                                    command=self.start_animation)
        self.start_button.grid(row=5, column=0, columnspan=cs, pady=10)
        # create the simulation frame
        self.simulation_frame = customtkinter.CTkFrame(self)
        self.simulation_frame.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(20, 0), sticky="nsew")

        self.canvas = tk.Canvas(self.simulation_frame, width=1200, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

    def main_button_event(self):  # frame activated when main is chosen
        # create frame of signals type choosing
        self.destroy()
        self.signals_type_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.signals_type_frame)
        self.signals_type_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="nsew")
        # todo: change the font
        font = customtkinter.CTkFont(size=15)
        self.label_type_1 = customtkinter.CTkLabel(master=self.signals_type_frame, text="Choose signal 1", width=70,
                                                   height=10, font=font)
        self.label_type_1.grid(row=0, column=0, padx=20, pady=20)
        optionmenu_var_1 = customtkinter.StringVar(value=self.signal1.get_type())  # set initial value

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.signals_type_frame, dynamic_resizing=False,
                                                        values=["Rectangle", "Triangle", "Sinus", "Cosinus",
                                                                "Exponential"], width=100, height=20,
                                                        command=self.choose_type_1_event, variable=optionmenu_var_1)

        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.label_type_2 = customtkinter.CTkLabel(master=self.signals_type_frame, text="Choose signal 2", width=70,
                                                   height=25, font=font)
        self.label_type_2.grid(row=0, column=1, padx=20, pady=10)
        optionmenu_var_2 = customtkinter.StringVar(value=self.signal2.get_type())  # set initial value

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.signals_type_frame, dynamic_resizing=False,
                                                        values=["Rectangle", "Triangle", "Sinus", "Cosinus",
                                                                "Exponential"], width=100, height=20,
                                                        command=self.choose_type_2_event, variable=optionmenu_var_2)

        self.optionmenu_2.grid(row=1, column=1, padx=20, pady=(5, 10))

        # create frame of signals parameters choosing
        signal1 = self.signal1.get_type()
        signal2 = self.signal2.get_type()
        self.signals_parameters_frame = customtkinter.CTkFrame(self)
        self.separator = ttk.Separator(self.signals_parameters_frame, orient="vertical")
        self.separator.grid(row=0, column=3, rowspan=3, padx=5, sticky="ns")
        self.separator2 = ttk.Separator(self.signals_parameters_frame, orient="horizontal")
        self.separator2.grid(row=3, column=0, columnspan=7, sticky="ew", pady=(10,0))
        self.modifying_frames.append(self.signals_parameters_frame)
        self.signals_parameters_frame.grid(row=0, column=2, padx=(10, 0), pady=(20, 10), sticky="nsew")
        self.label1 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter signal 1 parameters:",
                                             font=font)
        self.label1.grid(row=0, column=0, columnspan=3, pady=(20, 0))

        # create input for signal1
        # labels of inputs and its amount depends on the chosen type of signal
        if signal1 == "Rectangle" or signal1 == "Triangle":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Shift in time")
            self.label_S.grid(row=1, column=1)
            self.label_W = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Width")
            self.label_W.grid(row=1, column=2, padx=(10,0))
            self.columns_num_1 = 3
        if signal1 == "Sinus" or signal1 == "Cosinus":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0, padx=10)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Frequency")
            self.label_S.grid(row=1, column=1, padx=10)
            self.label_W = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Phase")
            self.label_W.grid(row=1, column=2, padx=(10,0))
            self.columns_num_1 = 3
        if signal1 == "Exponential":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0, padx=10)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Decay rate")
            self.label_S.grid(row=1, column=1, padx=10)
            self.columns_num_1 = 2

        # create input for signal2
        self.label2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter signal 2 parameters:",
                                             font=font)
        self.label2.grid(row=0, column=4, columnspan=4, pady=(20, 5))
        if signal2 == "Rectangle" or signal2 == "Triangle":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=1, column=4, padx=10)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Shift in time")
            self.label_S_2.grid(row=1, column=5, padx=10)
            self.label_W_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Width")
            self.label_W_2.grid(row=1, column=6, padx=10)
            self.columns_num_2 = 3
        if signal2 == "Sinus" or signal2 == "Cosinus":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=1, column=4, padx=10)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Frequency")
            self.label_S_2.grid(row=1, column=5, padx=10)
            self.label_W_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="phase")
            self.label_W_2.grid(row=1, column=6, padx=10)
            self.columns_num_2 = 3
        if signal2 == "Exponential":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=1, column=4, padx=10)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Decay rate")
            self.label_S_2.grid(row=1, column=5, padx=10)
            self.columns_num_2 = 2
        self.entries_1 = []
        self.entries_2 = []

        # Create widgets for entries_1
        for i in range(self.columns_num_1):
            entry = customtkinter.CTkEntry(self.signals_parameters_frame)  # Set width to 5
            entry.grid(row=2, column=i, padx=(5, 5), pady=(0, 0), sticky="nsew")
            self.entries_1.append(entry)

        # Create widgets for entries_2
        for i in range(self.columns_num_2):
            entry = customtkinter.CTkEntry(self.signals_parameters_frame)  # Set width to 5
            entry.grid(row=2, column=i + 4, padx=(5, 5), pady=(0, 0), sticky="nsew")
            self.entries_2.append(entry)
        self.current_fg_color = self.entries_2[0].cget('fg_color')
        # Create confirm parameters button
        self.confirm_params_button = customtkinter.CTkButton(self.signals_parameters_frame,
                                                             text="Confirm parameters",
                                                             command=self.on_confirm_params_button_click)
        self.confirm_params_button.grid(row=3, column=0, columnspan = 7, pady=(20, 20))


        # create the simulation frame
        self.simulation_frame = customtkinter.CTkFrame(self, height=1000)
        self.modifying_frames.append(self.simulation_frame)  # Allow the graph to expand horizontally
        self.simulation_frame.grid(row=1, column=1, columnspan=2, padx = (20,10), pady=(20, 0), sticky="nsew")
        # top text
        continue_img = Image.open('resources/continue_blue.png')
        continue_photo_img = customtkinter.CTkImage(continue_img)
        pause_img = Image.open('resources/pause_50.png')
        pause_photo_img = customtkinter.CTkImage(pause_img)


        # self.animated_plot = AnimatedPlot(self.simulation_frame, self.signal1, self.signal2)

        self.continueButton = customtkinter.CTkButton(
            self.simulation_frame,
            text='',
            image=continue_photo_img,
            border_width=0,
            width=50,
            fg_color='transparent',
            hover=False,
            command=self.toggle_start_animation
        )
        self.continueButton.bind("<Enter>", self.on_enter_continue)
        self.continueButton.bind("<Leave>", self.on_leave_continue)
        self.continueButton.grid(column=1, row=3,padx=(10,550), pady=(10, 10), sticky="e")

        self.pauseButton = customtkinter.CTkButton(
            self.simulation_frame,
            text='',
            image=pause_photo_img,
            border_width=0,
            width=50,
            fg_color='transparent',
            hover=False,
            command=self.toggle_pause_animation
        )
        self.pauseButton.bind("<Enter>", self.on_enter_pause)
        self.pauseButton.bind("<Leave>", self.on_leave_pause)
        self.pauseButton.grid(row=3, column=0,padx=(550,10), pady=(10, 10), sticky="w")

        def on_enter_pause(self, event):
            pause_img_hover = Image.open('resources/pause_hover_red.png')
            pause_photo_img_hover = customtkinter.CTkImage(pause_img_hover)
            self.pauseButton.configure(image=pause_photo_img_hover)
            self.pauseButton.configure(fg_color='transparent')

        def on_leave_pause(self, event):
            pause_img = Image.open('resources/pause_50.png')
            pause_photo_img = customtkinter.CTkImage(pause_img)
            self.pauseButton.configure(image=pause_photo_img)
            self.pauseButton.configure(fg_color='transparent')


    def help_button_event(self):
        self.destroy()
        self.text_about_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.text_about_frame)
        self.text_about_frame.grid(column=1, columnspan=2, row=0, padx=(20, 20), pady=(20, 20))
        self.text_frame_label = customtkinter.CTkLabel(self.text_about_frame, text="FAQ",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.text_frame_label.grid(row=0, column=0, pady=(20, 0))
        self.textbox = customtkinter.CTkTextbox(self.text_about_frame, width=960, height=450)
        help_text = """
            """
        self.textbox.insert("0.0", help_text)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def about_button_event(self):
        self.destroy()
        self.text_about_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.text_about_frame)
        self.text_about_frame.grid(column=1, columnspan=2, row=0, padx=(20, 20), pady=(20, 20))
        self.text_frame_label = customtkinter.CTkLabel(self.text_about_frame, text="About Us",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.text_frame_label.grid(row=0, column=0, pady=(20, 0))
        self.textbox = customtkinter.CTkTextbox(self.text_about_frame, width=960, height=450)
        help_text = """
        """

        self.textbox.insert("0.0", help_text)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    # def destroy_frames(self):
    #     for frame in self.modifying_frames:
    #         if frame.winfo_exists():  # Check if the frame still exists
    #             frame.tkinter.Tk.quit()
    #
    # def on_closing(self):
    #     self.destroy_frames()
    #     super().tkinter.Tk.quit()

    def destroy_frames(self):
        for frame in self.modifying_frames:
            if frame.winfo_exists():
                frame.destroy()

    def on_closing(self):
        self.destroy_frames()
        self.quit()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()