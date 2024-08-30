import uuid
import socket
from os import environ
from contextlib import closing
import mysql.connector

def get_db():
    db = mysql.connector.connect(
        host = environ['DB_HOST'],
        username = environ['DB_USERNAME'],
        password = environ['DB_PASSWORD'],
        database = environ['DB_DATABASE']
    )
    return db

def get_ports_to_scan():
    ports = []
    with open("ports2scan") as file:
        ports = [line.rstrip() for line in file]
    return ports

def get_scan_id():
    return uuid.uuid4().hex

def run_scan(ip):
    open_ports = []
    ports_to_scan = get_ports_to_scan()
    for port in ports_to_scan:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            # add timeout for when IP doesn't exist
            sock.settimeout(.1)
            if sock.connect_ex((ip, int(port))) == 0:
                open_ports.append(port)
    return open_ports

def store_scan_results(ip, scan_id, open_ports):
    db = get_db()
    csr = db.cursor()
    sql = "insert into portscan (ip, scan_id, open_ports) Values(%s, %s, %s)"
    csr.execute(sql,[ip,scan_id,','.join(open_ports)])
    db.commit()

    return (0)

def retreive_scan_results(ip=None, scan_id=None):
    db = get_db()
    csr = db.cursor()
    scan_results = []
    if ip:
        sql = "select * from portscan where ip = %s"
        csr.execute(sql, [ip])
    elif scan_id:
        sql = "select * from portscan where scan_id = %s"
        csr.execute(sql, [scan_id])
    for scan in csr.fetchall():
        result = {"timestamp": scan[0], "id": scan[1], "ip": scan[2], "open_ports": scan[3]}
        scan_results.append(result)
    return scan_results

def get_matching_ips(scan_1, scan_2):
    ips1 = []
    ips2 = []
    for item in scan_1:
        ips1.append(item["ip"])
    for item in scan_2:
        ips2.append(item["ip"])
    common_ips = set(ips1).intersection(ips2)
    return common_ips

def get_matching_ports(scan_1, scan_2, ip):
    ports1 = []
    ports2 = []
    for item in scan_1:
        if item["ip"] == ip:
            ports1 = item["open_ports"].split(",")
    for item in scan_2:
        if item["ip"] == ip:
            ports2 = item["open_ports"].split(",")
    common_ports = set(ports1).intersection(ports2)
    return common_ports

def get_ips_only_in(scan_only, scan_other):
    ips1 = []
    ips2 = []
    only_ips = []
    for item in scan_only:
        ips1.append(item["ip"])
    for item in scan_other:
        ips2.append(item["ip"])
    for ip in ips1:
        if ip not in ips2:
            only_ips.append(ip)
    return only_ips

def get_ports_only_in(scan_only, scan_other, ip):
    ports1 = []
    ports2 = []
    only_ports = []
    for item in scan_only:
        if item["ip"] == ip:
            ports1 = item["open_ports"].split(",")
    for item in scan_other:
        if item["ip"] == ip:
            ports2 = item["open_ports"].split(",")
    for port in ports1:
        if port not in ports2:
            only_ports.append(port)
    return only_ports

def get_open_ports_ip_list(scan, ips):
    ports = []
    for item in scan:
        if item["ip"]in ips:
            ports.append({item["ip"]: item["open_ports"].split(",")})
    return ports
