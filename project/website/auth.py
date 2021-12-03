from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import column, text

from website import database

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if request.method == 'GET':
        if 'id' in request.args and 'password' in request.args:
            # Use database connection to check if the user account is valid
            res = database.db.session.execute(
                text(f'SELECT Passwd, Name FROM User where UserID = {request.args.get("id")}')).all()
            print(res)

            if not res:
                return render_template("login.html", info="User not found")

            # Validate password
            password, name = res[0]
            if request.args.get('password') == password:
                # Determine account type
                if database.db.session.execute(
                        text(f'SELECT * FROM Buyer where BuyerID = {request.args.get("id")}')).rowcount > 0:
                    session['login.type'] = 'buyer'
                elif database.db.session.execute(
                        text(f'SELECT * FROM Seller where SellerID = {request.args.get("id")}')).rowcount > 0:
                    session['login.type'] = 'seller'
                elif database.db.session.execute(
                        text(f'SELECT * FROM Admin where AdminID = {request.args.get("id")}')).rowcount > 0:
                    session['login.type'] = 'admin'
                else:
                    return render_template("login.html", info="Login is valid, but no account type could be found")

                # Set session variables accordingly
                session['login.id'] = request.args.get('id')
                session['login.name'] = name
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
    return redirect(url_for('auth.login'))


@auth.route('/sign_up')
def signUp():
    if request.method == 'GET':
        if session:
            # Already logged in
            return render_template("sign_up_success.html")
        elif all(x in request.args for x in ['name', 'email', 'password', 'phone', 'address', 'account-type']):
            # All args passed, create new user in database
            new_user_vals = 'DEFAULT, "{}", "{}", "{}", "{}", "{}"'.format(
                request.args.get('name'),
                request.args.get('email'),
                request.args.get('password'),
                request.args.get('phone'),
                request.args.get('address')
            )
            statement = (f'INSERT INTO User (UserID, Name, Email, Passwd, PhoneNum, HomeAddr)\n'
                         f'    VALUES ({new_user_vals});')
            database.db.session.execute(text(statement))

            # Fetch ID of inserted user. Must do this because of autoincrement
            res = database.db.session.execute(text('SELECT LAST_INSERT_ID();')).all()
            print(res)
            if not res:
                return render_template("sign_up.html", info="Error occurred, could not sign up")
            new_id = res[0][0]

            # Insert user into Buyer or Seller table accordingly
            if request.args.get('account-type') == 'buyer':
                new_buyer_vals = '{}, "{}", "{}"'.format(
                    new_id,
                    request.args.get('shipping-address'),
                    request.args.get('city')
                )
                statement = (f'INSERT INTO Buyer (BuyerID, Address, City)\n'
                             f'    VALUES ({new_buyer_vals});')
                database.db.session.execute(text(statement))
            elif request.args.get('account-type') == 'seller':
                new_seller_vals = '{}, "{}", "{}"'.format(
                    new_id,
                    request.args.get('account-num'),
                    request.args.get('routing-num')
                )
                statement = (f'INSERT INTO Seller (SellerID, AccountNum, RoutingNum)\n'
                             f'    VALUES ({new_seller_vals});')
                database.db.session.execute(text(statement))
            elif request.args.get('account-type') == 'admin':
                statement = (f'INSERT INTO Admin (AdminID)\n'
                             f'    VALUES ({new_id});')
                database.db.session.execute(text(statement))

            # Set session variables accordingly
            session['login.id'] = str(new_id)
            session['login.type'] = request.args.get('account-type')
            session['login.name'] = request.args.get('name')
            session['login.password'] = request.args.get('password')

            # Commit changes to database
            database.db.session.commit()

            return render_template("sign_up_success.html")
        else:
            return render_template("sign_up.html")
    else:
        return redirect(url_for('auth.signUp'))
