from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes.auth_route import router as auth_router
from app.routes.family_route import router as family_router
from app.routes.income_source_route import router as income_source_router
from app.routes.income_route import router as income_router
from fastapi import APIRouter
from app.core.exceptions import AppException
from app.routes.profile_route import router as profile_router
from app.routes.expense_source_route import router as expense_source_router
from app.routes.expense_route import router as expense_router

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
api_router.include_router(family_router)
api_router.include_router(income_source_router)
api_router.include_router(income_router)
api_router.include_router(expense_source_router)
api_router.include_router(expense_router)
app.include_router(api_router)

app.include_router(profile_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Semaforo Financiero backend activo"}


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    payload = {"error": {"code": exc.code, "message": exc.message}}
    if exc.details:
        payload["error"]["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        payload = {"error": detail}
    else:
        payload = {"error": {"message": detail}}
    return JSONResponse(status_code=exc.status_code, content=payload)
