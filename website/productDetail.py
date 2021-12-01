from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy.sql.elements import Null
from website import database
from sqlalchemy import column, text
from datetime import datetime

prodDetail = Blueprint('prodDetail', __name__)

"""
Logic For Feedback : 
1.  EndDate of current product should be less than current date, 
    1.1     Current User should be either Seller or Buyer with highest Bid and there shouldn't be any comment for this
            current user for current item in Buys Table.(This would mean that the current user has already given the feedback).


"""
@prodDetail.route('/product/<int:itemId>', methods=['GET', 'POST'])
def product_Detail(itemId):
    if request.method == 'GET':
        #Get product Details for this itemID.
        try: 
            statement = (f'SELECT * FROM ONLINE_AUCTION.Item WHERE ItemID = { itemId };')
            prod_query = database.db.session.execute(text(statement)).all()
        except:
            print("Product Doesn't Exists!!")
            return redirect('/')
        
        #If product for this exist.
        if prod_query: 
            for item in prod_query: #this result of query is a list, converting to named tuple.
                prod_details = item._asdict()
            
            if not int(prod_details['IsActive']): #If current product is inactive.
                flash("Product is Currently Inactive", category='error')
                return render_template("product_detail.html", prod  = prod_details)

            #Getting seller details for this itemID.
            s_id = prod_details['SellerID']
            statement = (f'SELECT * FROM ONLINE_AUCTION.V_Sellers WHERE SellerID = { s_id };')
            seller_query = database.db.session.execute(text(statement)).all()
            
            if len(seller_query):
                for item in seller_query:
                    seller_details = item._asdict()
            else:
                statement = (f'SELECT * FROM ONLINE_AUCTION.User WHERE UserID = { s_id };')
                seller_query = database.db.session.execute(text(statement)).all()
                for item in seller_query:
                    seller_details = item._asdict()

            
            #Getting list of all bidders for this item.
            statement = (f'SELECT * FROM ONLINE_AUCTION.Bids_for WHERE ItemID = { itemId };')
            bidders_query = database.db.session.execute(text(statement)).all()
            list_bidders = []
            for item in bidders_query:
                list_bidders.append(item._asdict())

            #Get the highest bid.
            statement = (f'SELECT HighestBid FROM ONLINE_AUCTION.V_Highest_Bids WHERE ItemID = { itemId };')
            highest_bid_query = database.db.session.execute(text(statement)).all()
            
            if len(highest_bid_query):
                for item in highest_bid_query:
                    highest_bid = item._asdict()
            else:
                highest_bid = {'HighestBid' : prod_details['StartingBid']}
            
            if prod_details['StartDate'] > datetime.now():
                if prod_details['Photo']:
                        prod_details['Photo'] = prod_details['Photo'].decode("utf-8")
                return render_template("product_detail.html", prod  = prod_details, seller = seller_details, bidderList = list_bidders, highestBid = highest_bid, is_Feedback = False, is_active = False)
                
            if prod_details['EndDate'] < datetime.now(): #Since Bid time is over, we would check if there is any feedback or not.
                statement = (f'SELECT * FROM V_Highest_Bid_Details WHERE ItemID = { itemId };')
                buyer_seller_query = database.db.session.execute(text(statement)).all()
                if len(buyer_seller_query):
                    for item in buyer_seller_query:
                        buyer_seller_details = item._asdict()
                else:
                    if prod_details['Photo']:
                        prod_details['Photo'] = prod_details['Photo'].decode("utf-8")
                    return render_template("product_detail.html", prod  = prod_details, seller = seller_details, bidderList = list_bidders, highestBid = highest_bid, is_Feedback = False, is_active = False)
                
                #check if it is buyer's account or seller's account. 
                user_id = session['login.id']
                user_id = int(user_id)
                is_current_user_buyer = False
                if user_id == buyer_seller_details['BuyerID']:
                    is_current_user_buyer = True
                
                #For a feedback, current user should be either Seller or Highest Bidder.
                if user_id == buyer_seller_details['BuyerID'] or user_id == buyer_seller_details['SellerID']:
                    is_Feedback = True
                    b_id = buyer_seller_details['BuyerID']
                    s_id = buyer_seller_details['SellerID']

                    #Query to check if current user has already given the feedback
                    statement = (f'SELECT * FROM ONLINE_AUCTION.Buys WHERE ItemID = { itemId } AND BuyerID={b_id};')
                    check_feedback_query = database.db.session.execute(text(statement)).all()
                    if len(check_feedback_query):
                        for item in check_feedback_query:
                            check_feedback = item._asdict()
            
                        if not((user_id == b_id and check_feedback['SellerComment'] == 'None') or (user_id == s_id and check_feedback['BuyerComment'] == 'None')):
                            is_Feedback = False
                        else:
                            is_Feedback = True

                    if prod_details['Photo']:
                        prod_details['Photo'] = prod_details['Photo'].decode("utf-8")
                    return render_template("product_detail.html", prod  = prod_details, seller=seller_details, bid_details = buyer_seller_details, is_buyer = is_current_user_buyer, is_Feedback = is_Feedback, highestBid = highest_bid, bidderList = list_bidders, is_active=False)
            
            
            #Converting image src as this is stored byte string. Converting to string. 
            if prod_details['Photo']:
                prod_details['Photo'] = prod_details['Photo'].decode("utf-8")
            
            return render_template("product_detail.html", prod  = prod_details, seller = seller_details, bidderList = list_bidders, highestBid = highest_bid, is_Feedback = False, is_active = True)
        else:
            return redirect('/')
    else:
        #Need to get session id of the current logged in User.
        user_id = session['login.id']
        statement = (f'SELECT BuyerID FROM ONLINE_AUCTION.Buyer WHERE BuyerID = { user_id };')
        user_query = database.db.session.execute(text(statement)).all()
        if not user_query:
            flash("Current Logged in account not a Buyer!", category='error')
            return redirect(url_for('prodDetail.product_Detail', itemId=itemId))
        try:
            new_bid_vals = '"{}", "{}", "{}", "{}"'.format(
                    itemId,
                    session['login.id'],
                    datetime.now(),
                    request.values.get('bidValue')
                )
            statement = (f'INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)\n'
                            f'    VALUES ({new_bid_vals});')
            database.db.session.execute(text(statement))
            database.db.session.commit()
        except:
            flash("Couldn't write to Database!", category='error')
            return redirect(url_for('prodDetail.product_Detail', itemId=itemId))

        flash("Congrats on your new Bid!", category='success')
        return redirect(url_for('prodDetail.product_Detail', itemId=itemId))



