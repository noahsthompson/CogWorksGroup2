
import nltk, pickle as pkl
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import string
import time
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
        return nltk.word_tokenize(sentence)
    def getEntities(self,words):
        tokens=word_tokenize(words)
        pos = nltk.pos_tag(tokens)
        named_entities = nltk.ne_chunk(pos, binary=True)
        entities=[]
        for i in range(0, len(named_entities)):
            ents = named_entities.pop()
            if getattr(ents, 'label', None) != None and ents.label() == "NE": 
                entities.append(tuple([ne[0] for ne in ents]))
        return entities
    def add(self,doc,id):
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
        if not(id in self.id_entity_count.keys()):
            raise Exception("Not In Database")
        entities=(self.id_entity_count[id].keys())
        for entity in entities:
            self.entity_doc[entity].remove(id)
    def encode(self, entities, code):
        c=[]
        for entity in entities:
            c.append(code[entity])
        return c

    def associateEntity(self,entity,k=None):
        related=self.entity_relationships[entity].most_common(k)
        return unzip(related)[0]
    def associateTopic(self,topic,engine,context=5,out=5):
        ids=engine.query(topic)
        totalCount=Counter()
        for id in ids:
            if id in self.id_entity_count.keys():
                relatedEntity=self.id_entity_count[id].most_common(context)
                for e in relatedEntity.keys():
                    totalCount[e]+=1
        return totalCount.most_common(out)
         
    
        
    
