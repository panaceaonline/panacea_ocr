#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import json
import shutil
import hashlib
sys.path.append("./lib")

home = '/home/rustam/projects/panacea_ocr/'
sys.path.append(home)


from colorama import *
init(autoreset=True)

from lib.decorator import *

dir_out = 'out/'


@decor_function_call
def rotateImage(image_input, dir_out):
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
def cropImage(image_input, dir_out):
    """
    Кропаем картинку, ищем текстовый блок

    """

    # from process_image import crop_morphology

    image_out = dir_out + '2.crop.png'

    # ТОДО переписать на функцию
    os.system(home + "lib/crop_morphology.py {} {}".format(image_input, image_out))

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
def cleanImage(image_input, dir_out):
    """
    Используем шел скрипт textcleaner
    http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
    """

    image_out = dir_out + '3.2.clean.png'
    # options = ' -g -e stretch -f 25 -o 20 -t 30 -u -s 1 -T -p 20 '
    options = ' -T -p 20 '

    os.system("sh {}lib/textcleaner {} {} {}".format(home, options, image_input, image_out))

    return image_out


# @decor_function_call
def extractTextTesseract(image_input):
    """
    Распознаем текст tesseract-ocr
    """
    from PIL import Image
    import pytesseract

    def countWords(text):
        "Чистим текст и оставляем слова больше 2х символов"

        import re
        clear = re.findall(u"[а-яА-Яa-zA-Z]+", text, re.UNICODE)
        clear_list = [s for s in clear if len(s) > 2]
        clear_list = sorted(clear_list)

        print(json.dumps(clear_list,  sort_keys=True, ensure_ascii=False))
        clear_len = len(clear_list)
        print (Fore.YELLOW + 'Количество слов: ' + str(clear_len))
        return clear_list

    def correctWords(text_list):
        "Отправляем наш сканированные списки на проверку по словарю"

        import lib.nlp
        # cor = nlp.correct_words(text_list)
        cor = lib.nlp.spell(text_list)
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
        "Выделяем слова не из словаря"

        list_diff = list(set(list1)-set(list2))
        print('Diff ---------------')
        print(json.dumps(list_diff,  sort_keys=True, ensure_ascii=False))
        return list_diff

    out_text = pytesseract.image_to_string(Image.open(image_input), lang='rus')

    clear_list = countWords(out_text)
    correct_list = correctWords(clear_list)
    list_diff(clear_list, correct_list)

    d = {
        'metrika': metrika(clear_list, correct_list),
        'text': out_text,
        'text_clear': clear_list,
        'text_clear_len': len(clear_list),
        'text_spell': correct_list,
        'text_spell_len': len(correct_list),
        # 'text_no_spell': list_diff,
        # 'angle': 0,
    }
    # print(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False))

    return d


def rescaleImage(image_input, dir_out, width=1000):
    """
    Увеличиваем размерчик
    convert example.png -resize 200 example.png
    """

    image_out = dir_out + '3.1.rescale.png'

    os.system("convert {} -resize {} -auto-level {}".format(image_input, width, image_out))

    return image_out


def angleImage(image_input, dir_out, angle=90):
    """
    Поворот картинки по 90 градусов
    """

    image_out = dir_out + 'rotate{}.png'.format(angle)

    os.system("convert {} -rotate {} {}".format(image_input, angle, image_out))

    return image_out


def start(image_input, dir_out = 'out/'):
    """
    Основные шаги, главная функция
    """

    # делаем папку с мд5 именем по файлу
    # dir_out += hashlib.md5(image_input).hexdigest() + '/'


    hasher = hashlib.md5()
    with open(str(image_input), 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)

    md5 = hasher.hexdigest()

    dir_out += md5  + '/'

    print (dir_out)

    if os.path.exists(dir_out):
        shutil.rmtree(dir_out)
    os.makedirs(dir_out)

    os.system("convert {} {}".format(image_input, dir_out + '0.original.png'))

    # начинаем обработку
    # rescaleInput = rescaleImage(image_input, width=2000)

    image1step = rotateImage(image_input=image_input, dir_out=dir_out)
    text_dict = extractTextTesseract(image1step)
    # проверяем правильно ли мы повернули
    maxmet = 0
    angle = 0
    finalrotated = ''
    if int(text_dict['metrika'])<0.5:
        print('Маленькая метрика: ' + str(text_dict['metrika']))
        for i in range(3):
            angle += 90
            print i, angle
            imagestep = angleImage(image_input=image1step, dir_out=dir_out, angle=angle)
            text_dict = extractTextTesseract(imagestep)
            if text_dict['metrika']>maxmet:
                maxmet = text_dict['metrika']
                finalrotated = imagestep
                print ('!!!!Selected', str(maxmet))
                print('--------------------')

        if finalrotated:
            image1step = finalrotated

    image2step = cropImage(image_input=image1step, dir_out=dir_out)
    rescaled = rescaleImage(image2step, dir_out, width=1000)
    text = extractTextTesseract(rescaled)

    image3step = cleanImage(image_input=rescaled, dir_out=dir_out)
    text = extractTextTesseract(image3step)
    print (len(text))

    domain = 'http://fb694534.ngrok.io'

    text.update({
        'image_original': '{}/{}0.original.png'.format(domain, dir_out),
        'image_final': '{}/{}3.2.clean.png'.format(domain, dir_out),
        'md5': md5,
        'blood':
            {
                'erythrocyte': 4.7,
                'hemoglobin': 118.1,
                'leukocyte': 5.3,
                'thrombocyte': 153,
            }
    })

    return text



##########################################################################
if __name__ == '__main__':

    if len(sys.argv) > 1:
        # получили айди напрямую
        print sys.argv
        image_input = str(sys.argv[1])

    if image_input:
        print(image_input)

        start(image_input)
