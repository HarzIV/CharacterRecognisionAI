import tkinter as tk

root = tk.Tk()

clear_button = tk.Button(root, text="Button", padx=5)
clear_button.pack()

recognise_button = tk.Button(root, text="Recognise")
recognise_button.pack()


canvas_width = 500
canvas_height = 150

# def paint(event):
#     python_green = "#476042"
#     x1, y1 = (event.x - 1), (event.y - 1)
#     x2, y2 = (event.x + 1), (event.y + 1)
#     w.create_oval(x1, y1, x2, y2, fill=python_green)

# previous_x
# previous_y

def paint(event):
    python_green = "#476042"

    w.create_line
    w.create_rectangle(event.x,event.y,(event.x+5),(event.y+5),outline=python_green,fill=python_green)

w = tk.Canvas(root,
            bd = 2,
            bg = 'white',
            highlightthickness  = 1, 
            # highlightbackground = 'white',
            width=canvas_width,
            height=canvas_height)
w.pack(expand=tk.YES, fill=tk.BOTH)
w.bind("<B1-Motion>", paint)

message = tk.Label(root, text="Press and Drag the mouse to draw")
message.pack(side=tk.BOTTOM)

root.mainloop()