import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from trytry import conv_plot, tri_plot
from animatedPlot import AnimatedPlot

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Yikes")


        frame = ttk.Frame(self.master, width=500)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        #frame_conv = ttk.Frame(self.master)
        #frame_conv.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #function_figure_conv = conv_plot()

        #canvas_conv = FigureCanvasTkAgg(function_figure_conv, frame_conv)
        #canvas_widget_conv = canvas_conv.get_tk_widget()
        #canvas_widget_conv.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame_tri = ttk.Frame(self.master)
        frame_tri.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        function_figure_tri = tri_plot()

        canvas_tri = FigureCanvasTkAgg(function_figure_tri, frame_tri)
        canvas_widget_tri = canvas_tri.get_tk_widget()
        canvas_widget_tri.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        frame_animation = ttk.Frame(self.master)
        frame_animation.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        #Parametry na razie nie działają i zawsze sie rysuje splot trojkata z kwadratem
        AnimatedPlot(frame_animation, "tri", "sqr", 1, 2)




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
