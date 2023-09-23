import json
import os
import socket
import nmap
from flask import Blueprint, render_template
from utils import get_local_path,get_network,get_host_name


host_inventory_bp = Blueprint('host_inventory', __name__)



def scan_network(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments="-O -p 445")
    added=False
    pcs=[]
    for host in nm.all_hosts():
        if 'osmatch' in nm[host] and nm[host]['osmatch']:
            os_list=nm[host]['osmatch']
            added=False
            for osm in os_list:
                osclass = osm['osclass']
                for os in osclass:
                    if os['osfamily'] == 'Windows':  
                        pcs.append({'ip':host,'name':get_host_name(host)})
                        added=True
                        break
                if added:
                    break
    return pcs
    
def list_host():
    local_net=get_network()
    path_file=get_local_path() + '/database/'+ local_net.replace('.','_') + '.txt'
    list_hosts=[]
    if os.path.isfile(path_file):
        with open(path_file, "r") as file:
            list_hosts = file.readlines()
    else:
        list_hosts=scan_network(local_net + '-254')
        with open(path_file, "w") as file:
            file.write(json.dumps(list_hosts))
    
@host_inventory_bp.route('/')
def index():
    list_pcs=list_host()
    return render_template('script_pages/hosts_inventory.html')

if __name__== '__main__':
    list_host()