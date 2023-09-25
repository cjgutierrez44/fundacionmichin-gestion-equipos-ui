import os
import socket

def get_local_path():
    actual_path = os.getcwd()
    return actual_path

def get_pc_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    return ip_local

def get_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    octetos=ip_local.split('.')
    octetos[3]='1'
    s.close()    
    return '.'.join(octetos)

def get_host_name(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except Exception as e:
        return ''
    