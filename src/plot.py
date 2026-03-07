import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Probability Graph")

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Initialize 10 bars with zero height
        self.x_indices = np.arange(10)
        self.bars = self.ax.bar(self.x_indices, np.zeros(10), color='red')
        
        self.ax.set_ylim(0, 1) 
        self.ax.set_xticks(self.x_indices)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def play_sequence(self, data_list, index=0):
        if index < len(data_list):
            new_data = data_list[index]
            
            for bar, val in zip(self.bars, new_data):
                bar.set_height(val)
            
            self.canvas.draw()
            
            self.root.after(1000, lambda: self.play_sequence(data_list, index + 1))
