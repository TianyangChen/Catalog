from flask import Blueprint
delete = Blueprint('delete', __name__)

import sys
sys.path.append("..")
from application import *
# Delete an item


@delete.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    """
    Delete an item from database

    First, check whether user has login, if not, redirect to the index page.
    Second, check whether current user has permission to delete this item.
    Third, check the method. If method is 'GET', ask user for double check; if method is 'POST', delete it.
    """
    if 'username' not in login_session:
        return redirect('/')
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    if item.user_id != login_session['user_id']:
        return jsonify({"error": "Permission denied, you cannot delete this item."})
    if request.method == 'POST':
        item_delete = session.query(
            CategoryItem).filter_by(name=item_name).one()
        session.delete(item_delete)
        session.commit()
        return redirect('/')
    else:
        item_delete = session.query(
            CategoryItem).filter_by(name=item_name).one()
        return render_template('delete_login.html', item=item_delete, user_name=login_session['username'])
