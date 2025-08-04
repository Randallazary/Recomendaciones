import joblib

class OcasionService:
    def __init__(self):
        # Asegúrate de que las rutas sean correctas
        self.model = joblib.load('models_ocasion.pkl')
        self.vectorizer = joblib.load('vectorizer_ocasion.pkl')

    def classify(self, product_data: dict) -> str:
        text = f"{product_data['name']} {product_data.get('description', '')} {product_data['category']}".lower()
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]