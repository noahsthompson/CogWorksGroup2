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


def unzip(pairs):
    """Splits list of pairs (tuples) into separate lists.
    
    Example: pairs = [("a", 1), ("b", 2)] --> ["a", "b"] and [1, 2]
    
    This should look familiar from our review back at the beginning of week 1
    :)
    """
    return tuple(zip(*pairs))
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
def formatHeadlines(headlines):
    headlineOut=""
    length=len(headlines)
    for h in range(length):
        headl=headlines[h].replace("\n",", ")
        headlineOut+=headl+". "
    return headlineOut
        
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
    
    session.attributes["lastIntent"]="WhatsNewIntent"
    session.attributes["lastIntentData"]={}
    print("loading whats new")
    print(query)
    whatsNew=se.whatIsNew(query)
    print(whatsNew)
    
    if(whatsNew==None):
        return statement("I couldn't find any matches to your query in my database")
    numberOfHeadlines=len(unzip(whatsNew)[1])
    session.attributes["lastIntentData"]["Headlines"]=unzip(whatsNew)[1]
    session.attributes["lastIntentData"]["IDs"]=unzip(whatsNew)[0]
    session.attributes["lastIntentData"]["length"]=numberOfHeadlines
    whatsNewStr=formatHeadlines(unzip(whatsNew)[1])
    print("returning")
    if(numberOfHeadlines>1):
        whatsNewStr+="Would you like to hear more about any of these headlines"
    else:
        whatsNewStr+="Would you like to hear more about this headline"
    return question(whatsNewStr)
@ask.intent("TellMeMoreIntent")
def tellMeMore(Headlines=None,ID=None,length=None,number=None, keywords=None):

    if(session.attributes["lastIntent"]=="WhatsNewIntent"):
        if(Headlines==None):
            Headlines=session.attributes["lastIntentData"]["Headlines"]
        if(ID==None):
            ID=session.attributes["lastIntentData"]["IDs"]
        if(length==None):
            length=session.attributes["lastIntentData"]["length"]
        print("printing Numbers?")
        if( number != None):
            number=int(number)
        print(number)

        print("printing Keywords?")
        print(keywords)
        print("printing Headlines")
        print(Headlines)
        print("printing ID")
        print(ID)
        if(length==1):
            return statement(se.get(ID[0]))
        elif(number == None and keywords ==None):
            return question("Please specify which article to read")
        elif(number != None):
            if(number-1)>= 0 and (number-1)<length:
                return statement(se.get(ID[number-1]))
            else:
                return statement("That number is not in the appropret range of headlines")
        elif(keywords != None):
            headlineSearch=MySearchEngine()
            for i in range(length):
                headlineSearch.add(Headlines[i],ID[i])
            tId=headlineSearch.query(keywords)
            print(tId)
            if(len(tId) <= 0):
                return statement("No document matches those keywords")
            else:
                return statement(se.get(tId[0][0]))                      
        return statement("Sorry?")
@ask.intent("YesIntent")
def yesHandler():
    print(session.attributes["lastIntent"])
    if(session.attributes["lastIntent"]=="WhatsNewIntent"):
        Headlines=session.attributes["lastIntentData"]["Headlines"]
        Ids=session.attributes["lastIntentData"]["IDs"]
        length=session.attributes["lastIntentData"]["length"]
        if(length == 1):
            return tellMeMore(Headlines,Ids,length)
        return statement("Could you specify which article you'd like to hear more about")
    elif(session.attributes["lastIntent"]=="AssociateEIntent"):
        el=session.attributes["lastIntentData"]["entityList"]
        if(not(session.attributes["lastIntentData"]["failb"])):
            if(len(el)>1):
                return question("Try again, but specify which entity you'd like me to search")
            elif(len(el)==1):
                return get_EAssociation(el[0])
            else:
                return statement("Yes?")
        else:
            return statement("Yes?")
    elif(session.attributes["lastIntent"]=="AssociateTIntent"):
        if(not(session.attributes["lastIntentData"]["Failbool"])):
            return statement("Please try again with another topic")
        else:
            return statement("Yes?")
        
@ask.intent("AssociateEIntent")
def get_EAssociation(entity):
    session.attributes["lastIntent"]="AssociateEIntent"
    session.attributes["lastIntentData"]={}
    print("loading whats new")
    entitieslist=ed.associateEntity(entity,5)
    failb=entitieslist[1]
    el=entitieslist[0]
    session.attributes["lastIntentData"]["failb"]=failb
    session.attributes["lastIntentData"]["entityList"]=el
    
    if(not(entitieslist[1])):
        msg= "I'm sorry, I couldn't find any matches to that entity in my database. "
        if len(el) > 0:
            msg+="Would you like me to search for: "+formatList(el,failb)+" instead?"
            return question(msg)
        else:
            return statement(msg)
    else:
        msg="I found the following entities that relate to your query: "+formatList(el,failb)
        return statement(msg)    
    
@ask.intent("AssociateTIntent")
def get_TAssociation(topic):
    session.attributes["lastIntent"]="AssociateTIntent"
    session.attributes["lastIntentData"]={}
    print("loading whats new")
    entitieslist=ed.associateTopic(topic,se,out=5)
    if(len(entitieslist) == None):
        session.attributes["lastIntentData"]["Failbool"]=False
        msg= "I'm sorry, I couldn't find any entitys that match that topic in my database. Would you like to try again?"
        return question(msg)
    else:
        session.attributes["lastIntentData"]["Failbool"]=True
        msg="I found the following entities that relate to your query: "+formatList(entitieslist,True)
        return statement(msg)  
if __name__ == '__main__':
    print("getting news")
    newss=newsScraper.formatNews()
    print("initailizing SE")
    global se
    se=primeSearchEngine(newss)
    print("initailizing ED")
    global ed
    ed=primeEntityDatabase(newss)
    app.run(debug=True)
