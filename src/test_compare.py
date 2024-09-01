import pytest
from flask import Flask, jsonify

@pytest.fixture
def client():
    from compare import compare
    app = Flask(__name__)
    app.register_blueprint(compare)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_utils(mocker):
    mocker.patch('utils.retrieve_scan_results')
    mocker.patch('utils.get_matching_ips', return_value=['192.168.1.1'])
    mocker.patch('utils.get_ips_only_in', side_effect=[['192.168.1.2'], ['192.168.1.3']])
    mocker.patch('utils.get_open_ports_ip_list', side_effect=[
        [{"192.168.1.2": ["22", "80"]}],
        [{"192.168.1.3": ["443"]}]
    ])
    mocker.patch('utils.get_matching_ports', return_value=['80'])
    mocker.patch('utils.get_ports_only_in', side_effect=[['22'], ['443']])

def test_compare_success(client, mock_utils, mocker):
    mocker.patch('utils.retrieve_scan_results', return_value=[
        [{"ip": "192.168.1.1", "open_ports": "22,80"}, {"ip": "192.168.1.2", "open_ports": "22,80"}],
        [{"ip": "192.168.1.1", "open_ports": "80"}, {"ip": "192.168.1.3", "open_ports": "443"}]
    ])

    response = client.get('/compare', query_string={"scan_id_1": "scan1", "scan_id_2": "scan2"})
    assert response.status_code == 200
    data = response.get_json()
    assert "common_ips" in data
    assert len(data["common_ips"]) == 1
    assert data["common_ips"][0]["192.168.1.1"]["common"] == ["80"]

def test_compare_invalid_payload(client):
    response = client.get('/compare')
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'Payload was invalid.'}

def test_compare_scan_id_1_not_found(client, mock_utils, mocker):
    mock_retrieve_scan_results = mocker.patch('utils.retrieve_scan_results')
    mock_retrieve_scan_results.side_effect = [
        [],
        [{"ip": "192.168.1.1", "open_ports": "80"}]
    ]

    response = client.get('/compare', query_string={"scan_id_1": "invalid_scan1", "scan_id_2": "scan2"})
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'invalid_scan1 was not found.'}

def test_compare_scan_id_2_not_found(client, mock_utils, mocker):
    mock_retrieve_scan_results = mocker.patch('utils.retrieve_scan_results')
    mock_retrieve_scan_results.side_effect = [
        [{"ip": "192.168.1.1", "open_ports": "22,80"}],
        []
    ]

    response = client.get('/compare', query_string={"scan_id_1": "scan1", "scan_id_2": "invalid_scan2"})
    assert response.status_code == 400
    assert response.get_json() == {'ERROR': 'invalid_scan2 was not found.'}
