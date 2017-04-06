# coding: utf-8
# web_utils.py	written by Duncan Murray 26/5/2014
# functions to convert data to HTML, etc for web dev
import csv
import os
import fnmatch
from flask import request

import sys
import csv


def GetFileList(rootPaths, lstXtn, shortNameOnly='Y'):
    """ 
    builds a list of files and returns as a list 
    """
    numFiles = 0    
    opFileList = []
    for rootPath in rootPaths:
        print(' rootPath = ', rootPath)
        for root, dirs, files in os.walk(rootPath):
            print('found ' + str(len(dirs)) + ' directories')
            for basename in files:
                for xtn in lstXtn:
                    if fnmatch.fnmatch(basename, xtn):
                        filename = os.path.join(root, basename)
                        numFiles = numFiles + 1
                        if shortNameOnly == 'Y':
                            opFileList.append( os.path.basename(filename))
                        else:
                            opFileList.append(filename)
                        
    return sorted(opFileList)

def build_search_form():
    """ 
    returns the html for a simple search form 
    """
    txt = '<form action="." method="POST">\n'
    txt += '  <input type="text" name="search_text">\n'
    txt += '  <input type="submit" name="my-form" value="Search">&nbsp;&nbsp;\n'
    txt += '  <input name="Folders" id="chkFolder" type="checkbox" checked="checked">Folders&nbsp;\n'
    txt += '  <input name="Tables" id="chkTables" type="checkbox" checked="checked">Tables&nbsp;\n'
    txt += '  <input name="Programs" id="chkPrograms" type="checkbox">Programs&nbsp;\n'
    txt += '  <input name="Data" id="chkData" type="checkbox">Data&nbsp;\n'
    txt += '</form>\n'
    return txt
    
 
def build_edit_form(title, id, cols, return_page):
    """ 
    returns the html for a simple edit form 
    """
    txt = '<H3>' + title + '<H3>'
    txt += '<form action="' + return_page + '" method="POST">\n' # return_page = /agents
    txt += '  updating id:' + str(id) + '\n<BR>'
    txt += '  <input type="hidden" name="rec_id" readonly value="' + str(id) + '"> '
    txt += '  <TABLE width=80% valign=top border=1>'
    
    for col_num, col in enumerate(cols):
        txt += '  <TR>\n'
        txt += '    <TD><div id="form_label">' + col + '</div></TD>\n'
        txt += '    <TD><div id="form_input"><input type="text" name="col_' + str(col_num) + '"></div></TD>\n'
        txt += '  </TR>\n'
    txt += '  <TR><TD></TD>\n'
    txt += '  <TD>\n'
    txt += '    <input type="submit" name="update-form" value="Save Changes">\n'
    txt += '    <input type="submit" name="delete-form" value="Delete">\n'
    txt += '    <input type="submit" name="add-form" value="Add">\n'
    txt += '  </TD></TR></TABLE>'
    txt += '</form>\n'
    return txt

def build_html_listbox(lst, nme):
    """
    returns the html to display a listbox
    """
    res = '<select name="' + nme + '" multiple="multiple">\n'
    for l in lst:
        res += '    <option>' + str(l) + '</option>\n'
    res += '</select>\n'

    return res
 
def filelist2html(lst, fldr, hasHeader='N'):
    """ 
    formats a standard filelist to htmk using table formats 
    """
    txt = '<TABLE width=100% border=0>'
    numRows = 1
    if lst:
        for l in lst:
            if hasHeader == 'Y':
                if numRows == 1:
                    td_begin = '<TH>'
                    td_end = '</TH>'
                else:
                    td_begin = '<TD>'
                    td_end = '</TD>'
            else:
                td_begin = '<TD>'
                td_end = '</TD>'
            numRows += 1
            txt += '<TR>'
            if type(l) is str:
                txt += td_begin + link_file(l, fldr) + td_end
            elif type(l) is list:
                txt += td_begin
                for i in l:
                    txt+= link_file(i, fldr) + '; '
                txt += td_end
            else:
                txt += td_begin + str(l) + td_end
            txt += '</TR>\n'
    txt += '</TABLE><BR>\n'
    return txt

def link_file(f, fldr):
    """ 
    creates a html link for a file using folder fldr 
    """
    fname = os.path.join(fldr,f)
    if os.path.isfile(fname):
        if 'data/' in request.path:
            return '<a href="' + f + '">' + f + '</a>'
        else:
            return '<a href="data/' + f + '">' + f + '</a>'
    else:
        return f
    
def read_csv_to_html_list(csvFile):
    txt = ''
    with open(csvFile) as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            txt += '<div id="table_row">'
            for col in row:
                txt += " "
                try:
                    txt += col
                except Exception:
                    txt += 'Error'
                txt += " "
            txt += "</div>\n"
    return txt
   
def read_csv_to_list(filename):
    """
    reads a CSV file to a list
    """
    import csv

    rows_to_load = []
    with open(filename, 'r', encoding='cp1252') as csvfile: # sort of works with , encoding='cp65001'
        csvreader = csv.reader(csvfile, delimiter = ',' )

        reader = csv.reader(csvfile)            

        rows_to_load = list(reader)
    return rows_to_load

   