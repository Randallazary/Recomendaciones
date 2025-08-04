from fastapi import FastAPI, HTTPException
from recomender_service import RecomenderService
from ocasion_service import OcasionService

app = FastAPI()

# Inicialización de servicios al iniciar la aplicación
recomender = RecomenderService()
ocasion_service = OcasionService()

@app.get('/')
async def root():
    return {
        "message": "Sistema de Recomendación y Clasificación por Ocasión",
        "endpoints": {
            "recomendaciones": "GET /recommend/{product_name}?n_items=10",
            "clasificacion": "POST /classify/occasion"
        }
    }

@app.get('/recommend/{name}')
async def get_recommendations(name: str, n_items: int = 10):
    """
    Obtiene recomendaciones de productos similares
    - name: Nombre o ID del producto de referencia
    - n_items: Número de recomendaciones (default: 10, máximo: 20)
    """
    try:
        # Validación básica
        if n_items <= 0 or n_items > 20:
            raise HTTPException(
                status_code=400,
                detail="El parámetro n_items debe estar entre 1 y 20"
            )
        
        recomendations = recomender.recomendation(name, n_items)
        
        return {
            "product": name,
            "recomendations": recomendations,
            "count": len(recomendations)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener recomendaciones: {str(e)}"
        )

@app.post('/classify/occasion')
async def classify_product_occasion(product_data: dict):
    """
    Clasifica un producto según su ocasión especial
    Requiere (JSON):
    {
        "name": "string",        # Nombre del producto
        "category": "string",    # Categoría
        "description": "string"  # Opcional
    }
    """
    try:
        # Validación de campos requeridos
        required_fields = ['name', 'category']
        if not all(field in product_data for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Faltan campos requeridos: {required_fields}"
            )
        
        # Procesamiento con el modelo
        prediction = ocasion_service.classify(product_data)
        
        return {
            "product": product_data['name'],
            "category": product_data['category'],
            "predicted_occasion": prediction,
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al clasificar: {str(e)}"
        )