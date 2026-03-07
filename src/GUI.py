import tkinter as tk
from PIL import Image, ImageGrab
from numpy import argmax

from ImageManipulation import ImMan
from ai import predictCharacter
from plot import Graph

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Charactor Recognition AI")
        self.root.attributes("-fullscreen", True)

        recogniseButton = tk.Button(self.root, text="Recognise")
        recogniseButton.bind("<Button>", self.evaluateCanvas)
        recogniseButton.pack()

        self.drawingCanvas = tk.Canvas(
            self.root,
            bd = 2,
            bg = 'white',
            highlightthickness  = 1, 
            # highlightbackground = 'white',
            # width="fill",
            height=350)
        self.drawingCanvas.pack(fill=tk.X, expand=True, anchor="n")
        
        self.drawingCanvas.bind("<Button-1>", self.setPreviousXY)
        self.drawingCanvas.bind("<B1-Motion>", self.paint)
        # If right click is double clicked
        self.drawingCanvas.bind("<Double-Button-3>", self.clearCanvas)

        # Info message at the bottom
        # message = tk.Label(self.root, text="Press and Drag the mouse to draw")
        # message.pack(anchor="n")
        
        # Create the class instance for the probability graphs
        self.probabilityGraph = Graph(self.root)
        # self.probabilityGraph.graphTkWidget.pack(anchor="w")

        self.previous_x = None
        self.previous_y = None
        
    def setPreviousXY(self, event) -> None:
        self.previous_x, self.previous_y = event.x, event.y
        
    def paint(self, event) -> None:
        # python_green = "#476042"
        
        self.drawingCanvas.create_line(
            self.previous_x, self.previous_y, event.x, event.y,
            width=24, fill="#111827", capstyle="round", smooth=True)
        
        self.previous_x, self.previous_y = event.x, event.y
    
    def clearCanvas(self, event) -> None:
        self.drawingCanvas.delete("all")
        
    def getCanvas(self) -> Image:
        image = ImageGrab.grab((self.drawingCanvas.winfo_rootx(), self.drawingCanvas.winfo_rooty(), (self.drawingCanvas.winfo_rootx()+self.drawingCanvas.winfo_width()), (self.drawingCanvas.winfo_rooty()+self.drawingCanvas.winfo_height())))

        return image
    
    def printPredictions(self, predictedCharacters: list) -> None:
        pass

    def evaluateCanvas(self, event) -> None:
        image = self.getCanvas()
        ImMan.savePILImage(image)

        processedImages = ImMan.getCharacterImages(image=image)
        

        # Pipe the images through the AI model to get predictions
        predictedCharacters = []
        groupProbabilities = []
        for image in processedImages:
            probabilities = predictCharacter("models/digit_model.keras", image)

            print(probabilities[0])
            
            groupProbabilities.append(probabilities[0])

            predictedCharacters.append(argmax(probabilities))

        print(predictedCharacters)
        print(type(groupProbabilities[0]))
        
        self.root.after(500, lambda: self.probabilityGraph.play_sequence(groupProbabilities))

    def run(self) -> None:
        self.root.mainloop()


if __name__=="__main__":
    program = GUI()
    program.run()