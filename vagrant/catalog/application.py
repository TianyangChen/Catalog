from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# show all categories and 10 recently added items


@app.route('/')
def show_index():
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

# show all the items belong to category_name


@app.route('/catalog/<string:category_name>/items')
def show_items(category_name):
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

# show the description of item_name


@app.route('/catalog/<string:category_name>/<string:item_name>')
def show_description(category_name, item_name):
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

# add a new item


@app.route('/add', methods=['GET', 'POST'])
def add_item():
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

# edit on item


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    if 'username' not in login_session:
        return redirect('/')
    elif request.method == 'POST':
        edited_item_name = request.form['name'].strip()
        # the item name should not be empty
        if edited_item_name == None or edited_item_name == "":
            flash("Item name should not be empty!")
            return redirect(url_for('edit_item', item_name=item_name))
        # because name is the primary key, check whether this new name is
        # already in the database
        exist_item = session.query(CategoryItem).filter_by(
            name=edited_item_name).all()
        if len(exist_item) > 0 and edited_item_name != item_name:
            flash("Cannot add " + edited_item_name +
                  ", this item has already exist.")
            return redirect(url_for('edit_item', item_name=item_name))
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

# Delete an item


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(item_name):
    if 'username' not in login_session:
        return redirect('/')
    elif request.method == 'POST':
        item_delete = session.query(
            CategoryItem).filter_by(name=item_name).one()
        session.delete(item_delete)
        session.commit()
        return redirect('/')
    else:
        item_delete = session.query(
            CategoryItem).filter_by(name=item_name).one()
        return render_template('delete_login.html', item=item_delete, user_name=login_session['username'])

# return all items in json format


@app.route('/catalog.json')
def show_json():
    categories = session.query(Category).all()
    all_data = {"category": []}
    for category in categories:
        category_dic = {"name": category.name}
        items = session.query(CategoryItem).filter_by(
            category_id=category.name).all()
        category_dic["items"] = [item.serialize for item in items]
        all_data["category"].append(category_dic)
    return jsonify(all_data)

# validate the token with google Oauth2


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return "login successful"


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        del login_session['username']
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # print 'In gdisconnect access token is %s', access_token
    # print 'User name is: '
    # print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print 'result is '
    # print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'lkGBDLHJ^&*FI*&RTF^F$665VJ7BKH'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
