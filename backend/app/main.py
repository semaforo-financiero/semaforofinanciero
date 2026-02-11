from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_route import router as auth_router
from fastapi import APIRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Semaforo Financiero backend activo 🚦"}
