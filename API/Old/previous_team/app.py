from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sql_collection import Sql_collection
from flask_bootstrap import Bootstrap
import os
import time
from datetime import date
# from cryptography.fernet import Fernet



#old one
#app = Flask(__name__, template_folder = template_dir)
app = Flask(__name__)
Bootstrap(app)

# Fill in the following fields according to the configurations of your database
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   #enter your sql pw
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'Recreate_Energy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
@app.route('/index.html')

def index():
    '''
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_all())
    results = cur.fetchall()

    '''    
    return render_template('index.html')    #probably need to change index file  https://pythonhosted.org/Flask-Bootstrap/basic-usage.html

#getTemp
@app.route('/graph1')
def graph1():   #parameters(chamberId, startTime, endTime)
    # graph_data = {"x":[1,2,3,4,5], "y":[1,2,3,4,5], "z":[1,2,3,4,5]}
    # resp = jsonify(graph_data)
    # return resp
    chamber = 1;
    startTime = '2021-10-08'
    endTime = '2021-10-10'      #remove hardcode
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_temp_in_dates(chamber, startTime, endTime))
    results = cur.fetchall()
    graph_data = {'temp':[], 'sub_date':[]}
    for values in results:
        graph_data['temp'].append(values.get('temp'))
        formatted_date = values.get('sub_date').strftime("%m-%d-%Y %H:%M:%S")
        graph_data['sub_date'].append(formatted_date)
    
    
    resp = jsonify(graph_data)
    return resp
    


#2
@app.route('/graph2')
def graph2():   #parameters (chamberId)
    chamberId = 1;    #remove hardcode
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_recent(chamberId))
    results = cur.fetchall()
    graph_data = {'chmb_id':[], 'temp':[], 'ph':[],'ADCRaw':[],'DOX':[], 'sub_date':[]}
    for values in results:
        graph_data['chmb_id'].append(values.get('chmb_id'))
        graph_data['temp'].append(values.get('temp'))
        graph_data['ph'].append(values.get('ph'))
        graph_data['ADCRaw'].append(values.get('ADCRaw'))
        graph_data['DOX'].append(values.get('DOX'))
        formatted_date = values.get('sub_date').strftime("%m-%d-%Y %H:%M:%S")
        graph_data['sub_date'].append(formatted_date)
    
    resp = jsonify(graph_data)       
    return resp
#3 get PH
@app.route('/graph3')
def graph3():   #paramters(chamberId, startTime, endTime)
    chamberId = 1;
    startTime = '2021-10-08'
    endTime = '2021-10-10'      #remove hardcode
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_ph_in_dates(chamberId, startTime, endTime))
    results = cur.fetchall()
    graph_data = {'ph':[], 'sub_date':[]}
    for values in results:
        graph_data['ph'].append(values.get('ph'))
        formatted_date = values.get('sub_date').strftime("%m-%d-%Y %H:%M:%S")
        graph_data['sub_date'].append(formatted_date)
    
    resp = jsonify(graph_data)
    return resp

#4 getADCRaw/ADCVolt
@app.route('/graph4')
def graph4():   #paramters(chamberId, startTime, endTime)
    chamberId = 1;
    startTime = '2021-10-08'
    endTime = '2021-10-10'      #remove hardcode
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_ADCRAW_ADCVOLT_in_dates(chamberId, startTime, endTime))
    results = cur.fetchall()
    graph_data = {'ADCRaw':[], 'ADCVolt': [], 'sub_date':[]}
    for values in results:
        graph_data['ADCRaw'].append(values.get('ADCRaw'))
        graph_data['ADCVolt'].append(values.get('ADCVolt'))
        formatted_date = values.get('sub_date').strftime("%m-%d-%Y %H:%M:%S")
        graph_data['sub_date'].append(formatted_date)
    resp = jsonify(graph_data)
    return resp

#5 getDox
@app.route('/graph5')
def graph5():   #paramters(chamberId, startTime, endTime)
    chamberId = 1;
    startTime = '2021-10-08'
    endTime = '2021-10-10'      #remove hardcode
    cur = mysql.connection.cursor()
    cur.execute(Sql_collection.select_DOX_in_dates(chamberId, startTime, endTime))
    results = cur.fetchall()
    graph_data = {'DOX':[], 'sub_date':[]}
    for values in results:
        graph_data['DOX'].append(values.get('DOX'))
        formatted_date = values.get('sub_date').strftime("%m-%d-%Y %H:%M:%S")
        graph_data['sub_date'].append(formatted_date)
    resp = jsonify(graph_data)
    return resp
    

@app.route("/console.html")
def console():
    return render_template('console.html')

@app.route("/charts.html")
def charts():
    return render_template('charts.html')

@app.route("/documentation.html")
def documentation():
    return render_template('documentation.html')

@app.route("/forgot-password.html")
def forgotPassword():
    return render_template('forgot-password.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/profile.html")
def profile():
    return render_template('profile.html')

@app.route("/register.html")
def register():
    return render_template('register.html')

@app.route("/settings.html")
def settings():
    return render_template('settings.html')


@app.route("/userreg", methods = ["POST"])
def userreg():
    email = request.form.get('email')
    psw = request.form.get('password')
    org_id = request.form.get('org_id')

    cur0 = mysql.connection.cursor()
    cur0.execute(Sql_collection.get_psw(email))
    results = cur0.fetchall()
    cur0.close()
    if len(results) > 0:
        return "user already exist"
    else:
        resp = "success"
        try:
            # write user data into db
            cur = mysql.connection.cursor()
            cur.execute(Sql_collection.add_user_n_psw(email, psw, org_id))
            mysql.connection.comit()
            cur.close()
        except:
            resp = "error"

        return resp



@app.route("/loginverify", methods = ["POST"])
def loginverify():
    email = request.form.get('email')
    psw_inputted = request.form.get('password')

    cur0 = mysql.connection.cursor()
    cur0.execute(Sql_collection.get_psw(email))
    results = cur0.fetchall()
    try:
        psw = results[0]["password"]
    except:
        psw = ""
    cur0.close()
    resp = {}
    if len(results) < 1:
        resp["status"] = "fail"
        resp["message"] = "no user found"
        return jsonify(resp)
    else:
        if psw == psw_inputted:
            '''Spencer's code
            cur = mysql.connection.cursor()
            cur.execute(Sql_collection.get_user_info())
            results = cur.fetchall()
            cur.close()
            '''
            resp["status"] = "success"
            resp["message"] = "success"
            
            return jsonify(resp)
        else:
            resp["status"] = "fail"
            resp["message"] = "wrong password"
            return resp






if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
