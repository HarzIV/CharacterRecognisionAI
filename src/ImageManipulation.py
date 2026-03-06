import cv2
import numpy as np
from PIL import Image, ImageOps

class ImMan:
    @staticmethod
    def savePILImage(image: Image) -> None:
        image.save("tmp/Raw.jpeg")
    
    @staticmethod
    def saveMatrixAsImg(matrix: np.ndarray):
        image = Image.fromarray(matrix)
        image.save("tmp/Prepared.jpeg")

    @classmethod
    def findPixelGroups(self, image: Image) -> np.ndarray:
        """
        Returns all groups of pixels that are touching each others, as an array.
        """

        # Convert the image captured by PIL into an np.array, because that is the format required by opencv
        imgArray = np.array(image)
        imgArray = cv2.cvtColor(imgArray, cv2.COLOR_RGB2BGR)

        # Greyscale the image and convert it to black and white. (In case of future expansion, to recognise actual handwriting images.)
        gray = cv2.cvtColor(imgArray, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        thresh = 255-thresh # Invert the matrix, because connectedComponents consideres black as the background.
        thresh = cv2.transpose(thresh) # Explained in docs/Transposing.md
        
        self.saveMatrixAsImg(thresh)

        connectivity = 4 # This means that only adjacent edges get counted as touching, 8 would also count diagonals.
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity)
        
        return num_labels, labels, stats, centroids
    
    @staticmethod
    def isolateImages(labels: np.ndarray, num_labels: int) -> np.array:
        labels = cv2.transpose(labels) # Transpose back
        # labels = 255-labels # Invert the color again

        images = []

        for labelNumber in range(1, num_labels):
            group = (labels == labelNumber)
            image = Image.fromarray(group)
            image = ImageOps.invert(image) # Invert the color again
            print(type(image))

            image.save(f"tmp/group{labelNumber}.jpeg")
            images.append(image)
        
        # images = np.array(images)
        
        return images
    
    @staticmethod
    def findBoundingBox(image: Image) -> tuple:
        boundingBox = image.getbbox()
    
        return boundingBox

    @classmethod
    def cropImages(self, image: Image) -> Image:
        boundingBox = self.findBoundingBox(image)
        croppedImage = image.convert("L").crop(boundingBox)

        return croppedImage

    @staticmethod
    def scaleImage(image: Image) -> Image:
        scaledImage = image.resize((28, 28), Image.Resampling.LANCZOS)

        return scaledImage
    
    @classmethod
    def getCharacterImages(self, image: Image) -> list:
        num_labels, labels, stats, centroids = self.findPixelGroups(image)
        images = self.isolateImages(labels, num_labels)
        print(type(image))
        
        processedImages = []
        
        for image in images:
            croppedImage = self.cropImages(image)
            scaledImage = self.scaleImage(croppedImage)

            processedImages.append(scaledImage)
        
        for i in range(len(processedImages)):
            processedImages[i].save(f"tmp/processed{i}.jpeg")
        
        return processedImages