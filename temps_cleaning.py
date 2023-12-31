import json
import os
import winrm
from flask import Blueprint, render_template
from utils import get_network,get_local_path,get_pc_ip, process_request

temps_cleaning_bp = Blueprint('temps_cleaning', __name__)

def clean(host):
    applications_list=[]
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    powershell_script ="""
                        Start-Process -filepath "cleanmgr.exe" -argumentlist "/sagerun:1" -wait
                        Start-Process -filepath "cleanmgr.exe" -argumentlist "/sagerun:2" -wait
                    """
    result = session.run_ps(powershell_script) 
    powershell_script = '''
                        $usersPath = "C:\\Users"
                            Get-ChildItem -Path $usersPath -Directory | ForEach-Object {
                                $tempPath = Join-Path $_.FullName "AppData\\Local\\Temp"
                                if (Test-Path $tempPath) {
                                    Remove-Item "$tempPath\*" -Force -Recurse -ErrorAction SilentlyContinue
                                }
                            }
                     '''
    result = session.run_ps(powershell_script) 
    powershell_script = '''
                        Start-Process "sfc.exe" -ArgumentList "/scannow" -WindowStyle Hidden
                     '''
    result = session.run_ps(powershell_script) 
    powershell_script = '''
                        Optimize-Volume -DriveLetter C -ReTrim -Verbose
                     '''
    result = session.run_ps(powershell_script) 
    powershell_script = '''
                        Clear-Host
                        Clear-DnsClientCache
                     '''
    result = session.run_ps(powershell_script) 
                     
    if result.status_code == 0:
        decoded_output = result.std_out
        

def clean_temp_files():
    file_database=get_network()
    path_file=get_local_path() + '/database/'+ file_database.replace('.','_')
    apps_x_host=[]
    if os.path.isfile(path_file + '.json'):
        with open(path_file + '.json', "r") as file:
            list_hosts = json.load(file)
        for ir in list_hosts:
            host=ir['ip']
            try:
                clean(host)
            except Exception as e:
                print (e)

@temps_cleaning_bp.route('/')
def index():
    try:
        clean_temp_files()
    except Exception as e:
        return process_request(function_result = False)
    return process_request(function_result = True, response_msg = 'Se han borrado los archivos temporales.')

if __name__=='__main__':
    clean_temp_files()