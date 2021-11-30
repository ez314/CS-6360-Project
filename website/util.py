from sqlalchemy import text

from website import database


def get_account_type(userId):
    # Determine account type
    if database.db.session.execute(
            text(f'SELECT * FROM Buyer where BuyerID = {userId}')).rowcount > 0:
        return 'buyer'
    elif database.db.session.execute(
            text(f'SELECT * FROM Seller where SellerID = {userId}')).rowcount > 0:
        return 'seller'
    elif database.db.session.execute(
            text(f'SELECT * FROM Admin where AdminID = {userId}')).rowcount > 0:
        return 'admin'
