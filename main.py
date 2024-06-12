import os
import time
import tkinter as tk
import random
from tkinter import ttk

import customtkinter
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from convolution import convolution, triangle_wave, square_wave, exponential_wave, sinusoidal_wave, cosinusoidal_wave
from discrete import init_animation, update_animation, pause_animation, resume_animation, next_step_animation, restart_animation

from PIL import Image, ImageTk


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")  # ,"green", "dark-blue"

class AnimatedPlot:
    def __init__(self, root, signal1, signal2, speed):
        self.signal1 = signal1
        self.signal2 = signal2
        self.dt = 0.005
        self.speed = speed

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
        def generate_legend_label(signal_type, **params):
            if signal_type == 'rect':
                label = r'rect: Width = {width}, Height = {height}'.format(**params)
            elif signal_type == 'tri':
                label = r'Triangular: Base = {base}, Height = {height}'.format(**params)
            elif signal_type == 'exp':
                label = r'Exponential: Rate = {rate}'.format(**params)
            else:
                label = 'Unknown Signal'
            return r'${}$'.format(label)


        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.line, = self.ax.plot(self.x, self.y, label=generate_legend_label('rect', width=10, height=1))
        self.ax.legend(loc='upper left')
        self.ax.set_xlim(-self.xmax-1, self.xmax+1)
        self.ax.set_xlabel('t', loc="right")
        self.ax.set_xlabel('t', fontsize=10, labelpad=20)

        self.ax.set_ylabel('Amplituda', rotation=0)
        self.ax.set_ylabel('Amplituda', fontsize=10, labelpad=20)
        self.ax.xaxis.set_label_coords(1, -0.05)
        self.ax.yaxis.set_label_coords(0.5, 1.02)

        if signal1.get_type() == 'Exponential' or signal2.get_type() == 'Exponential':
            self.ax.set_ylim(self.ylow, self.ylimexp+self.ylimexp*0.5)

        self.fig2, self.ax2 = plt.subplots(figsize=(5, 3))
        self.line_moving, = self.ax2.plot([], [], lw=2)
        self.line_static, = self.ax2.plot([], [], lw=2)
        self.ax2.set_xlabel('τ', loc="right")
        self.ax2.set_xlabel('τ', fontsize=10, labelpad=20)
        self.ax2.set_ylabel('Amplituda', rotation=0)
        self.ax2.set_ylabel('Amplituda', fontsize=10, labelpad=20)
        self.ax2.xaxis.set_label_coords(1, -0.05)
        self.ax2.yaxis.set_label_coords(0.5, 1.05)


        for axis in (self.ax, self.ax2):
            axis.spines['left'].set_position('zero')
            axis.spines['bottom'].set_position('zero')
            axis.spines['left'].set_color('black')
            axis.spines['right'].set_color('None')
            axis.spines['top'].set_color('None')

        self.ax2.set_xlim(-self.xmax, self.xmax)

        print(self.speed, "poczatek")
        self.frame_count = int(round(len(self.x)/200*self.speed**2, 0))
        self.num_frames = len(self.x)/self.frame_count
        self.anim = FuncAnimation(self.fig, self.update, frames=int(self.num_frames), init_func=self.init, blit=True, interval=50)
        self.anim2 = FuncAnimation(self.fig2, self.animate, frames=int(self.num_frames), init_func=self.init, blit=True, interval=50)

        # Add the plot widget to the Tkinter interface using grid
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=(10, 10), columnspan=2, sticky="nsew")
        self.canvas.draw()

        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=root)
        self.canvas2.get_tk_widget().grid(row=1, column=0, padx=10, pady=0, columnspan=2, sticky="nsew")
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
            #shift_caused_by_width = (self.xlim[1] - self.xlim[0])/2 + float(self.signal2.get_width())/2
            #shift_caused_by_shift = abs(float(self.signal2.get_shift()) + float(self.signal1.get_shift()))
            shift = (self.xlim[1] - self.xlim[0])/2 + float(self.signal2.get_width())/2 + float(self.signal1.get_width())/2 + abs(float(self.signal2.get_width()) - float(self.signal1.get_width()))/2 + float(self.signal1.get_width())/2

        else:
            shift = 0
        moving_center = frame * self.dt * self.frame_count - float(self.signal1.get_width())/2 - float(self.signal1.get_shift()) + self.t[0] + shift #+ shift_caused_by_width #+ shift_caused_by_shift

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


