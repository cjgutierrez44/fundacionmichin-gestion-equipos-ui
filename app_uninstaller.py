import json
import winrm
import time
from flask import Blueprint, render_template
from utils import get_pc_ip, process_request

app_uninstaller_bp = Blueprint('app_uninstaller', __name__)


def app_unistall(host, app_id):
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    powershell_script =f"""
                        Get-WmiObject -Class Win32_Product | Where-Object {{ $_.IdentifyingNumber -eq "{app_id}" }} | ForEach-Object {{ $_.Uninstall() }}
                    """
    session.run_ps(powershell_script)               

@app_uninstaller_bp.route('/host/<host>/app_id/<app_id>')
def index(host, app_id):
    try:
        app_unistall(host, app_id[1:-1])
    except Exception as e:
        return process_request(function_result = False)
    return process_request(function_result = True, response_msg = "Listado de actualizaciones actualizado.")

if __name__=='__main__':
    app_unistall('172.20.10.10','2D9D28CD-84DE-4DC7-BAD2-CA5505324049')