import json
import winrm
import os
from flask import Blueprint, render_template
from utils import get_local_path, get_network, get_pc_ip, process_request

updates_inventory_bp = Blueprint('updates_inventory', __name__)

def get_updates(host):
    applications_list=[]
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    powershell_script ="""
                        Get-WindowsUpdate | ConvertTo-Json
                    """
    result = session.run_ps(powershell_script)               
    if result.status_code == 0:
        decoded_output = json.loads(result.std_out.decode('latin-1').strip('\x00\r\n').replace('\r\n',''))
        aux=[]
        for ir in decoded_output:
            aux.append({'Name':ir['Title'],'Size':ir['Size']})
        return aux

def list_updates():
    file_database=get_network()
    path_file=get_local_path() + '/database/'+ file_database.replace('.','_')
    updates_x_host=[]
    if os.path.isfile(path_file + '_updates.json'):
        with open(path_file + '_updates.json', "r") as file:
            updates_x_host = json.load(file)
    elif os.path.isfile(path_file + '.json'):
        with open(path_file + '.json', "r") as file:
            list_hosts = json.load(file)
        for ir in list_hosts:
            try:
                host=ir['ip']
                updates_x_host.append({'ip':ir['ip']
                                    ,'host_name':ir['name']
                                    ,'updates':get_updates(host)
                                    })
            except Exception as e:
                print (e)
        with open(path_file + '_updates.json', "w") as file:
            file.write(json.dumps(updates_x_host))  
    return updates_x_host      

def list_updates_host(ip):
    list_updates_all = list_updates()
    pc_updates = None
    for pc in list_updates_all:
        if pc["ip"] == ip:
            pc_updates = pc
    return pc_updates

@updates_inventory_bp.route('/')
def index():
    try:
        list_updates()
    except Exception as e:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = "Listado de actualizaciones actualizado.")

def remove_database_file():
    path_file=get_local_path() + '/database/'+ get_network().replace('.','_') + '_updates.json'
    if os.path.isfile(path_file):
        os.remove(path_file)

@updates_inventory_bp.route('/re_scan')
def re_scan():
    remove_database_file()
    try:
        list_updates()
    except Exception as e:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = "Listado de actualizaciones actualizado.")
    

if __name__=='__main__':
    list_updates()
