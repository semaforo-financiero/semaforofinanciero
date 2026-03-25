from app.db.database import get_supabase_client
from app.services.model_training_service import ModelTrainingService

def main():
    supabase = get_supabase_client()
    service = ModelTrainingService(supabase)
    result = service.train_and_save_model()
    print(result)

if __name__ == "__main__":
    main()