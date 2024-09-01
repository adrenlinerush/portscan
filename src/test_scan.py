import pytest
from flask import Flask, jsonify
from utils import get_scan_id, run_scan, store_scan_results, retrieve_scan_results

@pytest.fixture
def client():
    from scan import scan
    app = Flask(__name__)
    app.register_blueprint(scan)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_utils(mocker):
    mocker.patch('utils.get_scan_id', return_value="mock_scan_id")
    mocker.patch('utils.run_scan', return_value=["22", "80"])
    mocker.patch('utils.store_scan_results')
    mocker.patch('utils.retrieve_scan_results', return_value=[
        {"timestamp": "2024-08-30 12:34:56", "id": "mock_scan_id", "ip": "127.0.0.1", "open_ports": "22,80"}
    ])

def test_run_scan_success(client, mock_utils):
    response = client.post('/scan', json={"ip_list": ["127.0.0.1"]})
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['ip'] == "127.0.0.1"
    assert data[0]['open_ports'] == "22,80"
def test_run_scan_invalid_payload(client):
    response = client.post('/scan', data="invalid_payload")
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'Payload was invalid.'}

def test_run_scan_invalid_ip(client):
    response = client.post('/scan', json={"ip_list": ["999.999.999.999"]})
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': '999.999.999.999 is not a valid IP address.'}

def test_get_scan_by_id_success(client, mock_utils):
    response = client.get('/scan/scan_id', query_string={"scan_id": "mock_scan_id"})
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['ip'] == "127.0.0.1"
    assert data[0]['open_ports'] == "22,80"

def test_get_scan_by_id_invalid_payload(client):
    response = client.get('/scan/scan_id')
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'Payload was invalid.'}

def test_get_scan_by_id_not_found(client, mocker):
    mocker.patch('utils.retrieve_scan_results', return_value=[])
    response = client.get('/scan/scan_id', query_string={"scan_id": "non_existent_id"})
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'non_existent_id was not found.'}

def test_get_scan_by_ip_success(client, mock_utils):
    response = client.get('/scan/ip', query_string={"ip": "127.0.0.1"})
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['ip'] == "127.0.0.1"
    assert data[0]['open_ports'] == "22,80"

def test_get_scan_by_ip_invalid_payload(client):
    response = client.get('/scan/ip')
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'Payload was invalid.'}

def test_get_scan_by_ip_invalid_ip(client):
    response = client.get('/scan/ip', query_string={"ip": "999.999.999.999"})
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': '999.999.999.999 is not a valid IP address.'}
