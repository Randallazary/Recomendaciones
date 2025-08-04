import joblib
from typing import Dict, Any
import pandas as pd

class OcasionService:
    # Rutas a los modelos (ajusta según tu estructura)
    MODEL_PATH: str = './models_ocasion.pkl'
    VECTORIZER_PATH: str = './vectorizer_ocasion.pkl'
    
    def __init__(self):
        """Carga los modelos necesarios al inicializar el servicio"""
        try:
            self.model = joblib.load(self.MODEL_PATH)
            self.vectorizer = joblib.load(self.VECTORIZER_PATH)
        except FileNotFoundError as e:
            raise RuntimeError(f"No se encontraron los archivos del modelo: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error al cargar los modelos: {str(e)}")
    
    def classify(self, product_data: Dict[str, Any]) -> str:
        """
        Clasifica un producto según su ocasión especial
        
        Args:
            product_data: Diccionario con:
                - name: Nombre del producto
                - category: Categoría del producto
                - description (opcional): Descripción del producto
        
        Returns:
            str: Ocasión predicha (ej. "Cumpleaños", "Amor", etc.)
        
        Raises:
            ValueError: Si faltan campos requeridos
        """
        # Validación de campos mínimos
        if not all(key in product_data for key in ['name', 'category']):
            raise ValueError("Los campos 'name' y 'category' son requeridos")
        
        # Preprocesamiento del texto
        description = product_data.get('description', '')
        text = f"{product_data['name']} {description} {product_data['category']}".lower().strip()
        
        try:
            # Vectorización y predicción
            X = self.vectorizer.transform([text])
            return self.model.predict(X)[0]
        except Exception as e:
            raise RuntimeError(f"Error durante la clasificación: {str(e)}")