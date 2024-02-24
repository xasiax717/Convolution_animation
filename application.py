import customtkinter
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")  # ,"green", "dark-blue"


# Create signals classes
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
        self.geometry(f"{1300}x{580}")
        # todo: set the icon  of the app
        # configure grid layout (3x3)
        self.grid_columnconfigure((1, 2), weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # todo: set the logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Convolution animation",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.main_button_event, text="Main")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.about_button_event,
                                                        text="About")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.help_button_event, text="Help")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["System","Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
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
                    setattr(self.signal1, attribute, default_value)

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

    def on_enter_continue(self, event):  # hover image continue button
        light_image = Image.open('resources/continue_hover_blue.png')
        photo_light_image = ImageTk.PhotoImage(light_image)
        self.continueButton.configure(image=photo_light_image)
        self.continueButton.configure(fg_color='transparent')

    def on_leave_continue(self, event):
        image = Image.open('resources/continue_blue.png')
        photo_image = ImageTk.PhotoImage(image)
        self.continueButton.configure(image=photo_image)
        self.continueButton.configure(fg_color='transparent')

    def on_enter_pause(self, event):  # hover image pause button
        pause_img = Image.open('resources/pause_hover_red.png')
        pause_photo_img = ImageTk.PhotoImage(pause_img)
        self.pauseButton.configure(image=pause_photo_img)
        self.pauseButton.configure(fg_color='transparent')

    def on_leave_pause(self, event):
        pause_img = Image.open('resources/pause_50.png')
        pause_photo_img = ImageTk.PhotoImage(pause_img)
        self.pauseButton.configure(image=pause_photo_img)
        self.pauseButton.configure(fg_color='transparent')

    def destroy(self):
        for frame in self.modifying_frames:
            frame.destroy()

    def main_button_event(self):  # frame activated when main is chosen
        # create frame of signals type choosing
        self.destroy()
        self.signals_type_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.signals_type_frame)
        self.signals_type_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # todo: change the font
        font = customtkinter.CTkFont(size=20)
        self.label_type_1 = customtkinter.CTkLabel(master=self.signals_type_frame, text="Choose signal 1", width=200,
                                                   height=25, font=font)
        self.label_type_1.grid(row=0, column=0, padx=20, pady=20)
        optionmenu_var_1 = customtkinter.StringVar(value=self.signal1.get_type())  # set initial value

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.signals_type_frame, dynamic_resizing=False,
                                                        values=["Rectangle", "Triangle", "Sinus", "Cosinus",
                                                                "Exponential"], width=200, height=50,
                                                        command=self.choose_type_1_event, variable=optionmenu_var_1)

        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(0, 10))
        self.label_type_2 = customtkinter.CTkLabel(master=self.signals_type_frame, text="Choose signal 2", width=200,
                                                   height=25, font=font)
        self.label_type_2.grid(row=2, column=0, padx=20, pady=10)
        optionmenu_var_2 = customtkinter.StringVar(value=self.signal2.get_type())  # set initial value

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.signals_type_frame, dynamic_resizing=False,
                                                        values=["Rectangle", "Triangle", "Sinus", "Cosinus",
                                                                "Exponential"], width=200, height=50,
                                                        command=self.choose_type_2_event, variable=optionmenu_var_2)

        self.optionmenu_2.grid(row=3, column=0, padx=20, pady=(5, 10))

        # create frame of signals parameters choosing
        signal1 = self.signal1.get_type()
        signal2 = self.signal2.get_type()
        self.signals_parameters_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.signals_parameters_frame)
        self.signals_parameters_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.label1 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter signal 1 parameters:",
                                             font=font)
        self.label1.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 0))

        # create input for signal1
        # labels of inputs and its amount depends on the chosen type of signal
        if signal1 == "Rectangle" or signal1 == "Triangle":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Shift in time")
            self.label_S.grid(row=1, column=1)
            self.label_W = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Width")
            self.label_W.grid(row=1, column=2)
            self.columns_num_1 = 3
        if signal1 == "Sinus" or signal1 == "Cosinus":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0, padx=20)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Frequency")
            self.label_S.grid(row=1, column=1, padx=20)
            self.label_W = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="phase")
            self.label_W.grid(row=1, column=2, padx=20)
            self.columns_num_1 = 3
        if signal1 == "Exponential":
            self.label_A = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A.grid(row=1, column=0, padx=20)
            self.label_S = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Decay rate")
            self.label_S.grid(row=1, column=1, padx=20)
            self.columns_num_1 = 2

        # create input for signal2
        self.label2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Enter signal 2 parameters:",
                                             font=font)
        self.label2.grid(row=3, column=0, columnspan=4, padx=20, pady=(20, 5))
        if signal2 == "Rectangle" or signal2 == "Triangle":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=4, column=0, padx=20)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Shift in time")
            self.label_S_2.grid(row=4, column=1, padx=20)
            self.label_W_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Width")
            self.label_W_2.grid(row=4, column=2, padx=20)
            self.columns_num_2 = 3
        if signal2 == "Sinus" or signal2 == "Cosinus":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=4, column=0, padx=20)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Frequency")
            self.label_S_2.grid(row=4, column=1, padx=20)
            self.label_W_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="phase")
            self.label_W_2.grid(row=4, column=2, padx=20)
            self.columns_num_2 = 3
        if signal2 == "Exponential":
            self.label_A_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Amplitude", anchor="w")
            self.label_A_2.grid(row=4, column=0, padx=20)
            self.label_S_2 = customtkinter.CTkLabel(master=self.signals_parameters_frame, text="Decay rate")
            self.label_S_2.grid(row=4, column=1, padx=20)
            self.columns_num_2 = 2
        self.entries_1 = []
        self.entries_2 = []

        # Create widgets for entries_1
        for i in range(self.columns_num_1):
            entry = customtkinter.CTkEntry(self.signals_parameters_frame)
            entry.grid(row=2, column=i, padx=(20, 20), pady=(0, 0), sticky="nsew")
            self.entries_1.append(entry)

        # Create widgets for entries_2
        for i in range(self.columns_num_2):
            entry = customtkinter.CTkEntry(self.signals_parameters_frame)
            entry.grid(row=5, column=i, padx=(20, 20), pady=(0, 0), sticky="nsew")
            self.entries_2.append(entry)
        self.current_fg_color = self.entries_2[0].cget('fg_color')
        # Create confirm parameters button
        self.confirm_params_button = customtkinter.CTkButton(self.signals_parameters_frame,
                                                             text="Confirm parameters",
                                                             command=self.on_confirm_params_button_click)
        self.confirm_params_button.grid(row=6, column=1, pady=(20, 20))

        # create the simulation frame
        self.simulation_frame = customtkinter.CTkFrame(self)
        self.modifying_frames.append(self.simulation_frame)
        self.simulation_frame.grid_rowconfigure((0, 2), weight=0)
        self.simulation_frame.grid_rowconfigure(1, weight=1)
        self.simulation_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.simulation_frame.grid(row=0, column=2, rowspan=2, padx=(0, 10), pady=(20, 0), sticky="nsew")

        # top text
        continue_img = Image.open('resources/continue_blue.png')
        continue_photo_img = ImageTk.PhotoImage(continue_img)
        pause_img = Image.open('resources/pause_50.png')
        pause_photo_img = ImageTk.PhotoImage(pause_img)
        self.text_label = customtkinter.CTkLabel(self.simulation_frame, text="Press    ", font=font)
        self.text_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))
        self.image_label = customtkinter.CTkLabel(self.simulation_frame, text='', image=continue_photo_img,
                                                  compound="left")
        self.image_label.grid(row=0, column=1, pady=(10, 10))
        rest_label = customtkinter.CTkLabel(self.simulation_frame, text="    to start the animation", font=font)
        rest_label.grid(row=0, column=2, padx=(0, 10), pady=(10, 10))

        # todo: import here the simulation window, use parameters of signals classes (column=0, row=1, columnspan=3)

        # bottom buttons
        self.continueButton = customtkinter.CTkButton(
            self.simulation_frame,
            text='',
            image=continue_photo_img,
            border_width=0,
            width=50,
            fg_color='transparent',
            hover=False
        )
        self.continueButton.bind("<Enter>", self.on_enter_continue)
        self.continueButton.bind("<Leave>", self.on_leave_continue)
        self.continueButton.grid(column=1, row=2, pady=(10, 10))

        self.pauseButton = customtkinter.CTkButton(
            self.simulation_frame,
            text='',
            image=pause_photo_img,
            border_width=0,
            width=50,
            fg_color='transparent',
            hover=False
        )
        self.pauseButton.bind("<Enter>", self.on_enter_pause)
        self.pauseButton.bind("<Leave>", self.on_leave_pause)

        self.pauseButton.grid(row=2, column=2, pady=(10, 10))

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
            ### Convolution Animation App

            Welcome to the Convolution Animation App! This application allows you to visualize convolution operations between two signals.

            #### What is Convolution?

            Convolution is a mathematical operation that combines two signals to produce a third signal. In the context of this app, you can choose different 
            types of signals (e.g., Rectangle, Triangle, Sinus, Cosinus, Exponential) and adjust their parameters to observe how convolution affects them.

            #### How to Use the Application:

            1. **Choosing Signal Types:**
               - Click on the "Choose signal 1" and "Choose signal 2" dropdown menus in the main window to select the types of signals you want to use for 
               convolution.

            2. **Setting Signal Parameters:**
               - After selecting signal types, enter the parameters for each signal in the provided input fields. The parameters to be entered depend on the 
               chosen signal types.

            3. **Confirming Parameters:**
               - Once you've entered the parameters for both signals, click the "Confirm parameters" button to validate and apply them.

            4. **Starting the Animation:**
               - After confirming the parameters, press the play button (green arrow) to start the animation. You can pause the animation at any time by 
               clicking the pause button (red square).

            #### Additional Options:

            - **Appearance Mode:** You can change the appearance mode of the app (Light, Dark, or System) using the dropdown menu in the sidebar.
            - **UI Scaling:** Adjust the size of UI elements by selecting a scaling option from the dropdown menu in the sidebar.

            For further assistance, please refer to the documentation or contact support.
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
        ### Our Team

        Hey there! We're a group of students from the Warsaw University of Technology, Faculty of Electronics and Information Technology. Meet the team:

        - Zuzanna Gorecka
        - Zofia Lewkowicz
        - Emilia Anczarska
        - Dana Betsina
        - Joanna Brodnicka

        Each member brings a unique set of skills and perspectives to the table, contributing to the success and innovation of our projects.

        ### Our Project

        We've got a project brewing that we're pretty excited about. Basically, we're working on an app to help young 
        students wrap their heads around a tricky part of signals theory called convolution.

        ### Our Goal

        Our main aim? To make learning about signals and convolution way less daunting. We want our app to be super user-friendly and fun to use, so students can dive into the world of signal processing with confidence.

        So, that's us in a nutshell – a bunch of tech enthusiasts on a mission to simplify the complicated and make learning awesome!
        """

        self.textbox.insert("0.0", help_text)
        self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
