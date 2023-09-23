from flask import Blueprint, render_template

updates_installer_bp = Blueprint('updates_installer', __name__)

@updates_installer_bp.route('/')
def index():
    return render_template('script_pages/updates_installer.html')