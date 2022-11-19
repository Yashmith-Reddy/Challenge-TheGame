from flask_pymongo import PyMongo
from os import listdir
import os
from flask import Flask, render_template, url_for, request, redirect, flash, session
import bcrypt

app = Flask(__name__)
app.secret_key = 'yashmith'
app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)
@app.route('/')
def my_home():
    return render_template('See.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/download', methods=['GET', 'POST'])
def download():
        print("Downloading")


        files = mongo.db.files.find()
        print("Downloading")

        file_names = []

        for file in files:
            print(file['file_name'])
            file_name = file['file_name']
            file_names.append(file_name)
            print (file_names)

        #return redirect(url_for('download_file', file_name = file_name ))


        # return render_template("SelfDownloadFileList.html", files=files, file_name=file_name)
        return render_template('selfDownloadFileList.html')
@app.route('/download_file/<file_name>', methods=['POST', 'GET'])
def download_file(file_name):
    print(download_file)
    return mongo.send_file(file_name)

if __name__ == '__main__':
    app.run(debug=True)

