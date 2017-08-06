from flask import Flask
from flask_ask import Ask, statement, question, session
import requests
import time
import unidecode
import json
from mySearchEngine import MySearchEngine
from EntityDatabase import entityDatabase
import newsScraper
import tldrskill
import hashlib

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
    """Given a list of articles, adds each article to the entity database.
        Params
        ------
        newss(list(str)): List of articles to be added to database
        Returns
        -------
        Entity database primed with articles
        """
    ed=entityDatabase()
    for news in newss:
        print("adding")
        ed.add(news)
    print("done")
    return ed
def primeHLD(newss):
    """Given the news(headline,document), maps each headline to article ID
        Params
        ------
        newss(list(tuple(str,str))): List of headline and their corrisponding articles
        Returns
        -------
        dict(ID:headline): returns database of ID's mapped to headlines."""
    hld={}
    for news in newss:
        hld[hashlib.sha224(news[1].encode('UTF-8')).hexdigest()]=news[0]
    return hld
    
def primeSearchEngine(newss):
    """Given a list of articles, adds each article to the search engine database.
        Params
        ------
        newss(list(str)): List of articles to be added to database
        Returns
        -------
        MySearchEngine():Search engine primed with the articles
        Note
        ----
        """
    se=MySearchEngine()
    for news in newss:
        print("adding")
        se.add(news)
    print("done")
    return se
def formatList(entitylist,failb):
    """Formats the entity list returned by get_EAssociation and get_TAssociation into readable string.
        Params
        ------
        entitylist:List(str), list of entitys.
        failb:(boolean) parameter that determines whether the last entity is preceded by an "and" or "or". Mainly used by 
        get_EAssociation, which returns a list of associations(which use "and") if it succeeds, of a list of suggestions(which
        use "or") if it fails.
        Return
        ------
        (str) readable string representation of entitys"""
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
    """formats headline list into readable string
        Params
        ------
        headlines(list(str)):list of headlines
        Returns
        -------
        (str)formatted headline string"""
    headlineOut=""
    length=len(headlines)
    for h in range(length):
        headl=headlines[h].replace("\n"," ")
        headlineOut+=headl+". "
    return headlineOut
        
def updateEDatabase():
    """Updates Entity Database with latest submissions
        Returns
        -------
        Updates Entity Database database"""
    newss=newsScraper.formatNews()
    ed=primeEntityDatabase(newss)
    return ed
def updateSearchEngine():
    """Updates Search Engine with latest submissions
        Returns
        -------
        Updates Search Engine database"""
    newss=newsScraper.formatNews()
    print("done Scraping")
    se=primeSearchEngine(newss)
    return se
@app.route('/')
def homepage():
    """Hompage of app"""
    return "Hello, this is news buddy"

@ask.launch
def start_skill():
    """start point: The first question upon launching skill, also the point newsbuddy returns to if it gets confused 
        with user inputs.
        Returns
        -------
        (str):"what would you like to hear about
        """
    msg = "What would you like to hear about?"
    return question(msg)

@ask.intent("WhatsNewIntent")
def get_whats_new(query=None,sindex=0):
    """Intent activated when the user posits a "Whats new" query (ie whats new, whats new with X)
        Params:
        query(str): String containing keywords to search in the search engine.
        sindex(int(optional,default=0)): Index which indicates what article to start reading
       Returns
       -------
       question: Headlines that match users query if one is given, or just recent headlines if one is not given. If query is not
       found in search engine, returns "I couldn't find any matches to your query in my database".
       Saves
       -----
       Saves intent name to key "last intent", saves dictionary {"Headline":(*list of headlines*),"IDs":(*list hash IDs that
       correspond to the document of each headline*),"length":(int corrisponding to the number of headlines that the query
       returned)} to "lastIntentData". Also saves the starting index of the query to 0. If query is given but no matches are
       found, then the function will save nothing.
       """
    if sindex == None:
        sindex=0
    session.attributes["lastIntent"]="WhatsNewIntent"
    session.attributes["lastIntentData"]={}
    whatsNew=se.whatIsNew(query,startindex=sindex)
    if(whatsNew==None):
        session.attributes.pop("lastIntent")
        session.attributes.pop("lastIntentData")
        return question("I couldn't find any matches to your query in my database")
    headlines=[]
    for id in whatsNew:
        headlines.append(hld[id])
    
    numberOfHeadlines=len(whatsNew)
    session.attributes["lastIntentData"]["Headlines"]=headlines
    session.attributes["lastIntentData"]["IDs"]=whatsNew
    session.attributes["lastIntentData"]["length"]=numberOfHeadlines
    session.attributes["lastIntentData"]["index"]=sindex
    session.attributes["lastIntentData"]["query"]=query
    whatsNewStr=formatHeadlines(headlines)
    print("returning")
    if(numberOfHeadlines>1):
        whatsNewStr+="Would you like to hear more about any of these headlines"
    else:
        whatsNewStr+="Would you like to hear more about this headline"
    return question(whatsNewStr)
