from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import column, text

from website import database

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if request.method == 'GET':
        if 'id' in request.args and 'password' in request.args:
            # Use database connection to check if the user account is valid
            res = database.db.session.query(column('Passwd'), column('Name')).from_statement(text(f'SELECT * FROM User where UserID = {request.args.get("id")}')).all()
            print(res)

            if not res:
                return render_template("login.html", info="User not found")

            password = res[0][0]
            if request.args.get('password') == password:
                # Set session variables accordingly
                session['login.id'] = request.args.get('id')
                session['login.name'] = res[0][1]
                session['login.password'] = request.args.get('password')
                return redirect(url_for('views.home'))
            else:
                return render_template("login.html", info='Credentials not accepted')
        else:
            return render_template("login.html")
    else:
        return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", info="Successfully logged out")


@auth.route('/sign_up_seller')
def signUpSeller():
    return render_template("sign_up_seller.html")


@auth.route('/sign_up_buyer')
def signUpBuyer():
    return render_template("sign_up_buyer.html")
