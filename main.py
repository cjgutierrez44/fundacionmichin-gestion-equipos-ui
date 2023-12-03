from flask import Flask, render_template, Blueprint,Response
import webbrowser
import threading


from app_inventory import app_inventory_bp
from temps_cleaning import temps_cleaning_bp
from reg_cleaning import reg_cleaning_bp
from updates_inventory import updates_inventory_bp
from updates_installer import updates_installer_bp
from app_uninstaller import app_uninstaller_bp
from host_inventory import host_inventory_bp, list_host
from site_blocker import site_blocker_bp
from utils import get_pc_ip, process_request

app = Flask(__name__) 

app1 = Flask(__name__) 

app.register_blueprint(host_inventory_bp, url_prefix='/host_inventory')
app.register_blueprint(app_inventory_bp, url_prefix='/app_inventory')
app.register_blueprint(temps_cleaning_bp, url_prefix='/temps_cleaning')
app.register_blueprint(reg_cleaning_bp, url_prefix='/reg_cleaning')
app.register_blueprint(updates_inventory_bp, url_prefix='/updates_inventory')
app.register_blueprint(updates_installer_bp, url_prefix='/updates_installer')
app.register_blueprint(app_uninstaller_bp, url_prefix='/app_uninstaller')
app.register_blueprint(site_blocker_bp, url_prefix='/site_blocker')


@app1.route('/')
def index1():
    return render_template('infoindex.html')

@app.route('/')
def index():
    return render_template('index.html', list_pcs = list_host(), infoPage = get_pc_ip())

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app1.route('/hosts')
def servir_archivo():
    ruta_al_archivo = get_local_path() + '/static/hosts'
    with open(ruta_al_archivo, 'r') as archivo:
        contenido = archivo.read()
    return Response(contenido, content_type='text/plain')

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")


def start_info_page():
    app1.run(host=get_pc_ip(), port=80)

if __name__ == '__main__':

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()

    info_page_thread = threading.Thread(target=start_info_page)
    info_page_thread.start()

    app.run()
   
