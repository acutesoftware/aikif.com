#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

print ("sys.version = ", sys.version)
print ("os.getcwd() = ", os.getcwd())

#AIKIF_WEB_VERSION = "PROD"
AIKIF_WEB_VERSION = "DEV"
AIKIF_VERSION_NUM = "Version 0.2.1 (alpha) - updated 15-Jan-2017"

import web_utils as web
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash   
   
from aikif import core_data   
   
   
print('core_data.core_data_types = ', core_data.core_data_types)   
   
import sqlite3
   
app = Flask(__name__)

menu = [
    ['/',        'Home',     'This is the admin web interface for AIKIF (Artificial Intelligence Knowledge Information Framework)'],
    ['/data',    'Data',     'Shows the available data sets for AIKIF'],
    ['/projects',    'Projects',     'Manage projects'],
    ['/agents',  'Agents',   'Describes the agents capabilities, and last run status'],
    ['/programs','Programs', 'Details of the modules in AIKIF'],
    ['/about',   'About',    'About AIKIF and author contact']
    ]

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

is_authenticated = False

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('page_home'))


@app.route("/")
def page_home():
    #user = g.user
    return render_template('index.html',
                           footer=get_footer())


                           
                           
                           
                           
                           

@app.route('/', methods=['POST'])
def search_post():
    return(_search(request.form['search_text']))
 
def _search(search_text):
    txt = aikif_web_menu()
    txt += web.build_search_form()
    import page_search
    txt += page_search.get_page(search_text)
    return txt



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
def page_data():
    return render_template('data.html',
                           data=get_data_list(),
                           rows = query_db('select * from CORE_FACTS'),
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
                           footer=get_footer())
 

    
@app.route("/data/<dataFile>")
def page_data_show(dataFile):
    print('page_data_show(dataFile)' , dataFile)
    # first step is to read the datatable (for now, just a hard coded table
    #res = query_db('select * from CORE_FACTS')
    #print('res = ' , res)
    
    return render_template('data.html',
                           data=get_data_list(),
                           rows = query_db('select * from CORE_FACTS'),
                           dataFile=dataFile,
                           footer=get_footer())
  

@app.route("/agents")
def page_agents():
    return render_template('agents.html',
                           agents=get_agents(),
                           footer=get_footer())



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
                           footer=get_footer())

    
@app.route("/programs/rebuild")
def page_programs_rebuild():
    txt = aikif_web_menu('Programs')
    import page_programs as prg
    prg.rebuild()
    txt += prg.get_page()
    return txt

@app.route("/about")
def page_about():
    return render_template('about.html',
                           footer=get_footer())


    
def page_error(calling_page):
    txt = '<BR><BR>'
    txt += '<H2>Error - problem calling ' + calling_page + '</H2>'
    txt += get_footer()
    return txt
    
def aikif_web_menu(cur=''):
    """ returns the web page header containing standard AIKIF top level web menu """
    pgeHdg = ''
    pgeBlurb = ''
    if cur == '': 
        cur = 'Home'
    txt = get_header(cur) #"<div id=top_menu>"
    txt += '<div id = "container">\n'
    txt += '   <div id = "header">\n'
    txt += '   <!-- Banner -->\n'
    txt += '   <img src = "' + os.path.join('/static','aikif_banner.jpg') + '" alt="AIKIF Banner"/>\n'
    txt += '   <ul id = "menu_list">\n'
    for m in menu:
        if m[1] == cur:
            txt += '      <LI id="top_menu_selected"><a href=' + m[0] + '>' + m[1] + '</a></li>\n'
            pgeHdg = m[1]
            try:
                pgeBlurb = m[2]
            except Exception:
                pass
        else:
            txt += '      <LI id="top_menu"><a href=' + m[0] + '>' + m[1] + '</a></li>\n'
    txt += "    </ul>\n    </div>\n\n"
    txt += '<H1>AIKIF ' + pgeHdg + '</H1>\n'
    txt += '<H4>' + pgeBlurb + '</H4>\n'
    return txt

###################### TEMPLATES #########################

def get_header(pge=''):
    txt = '<HTML><HEAD>\n'
    txt += '<title>AIKIF:' + pge + '</title>\n'
    txt += '<!-- Stylesheets for responsive design -->\n'
    txt += '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
    txt += '<link rel="stylesheet" type="text/css" href="' + os.path.join('/static','aikif.css') + '" media="screen" />\n'
    txt += '<link rel="stylesheet" href="' + os.path.join('/static','aikif_mob.css')
    txt += '" media="only screen and (min-device-width : 320px) and (max-device-width : 480px)">\n'
    txt += '</HEAD>\n'
    txt += '<body>\n'
    return txt
    
def get_footer():
    txt = AIKIF_WEB_VERSION + ':' + AIKIF_VERSION_NUM + '\n'
    txt += ', Python version:' + sys.version + '\n'
    return txt

def escape_html(s):
    res = s
    res = res.replace('&', "&amp;")
    res = res.replace('>', "&gt;")
    res = res.replace('<', "&lt;")
    res = res.replace('"', "&quot;")
    return res

def format_list_as_html_table_row(lst):
    txt = '<TR>'
    for i in lst:
        txt = txt + '<TD>' + i + '</TD>'
    txt = txt + '</TR>'	
    return txt
    
def format_csv_to_html(csvFile, opHTML):
    """
    print(len(opHTML))
    with open(csvFile) as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            txt += "<TR>"
            for col in row:
                txt += "<TD>"
                txt += escape_html(col)
                txt += "</TD>"
            txt += "</TR>"
        txt += "</TABLE>"
    """
    txt = 'TODO format_csv_to_html to convert' + csvFile + ' to ' + opHTML
    return txt
    

    
if __name__ == "__main__":
    start_server()
