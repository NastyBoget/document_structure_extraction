import pytesseract
import numpy as np
import cv2
import pdf2image as p2i


def is_box_in(box1, box2):
    """
    check if box1 is in box2
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return (x1 >= x2) and (y1 >= y2) and (x1 + w1 <= x2 + w2) and (y1 + h1 <= y2 + h2)


def preprocess(img):
    preprocess = "thresh"
    # загрузить образ и преобразовать его в оттенки серого
    #  image = cv2.imread('image.png') # image - numpy-array of pixels
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # проверим, следует ли применять пороговое значение для предварительной обработки изображения
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # если нужно медианное размытие, чтобы удалить шум
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)
    return gray


def pdf2text(path):
    """
    path - путь к файлу pdf/jpeg
    файл преобразуется в изображение, изображение преобразуется в текст
    возвращает список строк документа
    """
    if path.endswith('.pdf'):
        images = p2i.convert_from_path(path, fmt='png')
        image = []
        for img in images:
            image.append(np.array(img))
    elif path.endswith('.jpeg'):
        image = [cv2.imread(path)]
    else:
        print(path)
        return
    res = []
    for img in image:
        img = preprocess(img)
        text = pytesseract.image_to_string(img, lang='rus')
        res += text.split(sep='\n')
    return res


def pdf2data(path):
    """
    :param path: name of picture's file
    :return: list of lines' bounding boxes
    bounding box: {'text', 'bbox'}
    """
    img = cv2.imread(path)
    img = preprocess(img)
    h0 = img.shape[0]
    w0 = img.shape[1]
    d = pytesseract.image_to_data(img, lang='rus+eng', output_type=pytesseract.Output.DICT)
    boxes = []
    for i in range(len(d['level'])):
        if d['level'][i] == 4:  # bounding box of text line
            box = {'text': '', 'bbox': [d['left'][i],
                                        d['top'][i], d['width'][i], d['height'][i]]}
            boxes.append(box)
    for i in range(len(d['level'])):
        if d['level'][i] == 5:  # bounding box of some word
            box = d['left'][i], d['top'][i], d['width'][i], d['height'][i]
            for j in range(len(boxes)):
                if is_box_in(box, boxes[j]['bbox']):
                    if boxes[j]['text'] != '':
                        boxes[j]['text'] += ' '
                    boxes[j]['text'] += d['text'][i]
    for box in boxes:
        box['bbox'][0] /= w0
        box['bbox'][1] /= h0
        box['bbox'][2] /= w0
        box['bbox'][3] /= h0
    return boxes
