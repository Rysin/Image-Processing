from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

img_1 = cv2.imread('img_3.jpg')
img_1G = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
img_2 = cv2.imread('img_3x.jpg')
img_2G = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)
img_3 = cv2.imread('img_3y.jpg')
img_3G = cv2.cvtColor(img_3, cv2.COLOR_BGR2GRAY)

# ssim_Dx = ssim(img_1, img_2, multichannel=True)
# ssim_Dy = ssim(img_1, img_3, multichannel=True)
# ssim_Dxy = ssim(img_2, img_3, multichannel=True)

ssim_Dx = ssim(img_1G, img_2G, multichannel=False)
ssim_Dy = ssim(img_1G, img_3G, multichannel=False)
ssim_Dxy = ssim(img_2G, img_3G, multichannel=False)

print(ssim_Dx)
print(ssim_Dy)
print(ssim_Dxy)
