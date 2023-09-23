from flask import Blueprint, render_template

reg_cleaning_bp = Blueprint('reg_cleaning', __name__)

@reg_cleaning_bp.route('/')
def index():
    return render_template('script_pages/reg_cleaning.html')