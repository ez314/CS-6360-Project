from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import column, text

from website import database
from website.util import get_account_type

profile = Blueprint('profile', __name__)


@profile.route('/profile/<int:userId>')
def view_profile(userId):
    if request.method == 'GET':
        # Find user, if it exists
        res = database.db.session.execute(
            text(f'SELECT Name, Email, PhoneNum FROM User where UserID = {userId}')).all()
        print(res)
        if not res:
            return render_template("error.html", error="That user could not be found.")

        # Determine account type, if it exists
        user_account_type = get_account_type(userId)
        if not user_account_type:
            return render_template("error.html", error="That user does not have an associated account.")

        user = {
            'id': userId,
            'name': res[0][0],
            'email': res[0][1],
            'phone': res[0][2],
            'type': user_account_type.capitalize()
        }

        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('profile.profile'))
