import pytest
from unittest.mock import mock_open
from utils import *
import socket
from contextlib import closing


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


def test_store_scan_results(mocker):
    mock_db = mocker.patch('utils.get_db').return_value
    mock_cursor = mock_db.cursor.return_value

    result = store_scan_results('127.0.0.1', 'scan123', ['22', '80'])

    mock_db.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "insert into portscan (ip, scan_id, open_ports) Values(%s, %s, %s)",
        ['127.0.0.1', 'scan123', '22,80']
    )
    mock_db.commit.assert_called_once()
    assert result == 0


@pytest.mark.parametrize('ip,expected', [
    ('127.0.0.1', [{'timestamp': '2024-08-30 12:34:56', 'id': 'scan123', 'ip': '127.0.0.1', 'open_ports': '22,80'}]),
])
def test_retreive_scan_results_by_ip(mocker, ip, expected):
    mock_db = mocker.patch('utils.get_db').return_value
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [('2024-08-30 12:34:56', 'scan123', '127.0.0.1', '22,80')]

    results = retreive_scan_results(ip=ip)
    assert results == expected
    mock_cursor.execute.assert_called_once_with("select * from portscan where ip = %s", [ip])


@pytest.mark.parametrize('scan_id,expected', [
    ('scan123', [{'timestamp': '2024-08-30 12:34:56', 'id': 'scan123', 'ip': '127.0.0.1', 'open_ports': '22,80'}]),
])
def test_retreive_scan_results_by_scan_id(mocker, scan_id, expected):
    mock_db = mocker.patch('utils.get_db').return_value
    mock_cursor = mock_db.cursor.return_value
    mock_cursor.fetchall.return_value = [('2024-08-30 12:34:56', 'scan123', '127.0.0.1', '22,80')]

    results = retreive_scan_results(scan_id=scan_id)
    assert results == expected
    mock_cursor.execute.assert_called_once_with("select * from portscan where scan_id = %s", [scan_id])


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
