import cv2
import pytesseract


def is_box_in(box1, box2):
    """
    check if box1 is in box2
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    return (x1 >= x2) and (y1 >= y2) and (x1 + w1 <= x2 + w2) and (y1 + h1 <= y2 + h2)


def picture2boxes(path):
    """
    :param path: name of picture's file
    :return: list of lines' bounding boxes
    bounding box: {'text', 'bbox'}
    """
    img = cv2.imread(path)
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
