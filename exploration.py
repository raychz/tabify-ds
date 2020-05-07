import os
import time
import re
import json

from flask import request
from flask import Flask, render_template, Response
import mysql.connector
from mysql.connector import errorcode

def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None)
    username = os.environ.get("USER", None) or os.environ.get("username", None)
    password = os.environ.get("PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None)

    return db, username, password, hostname
def get_data(): 
    db, username, password, hostname = get_db_creds()
    
    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)
        cur = cnx.cursor()
        print("connection to Tabify DB")
        cur.execute("SELECT * from location")
        columns = cur.description 
        result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cur.fetchall()]
  
        if len(result) > 0:
            return Response(json.dumps(result), mimetype='application/json', status=200)
        else:
            not_found = {"Message":  "No pools to show"}
            return Response(json.dumps(not_found), mimetype='application/json', status=404)

    except Exception as exp:
        print("WRONG, in GET")
        print(exp)

if __name__ == "__main__":
    print(get_db_creds())
    