#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

print ("sys.version = ", sys.version)
print ("os.getcwd() = ", os.getcwd())


#AIKIF_WEB_VERSION = "PROD"
AIKIF_WEB_VERSION = "DEV"
AIKIF_VERSION_NUM = "Version 0.2.1 (alpha) - updated 15-Jan-2017"



 

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



 
from aikif import core_data   

import sqlite3
  


# --- local flask app files ---- 

import web_utils as web
from users import User



app = Flask(__name__)


menu = [
    ['/',        'Home',     'This is the admin web interface for AIKIF (Artificial Intelligence Knowledge Information Framework)'],
    ['/data',    'Data',     'Shows the available data sets for AIKIF'],
    ['/projects',    'Projects',     'Manage projects'],
    ['/agents',  'Agents',   'Describes the agents capabilities, and last run status'],
    ['/programs','Programs', 'Details of the modules in AIKIF'],
    ['/about',   'About',    'About AIKIF and author contact']
    ]

    
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
    with app.open_resource('schema.sql', mode='r') as f:
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

  

  
  


# Now, it is possible to create a database with the flask script:
#flask initdb
#Initialized the database.
  
#initdb_command()   # RUN THIS TO RE RUN schema.sql  
  
    
###################### HELPER FUNCTIONS#################
def start_server():
    if AIKIF_WEB_VERSION == "DEV":
        print("WARNING - DEBUG MODE ACTIVE")
        app.debug = True # TURN THIS OFF IN PRODUCTION
        app.run()
    else:
        app.run(threaded=True, host='0.0.0.0', port=5000)    

###################### ROUTING #########################


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
        except:
            pass   # ignore blank user/pass - they will be rejected further on
        if username != app.config['USERNAME']:
            error = 'Invalid username'
        elif password != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = username
            #user = User(username, password, 'blank@email.com')
            #login_user(user)
            flash('You were logged in')
            
            
            
            return redirect(url_for('page_home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('page_home'))


def am_i_authenticated():
    try:
        if session['logged_in'] == True:
            return True
    except:
        pass
    return False
    
    
@app.route("/")
def page_home():
    #user = g.user
    return render_template('index.html', 
        username = get_user(),
        logged_on=am_i_authenticated())


@app.route('/', methods=['POST'])
def search_post():

    return 'todo'
 


def get_data_list():
    return core_data.core_data_types
    
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(sql_str, vals):
    """
    runs an insert or update query against the database
    execute('insert into tablename values (?,?,?)', item)
    """
    print("insert_db(sql_str) = ", sql_str, ' vals = ', vals)
    db = get_db()
    db.execute(sql_str, vals)
    db.commit()


@app.route("/data")
#@login_required
def page_data():
    return render_template('data.html',
                           data=get_data_list(),
                           rows = query_db('select * from CORE_FACTS'),
                           logged_on=am_i_authenticated(),
                           username = get_user(),
                           dataFile = '')

  
    
@app.route("/data", methods=['POST'])
def add_data():
    editedinfo = []
    #editedinfo.append('first_record')
    editedinfo.append(request.form['col_1'])
    editedinfo.append(request.form['col_2'])
    editedinfo.append(request.form['col_3'])
    res = request.form['add-data']   # this gets the button value if Add button clicked
    print('Adding data : ', editedinfo )
        
    sql_str = "INSERT INTO CORE_FACTS ('NAME','KEY','VALUE') VALUES (?,?,?)"
    insert_db(sql_str, editedinfo)

    return render_template('data.html',
                           data=get_data_list(),
                           rows = query_db('select * from CORE_FACTS'),
                           dataFile = '',
                           username = get_user(),
                           logged_on=am_i_authenticated()
                           )
 

    
@app.route("/data/<dataFile>")
def page_data_show(dataFile):
    print('page_data_show(dataFile)' , dataFile)
    # first step is to read the datatable (for now, just a hard coded table
    #res = query_db('select * from CORE_FACTS')
    #print('res = ' , res)
    
    return render_template('data.html',
                           data=get_data_list(),
                           rows = query_db('select * from CORE_FACTS'),
                           logged_on=am_i_authenticated(),
                           username = get_user(),
                           dataFile=dataFile
                           )
  

@app.route("/agents")
def page_agents():
    return render_template('agents.html',
                           agents=get_agents(),
                           username = get_user(),
                           logged_on=am_i_authenticated()
                           )



def get_agents():
    """
    return the list of agents
    """
    res = ['AgentInterfaceEnv:Agent Enviroment Interface',
    'AgentInterfaceWindows:Windows Interface',
    'Hard coded Test'
    ]

    
    #with open(os.path.join(os.getcwd(), 'list_agent_names.txt'), 'r') as f:
    #    for line in f:
    #        if line != '':
    #            res.append(line)
    
    return res
                           
@app.route("/agents", methods=['POST'])
def edit_agents():
    res = ''
    editedinfo = []
    print('hi - about to get form values', request.form)
    #editedinfo.append(request.form['Agent Name']) # request.form['search_text']
    #editedinfo.append(request.form['Program Location'])
    #editedinfo.append(request.form['params'])
    
    for i in range(0,3):
        editedinfo.append(request.form['col_' + str(i)])
        
    #print('update-form ',   request.form['update-form'] )
    #print('add-form ',   request.form['add-form'] )
    #print('delete-form ',   request.form['delete-form'] )
    
    try:
        res = request.form['update-form']
    except:
        pass
    try: 
        res = request.form['add-form']
    except:
        pass
    try:
        res = request.form['delete-form']
    except:
        pass
    
    return res + str(editedinfo)
    
@app.route("/programs")
def page_programs():
    return render_template('programs.html',
                username = get_user(),
                logged_on=am_i_authenticated())

    
@app.route("/programs/rebuild")
def page_programs_rebuild():
    return 'todo'

@app.route("/about")
def page_about():
    return render_template('about.html',
                    username = get_user(),
                    logged_on=am_i_authenticated())


     
if __name__ == "__main__":
    start_server()