@prodDetail.route('/feedback/<int:SellerID>/<int:BuyerID>/<int:ItemID>', methods=['POST'])
def feedback(SellerID, BuyerID, ItemID):
    statement = (f'SELECT * FROM ONLINE_AUCTION.Buys WHERE ItemID = { ItemID } AND BuyerID = { BuyerID };')
    check_query = database.db.session.execute(text(statement)).all()
    b_c = request.values.get('buyer_comment')
    b_f = request.values.get('buyer_rating')
    s_c = request.values.get('seller_comment')
    s_f = request.values.get('seller_rating')
    user_id = session['login.id']
    if check_query:
        for item in check_query:
            check_details = item._asdict()
        
        if int(user_id) == SellerID:
            statement = (f'UPDATE Buys SET BuyerFeedback = { b_f }, BuyerComment = "{ b_c}" WHERE BuyerID = {BuyerID} AND ItemID = {ItemID};')
        else:
            statement = (f'UPDATE Buys SET SellerComment = "{ s_c }", SellerFeedback={s_f} WHERE ItemID = { ItemID } AND BuyerID = { BuyerID };')
    else:
        if not b_f:
            b_f = 0
        if not s_f:
            s_f = 0
        new_bid_vals = '"{}", "{}", "{}", "{}", "{}", "{}"'.format(
                    ItemID,
                    BuyerID,
                    s_c,
                    s_f,
                    b_c, 
                    b_f
                )
        statement = (f'INSERT INTO Buys (ItemID, BuyerID, SellerComment, SellerFeedback, BuyerComment, BuyerFeedback)\n'
                            f'    VALUES ({new_bid_vals});')

    database.db.session.execute(text(statement))
    database.db.session.commit()
    return redirect(url_for('prodDetail.product_Detail', itemId=ItemID))

