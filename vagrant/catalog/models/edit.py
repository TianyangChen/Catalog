from flask import Blueprint
edit = Blueprint('edit', __name__)

import sys
sys.path.append("..")
from application import *
# edit on item


@edit.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    """
    Edit an existing item in database

    First, check whether user has login, if not, redirect to the index page.
    Second, check whether current user has permission to delete this item.
    Third, check the method. If method is 'GET', show the form to edit item; if method is 'POST', before update the database, check whether its name is empty and whether it has already exist.
    """
    if 'username' not in login_session:
        return redirect('/')
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    if item.user_id != login_session['user_id']:
        return jsonify({"error": "Permission denied, you cannot edit this item."})
    if request.method == 'POST':
        edited_item_name = request.form['name'].strip()
        # the item name should not be empty
        if edited_item_name == None or edited_item_name == "":
            flash("Item name should not be empty!")
            return redirect(url_for('edit.edit_item', item_name=item_name))
        # because name is the primary key, check whether this new name is
        # already in the database
        exist_item = session.query(CategoryItem).filter_by(
            name=edited_item_name).all()
        if len(exist_item) > 0 and edited_item_name != item_name:
            flash("Cannot add " + edited_item_name +
                  ", this item has already exist.")
            return redirect(url_for('edit.edit_item', item_name=item_name))
        edited_item = session.query(
            CategoryItem).filter_by(name=item_name).one()
        edited_item.name = edited_item_name
        edited_item.description = request.form['description']
        edited_item.category_id = request.form['category']
        return redirect('/')
    else:
        edited_item = session.query(
            CategoryItem).filter_by(name=item_name).one()
        categories = session.query(Category).all()
        return render_template('edit_login.html', item=edited_item, user_name=login_session['username'], categories=categories)
