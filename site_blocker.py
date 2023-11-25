import json
import winrm
import os
from flask import Blueprint, render_template
from utils import get_local_path, get_network, get_pc_ip, process_request

site_blocker_bp = Blueprint('site_blocker', __name__)

def block(host):

    info_page_ip = get_pc_ip()

    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    x=0
    url_hosts_file='https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
    powershell_script='''
        reg add "HKLM\\SYSTEM\\CurrentControlSet\\services\\Dnscache" /v Start /t REG_DWORD /d 4 /f
        '''
    result = session.run_ps(powershell_script) 
    powershell_script = f'''
                    $url = "{url_hosts_file}"
        $hostsPath = "C:\\Windows\\System32\\drivers\\etc"
        $originalHosts = Join-Path $hostsPath "hosts"
        $backupHosts = Join-Path $hostsPath "hosts.backup"

        # Crear una copia de seguridad del archivo hosts original
        if (Test-Path $originalHosts) {{
            Copy-Item -Path $originalHosts -Destination $backupHosts -Force
        }}

        # Descargar el archivo hosts
        Invoke-WebRequest -Uri $url -OutFile $originalHosts -UseBasicParsing

        # Leer el contenido del archivo hosts, reemplazar 0.0.0.0 por 192.168.1.1 y guardar los cambios
        $content = Get-Content $originalHosts -Raw
        $modifiedContent = $content.Replace('0.0.0.0', '{info_page_ip}')
        Set-Content -Path $originalHosts -Value $modifiedContent
                    '''
    result = session.run_ps(powershell_script)
    if result.status_code != 0:
        print(f"Error en el host {host}: {result.std_err}")
    else:
        print(f"Archivo hosts actualizado con éxito en {host}")  
                 
def site_blocker():
    file_database=get_network()
    path_file=get_local_path() + '/database/'
    blocked_hosts=[]
    
    path_file=path_file + file_database.replace('.','_')    
    if os.path.isfile(path_file + '.json'):
        with open(path_file + '.json', "r") as file:
            list_hosts = json.load(file)
            for ir in list_hosts:
                try:
                    host=ir['ip']
                    block(host)
                except Exception as e:
                    print (e)
                    
@site_blocker_bp.route('/')
def index():
    try:
        site_blocker()
    except Exception as e:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = 'Se han bloqueado los sitios web.')
   
if __name__ =='__main__':
    site_blocker()
    