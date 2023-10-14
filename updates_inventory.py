import json
import winrm
import os
from flask import Blueprint, render_template

from utils import get_local_path, get_network, get_pc_ip

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
            host=ir['ip']
            updates_x_host.append({'ip':ir['ip']
                                  ,'host_name':ir['name']
                                  ,'updates':get_updates(host)
                                  })
        with open(path_file + '_updates.json', "w") as file:
            file.write(json.dumps(updates_x_host))  
    return updates_x_host      

@updates_inventory_bp.route('/')
def index():
    # list_updates()
    return render_template('script_pages/updates_inventory.html')

if __name__=='__main__':
    list_updates()