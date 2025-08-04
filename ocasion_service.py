import joblib

class OcasionService:
    def __init__(self):
        # Cargamos los modelos (asegúrate de que los archivos existan)
        self.model = joblib.load('models_ocasion.pkl')
        self.vectorizer = joblib.load('vectorizer_ocasion.pkl')
    
    def classify(self, product_data: dict) -> str:
        """Clasifica un producto según su ocasión"""
        # Preparamos el texto combinando name, description (opcional) y category
        description = product_data.get('description', '')
        text = f"{product_data['name']} {description} {product_data['category']}".lower().strip()
        
        # Vectorizamos y predecimos
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]