class TitlePage(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Title Page")
        self.geometry("800x600")

        # Logo
        logo_image = Image.open("resources/logo.png").resize((90, 50))
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = customtkinter.CTkLabel(self, image=logo_photo, text="")
        logo_label.image = logo_photo
        logo_label.pack(pady=10)

        title_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold")

        title_label = customtkinter.CTkLabel(self, text="We Are Enough", font=title_font)
        title_label.pack(pady=10)

        project_label = customtkinter.CTkLabel(self, text="Project Name: Convolution Animation", font=("Helvetica", 24))
        project_label.pack(pady=5)

        university_label = customtkinter.CTkLabel(self, text="Warsaw University of Technologies",
                                                  font=("Helvetica", 20))
        university_label.pack(pady=5)

        team_title_label = customtkinter.CTkLabel(self, text="Names of our team:", font=("Helvetica", 20, "bold"))
        team_title_label.pack(pady=10)

        team_members = [
            "Joanna Brodnicka (Product Owner)",
            "Zofia Lewkowicz (Scrum Master)",
            "Emilia Janczarska (Naczelny Developer Kraju)",
            "Zuzanna Górecka (Bober)",
            "Dana Betsina (Kluska)"
        ]

        for member in team_members:
            member_label = customtkinter.CTkLabel(self, text=member, font=("Helvetica", 16))
            member_label.pack()

        welcome_label = customtkinter.CTkLabel(self, text="Hello and welcome to our application!",
                                               font=("Helvetica", 20))
        welcome_label.pack(pady=20)

        start_button = customtkinter.CTkButton(self, text="Start", command=self.start_application)
        start_button.pack(pady=20)

    def start_application(self):
        self.destroy()
        app = App()
        app.mainloop()


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
        self.button_discrete_mode = "Discrete"
        self.max_delay = 2000  # Maximum delay in milliseconds
        self.initial_delay = 500  # Initial delay in milliseconds
        self.y = []  # Initialize y here
        self.colors = ['#FFC0CB', '#40f4cd', '#faa009', '#d20057', '#135bb9', '#ffd700']
        self.continue_event = True
        self.speed = 2
        self.is_mode_kenaugh = False

        # Store the original colors
        self.original_bg_color = self.cget("fg_color")

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
        self.grid_rowconfigure(5, weight=1)
        custom_font = customtkinter.CTkFont(family="Times New Roman", size=15, weight="bold")

        self.title_label = customtkinter.CTkLabel(self.sidebar_frame, text="Convolution Animation",
                                                       font=custom_font)
        self.title_label.grid(row=0, column=0, padx=10, pady=10)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.main_button_event, text="Main")
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.about_button_event, text="About")
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.help_button_event, text="Help")
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=10)
        self.toggle_discrete_button = customtkinter.CTkButton(self.sidebar_frame, command=self.discrete_button_activator, text=self.button_discrete_mode, fg_color="red")
        self.toggle_discrete_button.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=10, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=10, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=9, column=0, padx=10, pady=(10, 20))
        self.main_button_event()

        self.set_icon()
        self.original_sidebar_color = self.sidebar_frame.cget("fg_color")
        self.original_button_colors = {
            self.sidebar_button_1: self.sidebar_button_1.cget("fg_color"),
            self.sidebar_button_2: self.sidebar_button_2.cget("fg_color"),
            self.sidebar_button_3: self.sidebar_button_3.cget("fg_color"),
        }
        self.original_optionmenu_colors = {
            self.appearance_mode_optionemenu: (self.appearance_mode_optionemenu.cget("fg_color"), self.appearance_mode_optionemenu.cget("button_color"), self.appearance_mode_optionemenu.cget("button_hover_color")),
            self.scaling_optionemenu: (self.scaling_optionemenu.cget("fg_color"), self.scaling_optionemenu.cget("button_color"), self.scaling_optionemenu.cget("button_hover_color"))
        }

    def set_icon(self):
        image_path = "resources/logo.png"
        image = Image.open(image_path)
        image = image.resize((120, 67), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.logo_label = customtkinter.CTkButton(
            self.sidebar_frame,
            command=self.change_kenaugh_mode,
            image=photo,
            text="",
            hover=False,
            fg_color="transparent"
            )
        self.logo_label.image = photo
        self.logo_label.grid(row=5, column=0, padx=10, pady=(170,170))
        self.iconphoto(True, photo)

    def colorChange(self, bg_color, fg_color):
        for frame in self.modifying_frames:
            frame.configure(fg_color=fg_color)
        self.sidebar_frame.configure(fg_color=fg_color)
        self.configure(fg_color=bg_color)

    def buttonsColorChange(self, fg_color, button_color, hover_color):
        # Iterate over all buttons and configure their foreground color
        for widget in [self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_3]:
            widget.configure(fg_color=fg_color, hover_color=hover_color)
        for widget in [self.appearance_mode_optionemenu, self.scaling_optionemenu]:
            widget.configure(fg_color=fg_color, button_color=button_color, button_hover_color=hover_color)

    def change_kenaugh_mode(self):
        customtkinter.set_appearance_mode("Light")
        self.is_mode_kenaugh = True

        self.colorChange("white", "#f1c6db")
        self.buttonsColorChange("#f300a2", "#30aefd", "#3559E0")
        self.randomKisses()

    def reset_to_original_colors(self):
        self.colorChange(self.original_bg_color, self.original_sidebar_color)
        for widget, original_color in self.original_button_colors.items():
            widget.configure(fg_color=original_color)
        for widget, (fg_color, button_color, hover_color) in self.original_optionmenu_colors.items():
            widget.configure(fg_color=fg_color, button_color=button_color, button_hover_color=hover_color)

    def change_appearance_mode_event(self, new_appearance_mode: str):  # change color scheme of app
        if self.is_mode_kenaugh:
            self.reset_to_original_colors()
            self.is_mode_kenaugh = False
            try:
                self.nails_button.destroy()
                self.pause_continue_button = customtkinter.CTkButton(self.simulation_frame, text="Pause",
                                                                     command=self.toggle_pause_continue)
                self.pause_continue_button.grid(row=2, column=1, pady=20, padx=(300, 10))
            except:
                ...
        customtkinter.set_appearance_mode(new_appearance_mode)

    def randomKisses(self):
        self.labelsKisses = []
        for i in range(50):
            # Schedule the creation of each kiss label with a delay
            self.after(i * 50, self.createKiss)
        # Schedule the fading of kiss labels after 5 seconds
        self.after(5000, self.startFadingKisses)

    def createKiss(self):
        x = random.randint(0, self.winfo_screenwidth() - 50)
        y = random.randint(0, self.winfo_screenheight() - 50)
        kiss = customtkinter.CTkLabel(self, text="💋", font=customtkinter.CTkFont(size=50))
        kiss.place(x=x, y=y)
        # Initial alpha value for fading
        kiss.alpha = 1.0
        self.labelsKisses.append(kiss)

    def startFadingKisses(self):
        for label in self.labelsKisses:
            self.fade_label(label)  # Start the fading process for each label

    def fade_label(self, label):
        if label.alpha > 0:
            label.alpha -= 0.01
            new_color = f"#{int(label.alpha * 255):02x}0000"  # Blend with the background color (assuming background is black)
            label.configure(fg_color=new_color)  # Update the label's color
            # Schedule the next fading step after a short delay
            self.after(50, self.fade_label, label)
        else:
            label.destroy()
    def on_enter_nails(self, event):
        self.nails_button.configure(text="💅🏿")

    def on_leave_nails(self, event):
        self.nails_button.configure(text="💅🏻")

    def discrete_button_activator(self):
        if self.button_discrete_mode == "Discrete":
            self.button_discrete_mode = "Functions"
            self.toggle_discrete_button.configure(text="Functions")
            self.discrete_button_event()
        else:
            self.button_discrete_mode = "Discrete"
            self.toggle_discrete_button.configure(text="Discrete")
            self.main_button_event()

    def add_title_label(self):
        title_label = tk.Label(self, text="Convolution animation", font=("Helvetica", 16))
        title_label.pack(pady=10)



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

            self.simulation_button_event()
            self.animated_plot = AnimatedPlot(self.simulation_frame, self.signal1, self.signal2, self.speed)
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


    def destroy(self):
        for frame in self.modifying_frames:
            frame.destroy()
    def toggle_pause_animation(self):
        if self.continue_event:
            self.pauseButton.configure(text="Continue")
            self.continue_event = False
        else:
            self.pauseButton.configure(text="Pause")
            self.continue_event = True

        if self.continue_event:
            self.animated_plot.toggle_start_animation()
        else:
            self.animated_plot.toggle_pause_animation()

    def toggle_pause_continue(self):
        if not self.is_mode_kenaugh:
            if self.animated_plot.anim_running:
                self.pause_continue_button.configure(text="Continue")
                self.animated_plot.toggle_pause_animation()
            else:
                self.pause_continue_button.configure(text="Pause")
                self.animated_plot.toggle_start_animation()
        else:
            if self.animated_plot.anim_running:
                self.animated_plot.toggle_pause_animation()
            else:
                self.animated_plot.toggle_start_animation()

    def confirm_discrete_parameters(self):
        valid_values = True
        for x_entry, h_entry in zip(self.entries_x, self.entries_h):
            if not self.check_discrete_value(x_entry.get()):
                x_entry.configure(fg_color='red')
                valid_values = False
            else:
                x_entry.configure(fg_color=self.current_fg_color)

            if not self.check_discrete_value(h_entry.get()):
                h_entry.configure(fg_color='red')
                valid_values = False
            else:
                x_entry.configure(fg_color=self.current_fg_color)
        if valid_values:
            self.start_discrete_animation()
        else:
            self.show_message_box("Invalid Input",
                                  "Please enter valid value (max 2 decimal places, [-1000, 1000]).")

    def check_discrete_value(self, value):
        try:
            float_value = float(value)

            if -100 <= float_value <= 100 and (
                    '{:.0f}'.format(float_value) == value or '{:.1f}'.format(float_value) == value):
                return True
            else:
                return False
        except ValueError:
            return False
    def start_discrete_animation(self):
        colors = ['#FFC0CB', '#40f4cd', '#faa009', '#d20057', '#135bb9', '#ffd700']
        x_values = [float(entry.get()) for entry in self.entries_x]
        h_values = [float(entry.get()) for entry in self.entries_h]
        global x, h, n, x_padded, h_padded
        x = np.array(x_values)
        h = np.array(h_values)
        self.y = []  # Use self.y
        n = len(x) + len(h) - 1
        x_padded = np.pad(x, (0, len(h) - 1), 'constant')
        h_padded = np.pad(h, (0, len(x) - 1), 'constant')
        init_animation(self.canvas, x, h, 50, 125, 25, 225)
        self.canvas.after(1000, update_animation, self.canvas, 0, x, h, 50, 125, 50, 225, 50, 25, colors, self.y, self.speed_slider, self.max_delay)


    def update_speed(self):
        speed = self.speed_var.get()
        if speed == "Low":
            speed_val = 1
        elif speed == "Medium":
            speed_val = 2
        elif speed == "High":
            speed_val = 3

        print(f"Speed updated to {self.speed}")
        self.animated_plot.destroy()
        self.animated_plot = AnimatedPlot(self.simulation_frame, self.signal1, self.signal2, speed_val)

    def discrete_button_event(self):
        self.destroy_modifying_frames()
        self.entries_x = []
        self.entries_h = []
        self.arrays_size_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.arrays_size_frame)
        self.arrays_size_frame.grid(row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="nsew")
        # todo: change the font
        font = customtkinter.CTkFont(size=15)
        self.label_type_1 = customtkinter.CTkLabel(master=self.arrays_size_frame, text="Choose 1 array size", width=70, height=10, font=font)
        self.label_type_1.grid(row=0, column=0, padx=20, pady=20)
        optionmenu_var_1 = customtkinter.StringVar(value=self.x_size)  # set initial value

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.arrays_size_frame, dynamic_resizing=False, values=['1', '2', '3', '4', '5', '6'], width=100, height=20, command=self.choose_array_size1_event, variable=optionmenu_var_1)

        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.label_type_2 = customtkinter.CTkLabel(master=self.arrays_size_frame, text="Choose 2 array size", width=70, height=25, font=font)
        self.label_type_2.grid(row=0, column=1, padx=20, pady=10)
        optionmenu_var_2 = customtkinter.StringVar(value=self.h_size)  # set initial value

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.arrays_size_frame, dynamic_resizing=False, values=['1', '2', '3', '4', '5', '6'], width=100, height=20, command=self.choose_array_size2_event, variable=optionmenu_var_2)

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
        self.label2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter array 2 parameters:", font=font)
        self.label2.grid(row=3, column=0, columnspan=cs, pady=(20, 0))

        for i in range(self.h_size):
            entry = customtkinter.CTkEntry(master=self.signals_parameters_frame, width=50, height=50)
            entry.grid(row=4, column=i, padx=1, pady=10)
            self.entries_h.append(entry)

        self.start_button = customtkinter.CTkButton(master=self.signals_parameters_frame, text="Start Animation", command=self.confirm_discrete_parameters)
        self.start_button.grid(row=5, column=0, columnspan=cs, pady=10)
        # create the simulation frame
        self.simulation_frame = customtkinter.CTkFrame(self)
        self.simulation_frame.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(20, 0), sticky="nsew")

        self.canvas = tk.Canvas(self.simulation_frame, width=1200, height=300)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.pause_button = customtkinter.CTkButton(master=self.simulation_frame, text="Pause", command=pause_animation)
        self.pause_button.grid(row=1, column=0, padx=(350,10), pady=10, sticky="w")

        self.resume_button = customtkinter.CTkButton(master=self.simulation_frame, text="Resume", command=lambda: resume_animation(self.canvas, len(self.y), x, h, 50, 150, 50, 250, 50, 50, self.colors, self.y, self.speed_slider, self.max_delay))
        self.resume_button.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.next_step_button = customtkinter.CTkButton(master=self.simulation_frame, text="Next Step", command=lambda: next_step_animation(self.canvas, x, h, 50, 150, 50, 250, 50, 50, self.colors, self.y, self.speed_slider, self.max_delay))
        self.next_step_button.grid(row=1, column=0, padx=(10,350), pady=10, sticky="e")

        self.speed_slider = tk.Scale(self.simulation_frame, from_=0, to=self.max_delay, orient=tk.HORIZONTAL, label="Speed (ms per step)")
        self.speed_slider.set(self.initial_delay)
        self.speed_slider.grid(row=2, column=0, padx=10, pady=10)

    def destroy_modifying_frames(self):
        for frame in self.modifying_frames:
            frame.destroy()
        self.modifying_frames = []
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
        self.confirm_params_button.grid(row=3, column=0, columnspan=7, pady=(20, 20))

    def simulation_button_event(self):
        # create the simulation frame
        self.simulation_frame = customtkinter.CTkFrame(self, height=1000)
        self.modifying_frames.append(self.simulation_frame)  # Allow the graph to expand horizontally
        self.simulation_frame.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(20, 0), sticky="nsew")
        if self.is_mode_kenaugh:
            self.nails_button = customtkinter.CTkButton(
                self.simulation_frame,
                text="💅🏻",
                border_width=0,
                width=50,
                fg_color='transparent',
                font=customtkinter.CTkFont(size=25),
                hover=False,
                command=self.toggle_pause_continue
            )
            self.nails_button.bind("<Enter>", self.on_enter_nails)
            self.nails_button.bind("<Leave>", self.on_leave_nails)
            self.nails_button.grid(row=2, column=1, pady=0, padx=(300,10))

        else:

            self.pause_continue_button = customtkinter.CTkButton(self.simulation_frame, text="Pause",
                                                             command=self.toggle_pause_continue)
            self.pause_continue_button.grid(row=2, column=1, pady=20, padx=(300,10))
        self.speed_var = customtkinter.StringVar(value="Medium")

        self.speed_label = customtkinter.CTkLabel(master=self.simulation_frame, text="Speed: ", width=70,
                                                   height=10)
        self.speed_label.grid(row=2, column=0, pady=0, padx=(0, 100), sticky="w")

        self.low_speed_rb = customtkinter.CTkRadioButton(
            self.simulation_frame, text="Low", variable=self.speed_var, value="Low",command=self.update_speed)
        self.low_speed_rb.grid(row=2, column=0, pady=0, padx=(100, 500))

        self.medium_speed_rb = customtkinter.CTkRadioButton(
            self.simulation_frame, text="Medium", variable=self.speed_var, value="Medium", command=self.update_speed)
        self.medium_speed_rb.grid(row=2, column=0, pady=0, padx=(100, 300))

        self.high_speed_rb = customtkinter.CTkRadioButton(
            self.simulation_frame, text="High", variable=self.speed_var, value="High", command=self.update_speed)
        self.high_speed_rb.grid(row=2, column=0, pady=0, padx=(100, 100))



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
    title_page = TitlePage()
    title_page.mainloop()