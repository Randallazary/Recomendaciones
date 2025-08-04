from fastapi import FastAPI, HTTPException
from recomender_service import RecomenderService  # Importación directa del archivo
from ocasion_service import OcasionService       # Importación directa del archivo

app = FastAPI()

# Inicializar servicios
recomender = RecomenderService()
ocasion_service = OcasionService()

@app.get('/')
async def root():
    return {"message": "Sistema de Recomendación y Clasificación"}

@app.get('/recommend/{name}')
async def recommend(name: str, n_items: int = 10):
    try:
        recommendations = recomender.recomendation(name, n_items)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/classify/occasion')
async def classify_occasion(product_data: dict):
    try:
        prediction = ocasion_service.classify(product_data)
        return {"occasion": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))