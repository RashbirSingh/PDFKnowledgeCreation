#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:59:50 2019

@author: ubuntu
"""
from pdf2image import convert_from_path 
from PIL import Image
import matplotlib.pyplot as plt
import ocr
import PIL.ImageOps
import pytesseract

pdf_path = '/home/ubuntu/Desktop/5.pdf'
img = convert_from_path(pdf_path, dpi=500, first_page=3, last_page=3)
img[0].save('Test.jpeg', 'JPEG')
imag = Image.open('Test.jpeg')
imag = imag.crop((294, 734, 3984, 3279))
imag.save('Test.jpeg', 'JPEG')

indexContent = str(pytesseract.image_to_string(Image.open('Test.jpeg'), lang='eng'))
plt.imshow(imag)
print(indexContent)