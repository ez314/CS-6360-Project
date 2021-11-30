from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy import column, text

from website import database

sell = Blueprint('sell', __name__)

@sell.route('/sell')
def sellForm():


        if request.method == 'GET':


            if all(x in request.args for x in ['name','desc', 'pic', 'sbid','bidinc','sdate','edate']):
                # All args passed, create new user in database
                new_item_vals = 'DEFAULT, "{}", "{}", "{}", {}, {},"{}","{}",{}'.format(

                    request.args.get('name'),
                    request.args.get('desc'),
                    request.args.get('pic'),
                    request.args.get('sbid'),
                    request.args.get('bidinc'),
                    request.args.get('sdate'),
                    request.args.get('edate'),
                    session['login.id']
                )
                statement = (f'INSERT INTO Item (ItemID, Name, Description, Photo, StartingBid, BidIncrement,StartDate,EndDate,SellerID)\n'
                             f'    VALUES ({new_item_vals});')
                database.db.session.execute(text(statement))

                # Fetch ID of inserted item. Must do this because of autoincrement
                res = database.db.session.execute(text('SELECT LAST_INSERT_ID();')).all()
                print(res)
                if not res:
                    return render_template("sell.html", info="Error occurred, could not sell the item")
                new_id = res[0][0]


                database.db.session.commit()

                return redirect(f"/product/{new_id}")
            else:
                return render_template("sell.html")
        else:
            return redirect(url_for('sell.sellForm'))
