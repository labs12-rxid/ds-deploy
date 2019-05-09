"""
Main application and routing logic
"""
<<<<<<< HEAD
from flask import Flask, request, render_template, jsonify
from joblib import load
from flask_cors import CORS
import datetime
import pandas as pd
import pytz
from pytz import timezone
import calendar
import psycopg2
from sqlalchemy import create_engine
import boto3
import os


#______DRUGSCOM imports _____
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import io
import time
import sys
import re
import numpy as np
import glob
import shutil
import json
import html
from string import punctuation
from collections import deque
=======
# _____ imports _____________
from flask import Flask, request, render_template, jsonify
from joblib import load
from flask_cors import CORS
import pandas as pd
import json

# ______ Module imports _____
from drugscom import drugscom
from rxid_util import parse_input
from rds_lib import db_connect, query_sql_data, verify_output
from rekog import post_rekog

drugs_com = drugscom()
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83

""" create + config Flask app obj """
application = Flask(__name__)
CORS(application)

<<<<<<< HEAD

# ______________ R O U T E S  _____________________
# ________  HOME __________
=======
# ______________ R O U T E S  _____________________
# ________ / HOME __________
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83
@application.route('/')
def index():
    return render_template('base.html', title='Home')

# ________  /indentify/  route __________
<<<<<<< HEAD
# __ input  image uri, S3 bucket
@application.route('/identify', methods=['GET', 'POST'])
def indentify():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
        return jsonify(output_info)
    else:

        results = drugscom()
        
        return jsonify("YOU just made a GET request to /identify : " + results)


# ________  /rxdata/  route __________
=======
# __ input  {'imprint' : 'M370',  'color' : 1,  'shape' : 6}    
@application.route('/identify', methods=['GET', 'POST'])
def identify():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        results = get_drugscom(post_params)
        return results
    else:
        return jsonify("GET request to /identify :")


# ________  /rxdata/  route __________
# __ {'imprint' : 'M370',  'color' : 1,  'shape' : 6}    
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83
@application.route('/rxdata', methods=['GET', 'POST'])
def rxdata():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
<<<<<<< HEAD
        return jsonify(output_info)
    else:
        return jsonify("YOU just made a GET request to /rxdata")

# ________  /nnet/  route __________
@application.route('/nnet', methods=['GET', 'POST'])
def nnet():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        output_info = query_sql_data(post_params)
        return jsonify(output_info)
    else:
        
        return jsonify("YOU just made a GET request to /nnet")
=======
        return output_info

    else:
        return jsonify("GET request to /rxdata :")

>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83

# ________  /rekog/  route __________
@application.route('/rekog', methods=['GET', 'POST'])
def rekog():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
<<<<<<< HEAD
=======
        # https://s3.amazonaws.com/labs12-rxidstore/reference/00002-3228-30_391E1C80.jpg
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83
        output_info = post_rekog(post_params)
        return jsonify(output_info)
    else:
        return jsonify("YOU just made a GET request to /rekog")

<<<<<<< HEAD

# ___________________ FUNCTIONS ________________________________
def drugscom():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/")
    element_text = driver.find_element_by_id("title").text
    return element_text

def post_rekog(post_params):
    return post_params

#  _____ query and return SQL data ______________
def query_sql_data(parameter_list):
    #  echo the output for now  -- needs query code 
    return parameter_list


# ____  download file from AWS S3 Bucket into local tmp dir_______
def download_from_S3(S3_bucketname, S3_filename, local_filename='S3file.jpg'):
    s3_resource = boto3.resource('s3')
    s3_resource.Object(S3_bucketname, S3_filename).download_file(f'./{local_filename}')
    return


