from flask import Blueprint
index = Blueprint('index', __name__)

import sys
sys.path.append("..")
from application import *


# show all categories and 10 recently added items
@index.route('/')
def show_index():
    """
    Display the index page with all categories and 10 recently added items.

    If user has login, show the page with user name.
    """
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()[::-1]
    if len(items) > 10:
        items = items[:10]
    else:
        pass
    if 'username' in login_session:
        return render_template('index_login.html', categories=categories, items=items, user_name=login_session['username'])
    else:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state
        return render_template('index.html', categories=categories, items=items, STATE=state)
