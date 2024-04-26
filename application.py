import tkinter
import tkinter as tk
from tkinter import ttk

import customtkinter
from PIL import Image
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")  # ,"green", "dark-blue"


# from convolution import triangle_wave_non_periodic, square_wave_non_periodic, convolution

class Signal1:
    def __init__(self):
        self.type = None
        self.amplitude = None
        self.phase = None
        self.frequency = None
        self.shift = None
        self.width = None
        self.rate = None

    def set_type(self, type):
        self.type = type

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def set_phase(self, phase):
        self.phase = phase

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

    def get_phase(self):
        return self.phase

    def get_shift(self):
        return self.shift

    def get_width(self):
        return self.width

    def get_rate(self):
        return self.rate


class Signal2:
    def __init__(self):
        super().__init__()
        self.type = None
        self.amplitude = None
        self.phase = None
        self.frequency = None
        self.shift = None
        self.width = None
        self.rate = None

    def set_type(self, type):
        self.type = type

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def set_phase(self, phase):
        self.phase = phase

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

    def get_phase(self):
        return self.phase

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
        self.signal2 = Signal2()
        self.signal2.set_type("Rectangle")

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

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=110, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # todo: set the logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Convolution animation",
                                                 font=customtkinter.CTkFont(size=10, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.main_button_event, text="Main")
        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.about_button_event,
                                                        text="About")
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.help_button_event, text="Help")
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=10)
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

    def on_confirm_params_button_click(
            self):  # check do all the parameters have the required format and then set it into signals classes
        global valid_values_1, valid_values_2
        values_1 = []
        values_2 = []
        for entry_1, entry_2 in zip(self.entries_1, self.entries_2):
            # Get the values entered in the entries
            value_1 = entry_1.get()
            value_2 = entry_2.get()
            if not self.check_decimal(value_1):
                entry_1.configure(fg_color='red')
                valid_values_1 = False

            else:
                entry_1.configure(fg_color=self.current_fg_color)
                valid_values_1 = True

            if not self.check_decimal(value_2):
                valid_values_2 = False
                entry_2.configure(fg_color='red')

            else:
                valid_values_2 = True
                entry_2.configure(fg_color=self.current_fg_color)

            values_1.append(value_1)
            values_2.append(value_2)

        # If all values fit the required format, proceed with further actions
        if valid_values_1 and valid_values_2:
            type_1 = self.signal1.get_type()
            type_2 = self.signal2.get_type()

            signal_attributes = {
                "Rectangle": ["amplitude", "shift", "width"],
                "Triangle": ["amplitude", "shift", "width"],
                "Sinus": ["amplitude", "frequency", "phase"],
                "Cosinus": ["amplitude", "frequency", "phase"],
                "Exponential": ["amplitude", "rate"]
            }

            # Set attributes for signal1
            for attribute, value in zip(signal_attributes.get(type_1, []), values_1):
                setattr(self.signal1, attribute, value)
                getattr(self.signal1, f"set_{attribute}")(value)

            # Set attributes for signal2
            for attribute, value in zip(signal_attributes.get(type_2, []), values_2):
                setattr(self.signal2, attribute, value)
                getattr(self.signal2, f"set_{attribute}")(value)

            default_attributes = {
                "Rectangle": {"frequency": None, "phase": None, "rate": None},
                "Triangle": {"frequency": None, "phase": None, "rate": None},
                "Sinus": {"shift": None, "width": None},
                "Cosinus": {"shift": None, "width": None},
                "Exponential": {"shift": None, "width": None}
            }
            # set default (None) values into the rest of attributes
            for attribute, default_value in default_attributes.get(type_1, {}).items():
                if attribute not in signal_attributes.get(type_1, []):
                    print(self.signal1.get_type())
                    setattr(self.signal1, attribute, default_value)
                    print(self.signal1.get_type())

            for attribute, default_value in default_attributes.get(type_2, {}).items():
                if attribute not in signal_attributes.get(type_2, []):
                    setattr(self.signal2, attribute, default_value)
        else:
            self.show_message_box("Invalid Input",
                                  "Please enter valid decimal values (max 2 decimal places, less than 1000000).")
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

    def on_enter_continue(self, event):
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

    # def plot_animation(self, signal1_name, signal2_name, param1, param2):
    #     dt = 0.01
    #     t = np.arange(-10, 10, dt)
    #
    #
    #     x, y = convolution(self.signal1, self.signal2, dt)
    #
    #     # Initialize the plot
    #     fig, ax = plt.subplots()
    #     line, = ax.plot(x, y)
    #
    #     def update(frame):
    #         ax.clear()  # Clear the previous frame
    #         ax.plot(x[:frame * 100], y[:frame * 100])  # Plot the updated data
    #         return line,
    #
    #     anim = FuncAnimation(fig=fig, func=update, frames=50, blit=True)
    #
    #
    #     canvas = FigureCanvasTkAgg(fig, master=self.simulation_frame)
    #     canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    #     canvas.draw()
    #
    #     return anim

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
            self.label_W = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="phase")
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
        self.simulation_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.simulation_frame)
        self.simulation_frame.grid_rowconfigure(0, weight=1)  # Allow the graph to expand vertically
        self.simulation_frame.grid_columnconfigure(0, weight=1)  # Allow the graph to expand horizontally
        self.simulation_frame.grid(row=1, column=1, columnspan=2, padx = (20,10), pady=(20, 0), sticky="nsew")
        # top text
        continue_img = Image.open('resources/continue_blue.png')
        continue_photo_img = customtkinter.CTkImage(continue_img)
        pause_img = Image.open('resources/pause_50.png')
        pause_photo_img = customtkinter.CTkImage(pause_img)
        self.text_label = customtkinter.CTkLabel(self.simulation_frame, text="Press    ", font=font)
        self.text_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))
        self.image_label = customtkinter.CTkLabel(self.simulation_frame, text='', image=continue_photo_img,
                                                  compound="left")
        self.image_label.grid(row=0, column=1, pady=(10, 10))
        rest_label = customtkinter.CTkLabel(self.simulation_frame, text="    to start the animation", font=font)
        rest_label.grid(row=0, column=2, padx=(0, 10), pady=(10, 10))

        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True

        fig = Figure(figsize=(7.00, 3.50))
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 2)
        ax.set_ylim(-1, 1)
        line, = ax.plot([], [], lw=2)

        canvas = FigureCanvasTkAgg(fig, master=self.simulation_frame)
        canvas.draw()

        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Define the animation functions
        def init():
            line.set_data([], [])
            return line,

        def animate(i):
            x = np.linspace(0, 2, 1000)
            y = np.sin(2 * np.pi * (x - 0.01 * i))
            line.set_data(x, y)
            return line,

        # Execute the animation loop
        anim = FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

        tkinter.mainloop()

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
        self.continueButton.grid(column=1, row=0, pady=(10, 10), sticky="e")

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
        self.pauseButton.grid(row=1, column=1, pady=(10, 10), sticky="w")

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

        def toggle_pause_animation(self):
            if hasattr(self, 'anim') and self.anim is not None:
                if self.anim.event_source is not None:
                    if self.anim._running:
                        self.anim.event_source.stop()
                    else:
                        self.anim.event_source.start()

        def toggle_start_animation(self):
            if not hasattr(self, 'anim') or self.anim is None:
                self.init()
                self.anim = FuncAnimation(self.fig, self.animate, frames=200, interval=20, blit=True)
                self.canvas.draw()



    # def toggle_pause_animation(self):
    #     if hasattr(self, 'animation_object') and self.animation_object is not None:
    #         if self.animation_object.event_source is not None:
    #             if self.animation_object._running:
    #                 self.animation_object.event_source.stop()  # Pause the animation
    #             else:
    #                 self.animation_object.event_source.start()  # Resume the animation
    #
    # def toggle_start_animation(self):
    #     if not hasattr(self, 'animation_object') or self.animation_object is None:
    #         # Start the animation
    #         self.animation_object = AnimatedPlot(self, "tri", "sqr", 1, 2)
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