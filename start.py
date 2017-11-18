#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import json

from colorama import *
init(autoreset=True)


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
    	output_file='./out/rotate.txt',
    	display_output='No',
        sigma=3.0,
        num_peaks=20,
        # plot_hough='yes',
        )
    sd.run()

    d = Deskew(
    	input_file=image_input,
    	display_image='No',
    	output_file='./out/1.rotated.jpg',
    	r_angle=0
    )
    d.run()

    return True


##########################################################################
if __name__ == '__main__':

    if len(sys.argv) > 1:
        # получили айди напрямую
        print sys.argv
        image_input = str(sys.argv[1])

    if image_input:
        print(image_input)

        # отправляем в обработку
        rotateImage(image_input)
