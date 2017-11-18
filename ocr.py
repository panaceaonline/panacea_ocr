#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import json
sys.path.append("./lib")

from colorama import *
init(autoreset=True)

from lib.decorator import *

@decor_function_call
def rotateImage(image_input):
    """
    Ищем угол поворота картинки
    https://github.com/kakul/Alyn

    sigma:canny edge detection blurring
    plot_hough: display hough lines detected
    num_peaks: control the number of hough line peaks

    """

    from alyn import SkewDetect
    from alyn import Deskew

    sd = SkewDetect(
    	input_file=image_input,
    	batch_path='./',
    	output_file='./out/1.rotate.txt',
    	display_output='No',
        sigma=3.0,
        num_peaks=20,
        plot_hough='No',
        )
    sd.run()

    image_out = './out/1.rotated.png'

    d = Deskew(
    	input_file=image_input,
    	display_image='No',
    	output_file=image_out,
    	r_angle=0
    )
    d.run()

    return image_out


@decor_function_call
def cropImage(image_input):
    """
    Кропаем картинку, ищем текстовый блок

    """

    # from process_image import crop_morphology

    image_out = './out/2.crop.png'

    # ТОДО переписать на функцию
    os.system("lib/crop_morphology.py {} {}".format(image_input, image_out))

    # process_image(image_input, image_out)

    return image_out


@decor_function_call
def binarImage(image_input):
    """
    Биномиризация картинки, ч.б.
    python lib/process_image.py out/2.crop.png out/3.binar.png
    """

    image_out = './out/3.binar.png'

    # ТОДО переписать на функцию
    os.system("lib/process_image.py {} {}".format(image_input, image_out))

    return image_out


# @decor_function_call
def extractTextTesseract(image_input):
    """
    Распознаем текст tesseract-ocr
    """
    from PIL import Image
    import pytesseract

    out_text = pytesseract.image_to_string(Image.open(image_input), lang='rus')

    print (out_text)

    return out_text


def rescaleImage(image_input):
    """
    Увеличиваем размерчик
    convert example.png -resize 200 example.png
    """

    image_out = './out/rescale.png'

    os.system("convert {} -resize 2000 -auto-level {}".format(image_input, image_out))

    return image_out




##########################################################################
if __name__ == '__main__':

    if len(sys.argv) > 1:
        # получили айди напрямую
        print sys.argv
        image_input = str(sys.argv[1])

    if image_input:
        print(image_input)

        # rescaled = rescaleImage(image_input)
        image1step = rotateImage(image_input=image_input)
        text = extractTextTesseract(image1step)
        print (len(text))

        image2step = cropImage(image_input=image1step)
        rescaled = rescaleImage(image2step)
        text = extractTextTesseract(rescaled)
        print (len(text))

        image3step = binarImage(image_input=image2step)
        text = extractTextTesseract(image3step)
        print (len(text))
