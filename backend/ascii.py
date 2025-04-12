import numpy as np
import cv2 as cv
import sys


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



strung = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^`'."
finalString = ""



with open("output.txt", "w") as f:
    sys.stdout = f

    for i in range(height):
        for j in range(width):
            intensity = img[i, j]
            #print(intensity)
            finalString += strung[int(intensity / 3.80)] + " "
        f.write(finalString + "\n")
        finalString = ""
        
f.close()           

