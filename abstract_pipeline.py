class AbstractModel:

    def train(self, X, y):
        return

    def predict(self, X):
        return []


class AbstractPreprocessor:

    def transform(data):
        return data


class Pipeline:

    def __init__(self, model: AbstractModel, preprocessor: AbstractModel = None) -> None:
        self.model = model
        self.preprocessor = preprocessor

    def train(self, data, target_column):
        y = data[target_column]
        X = data.drop(columns=[target_column])

        if self.preprocessor:
            X = self.preprocessor.transform(X)

        self.model.fit(X, y)
        return

    def predict(self, data):
        if self.preprocessor:
            data = self.preprocessor.transform(data)

        predicts = self.model.predict(data)
        return predicts
