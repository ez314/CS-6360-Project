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

# search the child category
# User enters parent category, we also send child category
# we do this by using the Parent category to get a list of child categories.
'''
SELECT Category.CategoryID
FROM Category
WHERE {{prod_query}} = Category.CategoryID
'''
# This gets a list of all descendents. I think
'''
;WITH Category AS
(
    SELECT Category.Categoryid,
            Category.ParentCategoryid
    FROM Category
    WHERE 1 = Category.Categoryid
    UNION ALL
    SELECT t.categoryid, t.ParentCategoryid
    FROM Category t
        INNER JOIN Category r ON r.Categoryid = t.ParentCategoryid
)
SELECT *
FROM Category;
'''


'''https://www.w3schools.com/howto/howto_js_sort_table.asp'''

@searchCategory.route('/search/', methods=['GET', 'POST'])
def search_Category():
    query_item = request.args.get('query') # name of the item
    query_category = request.args.get('category') # name of the category
    print(query_item)
    print(query_category)
    if request.method == 'GET':
        # get CategoryName
        categoryName = query_category
        # get categoryID
        statement = (f'SELECT CategoryID FROM ONLINE_AUCTION.Category WHERE ONLINE_AUCTION.Category.Name = "{query_category}" ;')
        categoryID = database.db.session.execute(text(statement)).all()
        if len(categoryID) == 0:
            categoryID = 10
        else:
            categoryID = categoryID[0][0]
        print(categoryID)

        # Worry about this later actually.-----------------------------
        # get child categoriesID
        '''statement = (fWITH Category AS
            (
                SELECT Category.Categoryid,
                        Category.ParentCategoryid
                FROM Category
                WHERE {categoryID[0][0]} = Category.Categoryid
                UNION ALL
                SELECT t.categoryid, t.ParentCategoryid
                FROM Category t
                    INNER JOIN Category r ON r.Categoryid = t.ParentCategoryid
            )
            SELECT *
            FROM Category;)
        
        childCategoriesID = database.db.session.execute(text(statement)).all()
        print("asdf")
        print(childCategoriesID)
        # Trim the tuples from size 2 to size 1.
        for i, tup in enumerate(childCategoriesID):
            listx = list(tup)
            listx.pop()
            childCategoriesID[i] = tuple(listx)
        print(childCategoriesID)
        '''
        # ------------------------------------------------

        # item_List = []
        # if prod_query:
        #     for item in prod_query:
        #         item_List.append(item._asdict())

        # # get ItemID
        # statement = (f'SELECT Item.ItemID FROM Item, Category, belongs_to WHERE Category.Name = "{prod_query}" and Category.CategoryID = belongs_to.CategoryID and belongs_to.ItemID = Item.ItemID and Item.EndDate > CURRENT_DATE() and Item.IsActive Group by Item.ItemID ORDER BY Item.EndDate;')
        # ItemID = database.db.session.execute(text(statement)).all()
        # #print(ItemID)

        print(query_item)
        # get Item Tuple
        if categoryName == 'All':
            statement= (f'''SELECT Item.ItemID, Item.Name, Item.Description, Item.Photo, Item.StartingBid, Item.BidIncrement,
                Item.StartDate, Item.EndDate, Item.SellerID
                FROM Item
                WHERE (lower(Item.name) LIKE lower("%{query_item}%") OR lower(Item.description) LIKE lower("%{query_item}%")) and Item.EndDate > CURRENT_DATE() and Item.IsActive
                Group by Item.ItemID
                ORDER BY Item.EndDate;
                ''')
        else:
            statement = (f'''SELECT Item.ItemID, Item.Name, Item.Description, Item.Photo, Item.StartingBid, Item.BidIncrement, 
                Item.StartDate, Item.EndDate, Item.SellerID
                FROM Item, Belongs_to, Category
                WHERE Category.Name = "{categoryName}" and Category.CategoryID = Belongs_to.CategoryID and Belongs_to.ItemID = Item.ItemID
                and Item.EndDate > CURRENT_DATE() and Item.IsActive
                Group by Item.ItemID
                ORDER BY Item.EndDate;''')
        ItemTuple = database.db.session.execute(text(statement)).all()
        print(ItemTuple)

        

        #render template
        return render_template("search_category.html", categoryName=categoryName, categoryID=categoryID ,ItemTuple = ItemTuple )
    else:
        pass