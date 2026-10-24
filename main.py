import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings  # <-- Добавили импорт настроек

# --- НАСТРОЙКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ---
class Settings(BaseSettings):
    # По умолчанию будет "development", но если в системе есть переменная ENV, 
    # Python автоматически прочитает её значение
    env: str = "development"

    class Config:
        env_file = ".env"  # Разрешаем читать настройки из вашего файла .env

settings = Settings()

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Currency ETL")

currency_dwh = {}

class CurrencyData(BaseModel):
    currency: str
    rate: float

@app.get("/health")
def health():
    return {"status": "OK"}

# --- МАРШРУТ С ИСПОЛЬЗОВАНИЕМ НАСТРОЙКИ ---
@app.get("/version")
def get_version():
    logger.info("Запрос версии приложения")
    # ТЗ выполнено: значение "environment" теперь динамически читается из настроек!
    return {"version": "1.0.0", "environment": settings.env}

@app.post("/etl/load-rate")
def ingest_currency(data: CurrencyData):
    logger.info(f"Получены данные для {data.currency}")
    if data.rate <= 0:
        logger.warning(f"DQ Alert: Некорректный курс {data.rate}")
        raise HTTPException(status_code=400, detail="Data Quality Error: Rate must be greater than 0")
        
    currency_dwh[data.currency.upper()] = data.rate
    return {"status": "success", "saved": data.currency.upper()}

@app.get("/dwh/rates")
def get_rates():
    return currency_dwh
