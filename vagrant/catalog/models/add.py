from flask import Blueprint
add = Blueprint('add', __name__)

import sys
sys.path.append("..")
from application import *
# add a new item


@add.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Add a new item to database.

    First, check whether user has login, if not, redirect to the index page.
    Second, check the method. If method is 'GET', show form to add item.
    Third, if method is 'POST', before add it to the database, check whether its name is empty and whether it has already exist.
    """
    if 'username' not in login_session:
        return redirect('/')
    elif request.method == 'POST':
        categories = session.query(Category).all()
        item_name = request.form['name'].strip()
        # the item name should not be empty
        if item_name == None or item_name == "":
            flash("Item name should not be empty!")
            return redirect('/add')
        # because name is the primary key, check whether this new item is
        # already in the database
        exist_item = session.query(
            CategoryItem).filter_by(name=item_name).all()
        if len(exist_item) > 0:
            flash("Cannot add " + item_name + ", this item has already exist.")
            return redirect('/add')
        new_item = CategoryItem(name=item_name, description=request.form[
                                'description'], category_id=request.form['category'], user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        return redirect('/')
    else:
        categories = session.query(Category).all()
        return render_template('add_login.html', categories=categories, user_name=login_session['username'])
