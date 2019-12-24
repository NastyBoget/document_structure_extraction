from pdf2text import pdf2text

print("Введите имя файла:")
path = input()
X = pdf2text(path)

from string2features import string2features
import pickle as pkl
clf = pkl.load(open("model.pkl", "rb"))
y = clf.predict(X)

res = []
for line, type_ in zip(X, y):
    res.append({"type": int(type_), "content": line})
print(*res, sep='\n')

import json
with open("result.json", "w") as write_file:
    json.dump(res, write_file, ensure_ascii=False)



