#!/usr/bin/env python
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify, redirect, make_response, url_for
import datetime, jwt, random, os
from dotenv import load_dotenv
from functools import wraps
load_dotenv()
app = Flask(__name__)
app.config["secret_k"] = os.getenv("TOKEN_KEY")
#----Timeout Setup
def Token_timer(x):
    @wraps(x)
    def wrapper(*a,**b):
        if not os.path.isfile('savefile/token.txt'):
           if not os.path.isdir('savefile'):
              os.mkdir("savefile")
           expire_date = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
           with open("savefile/token.txt","w") as f:
               create_token = jwt.encode({"type" : "timeout", "exp" : expire_date}, app.config["secret_k"], algorithm="HS256")
               f.write(create_token)
                
        with open("savefile/token.txt","r") as f:
            collect = f.read()
        try:
            data = jwt.decode(collect, app.config["secret_k"], algorithms="HS256")
            return jsonify({"status" : "Creation of tokens under timeout(est. of lift 2 minutes)"})
        except BaseException as e:
            print("---On Timeout zone-----")
            print(e)
            print("-----------------------")
            os.remove("savefile/token.txt")
        return x(*a,**b)
    return wrapper

#-----------end
@app.route ('/')
def Setup():
    session_id = random.randint(80000, 1000000)
    return render_template('setup.html', session_id=session_id)

@app.route ('/verify', methods=["POST", "GET"])
def Get_token():
    if (request.method == "POST"): 
        token = request.form["token"]
        try:
            data = jwt.decode(token,app.config["secret_k"],algorithms="HS256")
            return("it worked")
        except BaseException as e:
            return redirect("/")
            
#-------- ajax
@app.route('/ne_jax_w', methods=["POST"])
@Token_timer
def Prevent_spam():
    access_id = request.get_data()
    id_int = int((access_id.decode("UTF-8")).replace("Random=", ""))
    id_name = id_int
    print("\t >>>successful enter<<<")
    return jsonify({"status" : "acknowledged", "access_id" : id_int})

@app.route('/as_jax_token', methods=["POST"])
def Verify_token():
    token_received = request.get_data().decode("UTF-8").replace("token_sent=","")
    try:
        data = jwt.decode(token_received, app.config["secret_k"], algorithms="HS256")
        return jsonify({"response" : "valid"})
    except BaseException as e:
        print("-----------------------")
        print(e)
        print("-----------------------")
        return jsonify({"response" : "Token is invalid or has expired"})
    
#--------end
@app.route (f'/new', methods=["POST","GET"])
def Make_token():
    if (request.method == "POST"):
         if request.form["sent_value"]:
             id_generated = request.form["sent_value"]
             random_id = "{0:0=7d}".format(random.randint(1000,1000000))
             expire_date = (datetime.datetime.utcnow() + datetime.timedelta(minutes=1) )
             create_token = jwt.encode({"id" : random_id, "exp" : expire_date}, app.config["secret_k"], algorithm="HS256")
             Token = create_token
             app.config["cache"] = Token
             return redirect("/new")
    if (request.method == "GET" and app.config["cache"] != ""):
        Token = app.config["cache"]
        app.config["cache"] = ""
        return render_template("token_found.html", Token=Token)
    else:
         return make_response('Access Denied!',405,{"WWW-Authenticate":'Basic-realm="Login Required"'})
    
if __name__ == "__main__":
    app.run(debug=True)