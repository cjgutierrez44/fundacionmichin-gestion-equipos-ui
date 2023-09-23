from flask import Blueprint, render_template

app_uninstaller_bp = Blueprint('app_uninstaller', __name__)

@app_uninstaller_bp.route('/')
def index():
    return render_template('script_pages/app_uninstaller.html')    