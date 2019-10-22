import string
import random
import requests
import json
import httplib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from flask import session as login_session
from flask import Flask, render_template, request, redirect, \
    jsonify, flash
app = Flask(__name__)

# Load Google Sign-in API CLIENT_ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine(
    'sqlite:///catalog.db',
    connect_args={'check_same_thread': False})

Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Login
@app.route('/login')
def login():
    state = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
# Connecting to Google oAuth
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

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

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, cancel.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify the access token is used for intended user
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's client ID does not match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify access token is valid for this app
    if result['issued to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store token in session
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome back, '
    output += login_session['username']
    output += '!</h1'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; \
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    print("done!")
    return output

# Create new user


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']), one()
    return user.id

# Get user information


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get user ID


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None

# Disconnect user and reset login session
@app.route('/gdisconnect')
def gdisconnect():
    category = session.query(Categories)
    items = session.query(Items)
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s'), access_token
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully logged out")
        return redirect(
            url_for(
                'showCategories',
                category=category,
                items=items))
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON API's for all categories
@app.route('/category/JSON')
def CategoryJSON():
    jsonCategory = session.query(Categories).all()
    return jsonify(Category=[i.serialize for i in jsonCategory])

# JSON API's to view the catalog items information
@app.route('/category/<int:categories_id>/items/JSON')
def CategoryItemsJSON(categories_id):
    jsonCategories = session.query(
        Categories).filter_by(id=categories_id).one()
    CategoryItems = session.query(Items).filter_by(
        category_id=jsonCategories.id).all()
    return jsonify(CategoryItems=[i.serialize for i in CategoryItems])

# JSON API's to view a single items information
@app.route('/category/<int:categories_id>/<int:item_id>/JSON')
def CategorySingleItemJSON(categories_id, item_id):
    jsonSingleItem = session.query(
        Categories).filter_by(id=categories_id).one()
    CategoryItem = session.query(Items).filter_by(id=jsonSingleItem.id).one()
    return jsonify(CategoryItem=[CategoryItem.serialize])

# Show Categories
@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Categories).all()
    item = session.query(Items).all()
    return render_template('categories.html', category=categories, item=item)

# Show Category items
@app.route('/category/<int:categories_id>/items')
@app.route('/category/<int:categories_id>/')
def showCategoryItem(categories_id):
    categoryShow = session.query(
        Categories).filter_by(id=categories_id).one()
    itemsShow = session.query(Items).filter_by(category_id=categories_id)
    return render_template(
        'displayItem.html',
        category=categoryShow,
        items=itemsShow)

# Create a new category item
@app.route('/category/<int:categories_id>/item/new', methods=['GET', 'POST'])
def createItem(categories_id):
    if 'username' not in login_session:
        return redirect('/login')
    theCategory = session.query(Categories).filter_by(id=categories_id).one()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            category_id=theCategory.id,
            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'createItem.html',
            categories_id=categories_id)

# Edit a category item


@app.route(
    '/category/<int:categories_id>/<int:item_id>/edit',
    methods=[
        'GET',
        'POST'])
def editCategoryItem(categories_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Items).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('\
        You are not authorized to edit this item. \
        Please create your own item in order to edit.\
         ');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['Description']:
            editedItem.description = request.form['Description']
        session.add(editedItem)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'editItem.html',
            categories_id=categories_id,
            item_id=item_id,
            i=editedItem)

# Delete a category item


@app.route(
    '/category/<int:categories_id>/<int:item_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteCategoryItem(categories_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Items).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not \
        authorized to delete this item.\
        Please create your own item in order to delete.');}\
        </script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(
            url_for(
                'showCategoryItem',
                categories_id=categories_id))
    else:
        return render_template(
            'deleteItem.html',
            categories_id=categories_id,
            i=itemToDelete)

# Show item description
@app.route('/category/<int:categories_id>/<int:item_id>/description')
def showItemDescription(categories_id, item_id):
    category = session.query(Categories).filter_by(id=categories_id).one()
    itemDeletion = session.query(Items).filter_by(id=item_id).one()
    return render_template('displayItemDescription.html',
                           category=category, items=itemDeletion)


if __name__ == '__main__':
    app.secret_key = 'really_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
