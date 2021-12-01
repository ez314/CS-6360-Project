import statistics

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import column, text

from website import database
from website.util import get_account_type

profile = Blueprint('profile', __name__)


@profile.route('/profile/<int:userId>')
def view_profile(userId):
    userId = str(userId)
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

        # Determine feedback stats
        feedback = gather_user_feedback(userId, user_account_type)

        user = {
            'id': str(userId),
            'name': res[0][0],
            'email': res[0][1],
            'phone': res[0][2],
            'type': user_account_type.capitalize(),
            'num_transactions': len(feedback),
            'avg_rating': f'{statistics.mean([x[0] for x in feedback]):.2f}' if feedback else 'N/A',
            'comments': [x[1:] for x in feedback]
        }

        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('views.home'))


@profile.route('/edit_profile/<int:userId>')
def edit_profile(userId):
    userId = str(userId)
    # Verify the user is allowed to edit
    if session['login.id'] != userId and session['login.type'] != 'admin':
        return render_template("error.html", error="You are not allowed to edit this profile.")

    if request.method == 'GET':
        if all(x in request.args for x in ['email', 'phone', 'address', 'edit-password']):
            # Ensure the password matches
            if not request.args.get('edit-password') == session['login.password']:
                return render_template("edit_profile.html", user=gather_user_attributes_editable(userId),
                                       info="Password not accepted. Please enter the password for the account you are currently logged into.")
            # Set new User table values
            update_user_vals = 'Email="{}", PhoneNum="{}", HomeAddr="{}"'.format(
                request.args.get('email'),
                request.args.get('phone'),
                request.args.get('address')
            )
            database.db.session.execute(
                text(f'Update User SET {update_user_vals} WHERE UserID = {userId};'))

            # Set new Buyer or Seller table values, if applicable
            user_account_type = get_account_type(userId)
            if user_account_type == 'buyer':
                update_buyer_vals = 'Address="{}", City="{}"'.format(
                    request.args.get('shipping-address'),
                    request.args.get('city')
                )
                database.db.session.execute(
                    text(f'Update Buyer SET {update_buyer_vals} WHERE BuyerID = {userId};'))
            elif user_account_type == 'seller':
                update_seller_vals = 'AccountNum="{}", RoutingNum="{}"'.format(
                    request.args.get('account-num'),
                    request.args.get('routing-num')
                )
                database.db.session.execute(
                    text(f'Update Seller SET {update_seller_vals} WHERE SellerID = {userId};'))

            # Commit changes to database
            database.db.session.commit()

            return redirect(url_for('profile.view_profile', userId=userId))
        else:
            user = gather_user_attributes_editable(userId)

            if user is None:
                return render_template("error.html", error="That user could not be found.")

            return render_template("edit_profile.html", user=user)
    else:
        return redirect(url_for('views.home'))


def gather_user_attributes_editable(userId):
    # Find user, if it exists
    res = database.db.session.execute(
        text(f'SELECT Name, Email, PhoneNum, HomeAddr FROM User where UserID = {userId}')).all()
    if not res:
        return None

    # Define user attributes
    user = {
        'id-noedit': str(userId),
        'name-noedit': res[0][0],
        'email': res[0][1],
        'phone': res[0][2],
        'address': res[0][3]
    }

    # Determine account type if buyer or seller, and add values accordingly
    buyerData = database.db.session.execute(
        text(f'SELECT Address, City FROM Buyer where BuyerID = {userId}')).all()
    if buyerData:
        user['shipping-address'], user['city'] = buyerData[0]
        user['type-noedit'] = 'buyer'
    else:
        sellerRes = database.db.session.execute(
            text(f'SELECT AccountNum, RoutingNum FROM Seller where SellerID = {userId}')).all()
        if sellerRes:
            user['account-num'], user['routing-num'] = sellerRes[0]
            user['type-noedit'] = 'seller'
        else:
            user['type-noedit'] = 'unknown-or-admin'

    return user


def gather_user_feedback(userId, type):
    # Find all relevant entries in the database
    if type == 'buyer':
        return database.db.session.execute(
            text(f'SELECT BuyerFeedback, BuyerComment, Item.ItemID, Item.Name'
                 f'  FROM Item, Buys '
                 f'  WHERE Item.ItemID = Buys.ItemID AND Buys.BuyerID = {userId}'
                 )).all()
    elif type == 'seller':
        return database.db.session.execute(
            text(f'SELECT SellerFeedback, SellerComment, Item.ItemID, Item.Name'
                 f'  FROM Item, Buys '
                 f'  WHERE Item.ItemID = Buys.ItemID AND Item.SellerID = {userId}'
                 )).all()
    else:
        return []
