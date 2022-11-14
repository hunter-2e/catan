import cv2
import numpy as np
from PIL import Image

im_cv = cv2.imread('test.png')

im_cv = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)

cv2.imwrite('test.png', im_cv)