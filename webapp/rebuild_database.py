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

os.environ['FLASK_APP'] = "aikif_web.py"
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """
    Connects to the specific database.
    """
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
    """
    Initializes the database.
    """
    init_db()
    print('Initialized the database.')    
    
def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, database_filename): # was 'sqlite_db'
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request.
    """
    if hasattr(g, database_filename): # was 'sqlite_db'
        g.sqlite_db.close()

  
initdb_command()   # RUN THIS TO RE RUN schema.sql  
  
      