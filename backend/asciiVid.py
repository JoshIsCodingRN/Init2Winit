from pathlib import Path
from time import sleep
import numpy as np
import cv2 as cv
import sys
import imageio.v2 as io
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont


cap = cv.VideoCapture(r"C:\Users\howar\Downloads\9000.gif")
assert cap is not None, "read error"

w = cap.get(cv.CAP_PROP_FRAME_WIDTH);
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT); 

#fourcc = cv.VideoWriter_fourcc(*'mp4v')
#out = cv.VideoWriter('output.avi', fourcc, 1, (int(w), int(h)))

for n in range(int(cap.get(cv.CAP_PROP_FRAME_COUNT))):
    _, img = cap.read()
    
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    img = cv.Laplacian(gray, cv.CV_64F)

    height, width = img.shape

    #print(height, "\n")
    #print(width)

    while (height > 640 or width > 500):
        img = cv.resize(img, (0,0), fx= 0.9, fy = 0.9)
        height, width = img.shape

    #print(height, "\n")
    #print(width)

    #Gaussian filtering
    #blur = cv.GaussianBlur(img,(5,5),0)
    #img = blur



    strung = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
    finalString = ""

    

    #with open("output.txt", "w") as f:
    #   sys.stdout = f
    image = Image.new('RGB', (width * 12, height * 12), (255, 255 , 255))

    draw = ImageDraw.Draw(image)

    for i in range(height):
        for j in range(width):
            intensity = abs(img[i, j])

            if(intensity * 3.8 > 255):
                finalString += "." + " "
            else:
            #print(intensity)
                finalString += strung[int(intensity / 3.80)] + " "
        #f.write(finalString + "\n")
        draw.text((0,i * 12), finalString + "\n", font = ImageFont.truetype("consola.ttf"), fill = "black")
        finalString = ""

    image.save(r".\frames\\" + str(n) + ".png")
    
    print(n / int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
    #f.close()
    
images = []

for file in Path("C:\\Users\\howar\\Documents\\Workspace1\\Apphack25\\Init2Winit\\backend\\frames\\").iterdir():
    images.append(io.imread(str(file)))

io.mimsave("output.gif", images, duration = cap.get(cv.CAP_PROP_FPS), loop = 0)

"""
with io.get_writer("output.gif", mode = 'I') as writer:
    for filename in "C:\\Users\\howar\\Documents\\Workspace1\\Apphack25\\Init2Winit\\backend\\frames\\":
        image = io.imread(filename)
        writer.append_data(image)
"""

cap.release()