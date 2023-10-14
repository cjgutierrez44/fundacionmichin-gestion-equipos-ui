from flask import Blueprint, render_template, make_response, jsonify
from utils import get_local_path, get_network, get_pc_ip, process_request
import time
import random
import json
import winrm
import os


updates_installer_bp = Blueprint('updates_installer', __name__)


def update(host):
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    x=0
    
    powershell_script = f'''
                        Install-WindowsUpdate -AcceptAll -AutoReboot
                        '''
    result = session.run_ps(powershell_script)  

def update_windows():
    file_database=get_network()
    path_file=get_local_path() + '/database/'+ file_database.replace('.','_')
    if os.path.isfile(path_file + '_updates.json'):
        with open(path_file + '_updates.json', "r") as file:
            list_hosts = json.load(file)
        for ir in list_hosts:
            host=ir['ip']
            if ir['updates']:
                update(host)

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


