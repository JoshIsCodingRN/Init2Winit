from pathlib import Path
from time import sleep
import numpy as np
import cv2 as cv
import sys
import os
import imageio.v2 as io
from PIL import Image, ImageDraw, ImageFont


cap = cv.VideoCapture(r"./images/9000.gif")

w = cap.get(cv.CAP_PROP_FRAME_WIDTH);
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT); 

# get resize factor to fit within 200x200 pixels
# This is done to avoid slow speed issues with large images
resizeFactor = 0
while (h > 200 or w > 200):
    h = h * 0.9
    w = w * 0.9
    resizeFactor += 1
print("resize factor:" + str(resizeFactor))
rf = pow(0.9, resizeFactor)

# list of every character in the ascii table with decreasing intensity
strung = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
frames = []

# LOOP FOR EACH FRAME
for n in range(int(cap.get(cv.CAP_PROP_FRAME_COUNT))):
    finalString = ""
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

    frames.append(image)
    
    print(str(int(100 * (n /cap.get(cv.CAP_PROP_FRAME_COUNT)))) + "%")
    
io.mimsave("output.gif", frames, duration = cap.get(cv.CAP_PROP_FPS), loop = 0)

cap.release()