#                t=tldrskill.tldr()
 #               t.add(se.get(ID[number-1]))
@ask.intent("summarizeIntent")
def summarize(Headlines=None,ID=None,length=None,number=None, keywords=None):
        """Based off tellMeMore, but instead of returning the full doc, it only prints out the summerized doc".
        Params
        ------
        Headlines(list(str)(optional,default=None)): Because tell me more can be called by other functions outside of just the
        intent, optional
        variables have been included. If they are not given, then the function will assume the previous intent stashed them
        inside session.attributes["lastIntentData"], and try to recover Headline, ID, and length from there. Headline is a list
        of headline(in string form).
        ID(list(str)(optional,default=None)): Hashes corresponding to headline's document in search engine and entity database.
        length(int(optional,default=None)):Length of list of headlines. Comes in handy for automated features and preseving
        correct grammer.
        number(int/string(optional,default=None)):The number in the list of headlines to target, if given, tell me more will
        target the document corresponding with that headline.
        keywords(str(optional,default=None)): String of keywords in headline. If given, tell me more will search through the
        headlines to find the best match to the keywords and target its corresponding document. However, if the [lastintent] is 
        not "WhatsNewIntent", then it will return the result of a whats new query for those keywords.
        Returns
        -------
        (question): If number is given, then the summerized document corrisponding to the headline at the nth position,otherwise, 
        If keywords are given, then the summerized document corrisponding to the best match of the keywords over the headlines, 
        else, if neither are given, then will ask user to be more specific"""
        tellMeMore(Headlines,ID,length,number,keywords)
        if not( "lastIntentData" in session.attributes.keys()):
            return start_skill()
        elif(not("targetID" in session.attributes["lastIntentData"].keys())):
            return question("Please correctly specify which article to read")
        elif("targetID" in session.attributes["lastIntentData"].keys()):
            ID=session.attributes["lastIntentData"]["targetID"]
            t=tldrskill.tldr()
            t.add(se.get(ID))
            return question(t.get_summs())
@ask.intent("TellMeMoreIntent")
def tellMeMore(Headlines=None,ID=None,length=None,number=None, keywords=None):
    """Handels ambigous important phrase "tell me more".
        Params
        ------
        Headlines(list(str)(optional,default=None)): Because tell me more can be called by other functions outside of just the
        intent, optional
        variables have been included. If they are not given, then the function will assume the previous intent stashed them
        inside session.attributes["lastIntentData"], and try to recover Headline, ID, and length from there. Headline is a list
        of headline(in string form).
        ID(list(str)(optional,default=None)): Hashes corresponding to headline's document in search engine and entity database.
        length(int(optional,default=None)):Length of list of headlines. Comes in handy for automated features and preseving
        correct grammer.
        number(int/string(optional,default=None)):The number in the list of headlines to target, if given, tell me more will
        target the document corresponding with that headline.
        keywords(str(optional,default=None)): String of keywords in headline. If given, tell me more will search through the
        headlines to find the best match to the keywords and target its corresponding document. However, if the [lastintent] is 
        not "WhatsNewIntent", then it will return the result of a whats new query for those keywords.
        Returns
        -------
        (question): If number is given, then the full document corrisponding to the headline at the nth position, otherwise,
        If keywords are given, then the full document corrisponding to the best match of the keywords over the headlines, else,
        if neither are given, then will ask user to be more specific"""
    if not( "lastIntent" in session.attributes.keys()):
        return start_skill()
    if(session.attributes["lastIntent"]=="WhatsNewIntent"):
        if(Headlines==None):
            Headlines=session.attributes["lastIntentData"]["Headlines"]
        if(ID==None):
            ID=session.attributes["lastIntentData"]["IDs"]
        if(length==None):
            length=session.attributes["lastIntentData"]["length"]
        if( number != None):
            number=int(number)
        if(length==1):
            session.attributes["lastIntentData"]["targetID"]=ID[0]
            return question(se.get(ID[0]))
        elif(number == None and keywords ==None):
            session.attributes["lastIntentData"]["index"]+=5
            return get_whats_new(session.attributes["lastIntentData"]["query"],session.attributes["lastIntentData"]["index"])
        elif(number != None):
            if(number-1)>= 0 and (number-1)<length:
                session.attributes["lastIntentData"]["targetID"]=ID[number-1]
                return question(se.get(ID[number-1]))
            else:
                return question("That number is not in the appropriate range of headlines")
        elif(keywords != None):
            headlineSearch=MySearchEngine()
            for i in range(length):
                headlineSearch.add(Headlines[i],ID[i])
            tId=headlineSearch.query(keywords)
            print(tId)
            if(len(tId) <= 0):
                return question("No document matches those keywords")
            else:
                session.attributes["lastIntentData"]["targetID"]=tId[0][0]
                if(se.get(tId[0][0])==None or se.get(tId[0][0])==[]):
                    return question("No document matches those keywords")
                return question(se.get(tId[0][0]))                      
        return question("Sorry?")
    
