import json
import os
import winrm
import codecs
from flask import Blueprint, render_template
from utils import get_network,get_local_path,get_pc_ip, json_str_to_json_list
from updates_inventory import list_updates_host


app_inventory_bp = Blueprint('app_inventory', __name__)
def query_apps(host):
    applications_list=[]
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    powershell_script = '''
                        $apps = Get-WmiObject -Query "SELECT * FROM Win32_Product  WHERE (NOT (Name LIKE 'Microsoft%'))"
                        $apps | ForEach-Object {
                            [PSCustomObject]@{
                                Name = $_.Name
                                IdentifyingNumber = $_.IdentifyingNumber
                            }
                        } | ConvertTo-Json
                        '''

    result = session.run_ps(powershell_script)
    if result.status_code == 0:
        decoded_output = result.std_out.decode('latin-1').strip('\x00\r\n').replace('\r\n','')
        applications_list=json.loads(decoded_output)
    return applications_list
    
def get_app_list():
    file_database=get_network()
    path_file=get_local_path() + '/database/'+ file_database.replace('.','_')
    apps_x_host=[]
    if os.path.isfile(path_file + '_apps.json'):
        with open(path_file + '_apps.json', "r") as file:
            apps_x_host = json.load(file)

    elif os.path.isfile(path_file + '.json'):
        with open(path_file + '.json', "r") as file:
            list_hosts = json.load(file)
        for ir in list_hosts:
            host=ir['ip']
            try:
                apps_x_host.append({'ip':ir['ip']
                                ,'host_name':ir['name']
                                ,'apps':query_apps(host)})
            except Exception as e:
                print (e)
        with open(path_file + '_apps.json', "w") as file:
            file.write(json.dumps(apps_x_host))        
    return apps_x_host
    
@app_inventory_bp.route('/pc/<ip>')
def index(ip):
    list_apps=get_app_list()
    pc_apps = None
    pc_updates = None
    for pc in list_apps:
        if pc["ip"] == ip:
            pc_apps = pc
            pc_updates = list_updates_host(ip)
    return render_template('script_pages/app_inventory.html', pc_apps = pc_apps, pc_updates = pc_updates)

@app_inventory_bp.route('/re_scan')
def re_scan():
    path_file=get_local_path() + '/database/'+ get_network().replace('.','_') + '_apps.json'
    if os.path.isfile(path_file):
        os.remove(path_file)
    get_app_list()

if __name__=='__main__':
    get_app_list()


