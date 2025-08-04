from fastapi import FastAPI
from services.recomender_service import RecomenderService
from services.ocasion_service import OcasionService

app = FastAPI()

# Inicializar servicios
recomender = RecomenderService()
ocasion_service = OcasionService()

@app.get('/')
async def root():
    return {"message": "Sistema de Recomendación y Clasificación"}

# Rutas existentes para recomendación
@app.get('/recommend/{name}')
async def recommend(name: str, n_items: int = 10):
    recommendations = recomender.recomendation(name, n_items)
    return {"recommendations": recommendations}

# Nueva ruta para clasificación de ocasión
@app.post('/classify/occasion')
async def classify_occasion(product_data: dict):
    try:
        prediction = ocasion_service.classify(product_data)
        return {"occasion": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))