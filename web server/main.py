from flask_pymongo import PyMongo
from os import listdir
from collections import OrderedDict
import os
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
from flask import Flask, render_template, url_for, request, redirect, flash, session
import bcrypt
import math, random
import re
import random

app = Flask(__name__)
app.secret_key = 'yashmith'
app.config['MONGO_URI'] = "mongodb://localhost:27017/C_UR_LUCK"

mongo = PyMongo(app)

currScore = 0
numOfAttempts = 0

@app.route('/')
def my_home():
    return render_template('register.html')


@app.route('/fruits', methods=['POST'])
def fruits():
    users = mongo.db.users
    attempts = 0
    dbRecord = users.find_one({'email': session['email']})
    attempts = dbRecord['attempts']
    myquery = users.find_one({'email': session['email']})
    attempts += 1
    newvalues = {"$set": {"attempts": attempts}}

    users.update_one(myquery, newvalues)
    f = request.form
    a = random.randint(1, 4)
    for key in f.keys():
        for value in f.getlist(key):
            print(key, ":", value)
    b = ''
    score = 0
    dbRecord = users.find_one({'email': session['email']})
    for i in f.getlist(key):
        i = int(i)
        if i == a:
            if i == 1:
                i = 'Apple'
            elif i == 2:
                i = 'Banana'
            elif i == 3:
                i = 'Watermelon'
            elif i == 4:
                i = 'Mango'
            elif i == 5:
                i = 'Ice apple'
            dbRecord = users.find_one({'email': session['email']})
            score = dbRecord['score']
            myquery = users.find_one({'email': session['email']})
            dh = random.randint(1, 3)
            b = f'You won as you selected {i} and you scored {dh} points!'
            score += dh
            newvalues = {"$set": {"score": score}}
            users.update_one(myquery, newvalues)
            dbRecord = users.find_one({'email': session['email']})
    if i == 1:
        i = 'Apple'
    elif i == 2:
        i = 'Banana'
    elif i == 3:
        i = 'Watermelon'
    elif i == 4:
        i = 'Mango'
    elif i == 5:
        i = 'Ice apple'
    if a == 1:
        a = 'Apple'
    elif a == 2:
        a = 'Banana'
    elif a == 3:
        a = 'Watermelon'
    elif a == 4:
        a = 'Mango'
    elif a == 5:
        a = 'Ice apple'

    if 'You won' not in b:
        b = f'Oooooch! You lose because you selected {i} and the computer selected {a}'
    global numOfAttempts
    numOfAttempts += 1
    # print("Your current score: ", currScore, "Number Of Attempts: ", numOfAttempts)
    df = score / attempts
    myquery2 = users.find_one({'email': session['email']})
    newvalues2 = {"$set": {"accuracy": score / attempts}}

    users.update_one(myquery2, newvalues2)


    score = dbRecord['score']
    name = dbRecord['name']

    mail = []
    ad = users.find().sort("score", -1)
    i = 0
    rank = 0
    fg = 0

    for x in ad:
        fg += 1
        mail.append({'rank': fg, 'name': x['name'], 'email': x['email'], 'score': x['score']})
        i += 1
        print("ad = ", x)
        print(x['name'])
        if x['email'] == session['email']:
            rank = i
        if fg == 5:
            break
    print(mail)

    print("X Value")

    return render_template('index.html', b=b, mail=mail, name=name, score=score, attempts=attempts,
                           dbRecord=session['email'], rank=rank, accuracy=newvalues2, i=i, a=a, ad=ad)



@app.route('/register', methods=['POST', 'GET'])
def register():
    f = request.form

    for key in f.keys():
        for value in f.getlist(key):
            print(key, ":", value)

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email': request.form['email']})
        if existing_user is None:
            # hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            hashpass = request.form['password']

            users.insert(
                {'email': request.form['email'], 'name': request.form['name'], 'password': hashpass, 'score': 0,
                 'attempts': 0, 'accuracy': 0})
            session['email'] = request.form['email']
            score = 0  # users['score']
            attempts = 0  # users['attempts']

            mail = []
            ad = users.find().sort("score", -1)
            i = 0
            rank = 0
            fg = 0

            for x in ad:
                fg += 1
                mail.append({'rank': fg, 'name': x['name'], 'email': x['email'], 'score': x['score']})
                i += 1
                print("ad = ", x)
                print(x['name'])
                if x['email'] == session['email']:
                    rank = i
                if fg == 5:
                    break
            print(mail)

            print("X Value")

            return render_template('register.html', score=score, name=request.form['name'], attempts=attempts,mail=mail,
                                   dbRecord=request.form['email'])
        return 'That email already exists!'


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user is None:
            err_string = "Invalid user name"
            print(err_string)
            return render_template('register.html', err_string=err_string)

        else:
            # if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user[
            #     'password']:
            if request.form['password'] == login_user['password']:
                session['email'] = request.form['email']

                mail = []
                ad = users.find().sort("score", -1)
                i = 0
                rank = 0
                fg = 0

                for x in ad:
                    fg += 1
                    mail.append({'rank': fg, 'name': x['name'], 'email': x['email'], 'score': x['score']})
                    i += 1
                    print("ad = ", x)
                    print(x['name'])
                    if x['email'] == session['email']:
                        rank = i
                    if fg == 5:
                        break
                print(mail)
                return render_template('index.html',mail=mail,rank=rank, score=login_user['score'], name=login_user['name'],
                                       attempts=login_user['attempts'], dbRecord=request.form['email'])
            else:
                err_string = "Invalid password"
                return render_template('register.html', err_string=err_string)

@app.route('/forgot1', methods=['POST', 'GET'])
def forgot1():
    print('forgot1 called')
    return render_template('forgot.html')

@app.route('/forgot_reset', methods=['POST', 'GET'])
def forgot_reset():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})
        if login_user is None:
            err_string = "email does not exits"
            print(err_string)
            return render_template('forgot.html', err_string=err_string)

        else:
            err_string = "your password has been sent to your registered email"
            password = login_user['password']
            email = EmailMessage()
            email['from'] = 'Challenge.com'
            email['to'] = request.form['email']
            email['subject'] = 'Your password'
            content = f"Your password is {password}"
            email.set_content(content)

            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('canucatch@gmail.com', 'dxvbpihxvgrmzcjl')
                smtp.send_message(email)
                print('Email sent with password')
            return render_template('forgot.html',err_string=err_string)

@app.route('/login2', methods=['POST', 'GET'])
def login2():
    print('fi')
    return render_template('register.html')
