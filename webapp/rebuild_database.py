#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

print ("sys.version = ", sys.version)
print ("os.getcwd() = ", os.getcwd())


#AIKIF_WEB_VERSION = "PROD"
AIKIF_WEB_VERSION = "DEV"
AIKIF_VERSION_NUM = "Version 0.2.2 (alpha) - updated 6-Apr-2017"



 

from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash   
   
from flask_login import LoginManager   
from flask_login import UserMixin   
from flask_login import login_required
from flask_login import login_user

import sqlite3
  
import logging
from logging.handlers import RotatingFileHandler

from aikif import core_data   

# --- local flask app files ---- 

import web_utils as web
from users import User

DATABASE_DDL = 'schema_PostgreSQL.sql'
DATABASE_DDL = 'schema_sqlite.sql'


app = Flask(__name__)


menu = [
    ['/',        'Home',     'This is the admin web interface for AIKIF (Artificial Intelligence Knowledge Information Framework)'],
    ['/data',    'Data',     'Shows the available data sets for AIKIF'],
    ['/projects',    'Projects',     'Manage projects'],
    ['/agents',  'Agents',   'Describes the agents capabilities, and last run status'],
    ['/programs','Programs', 'Details of the modules in AIKIF'],
    ['/about',   'About',    'About AIKIF and author contact']
    ]

 
upload_folder = os.getcwd()
 
###### User Authentication ####

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_user():
    try:
        user = session['username']
    except:
        user = ''
    return user    
    
###### DATABASE #####

database_filename = 'aikif_db.db'

app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, database_filename),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='12345yesreally'
))

#os.environ['FLASK_APP'] = 'aikif.py'
os.environ['FLASK_APP'] = "aikif_web.py"
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource(DATABASE_DDL, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')    
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, database_filename): # was 'sqlite_db'
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, database_filename): # was 'sqlite_db'
        g.sqlite_db.close()

  


initdb_command()   # RUN THIS TO RE RUN schema.sql  
  
      