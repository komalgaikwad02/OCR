import re
from PIL import Image
import cv2
import numpy
import pytesseract

class Image_Orientation:

    def __init__(self):
        pass

    def handle_image_orientation(self, filename):
        img_path = Image.open(filename)
        opencvImage = cv2.cvtColor(numpy.array(img_path), cv2.COLOR_RGB2BGR)
        newdata = pytesseract.image_to_osd(opencvImage, nice=1)

        angle = int((re.search('(?<=Rotate: )\d+', newdata).group(0)))
        if angle == 90:
            image = Image.open(filename)
            return image.rotate(270, expand=True)

        if angle == 180:
            image = Image.open(filename)
            return image.rotate(180, expand=True)

        if angle == 270:
            image = Image.open(filename)
            return image.rotate(90, expand=True)
        if angle == 0:
            image = Image.open(filename)
            return image

'''
img_path = 'images/12.jpg'
im = skimage.io.imread(img_path)
newdata = pytesseract.image_to_osd(im, nice=1)
angle = int((re.search('(?<=Rotate: )\d+', newdata).group(0)))
if angle == 90:
    for file in glob.glob(img_path):
        image = Image.open(file)
        image.rotate(270, expand=True).save('images/rotated.jpg')

if angle == 180:
    for file in glob.glob(img_path):
        image = Image.open(file)
        image.rotate(180, expand=True).save('images/rotated.jpg')

if angle == 270:
    for file in glob.glob(img_path):
        image = Image.open(file)
        image.rotate(90, expand=True).save('images/rotated.jpg')

'''