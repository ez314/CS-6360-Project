from flask import Blueprint, render_template, request, redirect, url_for

prodDetail = Blueprint('prodDetail', __name__)


@prodDetail.route('/product/<int:itemId>', methods=['GET', 'POST'])
def product_Detail(itemId):
    if request.method == 'GET':
        seller = {'Name':'Utsav', 'rating': 5 }
        prod = {'ItemID': itemId, 'Name' : 'Watch', 
                'Description': 'Hello this is just a trial Product', 
                'StartingBid': 100, 'BidIncrement': 3, 'StartDate': '2021-05-20', 
                'EndDate' : '2021-12-05'}
        bidderList = [{'BuyerID':101, 'BiddingTime':'2021-05-09', 'Price':218},  
                    {'BuyerID':211, 'BiddingTime':'2021-05-09', 'Price':115},
                    {'BuyerID':899, 'BiddingTime':'2021-05-09', 'Price':112},
                    {'BuyerID':101, 'BiddingTime':'2021-05-09', 'Price':109},
                    {'BuyerID':787, 'BiddingTime':'2021-05-09', 'Price':106},
                    {'BuyerID':999, 'BiddingTime':'2021-05-09', 'Price':103},
                    ]
        highestBid = 218
        sellerRating = 3
        return render_template("product_detail.html", prod  = prod, seller = seller, bidderList = bidderList, highestBid = highestBid, sellerRating = sellerRating)
    else:
        print("Post")
        return redirect(url_for('prodDetail.product_Detail', itemId=itemId))
        

