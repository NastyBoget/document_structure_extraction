from pdf2text import pdf2text
import pickle as pkl
from string2features import string2features, AddFeatures
import json
    
def doc2json(path):
    X = pdf2text(path)
    clf = pkl.load(open("model.pkl", "rb"))
    y = clf.predict(X)
    res = []
    for line, type_ in zip(X, y):
        res.append({"type": int(type_), "content": line})
    return json.dumps(res, ensure_ascii=False).encode('utf8')

print("введите путь к файлу")
path = input()
print(doc2json(path).decode())
