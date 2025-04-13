from pathlib import Path
from ascii import asciiImage
from time import sleep
import numpy as np
import cv2 as cv
import sys
import os
import imageio.v2 as io
from PIL import Image, ImageDraw, ImageFont

i = 0

directory = "./Init2Winit/backend/images/"
for filename in os.listdir(directory):
    i+=1
    print(str(i) + ":" + str(filename))

choice = input("choose the file you would like to ASCIIFY \n")
quality = int(input("Enter the output quality (50 -> 300) for videos \n\n"))


cap = cv.VideoCapture(directory + str(choice))
w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
# get resize factor to fit within 200x200 pixels
# This is done to avoid slow speed issues with large images
resizeFactor = 0
while (h > quality or w > quality):
    h = h * 0.9
    w = w * 0.9
    resizeFactor += 1
print("resize factor:" + str(resizeFactor))
rf = pow(0.9, resizeFactor)
# list of every character in the ascii table with decreasing intensity
strung = r"$B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
frames = []
# LOOP FOR EACH FRAME
for n in range(int(cap.get(cv.CAP_PROP_FRAME_COUNT))):
    finalString = ""
    # Read the frame into an image, numpy array
    _, img = cap.read()
    # turn the image into grayscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # laplacian filter to get the edges of the image
    if (cap.get(cv.CAP_PROP_FRAME_COUNT) > 1):
        pass
    else:
       asciiImage(choice)
       break
    # resizing the image to fit within 200x200 pixels
    img = cv.resize(img, (0,0), fx= rf, fy = rf)
    height, width = img.shape
    image = Image.new('RGB', (width * 12, height * 12), (255, 255 , 255))
    draw = ImageDraw.Draw(image)
    # loop through each pixel in the image and get the intensity of the pixel
    # then get the corresponding character from the string and add it to the final string
    for i in range(height):
        for j in range(width):
            intensity = img[i, j]
            if(intensity * 1.5 > 255):
                finalString += ".."
            else:
                finalString += strung[int(intensity / 3.8)]*2
        draw.text((0,i * 12), finalString + "\n", font = ImageFont.truetype("consola.ttf"), fill = "black")
        # reset final string each interation so it can fill up with characters from new frame
        finalString = ""
    frames.append(image)
    
    print(str(int(100 * (n / cap.get(cv.CAP_PROP_FRAME_COUNT)))) + "%")
    
if (cap.get(cv.CAP_PROP_FRAME_COUNT) > 1):
    io.mimsave("output.gif", frames, duration = cap.get(cv.CAP_PROP_FPS), loop = 0)

cap.release()
