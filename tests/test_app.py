from fastapi.testclient import TestClient
from app import app
import os
import pytest
import re

ROR_ID_REGEX = r'((https(:\/\/|%3A%2F%2F))ror\.org(\/|%2F))?0\w{6}\d{2}'
DEFAULT_ENV_VARS = {'TOKEN': 'mytoken', 'ROUTE_USER': 'user', 'ROR_API_URL': 'http://ror-api', 'ALLOWED_ORIGINS': 'http://localhost:8080'}

client = TestClient(app)

@pytest.fixture
def mock_default_env (monkeypatch):
    for k, v in DEFAULT_ENV_VARS.items():
        monkeypatch.setenv(k, v)

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

def test_generateid_dev(mock_default_env):
    assert os.environ.get('TOKEN') == 'mytoken'
    assert os.environ.get('ROUTE_USER') == 'user'
    params={'mode': 'dev'}
    response = client.get("/generateid", params=params)
    assert response.status_code == 200
    assert response.json() == {'id':'https://ror.org/012dev089'}

def test_generateid(mock_default_env):
    assert os.environ.get('TOKEN') == 'mytoken'
    assert os.environ.get('ROUTE_USER') == 'user'
    response = client.get("/generateid")
    response_json = response.json()
    print(response_json['id'])
    assert response.status_code == 200
    assert re.match(ROR_ID_REGEX, response_json['id'])

def test_generateid_bad_token(mock_default_env, monkeypatch):
    monkeypatch.setenv('TOKEN', 'badtoken')
    assert os.environ.get('TOKEN') == 'badtoken'
    assert os.environ.get('ROUTE_USER') == 'user'
    response = client.get("/generateid")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_generateid_bad_user(mock_default_env, monkeypatch):
    monkeypatch.setenv('ROUTE_USER', 'baduser')
    assert os.environ.get('TOKEN') == 'mytoken'
    assert os.environ.get('ROUTE_USER') == 'baduser'
    response = client.get("/generateid")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_indexdata(mock_default_env):
    assert os.environ.get('TOKEN') == 'mytoken'
    assert os.environ.get('ROUTE_USER') == 'user'
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {"status":"indexing data OK"}

def test_indexdata_bad_token(mock_default_env, monkeypatch):
    monkeypatch.setenv('TOKEN', 'badtoken')
    assert os.environ.get('TOKEN') == 'badtoken'
    assert os.environ.get('ROUTE_USER') == 'user'
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_generate_id_bad_user(mock_default_env, monkeypatch):
    monkeypatch.setenv('ROUTE_USER', 'baduser')
    assert os.environ.get('TOKEN') == 'mytoken'
    assert os.environ.get('ROUTE_USER') == 'baduser'
    response = client.get("/indexdata")
    assert response.status_code == 200
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_get_nonexistent_path():
    response = client.get("/foo")
    assert response.status_code == 404



