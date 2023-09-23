from flask import Blueprint, render_template

site_blocker_bp = Blueprint('site_blocker', __name__)

@site_blocker_bp.route('/')
def index():
    return render_template('script_pages/site_blocker.html')     