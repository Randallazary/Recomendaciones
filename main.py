from fastapi import FastAPI
from recomender_service import RecomenderService

app = FastAPI()

@app.get('/')
async def root():
  return {
    "message": "Sistema de Recomendación de Productos"
  }

@app.get('/recommend/{partNumber}')
async def predict(partNumber: str, n_items: int = 10):
  recomender = RecomenderService()
  recomendations: list[str] = recomender.recomendation(partNumber, n_items)
  
  return {
    "recomendations": recomendations
}
