from flask import Blueprint, render_template, request, redirect, url_for, session
from website import database
from sqlalchemy import column, text

prodDetail = Blueprint('prodDetail', __name__)

@prodDetail.route('/product/<int:itemId>', methods=['GET', 'POST'])
def product_Detail(itemId):
    if request.method == 'GET':
        #Get product Details for this itemID. 
        statement = (f'SELECT * FROM ONLINE_AUCTION.Item WHERE ItemID = { itemId };')
        prod_query = database.db.session.execute(text(statement)).all()
        if prod_query: 
            for item in prod_query: #this result of query is a list, converting to named tuple.
                prod_details = item._asdict()

            #Getting seller details for this itemID.
            seller_query = database.db.session.query(column('SellerID'), column('Name'), column('Feedback')).from_statement(text(f'SELECT * FROM ONLINE_AUCTION.V_Sellers where SellerID = 2')).all()
            for item in seller_query:
                seller_details = item._asdict()

            #Getting list of all bidders for this item.
            statement = (f'SELECT * FROM ONLINE_AUCTION.Bids_for WHERE ItemID = { itemId };')
            bidders_query = database.db.session.execute(text(statement)).all()
            list_bidders = []
            for item in bidders_query:
                list_bidders.append(item._asdict())

            #Get the highest bid.
            statement = (f'SELECT HighestBid FROM ONLINE_AUCTION.V_Highest_Bid WHERE ItemID = { itemId };')
            highest_bid_query = database.db.session.execute(text(statement)).all()
            
            if highest_bid_query:
                for item in highest_bid_query:
                    highest_bid = item._asdict()
            else:
                highest_bid = {'HighestBid' : prod_details['StartingBid']}
            print(highest_bid)
            
            #Converting image src as this is stored byte string. Converting to string. 
            if prod_details['Photo']:
                prod_details['Photo'] = prod_details['Photo'].decode("utf-8")
            return render_template("product_detail.html", prod  = prod_details, seller = seller_details, bidderList = list_bidders, highestBid = highest_bid)
    else:
        print("Post")
        print(request.values.get('bidValue'))
        #Need to get session id of the current logged in User.
        #Do we need to check that if current user is buyer or seller?

        new_bid_vals = '"{}", "{}", "{}", "{}"'.format(
                itemId,
                7,
                "2021-11-13",
                request.values.get('bidValue')
            )
        statement = (f'INSERT INTO Bids_for (ItemID, BuyerID, BiddingTime, Price)\n'
                        f'    VALUES ({new_bid_vals});')
        database.db.session.execute(text(statement))
        database.db.session.commit()

        return redirect(url_for('prodDetail.product_Detail', itemId=itemId))
        

