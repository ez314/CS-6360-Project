from flask import Blueprint, render_template
auth = Blueprint('auth', __name__)


@auth.route('/login_seller')
def login_Seller():
    return render_template("login_seller.html")


@auth.route('/login_buyer')
def login_Buyer():
    return render_template("login_buyer.html")


@auth.route('/logout')
def logout():
    return "<h1> Logout </h1>"
    
@auth.route('/sign_up_seller')
def signUpSeller():
    return render_template("sign_up_seller.html")

   
@auth.route('/sign_up_buyer')
def signUpBuyer():
    return render_template("sign_up_buyer.html")
