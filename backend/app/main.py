from fastapi import FastAPI
from app.db.database import get_supabase_client

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Semaforo Financiero backend activo"}


@app.get("/test-db")
def test_db():
    supabase = get_supabase_client()
    try:
        response = supabase.table("profiles").select("*").limit(1).execute()
        return {"status": "Supabase connected", "data": response}
    except Exception as e:
        return {"status": "Error", "message": str(e)}