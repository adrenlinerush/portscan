from flask import Blueprint, request, jsonify
from flasgger import swag_from
import utils
import ipaddress

scan = Blueprint('scan', __name__)

@scan.route('/scan', methods=['POST'])
@swag_from({
    'tags': ['Scan'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'A list of ip addresses to scan.',
            'schema': {
                'type': 'object',
                'properties': {
                    'ip_list': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'format': 'ipv4'
                        }
                    }
                },
                'required': ['ip_list']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Scan results',
            'schema': {
                'type': 'object',
                'properties': {
                    'scan_id': {'type': 'string'},
                    'results': {'type': 'array'}
                }
            }
        },
        400: {
            'description': 'Payload or IP error',
            'schema': {
                'type': 'object',
                'properties': {
                    'ERROR': {'type': 'string'}
                }
            }
        }
    }
})
def run_scan():
    """
    Endpoint to initiate a scan.
    """
    try:
        body = request.json
        ip_list = body['ip_list']
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error), 400
    scan_id = utils.get_scan_id()
    for scan_ip in ip_list:
        try:
            ipaddress.ip_address(scan_ip)
        except ValueError:
            ip_error = {'ERROR': scan_ip + " is not a valid IP address."}
            return jsonify(ip_error), 400
        open_ports = utils.run_scan(scan_ip)
        utils.store_scan_results(scan_ip, scan_id, open_ports)
    # appears to be a delay in the time from results being written to being available in opensearch ugly hack to fix later
    results = []
    while results == []:
        results = utils.retrieve_scan_results(scan_id=scan_id)
    return jsonify(results)

@scan.route('/scan/scan_id', methods=['GET'])
@swag_from({
    'tags': ['Scan'],
    'parameters': [
        {
            'description': 'The id of the scan to receive.',
            'name': 'scan_id',
            'in': 'query',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'scan_id': {'type': 'string'}
                },
                'required': ['scan_id']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Scan results by scan ID',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        },
        400: {
            'description': 'Payload error or Scan ID not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'ERROR': {'type': 'string'}
                }
            }
        }
    }
})
def get_scan_by_id():
    """
    Endpoint to retreive results from a single scan by id.
    """
    try:
        scan_id = request.args.get('scan_id')
        if not scan_id: raise Exception
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error), 400
    scans = utils.retrieve_scan_results(scan_id=scan_id)
    if not scans or len(scans) < 1:
        id_error = {'ERROR': scan_id + ' was not found.'}
        return jsonify(id_error), 400
    return jsonify(scans)

@scan.route('/scan/ip', methods=['GET'])
@swag_from({
    'tags': ['Scan'],
    'parameters': [
        {
            'name': 'ip',
            'description': 'The ip of the scan to receive.',
            'in': 'query',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'ip': {'type': 'string', 'format': 'ipv4'}
                },
                'required': ['ip']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Scan results by IP',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        },
        400: {
            'description': 'Payload error or invalid IP address',
            'schema': {
                'type': 'object',
                'properties': {
                    'ERROR': {'type': 'string'}
                }
            }
        }
    }
})
def get_scan_by_ip():
    """
    Endpoint to retrieve results from all scans on a specific ip.
    """
    try:
        ip = request.args.get('ip')
        if not ip: raise Exception
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error), 400
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        ip_error = {'ERROR': ip + ' is not a valid IP address.'}
        return jsonify(ip_error), 400
    scans = utils.retrieve_scan_results(ip=ip)
    return jsonify(scans)