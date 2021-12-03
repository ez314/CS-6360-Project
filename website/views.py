from flask import Blueprint, render_template, redirect, session, url_for, request
from website import database
from sqlalchemy import column, text

views = Blueprint('views', __name__)


@views.route('/')
def home():
    # # Redirect to login if not already logged in
    # if 'login.id' not in session:
    #     return redirect(url_for('auth.login'))
    statement = (f'SELECT * FROM Category;')
    category_query = database.db.session.execute(text(statement)).all()
    categories = []
    if category_query:
        for item in category_query:
            #categories_details = item._asdict()
            categories.append(item['Name'])
    print(categories)
    return render_template("home.html", categories = categories)


@views.route('/adminHome')
def adminHome():
    # Get the queries for the tables done
    userStatement = (f'SELECT * FROM ONLINE_AUCTION.User;')
    itemStatement = (f'SELECT * FROM ONLINE_AUCTION.Item;')

    userQuery = database.db.session.execute(text(userStatement)).all()
    itemQuery = database.db.session.execute(text(itemStatement)).all()

    # The tuples for passing the date to html
    # Turn the queries into tuples
    userData = tuple(userQuery)
    itemData = tuple(itemQuery)

    userHeadings = ("ID", "Name", "Email", "Password", "Phone Num", "Home Address", "Is Active")
    itemHeadings = ("ID", "Name", "Description", "Photo", "Starting Bid", "Bid Increment", "Start Date", "End Date")

    return render_template("adminHome.html", userHeadings=userHeadings, itemHeadings=itemHeadings, userData=userData, itemData=itemData)

@views.route('/adminDeleteUserPage', methods=['GET', 'POST'])
def adminDeleteUserPage():
    # Get the queries for the tables done
    userStatement = (f'SELECT * FROM ONLINE_AUCTION.User;')

    userQuery = database.db.session.execute(text(userStatement)).all()

    # The tuples for passing the date to html
    # Turn the queries into tuples
    userData = tuple(userQuery)

    userHeadings = ("ID", "Name", "Description", "Photo", "Starting Bid", "Bid Increment", "Start Date", "End Date")

    if request.method == "POST":
        try:
            if request.form['id']:
                user_id = request.values.get('id')
                user_id = int(user_id)
                statement = (f'UPDATE ONLINE_AUCTION.User SET IsActive = 0 WHERE UserID={ user_id };')
                database.db.session.execute(text(statement))
                database.db.session.commit()

                # Redo query for users to show that user has been successfully deleted
                userQuery = database.db.session.execute(text(userStatement)).all()

                # The tuples for passing the date to html
                # Turn the queries into tuples
                userData = tuple(userQuery)

                return render_template("adminDeleteUserPage.html", userHeadings=userHeadings, userData=userData, info="Successfully Deleted user")

            else:
                return render_template("adminDeleteUserPage.html", userHeadings=userHeadings, userData=userData)

        except Exception as e:
            print(e)
            return render_template("adminDeleteUserPage.html", userHeadings=userHeadings, userData=userData, info="Failed to Delete user")

    # Simply render the page
    if request.method == "GET":
        return render_template("adminDeleteUserPage.html", userHeadings=userHeadings, userData=userData, info="No Entered Item")

@views.route('/adminDeleteItemPage', methods=['GET', 'POST'])
def adminDeleteItemPage():
    # Get the queries for the tables done
    itemStatement = (f'SELECT * FROM ONLINE_AUCTION.Item;')

    itemQuery = database.db.session.execute(text(itemStatement)).all()

    # The tuples for passing the date to html
    # Turn the queries into tuples
    itemData = tuple(itemQuery)

    itemHeadings = ("ID", "Name", "Description", "Photo", "Starting Bid", "Bid Increment", "Start Date", "End Date")

    if request.method == "POST":
        try:
            if request.form['id']:
                user_id = request.values.get('id')
                user_id = int(user_id)
                statement = (f'DELETE FROM ONLINE_AUCTION.Item WHERE ItemID = {user_id};')
                database.db.session.execute(text(statement))
                database.db.session.commit()

                # Redo query for items to show that item has been successfully deleted
                itemQuery = database.db.session.execute(text(itemStatement)).all()

                # The tuples for passing the date to html
                # Turn the queries into tuples
                itemData = tuple(itemQuery)

                return render_template("adminDeleteItemPage.html", itemHeadings=itemHeadings, itemData=itemData, info="Successfully Deleted item")

            else:
                return render_template("adminDeleteItemPage.html", itemHeadings=itemHeadings, itemData=itemData, info="No Entered Item")

        except Exception as e:
            print(e)
            return render_template("adminDeleteItemPage.html", itemHeadings=itemHeadings, itemData=itemData, info="Failed to Delete item")

    # Simply render the page
    if request.method == "GET":
        return render_template("adminDeleteItemPage.html", itemHeadings=itemHeadings, itemData=itemData)
