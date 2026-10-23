from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_currency_etl_success():
    # Отправляем хороший курс
    response = client.post("/etl/load-rate", json={"currency": "USD", "rate": 95.5})
    assert response.status_code == 200
    
    # Проверяем, что он сохранился в витрине
    dwh_resp = client.get("/dwh/rates")
    assert dwh_resp.json()["USD"] == 95.5

def test_currency_data_quality_fail():
    # Отправляем плохой курс (отрицательный)
    response = client.post("/etl/load-rate", json={"currency": "EUR", "rate": -10.0})
    assert response.status_code == 400
