from flask import Flask, render_template, request
import requests
app = Flask(__name__)
import datetime 
import numpy as num
from dateutil.relativedelta import *
from email_validator import validate_email, EmailNotValidError


@app.route('/')
def student():
   return render_template('index.html')


@app.route('/emailChecker',methods = ['POST', 'GET'])
def mail():
    if request.method == 'GET':
        return render_template('emailChecker.html')
    else:
        email = request.form['email']
        isValid = False

        try:
            e = validate_email(email)
            isValid = True
            print(e)
        except EmailNotValidError as e:
            print(str(e))
        return render_template('emailChecker.html',isValid=isValid,mailid=email)

@app.route('/quiz',methods = ['POST', 'GET'])
def result():   
    print(request.form['dob']) 
    dob = request.form['dob']
    [year,month,exactdate] = num.array(dob.split('-'))
    present_datetime = datetime.datetime.now()
    birthday = datetime.datetime(int(year), int(month), int(exactdate)) 
    age = relativedelta(present_datetime, birthday).years
    if(age<15):
        difficulty = "easy"
    elif(age < 20 and age > 15):
        difficulty = "medium"
    else:
        difficulty = "hard"
    url =   "https://the-trivia-api.com/api/questions?categories=arts_and_literature&limit=2&region=IN&difficulty=" + difficulty
    result = requests.get(url).json()
    print(result)
    return render_template("index.html",result = result,age=age,difficulty=difficulty)

if __name__ == '__main__':
   app.run(debug = True)