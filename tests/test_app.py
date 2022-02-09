from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_get_heartbeat():
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.json() == {'status': 'OK'}

def test_get_address():
    locationid = '2643743'
    params={'locationid': locationid}
    response = client.get("/address", params=params)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['geonameId'] == int(locationid)

def test_generateid_dev(monkeypatch):
    monkeypatch.setenv('TOKEN', 'mytoken')
    monkeypatch.setenv('ROUTE_USER', 'user')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    params={'mode': 'dev'}
    response = client.get("/generateid", params=params)
    assert response.status_code == 200
    assert response.json() == {'id':'https://ror.org/012dev089'}

def test_generateid_bad_token(monkeypatch):
    monkeypatch.setenv('TOKEN', 'badtoken')
    monkeypatch.setenv('ROUTE_USER', 'user')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    response = client.get("/generateid")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_generateid_bad_user(monkeypatch):
    monkeypatch.setenv('TOKEN', 'mytoken')
    monkeypatch.setenv('ROUTE_USER', 'baduser')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    response = client.get("/generateid")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_indexdata(monkeypatch):
    monkeypatch.setenv('TOKEN', 'mytoken')
    monkeypatch.setenv('ROUTE_USER', 'user')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {"status":"indexing data OK"}

def test_indexdata_bad_token(monkeypatch):
    monkeypatch.setenv('TOKEN', 'badtoken')
    monkeypatch.setenv('ROUTE_USER', 'user')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_generate_id_bad_user(monkeypatch):
    monkeypatch.setenv('TOKEN', 'mytoken')
    monkeypatch.setenv('ROUTE_USER', 'baduser')
    monkeypatch.setenv('ROR_API_URL', 'http://ror-api')
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://localhost:8080')
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_get_nonexistent_path():
    response = client.get("/foo")
    assert response.status_code == 404



