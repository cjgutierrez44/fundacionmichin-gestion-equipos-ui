import json
import winrm
import os
from flask import Blueprint, render_template
from utils import get_local_path, get_network, get_pc_ip, process_request

site_blocker_bp = Blueprint('site_blocker', __name__)

def block(host,content):
    applications_list=[]
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    x=0
    powershell_script = f'''
                        Set-Content -Path C:\\Windows\\System32\\drivers\\etc\\hosts -Value "# DNS Filtering"
                            '''
    result = session.run_ps(powershell_script)  
    while x<len(content): 
        new_hosts_content='\n'.join(content[x:x+20])
        powershell_script = f'''
                            Add-Content -Path C:\\Windows\\System32\\drivers\\etc\\hosts -Value "{new_hosts_content}"
                            '''
        result = session.run_ps(powershell_script)  
        x+=20
    powershell_script = f'''
                        ipconfig /flushdns
                            '''
    result = session.run_ps(powershell_script)  
                 
def site_blocker():
    file_database=get_network()
    path_file=get_local_path() + '/database/'
    blocked_hosts=[]
    with open(path_file + 'contenidoadulto.txt', "r") as file:
        for linea in file:
            blocked_hosts.append(linea.strip())
    with open(path_file + 'apuestas.txt', "r") as file:
        for linea in file:
            blocked_hosts.append(linea.strip())
    with open(path_file + 'social.txt', "r") as file:
        for linea in file:
            blocked_hosts.append(linea.strip())
    path_file=path_file + file_database.replace('.','_')    
    if os.path.isfile(path_file + '.json'):
        with open(path_file + '.json', "r") as file:
            list_hosts = json.load(file)
            for ir in list_hosts:
                host=ir['ip']
                block(host,blocked_hosts)
                
@site_blocker_bp.route('/')
def index():
    try:
        site_blocker()
    except Exception as e:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = 'Se han bloqueado los sitios web.')
   

if __name__ =='__main__':
    site_blocker()
    