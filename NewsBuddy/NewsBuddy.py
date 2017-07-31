from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
from mySearchEngine import MySearchEngine
from EntityDatabase import entityDatabase
import newsScraper

app = Flask(__name__)
ask = Ask(app, '/')



def primeEntityDatabase(newss):
    ed=entityDatabase()
    for news in newss:
        try:
            print("adding")
            ed.add(news)
        except(Exception):
            print("whoops")
            pass
    print("done")
    return ed
def primeSearchEngine(newss):
    se=MySearchEngine()
    for news in newss:
        try:
            print("adding")
            se.add(news)
        except(Exception):
            print("whoops")
            pass
    print("done")
    return se
def formatList(entitylist,failb):
    entityString=""
    length=len(entitylist)
    for i in range(length):
        entity=""
        for j in entitylist[i]:
            entity+=" "+j
        if i < length-1:
            entityString+=entity+", "
        elif i == length-1 and length > 1 :
            if(failb):
                entityString+="and "+ entity
            else:
                entityString+="or "+ entity
        else:
            entityString+=entity
    return entityString
        
def updateEDatabase():
    newss=newsScraper.formatNews()
    ed=primeEntityDatabase(newss)
    return ed
def updateSearchEngine():
    newss=newsScraper.formatNews()
    print("done Scraping")
    se=primeSearchEngine(newss)
    return se
@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():

    msg = "What would you like to hear about?"
    return question(msg)

@ask.intent("WhatsNewIntent")
def get_whats_new(query):
    print("loading whats new")
    whatsNewStr=se.whatIsNew(query)
    print("returning")
    return statement(whatsNewStr)

@ask.intent("AssociateEIntent")
def get_EAssociation(entity):
    print("loading whats new")
    entitieslist=ed.associateEntity(entity,5)
    failb=entitieslist[1]
    el=entitieslist[0]
    if(not(entitieslist[1])):
        msg= "I'm sorry, I couldn't find any matches to that entity in my database. "
        if len(el) > 0:
            msg+="Would you like me to search for: "+formatList(el,failb)+" instead?"
        return question(msg)
    else:
        msg="I found the following entities that relate to your query: "+formatList(el,failb)
        return statement(msg)    
@ask.intent("AssociateTIntent")
def get_TAssociation(topic):
    print("loading whats new")
    entitieslist=ed.associateTopic(topic,se,out=5)
    if(len(entitieslist) == None):
        msg= "I'm sorry, I couldn't find any entitys that match that topic in my database. Would you like to try again?"
        return question(msg)
    else:
        msg="I found the following entities that relate to your query: "+formatList(entitieslist,True)
        return statement(msg)  
if __name__ == '__main__':
    print("initailizing SE")
    newss=newsScraper.formatNews()
    global se
    se=primeSearchEngine(newss)
    print("initailizing ED")
    global ed
    ed=primeEntityDatabase(newss)
    app.run(debug=True)