# _______ GET CURRENT DAY AND HOUR __________
def day_hour():
    # get current time in pacific timezone
    utc = pytz.utc
    utc.zone
    pacific = timezone('US/Pacific')
    
    #  bin the current hour
    time = datetime.datetime.today().astimezone(pacific)    
    hour = (time.hour)
    if hour <= 4:
        hour = 1
    elif 4 > hour <= 8:
        hour = 2
    elif 8 > hour <= 12:
        hour = 3
    elif 12 > hour <= 16:
        hour = 4
    elif 16 > hour <= 20:
        hour = 5
    else:
        hour = 6

    # Day of the week
    weekday = time.isoweekday()
    d = {1: 'MONDAY', 2: 'TUESDAY', 3: 'WEDNESDAY', 4: 'THURSDAY', 
        5: 'FRIDAY', 6: 'SATURDAY', 7: 'SUNDAY'}
    for key, value in d.items():
        if key == weekday:
            weekday = value
    return weekday, hour


# _________ Parse API input string for parameters _________________
#  input->  sample API input string(s)-> /indentify/param1=Red&param2=Pill
#  ouputs -->  
def parse_input(s):

    weekday, hour = day_hour()

    # parse input string for model input values
    weather_str = ''
    weather_loc = s.find("weather=") # returns -1 if not found
    if weather_loc > 0:
        weather_str = s[s.find("weather=")+8:s.find("&",weather_loc)]

    day_str = ''
    day_loc = s.find("day=")
    if day_loc > 0:
        day_str = s[day_loc+4:s.find("&",day_loc)]

    month_num = 1
    month_loc = s.find("month=")
    if month_loc > 0:
        month_str = s[month_loc+7:s.find("&",month_loc)]
        month_str = s.find()
        month_num = 1
        month_dict = dict((v,k) for k,v in enumerate(calendar.month_name))
        for key, value in month_dict.items():
            if key == month_str:
                month_num = value


#  ____________  CONNECT TO DATABASE ___________________
def db_connect():
    # __ Connect to AWS-RDS(postgres) (SQLalchemy.create_engine) ____
    dbname = ''
    user = ''
    host = ''
    password = ''
    file = open('aws.rxidds.pwd', 'r')
    ctr = 1
    for line in file:
        line = line.replace('\n', '')
        if ctr == 1: dbname = line
        if ctr == 2: user = line
        if ctr == 3: host = line
        if ctr == 4: passw = line
        ctr = ctr + 1
    pgres_str = 'postgresql+psycopg2://'+user+':'+passw+'@'+host+'/'+dbname
    pgres_engine = create_engine(pgres_str)
    return pgres_engine


# ________  Verfiy Output From DataBase ______
def verify_output(pgres_engine):
    # ______  verify output-table contents ____
    schema_name = 'rxid'
    table_name = 'rxid_meds_data'
    table_string = schema_name + '.' + table_name 
    query = 'SELECT * FROM ' + table_string + ' LIMIT 10;'
    for row in pgres_engine.execute(query).fetchall():
        print(row)
    return
=======
# ________  /nnet/  route __________
@application.route('/nnet', methods=['GET', 'POST'])
def nnet():
    if request.method == 'POST':
        post_params = request.get_json(force=True)
        return jsonify(post_params)
    else:
        return jsonify("YOU just made a GET request to /nnet")


# ___________________ FUNCTIONS ________________________________
def get_drugscom(query_string):
    out_put = ''
    try:
        d_data = drugs_com.get_data(query_string)
        out_put = json.dumps(d_data, indent=4)
    except Exception as e:
        out_put = f'error: {e}'
    finally:
        if drugs_com is not None: 
            drugs_com.close()
    return out_put
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83


# __________ M A I N ________________________
if __name__ == '__main__':
    application.run(debug=False)

    # --- browser debugging
    # application.run(debug=True)

    #  --- for terminal debugging ------
<<<<<<< HEAD
    #input_str = 'RED PILL'
    #print(predict(input_str))

=======
    # results = get_drugscom()
    # print(results)
# __________________________________________________
>>>>>>> 073ad39da74296166c6663ce4eb236fa50451c83
# to launch from terminal : 
#    change line 25 to  application.run(debug=True)
#    cd to folder (where application.py resides)
#    run >python application.py 