@ask.intent("YesIntent")
def yesHandler():
    """Handles ambigous responce "yes", depending on the previous intents
       Returns
       -------
       question(): If the last intent is not in session.attributes, then it will return to the start skill.
                   If the intent is activated after "WhatsNewIntent", and the length of the headline list is one,
                   then it returns the tellMeMore of that single document, otherwise it asks user to be more specific.
                   If the last intent is AssociateEIntent, then it checks session.attributes["lastIntentData"] to see if 
                   that association failed, in which case it is assumed the user is responding to "would you like me to search
                   for X instead", in which case if the lenght of the entitylist stashed by AssociateEIntent is one, it will
                   return the AssociateEIntent of that entity, otherwise it will ask user to be more specific. If
                   AssociateEIntent did not fail, then it returns to the start skill. Else, if yes intent is called with
                   AssociateTIntent, it will check to see if it failed too. If it did, then it will ask the user to specify
                   what entity to search. Otherwise, if AssociateTIntent did not fail, it will return to startskill. 
                   """
    if not( "lastIntent" in session.attributes.keys()):
        return start_skill()
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
                return start_skill()
        else:
            return start_skill()
    elif(session.attributes["lastIntent"]=="AssociateTIntent"):
        if(not(session.attributes["lastIntentData"]["Failbool"])):
            return question("Please try again with another topic")
        else:
            return start_skill()
    return start_skill()

@ask.intent("associateIntent")
def associate(query):
    if query in ed.entity_doc.keys():
        return get_EAssociation(query)
    elif query in se.doc_freq.keys():
        return get_TAssociation(query)
    else:
        return get_EAssociation(query)
@ask.intent("AssociateEIntent")
def get_EAssociation(entity):
    """Gets the entities related to entity in entity database. If no matches returned, then it will return a list of close
        matches
        Params
        ------
        entity(str):entity query to search the database.
        Returns
        -------
        question(): The formatted string of entitys found is the query was successful. If the query failed to find matches, it
        will return a apology and ask the user if it would like to search the close matches found in the database. If there are
        no close matchs, it will just return an apology.
        Saves
        -----
        Will save session.attributes["lastIntent"]="AssociateEIntent", and also will save the failure state(did query
        fail/succeed) in session.attributes["lastIntentData"]["failb"]=failb, and saves entity list (either related entitys
        if failb=True, or close matches if failb=False) to session.attributes["lastIntentData"]["entityList"].
        
        """
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
    """Gets the entitys related to a certain topic. IF no matches found, will just apologise. 
       Params
       ------
       topic: topic to query search engine with.
       Return
       ------
       question(): If successful, then it will return a list of entitys. If not, then it return an apology
       Saves
       -----
       saves session.attributes["lastIntent"]="AssociateTIntent", also saves fail state(did query fail/succeed) 
       to session.attributes["lastIntentData"]["failb"], and saves entitys to session.attributes["lastIntentData"]
       ["entityList"]."""
    session.attributes["lastIntent"]="AssociateTIntent"
    session.attributes["lastIntentData"]={}
    print("loading whats new")
    entitieslist=ed.associateTopic(topic,se,out=5)
    if(len(entitieslist) == None):
        session.attributes["lastIntentData"]["failb"]=False
        session.attributes["lastIntentData"]["entityList"]=[]
        msg= "I'm sorry, I couldn't find any entitys that match that topic in my database. Would you like to try again?"
        return question(msg)
    else:
        session.attributes["lastIntentData"]["entityList"]=entitieslist
        session.attributes["lastIntentData"]["failb"]=True
        msg="I found the following entities that relate to your query: "+formatList(entitieslist,True)
        return statement(msg)  

if __name__ == '__main__':
    print("getting news")
    newss=newsScraper.formatNews()
    print("initailizing SE")
    global se
    se=primeSearchEngine(unzip(newss)[1])
    print("initailizing ED")
    global ed
    ed=primeEntityDatabase(unzip(newss)[1])
    global hld #Headline database
    hld=primeHLD(newss)
    print(hld)
    app.run(debug=True)
