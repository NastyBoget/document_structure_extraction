from PIL import Image
import pytesseract
import numpy as np
import cv2
import os
import pdf2image as p2i

def pdf2text(path):
    """
    path - путь к файлу pdf
    файл преобразуется в изображение, изображение преобразуется в текст
    возвращает список строк документа
    """
    images = p2i.convert_from_path(path, fmt='png')
    image = []
    for img in images:
        image.append(np.array(img))
    res = []
    for img in image:
        preprocess = "thresh"
        # загрузить образ и преобразовать его в оттенки серого
        #image = cv2.imread('image.png') # image - numpy-array of pixels
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # проверим, следует ли применять пороговое значение для предварительной обработки изображения
        if preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # если нужно медианное размытие, чтобы удалить шум
        elif preprocess == "blur":
            gray = cv2.medianBlur(gray, 3)
        # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        # загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
        text = pytesseract.image_to_string(Image.open(filename), lang='rus') #to_data
        os.remove(filename)
        res += text.split(sep='\n')
    return res
