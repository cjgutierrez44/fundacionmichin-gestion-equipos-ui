import json
import winrm
import os
from flask import Blueprint, render_template
from utils import get_local_path, get_network, get_pc_ip

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
            

@updates_installer_bp.route('/')
def index():
    return render_template('script_pages/updates_installer.html')

if __name__=='__main__':
    update_windows()