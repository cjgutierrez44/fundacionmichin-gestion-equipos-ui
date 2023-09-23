from flask import Blueprint, render_template

temps_cleaning_bp = Blueprint('temps_cleaning', __name__)

@temps_cleaning_bp.route('/')
def index():
    return render_template('script_pages/temps_cleaning.html')