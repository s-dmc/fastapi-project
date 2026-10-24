from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_currency_etl_flow():
    # 1. Добавляем курс
    response = client.post("/etl/load-rate", json={"currency": "USD", "rate": 95.5})
    assert response.status_code == 200
    
    # 2. Проверяем список всех валют
    dwh_resp = client.get("/dwh/rates")
    assert dwh_resp.json()["USD"] == 95.5

    # 3. Проверяем получение конкретной валюты
    single_resp = client.get("/dwh/rates/usd")
    assert single_resp.status_code == 200
    assert single_resp.json()["rate"] == 95.5

    # 4. Тестируем удаление этой валюты
    delete_resp = client.delete("/dwh/rates/usd")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["status"] == "success"

    # 5. Проверяем, что после удаления валюты больше нет в базе
    check_resp = client.get("/dwh/rates/usd")
    assert check_resp.status_code == 404

def test_currency_data_quality_fail():
    response = client.post("/etl/load-rate", json={"currency": "EUR", "rate": -10.0})
    assert response.status_code == 400

def test_delete_not_found():
    response = client.delete("/dwh/rates/rub")
    assert response.status_code == 404
