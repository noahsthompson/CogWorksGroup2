
import nltk, pickle as pkl
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import string
import time
import itertools
import hashlib
def unzip(pairs):
    """Splits list of pairs (tuples) into separate lists.
    
    Example: pairs = [("a", 1), ("b", 2)] --> ["a", "b"] and [1, 2]
    
    This should look familiar from our review back at the beginning of week 1
    :)
    """
    return tuple(zip(*pairs))
class entityDatabase():
    def __init__(self):
        #Document ID to Counter of entities in doc
        self.id_entity_count={}
        #Entity to set of IDs of docs that contain that entity
        self.entity_doc=defaultdict(set)
        #dictionary of counts 
        self.entity_relationships=defaultdict(Counter)
    def tokenize(self,text):
        """" Tokenizes text
             param: text(str) - the string to be tokenized
             return: (list(str) - the list of tokens)
             """
        return nltk.word_tokenize(text)
    def getEntities(self,words):
        """Gets the list of entities in a text
           Param: words(str/list(str)) - String or list of tokens to find the entities in
           Return: (list(tuple(str)) - A list of tuples, where each tuple is a tokenized entity
           """
        if (isinstance(words,str)):
            tokens=word_tokenize(words)
            print(tokens)
        else:
            tokens=words
        pos = nltk.pos_tag(tokens)
        print(pos)
        named_entities = nltk.ne_chunk(pos, binary=True)
        print(named_entities)
        entities=[]
        for i in range(0, len(named_entities)):
            ents = named_entities.pop()

            if getattr(ents, 'label', None) != None and ents.label() == "NE": 
                entities.append(tuple([(ne[0].lower()) for ne in ents]))
        print(entities)
        return entities
    
    def add(self,doc,id=None):
        """Adds all entities in doc to database, relates each entity to document id and each entity in the doc to each other
            Params: doc(str)- The document to be added
                    id(str)(optional, default=None)- Unique id for document in database. If none, database will generate a 
                    SHA224 hash on the document for the id.
            Returns: None
            """
        if id == None:
            id=hashlib.sha224(doc.encode('UTF-8')).hexdigest()
        if id in self.id_entity_count.keys():
            raise Exception("Already In Database")
        entities=self.getEntities(doc)
        self.id_entity_count[id]=Counter(entities)
        
        for entity in entities:
            self.entity_doc[entity].add(id)
            for e in entities:
                if(e != entity):
                    self.entity_relationships[entity][e]+=1
          
        
            
    def remove(self,id):
        """Removes all traces of doc from database
            Params: id(str)-id of document to be removed.
            Returns: None
            """
        if not(id in self.id_entity_count.keys()):
            raise Exception("Not In Database")
        entities=list(self.id_entity_count[id].keys())
        print(entities)
        for entity in entities:
            self.entity_doc[entity].remove(id)
            for e in entities:
                if(e != entity):
                    self.entity_relationships[entity][e]-=1
                    if self.entity_relationships[entity][e] == 0:
                        self.entity_relationships[entity].pop(e)
            if len(self.entity_relationships[entity]) ==0:
                self.entity_relationships.pop(entity)
            if len(self.entity_doc[entity]) == 0:
                self.entity_doc.pop(entity)
        
    
    def associateEntity(self,entity,k=None):
        """Associates entity in database to entitys that appear in a similar context.
           Params:entity(str/tuple(str))- target entity. Can either be a string (assumes full
                  string is one entity) or an entity(a tuple of strings).
                  k(int)- Number of entitys returned, in order of most related to least related. If none, return all
                  relations. Will not return entitys with relation score equal to 0.
           Return:(tuple(list(tuple(str),bool)- Returns a tuple containing a list of related entitys(tuples of strings) and a
                   boolean indicating whether the association failed. The association is "failed" if the target entity is not
                   found in the database, in which case the function will return a list of close matches(entitys that contain)
                   elements similar to the target entity (ie if the target entity ("Donald") is not found in the database, but
                   the database does contain entities ("Donald","Trump") and ("Donald", "Glover") the function will return 
                   ([("Donald","Trump"),("Donald","Glover")],False), indicating it has failed to find a perfect match, but
                   managed to find 2 partial matches. If the database contained a reference to ("Donald"), it will return
                   ([**list of related entitys**],True)).
           Notes: This function is basically a suped up wrapper for getRelatedEntity, made specifically for integration with
           Alexia.(faulty abstraction)
           """
        print(entity)
        if(isinstance(entity,str)):
            tokens=self.tokenize(entity)
            tokens=[tokens[i].lower().capitalize() for i in range(len(tokens))]
            es=self.getEntities(tokens)
            if len(es)>0:
                entity=self.getEntities(tokens)[0]
            else:
                entity=tuple(tokens)
        else:
            entity=tuple([e.lower() for e in entity])
        print(entity)
        
        entities=list(self.entity_relationships.keys())
        if entity in entities:
            return (self.getRelatedEntity(entity,k),True)
        else:
            out=[]
            for e in entities:
                for token in entity:
                    if token in e and not(e in out):
                        out.append(e)
            return (out,False)
            
    def getRelatedEntity(self,entity,k=None):
        """Takes an entity, finds related entities
            Params: Entity(tuple(str))- Target entity
                    k(int)(optional,default=None)- Number of entitys returned, in order of most related to least related. If
                    none, return all relations. Will not return entitys with relation score equal to 0.
                    """
        if not(entity in self.entity_relationships.keys()):
            raise Exception("Entity Not In Database")
        related=self.entity_relationships[entity].most_common(k)
        return [i[0] for i in list(itertools.filterfalse(lambda x:x[1]<=0,related))]
        
    def associateTopic(self,topic,engine,context=5,out=5):
        """Gets entities related to a topic
            Params: topic(str)- topic to relate to entities.
                    engine(searchEngine)- engine to search topic on. Document Ids returned will be cross referenced with entity
                    database, and the most referenced entity across the documents will be returned.
                    context(int)(Optional, default=5)- The number of entitys per document (ranked by frequency) to be
                    considered
                    out(int)(Optional, default=5)- The number of entities to be returned, ranked by how much each occurs across
                    the documents
            Returns: list(tuple(str))- list of related entitys
            Notes: Algorithim needs to be tweeked, a document with an overwhelming amount of one entity can unfairly shift
            balances
            """

        ids=engine.query(topic)
        if(len(ids) == 0):
            return None
        ids=unzip(ids)[0]
        totalCount=Counter()
        for id in ids:
            if id in self.id_entity_count.keys():
                relatedEntity=self.id_entity_count[id].most_common(context)
                if(len(relatedEntity) == 0):
                    continue
                relatedEntity=unzip(relatedEntity)[0]
                for e in relatedEntity:
                    totalCount[e]+=1
        return unzip(totalCount.most_common(out))[0]
         
    
        
    
