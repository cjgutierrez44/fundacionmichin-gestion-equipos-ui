from flask import Blueprint, render_template

updates_inventory_bp = Blueprint('updates_inventory', __name__)

@updates_inventory_bp.route('/')
def index():
    return render_template('script_pages/updates_inventory.html')