# Распознование табличных данных на фотографиях с анализами

## Исправление картинки

### 1 Повернуть изображение

* На нейросетках https://github.com/d4nst/RotNet
* https://github.com/kakul/Alyn

### 2 Кроп и исправление перспективы

https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

### 3 Биноризация

`python lib/process_image.py out/2.crop.png out/3.binar.png`

# Работа с текстом

* выделение блока с текстом http://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html

### Выделение таблиц

* https://github.com/HazyResearch/TreeStructure/blob/master/table-extraction/tutorials/table-extraction-demo.ipynb

### Выделение строк

### Распознование текста

* Питон тессеракт https://github.com/madmaze/pytesseract

### Распознование рукописных цифр


# INSTALL

python 2.7

### venv

```
virtualenv venv -p python2
source venv/bin/activate

```

### Tesseract
Tesseract - распознование текста

Надо поставить 4 версию

```
sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
sudo apt install tesseract-ocr
```

### Rus
Установить русский язык, можно скачав отсюда

`wget https://github.com/tesseract-ocr/tessdata/blob/master/rus.traineddata`

и скопировать сюда `/usr/share/tesseract-ocr/tessdata`

или `/usr/share/tesseract-ocr/4.00/tessdata`

### custom dictonary

https://github.com/tesseract-ocr/tesseract/wiki/FAQ#how-do-i-provide-my-own-dictionary
https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc#config-files-and-augmenting-with-user-data

rus.user-words
