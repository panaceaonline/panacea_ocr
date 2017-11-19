#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import json
import shutil
import hashlib
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
    	output_file=dir_out + '1.rotate.txt',
    	display_output='No',
        sigma=3.0,
        num_peaks=20,
        plot_hough='No',
        )
    sd.run()

    image_out = dir_out + '1.rotated.png'

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

    image_out = dir_out + '2.crop.png'

    # ТОДО переписать на функцию
    os.system("lib/crop_morphology.py {} {}".format(image_input, image_out))

    # process_image(image_input, image_out)

    return image_out


# @decor_function_call
# def binarImage(image_input):
#     """
#     Биномиризация картинки, ч.б.
#     python lib/process_image.py out/2.crop.png out/3.binar.png
#     """
#
#     image_out = dir_out + '3.binar.png'
#
#     # ТОДО переписать на функцию
#     os.system("lib/process_image.py {} {}".format(image_input, image_out))
#
#     return image_out


@decor_function_call
def cleanImage(image_input):
    """
    Используем шел скрипт textcleaner
    http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
    """

    image_out = dir_out + '3.2.clean.png'
    # options = ' -g -e stretch -f 25 -o 20 -t 30 -u -s 1 -T -p 20 '
    options = ' -T -p 20 '

    os.system("sh lib/textcleaner {} {} {}".format(options, image_input, image_out))

    return image_out


# @decor_function_call
def extractTextTesseract(image_input):
    """
    Распознаем текст tesseract-ocr
    """
    from PIL import Image
    import pytesseract

    def countWords(text):
        "Чистим текст и остовляем слова больше 2х символов"

        import re
        clear = re.findall(u"[а-яА-Яa-zA-Z]+", text, re.UNICODE)
        clear_list = [s for s in clear if len(s) > 2]
        clear_list = sorted(clear_list)

        print(json.dumps(clear_list,  sort_keys=True, ensure_ascii=False))
        clear_len = len(clear_list)
        print (Fore.YELLOW + 'Количество слов: ' + str(clear_len))
        return clear_list

    def correctWords(text_list):
        "Отправляем наш сканированные список на проверку по словарю"

        import nlp
        # cor = nlp.correct_words(text_list)
        cor = nlp.spell(text_list)
        # cor = list(set(cor))
        print(json.dumps(cor,  sort_keys=True, ensure_ascii=False))
        cor_len = len(cor)
        print (Fore.YELLOW + 'Количество корректных слов: ' + str(cor_len))
        return cor

    def metrika(list1, list2):
        "Метрика для оценки распознования, чем больше 0 тем лучше"

        len1 = len(list1)
        len2 = len(list2)
        metrika = 0
        if len2>0:
            metrika = round((len2*1.0)/len1, 2)

        print (Fore.YELLOW + 'METRIKA: ' + str(metrika))
        return metrika

    def list_diff(list1, list2):
        "Определяем слова не из словаря"

        list_diff = list(set(list1)-set(list2))
        print('Diff ---------------')
        print(json.dumps(list_diff,  sort_keys=True, ensure_ascii=False))
        return list_diff

    out_text = pytesseract.image_to_string(Image.open(image_input), lang='rus')

    clear_list = countWords(out_text)
    correct_list = correctWords(clear_list)
    metrika(clear_list, correct_list)
    list_diff(clear_list, correct_list)

    return out_text


def rescaleImage(image_input, width=1000):
    """
    Увеличиваем размерчик
    convert example.png -resize 200 example.png
    """

    image_out = dir_out + '3.1.rescale.png'

    os.system("convert {} -resize {} -auto-level {}".format(image_input, width, image_out))

    return image_out




##########################################################################
if __name__ == '__main__':

    if len(sys.argv) > 1:
        # получили айди напрямую
        print sys.argv
        image_input = str(sys.argv[1])

    if image_input:
        print(image_input)

        # делаем папку с мд5 именем по файлу
        dir_out = 'out/'
        dir_out += hashlib.md5(image_input).hexdigest() + '/'
        print (dir_out)

        if os.path.exists(dir_out):
            shutil.rmtree(dir_out)
        os.makedirs(dir_out)

        os.system("convert {} {}".format(image_input, dir_out + '0.original.png'))

        # начинаем обработку
        # rescaleInput = rescaleImage(image_input, width=2000)

        image1step = rotateImage(image_input=image_input)
        text = extractTextTesseract(image1step)
        print (len(text))

        image2step = cropImage(image_input=image1step)
        rescaled = rescaleImage(image2step, width=1000)
        text = extractTextTesseract(rescaled)
        print (len(text))

        image3step = cleanImage(image_input=rescaled)
        text = extractTextTesseract(image3step)
        print (len(text))
