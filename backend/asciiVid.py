from pathlib import Path
from time import sleep
import numpy as np
import cv2 as cv
import sys
import os
import imageio.v2 as io
from PIL import Image, ImageDraw, ImageFont


cap = cv.VideoCapture(r"./images/9000.gif")
relpath = r"./frames"
if not os.path.exists(relpath):
    os.makedirs(relpath)
assert cap is not None, "read error"

w = cap.get(cv.CAP_PROP_FRAME_WIDTH);
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT); 

# get resize factor to fit within 200x200 pixels
# This is done to avoid slow speed issues with large images
resizeFactor = 0
while (h > 200 or w > 200):
    h = h * 0.9
    w = w * 0.9
    resizeFactor += 1
print(resizeFactor)
rf = pow(0.9, resizeFactor)

# list of every character in the ascii table with decreasing intensity
strung = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."

# LOOP FOR EACH FRAME
for n in range(int(cap.get(cv.CAP_PROP_FRAME_COUNT))):
    # Read the frame into an image, numpy array
    _, img = cap.read()
    # turn the image into grayscale
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # laplacian filter to get the edges of the image
    img = cv.Laplacian(gray, cv.CV_64F)
    # resizing the image to fit within 200x200 pixels
    img = cv.resize(img, (0,0), fx= rf, fy = rf)
    height, width = img.shape

    image = Image.new('RGB', (width * 12, height * 12), (255, 255 , 255))

    draw = ImageDraw.Draw(image)

    # loop through each pixel in the image and get the intensity of the pixel
    # then get the corresponding character from the string and add it to the final string
    for i in range(height):
        for j in range(width):
            intensity = abs(img[i, j])

            if(intensity * 3.8 > 255):
                finalString += ".."
            else:
                finalString += strung[int(intensity / (3.80 - resizeFactor))]*2
        draw.text((0,i * 12), finalString + "\n", font = ImageFont.truetype("consola.ttf"), fill = "black")
        # reset final string each interation so it can fill up with characters from new frame
        finalString = ""

    image.save(r"./frames/frame" + str(n) + ".png")
    
    print(str(int(100 * (n /cap.get(cv.CAP_PROP_FRAME_COUNT)))) + "%")
    
images = []

for file in Path("./frames").iterdir():
    images.append(io.imread(str(file)))

io.mimsave("output.gif", images, duration = cap.get(cv.CAP_PROP_FPS), loop = 0)

cap.release()