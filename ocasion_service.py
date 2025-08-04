import joblib
from typing import Optional
from fastapi import HTTPException

class OcasionService:
    def __init__(self):
        self.model = joblib.load('./models/ocasion/modelo_ocasion.pkl')
        self.vectorizer = joblib.load('./models/ocasion/vectorizer_ocasion.pkl')

    def classify(self, product_data: dict) -> Optional[str]:
        try:
            text = f"{product_data['name']} {product_data.get('description', '')} {product_data['category']}".lower()
            X = self.vectorizer.transform([text])
            return self.model.predict(X)[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en clasificación: {str(e)}")