from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get('/')
    assert r.status_code == 200
    assert r.json().get('status') == 'ok'

def test_recommend_defaults():
    payload = {'user_id':1, 'pref':{}}
    r = client.post('/recommend', json=payload)
    assert r.status_code == 200
    assert 'recommendations' in r.json()
