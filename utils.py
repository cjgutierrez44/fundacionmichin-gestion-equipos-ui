from flask import make_response, jsonify
import os
import socket
import json

def get_local_path():
    actual_path = os.getcwd()
    return actual_path

def get_pc_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    return ip_local

def get_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    octetos=ip_local.split('.')
    octetos[3]='1'
    s.close()    
    return '.'.join(octetos)

def get_host_name(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except Exception as e:
        return ''

def json_str_to_json_list(json_in):
    json_out = None
    if len(json_in) == 1:
        try:
            json_out = json.loads(json_in[0])
        except json.JSONDecodeError as e:
            pass
    return json_out


def process_request(function_result = True, response_msg = 'Tabajo terminado. (pensar algo mejor)'):
    data = {
        'status_code' : '',
        'response': ''
    }

    if function_result:
        data['status_code'] = 200
        data['response'] = response_msg
    else:
        data['status_code'] = 500
        data['response'] = 'Ha ocurrido un error durante el proceso, intentelo más tarde.'

    return make_response(jsonify(data), data['status_code'], {'Content-Type': 'application/json'})