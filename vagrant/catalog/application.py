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

from models.add import add
app.register_blueprint(add)

from models.delete import delete
app.register_blueprint(delete)

from models.description import description
app.register_blueprint(description)

from models.edit import edit
app.register_blueprint(edit)

from models.google import google
app.register_blueprint(google)

from models.index import index
app.register_blueprint(index)

from models.items import items
app.register_blueprint(items)

from models.jsonapi import jsonapi
app.register_blueprint(jsonapi)


if __name__ == '__main__':
    app.secret_key = 'lkGBDLHJ^&*FI*&RTF^F$665VJ7BKH'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
