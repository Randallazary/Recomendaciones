import joblib
from pathlib import Path

class OcasionService:
    def __init__(self):
        # Usamos rutas absolutas basadas en la ubicación del archivo
        base_dir = Path(__file__).parent
        self.model = joblib.load(base_dir / 'models_ocasion.pkl')
        self.vectorizer = joblib.load(base_dir / 'vectorizer_ocasion.pkl')
    
    def classify(self, product_data: dict) -> str:
        text = f"{product_data['name']} {product_data.get('description', '')} {product_data['category']}".lower()
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]