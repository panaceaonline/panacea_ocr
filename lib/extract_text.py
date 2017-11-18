import sys
import os.path

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

input_file = sys.argv[1]
print pytesseract.image_to_string(Image.open(input_file), lang='rus')
