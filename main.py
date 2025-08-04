from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

app = FastAPI()

# Configura CORS para producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga diferida de servicios para mejor manejo de errores
def get_recomender_service():
    from recomender_service import RecomenderService
    return RecomenderService()

def get_ocasion_service():
    from ocasion_service import OcasionService
    return OcasionService()

@app.on_event("startup")
async def startup_event():
    """Inicializa los servicios al arrancar"""
    try:
        app.state.recomender = get_recomender_service()
        app.state.ocasion_service = get_ocasion_service()
    except Exception as e:
        raise RuntimeError(f"Error inicializando servicios: {str(e)}")

@app.get('/')
async def root():
    return {
        "message": "Sistema de Recomendación y Clasificación por Ocasión",
        "status": "operativo"
    }

@app.get('/recommend/{name}')
async def get_recommendations(name: str, n_items: int = 10):
    try:
        if not hasattr(app.state, 'recomender'):
            raise HTTPException(status_code=503, detail="Servicio no disponible")
            
        recommendations = app.state.recomender.recomendation(name, n_items)
        return {
            "product": name,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/classify/occasion')
async def classify_occasion(product_data: dict):
    try:
        if not hasattr(app.state, 'ocasion_service'):
            raise HTTPException(status_code=503, detail="Servicio no disponible")
            
        required = ['name', 'category']
        if not all(field in product_data for field in required):
            raise HTTPException(status_code=400, detail=f"Campos requeridos: {required}")
        
        prediction = app.state.ocasion_service.classify(product_data)
        return {"occasion": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))