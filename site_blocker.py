import json
import winrm
import os
from flask import Blueprint, render_template, request, jsonify, url_for, Response
from utils import get_local_path, get_network, get_pc_ip, process_request

site_blocker_bp = Blueprint('site_blocker', __name__)


@site_blocker_bp.route('/custom', methods=['GET', 'PUT', 'DELETE'])
def read_custom_block_list():
    if request.method == 'GET':
        return jsonify(get_sites())
    elif request.method == 'PUT' and request.args.get('site').strip() != '':
        delete_site(format_url(request.args.get('site')))
        add_site(format_url(request.args.get('site')))
        return jsonify("SITE ADDED")
    elif request.method == 'DELETE' and request.args.get('site').strip() != '':
        delete_site(format_url(request.args.get('site')))
        return jsonify("SITE DELETED")
    else:
        return jsonify("ERROR")


def format_url(url):
    return url.replace('www.', '').replace('https://', '').replace('http://', '').split('/')[0]

def get_sites():
    custom_list_flag = False
    path_file=get_local_path() + '/static/hosts'
    custom_list = []
    if os.path.isfile(path_file):
        with open(path_file, "r") as file:
            for line in file:
                if line.strip() == '#CUSTOM_LIST':
                    custom_list_flag = True
                if custom_list_flag and line.strip() != '#CUSTOM_LIST' and line.strip() != '':
                    custom_list.append(line.strip().split()[1])
        return custom_list

def add_site(site):
    path_file=get_local_path() + '/static/hosts'
    if os.path.isfile(path_file):
        new_lines = []
        with open(path_file, "r+") as file:
            lines = file.readlines()
            for line in lines:
                new_lines.append(line.strip())
                if line.strip() == '#CUSTOM_LIST':
                     new_lines.append(f'{get_pc_ip()} ' + site)
            file.seek(0)
            file.truncate()
            file.write('\n'.join(new_lines))

def delete_site(site):
    path_file=get_local_path() + '/static/hosts'
    new_lines = []
    with open(path_file, "r+") as file:
        lines = file.readlines()
        for line in lines:
            if site not in line:
                new_lines.append(line.strip())
        file.seek(0)
        file.truncate()
        file.write('\n'.join(new_lines))

def replaceIP():
    custom_list_flag = False
    path_file=get_local_path() + '/static/hosts'
    custom_list = []
    if os.path.isfile(path_file):
        with open(path_file, "r+") as file:
            for line in file:
                if line.strip() == '#CUSTOM_LIST':
                    custom_list_flag = True
                if custom_list_flag and line.strip() != '#CUSTOM_LIST' and line.strip() != '':
                    ip_address = line.split()[0]
                    custom_list.append(line.replace(ip_address, get_pc_ip()).strip())
                else:
                    custom_list.append(line.strip())
            file.seek(0)
            file.truncate()
            file.write('\n'.join(custom_list))

def block(host, list):

    info_page_ip = get_pc_ip()

    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    x=0

    url_hosts_file = ''

    if list == 'GENERIC':
        url_hosts_file = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts'
    else:
        url_hosts_file = f'http://{info_page_ip}/static/hosts'

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
        #$content = Get-Content $originalHosts -Raw
        #$modifiedContent = $content.Replace('0.0.0.0', '{info_page_ip}')
        #Set-Content -Path $originalHosts -Value $modifiedContent
                    '''
    result = session.run_ps(powershell_script)
    if result.status_code != 0:
        print(f"Error en el host {host}: {result.std_err}")
    else:
        print(f"Archivo hosts actualizado con éxito en {host}")  
                 
def site_blocker(list):
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
                    block(host, list)
                except Exception as e:
                    print (e)
                    
@site_blocker_bp.route('/<list>')
def index(list):
    replaceIP()
    if list == 'GENERIC' or list == 'CUSTOM':
        try:
            site_blocker(list)
        except Exception as e:
            return process_request(function_result = False)
    else:
        return process_request(function_result = False)

    return process_request(function_result = True, response_msg = 'Se han bloqueado los sitios web.')
   
if __name__ =='__main__':
    site_blocker()
    