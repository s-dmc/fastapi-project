import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "development"
    class Config:
        env_file = ".env"

settings = Settings()

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Currency ETL")

currency_dwh = {}

class CurrencyData(BaseModel):
    currency: str
    rate: float

# --- ТЕХНИЧЕСКИЕ МАРШРУТЫ ---
@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/version")
def get_version():
    logger.info("Запрос версии приложения")
    return {"version": "1.0.0", "environment": settings.env}


# --- ПОЛЕЗНЫЕ МАРШРУТЫ ПО ТЕМЕ (4 ШТУКИ) ---

# 1. Загрузка курса (POST)
@app.post("/etl/load-rate")
def ingest_currency(data: CurrencyData):
    logger.info(f"Получены данные для {data.currency}")
    if data.rate <= 0:
        logger.warning(f"DQ Alert: Некорректный курс {data.rate}")
        raise HTTPException(status_code=400, detail="Data Quality Error: Rate must be greater than 0")
        
    currency_dwh[data.currency.upper()] = data.rate
    return {"status": "success", "saved": data.currency.upper()}

# 2. Получение ВСЕХ курсов (GET)
@app.get("/dwh/rates")
def get_rates():
    logger.info("Запрос всей витрины данных")
    return currency_dwh

# 3. Получение курса КОНКРЕТНОЙ валюты (GET с параметром)
@app.get("/dwh/rates/{currency_code}")
def get_single_rate(currency_code: str):
    logger.info(f"Запрос курса для валюты: {currency_code}")
    code_upper = currency_code.upper()
    if code_upper not in currency_dwh:
        logger.warning(f"Валюта {code_upper} не найдена в системе")
        raise HTTPException(status_code=404, detail="Currency not found")
    return {"currency": code_upper, "rate": currency_dwh[code_upper]}

# 4. НОВЫЙ: Удаление валюты из витрины (DELETE с параметром)
@app.delete("/dwh/rates/{currency_code}")
def delete_rate(currency_code: str):
    logger.info(f"Запрос на удаление валюты: {currency_code}")
    code_upper = currency_code.upper()
    if code_upper not in currency_dwh:
        logger.warning(f"Попытка удалить несуществующую валюту: {code_upper}")
        raise HTTPException(status_code=404, detail="Currency not found to delete")
    
    del currency_dwh[code_upper]
    logger.info(f"Валюта {code_upper} успешно удалена из DWH")
    return {"status": "success", "message": f"Currency {code_upper} deleted"}
