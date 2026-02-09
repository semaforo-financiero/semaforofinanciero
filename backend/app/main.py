from fastapi import FastAPI
from app.routes.auth_route import router as auth_router
from fastapi import APIRouter

app = FastAPI()

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Semaforo Financiero backend activo 🚦"}
