sudo apt-get install python-imaging
sudo apt-get install python-opencv

sudo add-apt-repository ppa:alex-p/tesseract-ocr
sudo apt-get update
sudo apt install tesseract-ocr

wget https://github.com/tesseract-ocr/tessdata/blob/master/rus.traineddata
cp rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata
