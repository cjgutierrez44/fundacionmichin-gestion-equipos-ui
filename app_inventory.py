from flask import Blueprint, render_template

app_inventory_bp = Blueprint('app_inventory', __name__)

@app_inventory_bp.route('/')
def index():
    return render_template('script_pages/app_inventory.html')





