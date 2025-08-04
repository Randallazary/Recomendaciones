from fastapi import FastAPI
from recomender_service import RecomenderService

app = FastAPI()

@app.get('/')
async def root():
  return {
    "message": "Sistema de Recomendación de Productos"
  }

@app.get('/recommend/{name}')
async def predict(name: str, n_items: int = 10):
  recomender = RecomenderService()
  recomendations: list[str] = recomender.recomendation(name, n_items)
  
  return {
    "recomendations": recomendations
}
