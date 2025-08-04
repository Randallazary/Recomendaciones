from fastapi import FastAPI, HTTPException
from recomender_service import RecomenderService
from ocasion_service import OcasionService  # Importamos el nuevo servicio

app = FastAPI()

# Inicializamos ambos servicios al inicio (mejor performance)
recomender = RecomenderService()
ocasion_service = OcasionService()

@app.get('/')
async def root():
    return {
        "message": "Sistema de Recomendación y Clasificación por Ocasión"
    }

# Endpoint existente para recomendaciones (sin cambios)
@app.get('/recommend/{name}')
async def predict(name: str, n_items: int = 10):
    try:
        recomendations = recomender.recomendation(name, n_items)
        return {
            "recomendations": recomendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nuevo endpoint para clasificación por ocasión
@app.post('/classify/occasion')
async def classify_occasion(product_data: dict):
    try:
        # Validación básica de datos de entrada
        required_fields = ['name', 'category']
        if not all(field in product_data for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Faltan campos requeridos: {required_fields}"
            )
        
        # Procesamos con el modelo de ocasión
        prediction = ocasion_service.classify(product_data)
        
        return {
            "occasion": prediction,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))