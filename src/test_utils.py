import pytest
from unittest.mock import mock_open
from utils import *

def test_store_scan_results(mocker):
    mock_os_client = mocker.patch('utils.get_os').return_value
    mock_index = mock_os_client.index
    result = store_scan_results('127.0.0.1', 'scan123', ['22', '80'])
    expected_document = {
        'ip': '127.0.0.1',
        'scan': 'scan123',
        'open_ports': '22,80',
    }
    # I don't care if timestamp matches.
    actual_document = mock_index.call_args[1]['body']
    actual_document.pop('timestamp', None)

    mock_index.assert_called_once_with(index='portscan', body=expected_document)
    assert result == mock_index.return_value.get("result", "error")


@pytest.mark.parametrize('ip,expected', [
    ('scan123', [{'timestamp': '2024-08-30T12:34:56Z', 'ip': '127.0.0.1', 'open_ports': '22,80', 'scan_id': 'scan123'}]),
])
def test_retrieve_scan_results_by_ip(mocker, ip, expected):
    mock_os_client = mocker.patch('utils.get_os').return_value
    mock_search = mock_os_client.search
    mock_search.return_value = {
        "hits": {
            "hits": [
                {
                    "_id": "1",
                    "_source": {
                        "timestamp": "2024-08-30T12:34:56Z",
                        "ip": "127.0.0.1",
                        "open_ports": "22,80",
                        "scan": "scan123"
                    }
                }
            ]
        }
    }
    results = retrieve_scan_results(ip=ip)
    mock_search.assert_called_once_with(
        index="portscan",
        body={
            "query": {
                "bool": {
                    "must": [{"match": {"ip": ip}}]
                }
            }
        }
    )
    assert results == expected


@pytest.mark.parametrize('scan_id,expected', [
    ('scan123', [{'timestamp': '2024-08-30T12:34:56Z', 'ip': '127.0.0.1', 'open_ports': '22,80', 'scan_id': 'scan123'}]),
])
def test_retrieve_scan_results_by_scan_id(mocker, scan_id, expected):
    mock_os_client = mocker.patch('utils.get_os').return_value
    mock_search = mock_os_client.search
    mock_search.return_value = {
        "hits": {
            "hits": [
                {
                    "_id": "1",
                    "_source": {
                        "timestamp": "2024-08-30T12:34:56Z",
                        "ip": "127.0.0.1",
                        "open_ports": "22,80",
                        "scan": "scan123"
                    }
                }
            ]
        }
    }

    results = retrieve_scan_results(scan_id=scan_id)
    mock_search.assert_called_once_with(
        index="portscan",
        body={
            "query": {
                "bool": {
                    "must": [{"match": {"scan": scan_id}}]
                }
            }
        }
    )
    assert results == expected

def test_get_ports_to_scan(mocker):
    mocker.patch('builtins.open', mock_open(read_data="22\n80\n443\n"))
    ports = get_ports_to_scan()
    assert ports == ['22', '80', '443']


def test_get_scan_id():
    scan_id = get_scan_id()
    assert len(scan_id) == 32


def test_run_scan(mocker):
    mock_get_ports_to_scan = mocker.patch('utils.get_ports_to_scan', return_value=['22', '80'])
    mock_socket = mocker.patch('socket.socket')
    mock_sock_instance = mock_socket.return_value
    mock_sock_instance.connect_ex.side_effect = [0, 1]

    open_ports = run_scan('127.0.0.1')
    assert open_ports == ['22']
    mock_get_ports_to_scan.assert_called_once()
    assert mock_socket.call_count is 2

def test_get_matching_ips():
    scan_1 = [{'ip': '192.168.1.1'}, {'ip': '192.168.1.2'}]
    scan_2 = [{'ip': '192.168.1.2'}, {'ip': '192.168.1.3'}]
    common_ips = get_matching_ips(scan_1, scan_2)
    assert common_ips == {'192.168.1.2'}


def test_get_matching_ports():
    scan_1 = [{'ip': '192.168.1.1', 'open_ports': '22,80,443'}]
    scan_2 = [{'ip': '192.168.1.1', 'open_ports': '22,443'}]
    common_ports = get_matching_ports(scan_1, scan_2, '192.168.1.1')
    assert common_ports == {'22', '443'}


def test_get_ips_only_in():
    scan_1 = [{'ip': '192.168.1.1'}, {'ip': '192.168.1.2'}]
    scan_2 = [{'ip': '192.168.1.2'}, {'ip': '192.168.1.3'}]
    ips_only_in_scan_1 = get_ips_only_in(scan_1, scan_2)
    assert ips_only_in_scan_1 == ['192.168.1.1']


def test_get_ports_only_in():
    scan_1 = [{'ip': '192.168.1.1', 'open_ports': '22,80,443'}]
    scan_2 = [{'ip': '192.168.1.1', 'open_ports': '22,443'}]
    ports_only_in_scan_1 = get_ports_only_in(scan_1, scan_2, '192.168.1.1')
    assert ports_only_in_scan_1 == ['80']


def test_get_open_ports_ip_list():
    scan = [{'ip': '192.168.1.1', 'open_ports': '22,80,443'}]
    ips = ['192.168.1.1']
    open_ports_ip_list = get_open_ports_ip_list(scan, ips)
    assert open_ports_ip_list == [{'192.168.1.1': ['22', '80', '443']}]
