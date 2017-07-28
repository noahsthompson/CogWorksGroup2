from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json


app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "What would you like to hear about?"
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)
