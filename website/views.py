from flask import Blueprint, render_template, redirect, session, url_for

views = Blueprint('views', __name__)


@views.route('/')
def home():
    # # Redirect to login if not already logged in
    # if 'login.id' not in session:
    #     return redirect(url_for('auth.login'))
    return render_template("home.html")
