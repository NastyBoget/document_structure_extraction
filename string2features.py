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
        for line in X:
            if line.split():
                first_words.append(line.split()[0])
            else:
                first_words.append('')
        return first_words
