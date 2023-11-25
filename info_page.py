from flask import Flask, render_template
import threading
import socket

app = Flask(__name__) 

app1 = Flask(__name__) 



def get_pc_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_local = s.getsockname()[0]
    return ip_local

@app.route('/')
def index():
    return "81"

@app1.route('/')
def index1():
    return "82"

def open_browser():
    app1.run(host=get_pc_ip(), port=82)

if __name__ == '__main__':

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()

    app.run(host=get_pc_ip(), port=81)