import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Сборщик курсов валют (валютный ETL)")

# Наше мини-хранилище данных (DWH)
currency_dwh = {}

class CurrencyData(BaseModel):
    currency: str  # Например, "USD"
    rate: float    # Курс, например, 95.5

@app.get("/health")
def health():
    return {"status": "OK"}

# Наш эндпоинт загрузки и проверки данных (ETL + Data Quality)
@app.post("/etl/load-rate")
def ingest_currency(data: CurrencyData):
    logger.info(f"Получены данные для {data.currency}")
    
    # Data Quality: Проверка на бред (курс валюты не может быть нулевым или отрицательным)
    if data.rate <= 0:
        logger.warning(f"DQ Alert: Некорректный курс {data.rate}")
        raise HTTPException(status_code=400, detail="Data Quality Error: Rate must be greater than 0")
        
    # Сохраняем в DWH
    currency_dwh[data.currency.upper()] = data.rate
    return {"status": "success", "saved": data.currency.upper()}

# Витрина данных для аналитиков
@app.get("/dwh/rates")
def get_rates():
    return currency_dwh
