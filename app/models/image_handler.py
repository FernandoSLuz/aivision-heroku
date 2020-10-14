import cv2
import numpy as np 
from PIL import Image
#from matplotlib import pyplot as plt

def convertFromGrayScale(color, grayScaleImg):
        r = grayScaleImg.copy()
        g = grayScaleImg.copy()
        b = grayScaleImg.copy()
        r[r == 0] = color[0]
        g[g == 0] = color[1]
        b[b == 0] = color[2]
        grayScaleImg = cv2.merge((r,g,b))
        return grayScaleImg

def lerp(a, b, t):
    return a*(1 - t) + b*t

def convertFromGrayScaleGradient(color, grayScaleImg):
    white = np.array([255,255,255])
    r = grayScaleImg.copy()
    g = grayScaleImg.copy()
    b = grayScaleImg.copy()
    for x in range(255,-1,-1):
        percentage = float(x)/255
        colorOutput = lerp(color, white, percentage)
        #print(colorOutput)
        r[r == x] = colorOutput[0]
        g[g == x] = colorOutput[1]
        b[b == x] = colorOutput[2]
    grayScaleImg = cv2.merge((r,g,b))
    return grayScaleImg

def Edit_Frame (img, processed_img):
    #COLOR_BGR2YCR_CB
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
    if processed_img == "Pencil_Sketch":
        value = 250
        kernel = 89
        gray_blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
        processed_img = cv2.divide(gray, gray_blur, scale=value)
        processed_img = convertFromGrayScaleGradient(np.array([94,137,255]), processed_img)

    if processed_img == "Pencil_Edge":
        kernel = 7
        laplacian_filter = 5
        noise_reduction = 150
        gray = cv2.medianBlur(gray, kernel) 
        edges = cv2.Laplacian(gray, -1, ksize=laplacian_filter)
        edges_inv = 255-edges
        dummy, processed_img = cv2.threshold(edges_inv, noise_reduction, 255, cv2.THRESH_BINARY)
        processed_img = convertFromGrayScale([44,99,255], processed_img)

    if processed_img == "Grayscale":
        processed_img = gray
    
    return processed_img

###############################################################################
    

def Process_Frame(file, option):
    image = Image.open(file)
    img = np.array(image)
    processed_img_array = Edit_Frame(img, option)
    processed_img = Image.fromarray(processed_img_array)
    print(type(processed_img))
    return processed_img, processed_img_array

def debug_test():
    print("main test opencv and pillow")