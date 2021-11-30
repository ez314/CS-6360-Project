from flask import Blueprint, render_template, request, redirect, url_for, session
from website import database
from sqlalchemy import column, text

searchCategory = Blueprint('searchCategory', __name__)

# categories Electronics, Phone, Good Stuff

#select items 
select = '''
SELECT Item.ItemID, Item.Name, Item.Description, Item.Photo, Item.StartingBid, Item.BidIncrement, 
Item.StartDate, Item.EndDate, Item.SellerID,
    CASE WHEN MAX(CASE WHEN Bids_for.price is NULL THEN 1 ELSE 0 END) = 0
        THEN MAX(Bids_for.price)
    END
FROM Item, Bids_for, Belongs_to, Category
WHERE Category.CategoryID = Belongs_to.CategoryID and Belongs_to.ItemID = Item.ItemID and
Item.ItemID = Bids_for.ItemID and Item.EndDate > CURRENT_DATE() and Item.IsActive
Group by Item.ItemID
ORDER BY Item.EndDate;
'''

'''
SELECT Item.ItemID, Item.Name, Item.Description, Item.Photo, Item.StartingBid, Item.BidIncrement, 
Item.StartDate, Item.EndDate, Item.SellerID
FROM Item, Belongs_to, Category
WHERE Category.CategoryID = Belongs_to.CategoryID and Belongs_to.ItemID = Item.ItemID
and Item.EndDate > CURRENT_DATE() and Item.IsActive
Group by Item.ItemID
ORDER BY Item.EndDate;
'''
#/search/?search_item=Phone



@searchCategory.route('/search/', methods=['GET', 'POST'])
def search_Category():
    prod_query = request.args.get('search_item')
    print(prod_query)
    if request.method == 'GET':
        # get CategoryName
        categoryName = prod_query
        # get categoryID
        statement = (f'SELECT CategoryID FROM ONLINE_AUCTION.Category WHERE ONLINE_AUCTION.Category.Name = "{prod_query}" ;')
        categoryID = database.db.session.execute(text(statement)).all()
        print(categoryID)

        # item_List = []
        # if prod_query:
        #     for item in prod_query:
        #         item_List.append(item._asdict())

        # # get ItemID
        # statement = (f'SELECT Item.ItemID FROM Item, Category, belongs_to WHERE Category.Name = "{prod_query}" and Category.CategoryID = belongs_to.CategoryID and belongs_to.ItemID = Item.ItemID and Item.EndDate > CURRENT_DATE() and Item.IsActive Group by Item.ItemID ORDER BY Item.EndDate;')
        # ItemID = database.db.session.execute(text(statement)).all()
        # #print(ItemID)

        # get Item Tuple
        statement = (f'''SELECT Item.ItemID, Item.Name, Item.Description, Item.Photo, Item.StartingBid, Item.BidIncrement, 
            Item.StartDate, Item.EndDate, Item.SellerID
            FROM Item, Belongs_to, Category
            WHERE Category.Name = "{prod_query}" and Category.CategoryID = Belongs_to.CategoryID and Belongs_to.ItemID = Item.ItemID
            and Item.EndDate > CURRENT_DATE() and Item.IsActive
            Group by Item.ItemID
            ORDER BY Item.EndDate;''')
        ItemTuple = database.db.session.execute(text(statement)).all()
        print(ItemTuple)

        # get Item Description

        # get Item Photo

        # get Item StartingBid

        # get Item Bid Increment

        # get Item Highest Bid

        # get Item StartDate

        # get Item EndDate

        # get Item Seller ID

        #render template
        return render_template("search_category.html", categoryName=categoryName, categoryID=categoryID[0][0], ItemTuple = ItemTuple )
    else:
        pass