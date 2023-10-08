import json
import os
import socket
import nmap
from flask import Blueprint, render_template, redirect, url_for
from utils import get_local_path,get_network,get_host_name, json_str_to_json_list

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
    path_file=get_local_path() + '/database/'+ local_net.replace('.','_') + '.json'
    list_hosts=[]
    if os.path.isfile(path_file):
        with open(path_file, "r") as file:
            list_hosts = json_str_to_json_list(file.readlines())
    else:
        list_hosts=scan_network(local_net + '-254')
        with open(path_file, "w") as file:
            file.write(json.dumps(list_hosts))
    return list_hosts
    
@host_inventory_bp.route('/re_scan')
def re_scan():
    path_file=get_local_path() + '/database/'+ get_network().replace('.','_') + '.json'
    if os.path.isfile(path_file):
        os.remove(path_file)
    return redirect(url_for('host_inventory.index'))

@host_inventory_bp.route('/')
def index():
    list_pcs = list_host()
    return render_template('script_pages/hosts_inventory.html', list_pcs = list_pcs )


@host_inventory_bp.route('/re_scan/<page_from>?')
def re_scan(page_from = 'index'):
    print(page_from)
    path_file=get_local_path() + '/database/'+ get_network().replace('.','_') + '.json'
    if os.path.isfile(path_file):
        os.remove(path_file)
        return redirect(url_for(page_from))

