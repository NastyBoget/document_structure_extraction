import re


class string2features:
    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass

    def fit_transform(self, X, y):
        return self.transform(X)

    def transform(self, X):
        """
        X - список строк
        """
        first_words = []
        for elem in X:
            line = elem['text']
            if line.split():
                first_words.append(line.split()[0])
            else:
                first_words.append('')
        return first_words


RE_LIST = re.compile(r'\d+(\.\d+)*\D')  # для отдельного типа списка
RE_HEADER = re.compile(r'Раздел|Подраздел|Глава|Параграф|Секция|Часть|Статья')


class AddFeatures:
    def __init__(self):
        pass

    def fit(self):
        pass

    def transform(self, X):
        """
        returns 2 columns: 1-list, 2-header
        X - list of strings
        """
        features = []
        for elem in X:
            line = elem['text']
            match = RE_LIST.search(line)
            if match:
                if match.start() == 0:
                    features.append(elem['bbox'] + [1, 0])
                    continue
            match = RE_HEADER.search(line)
            if match:
                if match.start() == 0:
                    features.append(elem['bbox'] + [0, 1])
                    continue
            features.append(elem['bbox'] + [0, 0])
        return features

    def fit_transform(self, X, y=None):
        return self.transform(X)
