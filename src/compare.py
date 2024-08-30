from flask import Blueprint, request, jsonify
import utils

compare = Blueprint('compare', __name__)

@compare.route('/compare', methods=['GET'])
def run_scan():
    try:
        body = request.json
        scan_id_1 = body['scan_id_1']
        scan_id_2 = body['scan_id_2']
    except:
        payload_error = {'ERROR': 'Payload was invalid.'}
        return jsonify(payload_error)


    rslt1 = utils.retreive_scan_results(scan_id=scan_id_1)
    rslt2 = utils.retreive_scan_results(scan_id=scan_id_2)

    if not rslt1 or len(rslt1) < 1:
        id_error = {'ERROR': scan_id_1 + ' was not found.'}
        return jsonify(id_error)

    if not rslt2 or len(rslt2) < 1:
        id_error = {'ERROR': scan_id_2 + ' was not found.'}
        return jsonify(id_error)

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