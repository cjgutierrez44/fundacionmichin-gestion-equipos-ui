from flask import Flask, render_template, Blueprint
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


app = Flask(__name__)

app.register_blueprint(host_inventory_bp, url_prefix='/host_inventory')
app.register_blueprint(app_inventory_bp, url_prefix='/app_inventory')
app.register_blueprint(temps_cleaning_bp, url_prefix='/temps_cleaning')
app.register_blueprint(reg_cleaning_bp, url_prefix='/reg_cleaning')
app.register_blueprint(updates_inventory_bp, url_prefix='/updates_inventory')
app.register_blueprint(updates_installer_bp, url_prefix='/updates_installer')
app.register_blueprint(app_uninstaller_bp, url_prefix='/app_uninstaller')
app.register_blueprint(site_blocker_bp, url_prefix='/site_blocker')

@app.route('/')
def index():
    return render_template('index.html', list_pcs = list_host())

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    app.run()
