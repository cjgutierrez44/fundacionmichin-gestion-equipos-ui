from flask import Blueprint, render_template, make_response, jsonify
from utils import process_request
import time
import random

updates_installer_bp = Blueprint('updates_installer', __name__)


def install_updates_on_all_hosts():
    time.sleep(5)
    num = random.randint(1, 10)
    if num % 2 == 0:
        raise ValueError('No se pudo instalar ninguna actualizacion')
    return 'OK'


def install_updates(ip_address):
    time.sleep(5)
    num = random.randint(1, 10)
    if num % 2 == 0:
        raise ValueError('No se pudo actualizar este equipo')
    return 'OK'


@updates_installer_bp.route('/')
def index():
    try:
        install_updates_on_all_hosts()
    except Exception as e:
        print(e)
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = "Se han actualizado todos los equipos.")
    
@updates_installer_bp.route('/pc/<ip>')
def install_updates_host(ip):
    try:
        install_updates(ip)
    except Exception as e:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = "Equipo actualizado.")
