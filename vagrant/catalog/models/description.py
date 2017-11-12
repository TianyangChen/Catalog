from flask import Blueprint
description = Blueprint('description', __name__)

import sys
sys.path.append("..")
from application import *
# show the description of item_name


@description.route('/catalog/<string:category_name>/<string:item_name>')
def show_description(category_name, item_name):
    """
    Show the description of an item.

    First, check whether user has login
    Second, check whether current user has permission to edit or delete this item, if not, show the page without these two buttons
    """
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    if 'username' not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase +
                                      string.digits) for x in xrange(32))
        login_session['state'] = state
        return render_template('description.html', item=item, STATE=state)
    elif item.user_id != login_session['user_id']:
        return render_template('description_login_ban.html', item=item, user_name=login_session['username'])
    else:
        return render_template('description_login.html', item=item, user_name=login_session['username'])
