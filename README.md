# Валютный ETL и Data Quality Сервис

Микросервис на FastAPI, который симулирует ETL-процесс: принимает курсы валют от внешних источников, проверяет их на аномалии (Data Quality) и сохраняет в витрину данных.

## Стек технологий
* Python 3.11+
* FastAPI & Uvicorn
* Pydantic
* Pytest & HTTPX

## Как запустить проект локально

1. Активируйте виртуальное окружение:
   ```bash
   source venv/bin/activate
   ```

2. Установите зависимости:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Запустите сервер:
   ```bash
   uvicorn main:app --reload
   ```
   После этого сервис будет доступен по адресу: http://127.0.0.1:8000

## Как запустить автоматические тесты
```bash
python -m pytest
```
