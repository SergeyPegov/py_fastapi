from fastapi.testclient import TestClient
import pandas as pd
import os
import sys
import httpx
from main import app

client = TestClient(app)
sys.path.append(os.getcwd())
def test_dublic():
    response = client.post(
        "/case_sensitive",
        headers={"X-Token": "coneofsilence"},
        content='["Мама", "МАМА", "Мама", "папа", "ПАПА", "ДЯдя", "брАт", "Дядя", "Дядя"]'
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == [ "папа", "брат" ]

def test_dublic_empty():
    response = client.post(
        "/case_sensitive",
        headers={"X-Token": "coneofsilence"},
        content='["Мама", "МАМА", "Мама", "папа", "ПАПА", "ДЯдя", "брАт", "Дядя", "Дядя", "папа", "брАт"]'
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == []

def test_dublic_fail():
    response = client.post(
        "/case_sensitive",
        headers={"X-Token": "coneofsilence"}
    )
    print(response)
    assert response.status_code == 422
