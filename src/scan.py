from flask import Blueprint, request, jsonify
import utils
import ipaddress

scan = Blueprint('scan', __name__)

@scan.route('/scan', methods=['POST'])
def run_scan():
    try:
        body = request.json
        ip_list = body['ip_list']
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error)
    scan_id = utils.get_scan_id()
    for scan_ip in ip_list:
        try:
            ipaddress.ip_address(scan_ip)
        except ValueError:
            ip_error = {'ERROR': scan_ip + " is not a valid IP address."}
            return jsonify(ip_error)
        open_ports = utils.run_scan(scan_ip)
        utils.store_scan_results(scan_ip, scan_id, open_ports)
    results = utils.retreive_scan_results(scan_id=scan_id)
    return jsonify(results)

@scan.route('/scan/scan_id', methods=['GET'])
def get_scan_by_id():
    try:
        body = request.json
        scan_id = body['scan_id']
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error)
    scans = utils.retreive_scan_results(scan_id=scan_id)
    if not scans or len(scans) < 1:
        id_error = {'ERROR': scan_id + ' was not found.'}
        return jsonify(id_error)
    return jsonify(scans)

@scan.route('/scan/ip', methods=['GET'])
def get_scan_by_ip():
    try:
        body = request.json
        ip = body['ip']
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error)
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        ip_error = {'ERROR': ip + ' is not a valid IP address.'}
        return jsonify(ip_error)
    scans = utils.retreive_scan_results(ip=ip)
    return jsonify(scans)