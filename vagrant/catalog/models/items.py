from flask import Blueprint
items = Blueprint('items', __name__)

import sys
sys.path.append("..")

from application import *
# show all the items belong to category_name


@items.route('/catalog/<string:category_name>/items')
def show_items(category_name):
    """
    Display all the items belong to category_name and the number of items belong to this category.

    If user has login, show the page with user name.
    """
    categories = session.query(Category).all()
    items = session.query(CategoryItem).filter_by(
        category_id=category_name).all()
    num_items = len(items)
    if 'username' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state
        return render_template('items.html', items=items, categories=categories, category_name=category_name, num_items=num_items, STATE=state)
    else:
        return render_template('items_login.html', items=items, categories=categories, category_name=category_name, num_items=num_items, user_name=login_session['username'])
