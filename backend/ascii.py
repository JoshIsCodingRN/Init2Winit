import numpy as np
import cv2 as cv
import sys
from PIL import Image, ImageDraw, ImageFont


img = cv.imread(r"C:\Users\howar\Downloads\vegeta.jpg", cv.IMREAD_GRAYSCALE)
assert img is not None, "read error"

height, width = img.shape

print(height, "\n")
print(width)

while (height > 640 or width > 500):
    img = cv.resize(img, (0,0), fx= 0.9, fy = 0.9)
    height, width = img.shape

print(height, "\n")
print(width)

#Gaussian filtering
blur = cv.GaussianBlur(img,(5,5),0)
img = blur

strung = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
finalString = ""



#with open("output.txt", "w") as f:
#   sys.stdout = f
image = Image.new('RGB', (width * 12, height * 12), (0, 0 , 0))

draw = ImageDraw.Draw(image)

for i in range(height):
    for j in range(width):
        intensity = img[i, j]
        #print(intensity)
        finalString += strung[int(intensity / 3.80)] + " "
    #f.write(finalString + "\n")
    draw.text((0,i * 12), finalString + "\n", font = ImageFont.truetype("consola.ttf"))
    finalString = ""

image.show()
image.save("frame.jpg")
#f.close()           





