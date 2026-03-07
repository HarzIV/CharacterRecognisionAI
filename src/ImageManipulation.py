import cv2
import numpy as np
from PIL import Image, ImageOps
from os import listdir, path, remove

class ImMan:
    @staticmethod
    def savePILImage(image: Image) -> None:
        image.save("tmp/Raw.png")
    
    @staticmethod
    def saveMatrixAsImg(matrix: np.ndarray):
        image = Image.fromarray(matrix)
        image.save("tmp/Prepared.png")

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

            # image.save(f"tmp/group{labelNumber}.jpeg")
            images.append(image)
        
        # images = np.array(images)
        
        return images
    
    @staticmethod
    def findBoundingBox(stat: np.ndarray) -> tuple:
        x = stat[0]
        y = stat[1]
        w = stat[2]
        h = stat[3]

        boundingBox = x, y, x + w, y + h
    
        return boundingBox

    @classmethod
    def cropImages(self, image: Image, stat: np.ndarray) -> Image:
        boundingBox = self.findBoundingBox(stat)
        croppedImage = image.crop(boundingBox)
        
        return croppedImage
    
    @staticmethod
    def findBoundingBoxV2(image: Image):
        BORDER = 5
        pixels = image.load()
        w, h = image.size

        rx1, ry1, rx2, ry2 = w, h, 0, 0

        # Find bounding box of non-white pixels
        for y in range(BORDER, h - BORDER):
            for x in range(BORDER, w - BORDER):
                # print("Pixels: ", pixels[x, y])
                value = pixels[x, y]
                if value != 255:
                    rx1 = min(rx1, x)
                    ry1 = min(ry1, y)
                    rx2 = max(rx2, x)
                    ry2 = max(ry2, y)

        # Compute width and height
        nw, nh = rx2 - rx1 + 1, ry2 - ry1 + 1

        # Make square by expanding the smaller dimension
        if nw > nh:
            diff = nw - nh
            ry1 -= diff // 2
            ry2 += diff - diff // 2
        else:
            diff = nh - nw
            rx1 -= diff // 2
            rx2 += diff - diff // 2

        # Clamp to image boundaries
        rx1 = max(0, rx1)
        ry1 = max(0, ry1)
        rx2 = min(w - 1, rx2)
        ry2 = min(h - 1, ry2)

        return rx1, ry1, rx2, ry2
    
    @classmethod
    def cropV2(self, image: Image) -> Image:
        boundingBox = self.findBoundingBoxV2(image)
        
        croppedImage = image.crop(boundingBox)

        return croppedImage

    @staticmethod
    def scaleImage(image: Image) -> Image:
        scaledImage = image.resize((28, 28), Image.Resampling.LANCZOS)

        return scaledImage
    
    @staticmethod
    def deleteFiles(directory: str) -> None:
        for f in listdir(directory):
            remove(path.join(directory, f))
    
    @classmethod
    def getCharacterImages(self, image: Image) -> list:
        num_labels, labels, stats, centroids = self.findPixelGroups(image)
        # print(stats)
        stats = stats[1:] # Remove the first element, as thats the background.
        # print(stats)
        
        self.deleteFiles("tmp/processed/") # Delete files from previous process.
        images = self.isolateImages(labels, num_labels)

        processedImages = []
        
        for stat, image in zip(stats, images):
            print("Stats:")
            print(stat)
            image.save(f"tmp/unedited.png")
            croppedImage = self.cropV2(image)
            croppedImage.save(f"tmp/croppedImage.png")
            scaledImage = self.scaleImage(croppedImage)
            scaledImage.save(f"tmp/scaledImage.png")

            processedImages.append(scaledImage)
        
        for i in range(len(processedImages)):
            processedImages[i].save(f"tmp/processed/processed{i}.png")
        
        return processedImages