from flask import Blueprint
jsonapi = Blueprint('jsonapi', __name__)

import sys
sys.path.append("..")

from application import *
# return all items in json format


@jsonapi.route('/catalog.json')
def show_json():
    """
    Return all items in json format, group by category
    """
    categories = session.query(Category).all()
    all_data = {"category": []}
    for category in categories:
        category_dic = {"name": category.name}
        items = session.query(CategoryItem).filter_by(
            category_id=category.name).all()
        category_dic["items"] = [item.serialize for item in items]
        all_data["category"].append(category_dic)
    return jsonify(all_data)
