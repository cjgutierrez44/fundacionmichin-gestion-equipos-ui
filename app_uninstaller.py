import json
import winrm
from flask import Blueprint, render_template
from utils import get_pc_ip

app_uninstaller_bp = Blueprint('app_uninstaller', __name__)

@app_uninstaller_bp.route('/')

def app_unistall(host,app_id):
    if host==get_pc_ip():
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'))
    else:
        session = winrm.Session(f'http://{host}:5985/wsman',auth=('support', 'support12345'),transport='ntlm')
    powershell_script =f"""
                        Get-WmiObject -Class Win32_Product | Where-Object {{ $_.IdentifyingNumber -eq "{app_id}" }} | ForEach-Object {{ $_.Uninstall() }}
                    """
    session.run_ps(powershell_script)               
    
def index():
    return render_template('script_pages/app_uninstaller.html')    

if __name__=='__main__':
    app_unistall('192.168.20.8',)