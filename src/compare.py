from flask import Blueprint, request, jsonify
from flasgger import swag_from
import utils

compare = Blueprint('compare', __name__)

@compare.route('/compare', methods=['GET'])
@swag_from({
    'tags': ['Compare'],
    'parameters': [
        {
            'name': 'scan_id_1',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The first scan ID to compare'
        },
        {
            'name': 'scan_id_2',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The second scan ID to compare'
        }
    ],
    'responses': {
        200: {
            'description': 'Comparison results of the two scans',
            'schema': {
                'type': 'object',
                'properties': {
                    'common_ips': {'type': 'array'},
                    'scan_id_1': {'type': 'array'},
                    'scan_id_2': {'type': 'array'}
                }
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
def run_scan():
    """
    Endpoint to compare results from two scans.
    """
    try:
        scan_id_1 = request.args.get('scan_id_1')
        if not scan_id_1: raise Exception
        scan_id_2 = request.args.get('scan_id_2')
        if not scan_id_2: raise Exception
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error), 400


    rslt1 = utils.retreive_scan_results(scan_id=scan_id_1)
    rslt2 = utils.retreive_scan_results(scan_id=scan_id_2)

    if not rslt1 or len(rslt1) < 1:
        id_error = {'ERROR': scan_id_1 + ' was not found.'}
        return jsonify(id_error), 400

    if not rslt2 or len(rslt2) < 1:
        id_error = {'ERROR': scan_id_2 + ' was not found.'}
        return jsonify(id_error), 400

    compare_results = {}
    matching_ips = utils.get_matching_ips(rslt1, rslt2)
    scan_1_only = utils.get_ips_only_in(rslt1, rslt2)
    compare_results[scan_id_1] = utils.get_open_ports_ip_list(rslt1, scan_1_only)
    scan_2_only = utils.get_ips_only_in(rslt2, rslt1)
    compare_results[scan_id_2] = utils.get_open_ports_ip_list(rslt2, scan_2_only)

    compare_results["common_ips"] = []
    for ip in matching_ips:
        common_ports = utils.get_matching_ports(rslt1, rslt2, ip)
        ports_1_only = utils.get_ports_only_in(rslt1, rslt2, ip)
        ports_2_only = utils.get_ports_only_in(rslt2, rslt1, ip)
        compare_results["common_ips"].append({ip:{"common":list(common_ports),scan_id_1:ports_1_only,scan_id_2:ports_2_only}})

    return jsonify(compare_results)