import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet


def isALocation(word):
  word = word.replace(" ","_")
  synsets=wordnet.synsets(word)
  location = wordnet.synset('location.n.01')
  for s in synsets:
    for h in s.common_hypernyms(location):
      if location==h:
        return True
  
  return False

def isATimeIndicator(word):
  word = word.replace(" ","_")
  synsets=wordnet.synsets(word)
  time = wordnet.synset('time_period.n.01')
  for s in synsets:
    for h in s.common_hypernyms(time):
      if time==h:
        return True
  
  return False

def isMurder(word):
  word = word.replace(" ","_")
  word =word.replace("-","_")
  synsets=wordnet.synsets(word)
  if len(synsets)==0 :
    #It means that the program cannot find the meaning of the expression
    #we check that the error does not come from the fact that ther is several word 
    words_group=word.split('_')
    #if actually there are several words
    if len(words_group)>1:
        for w in words_group:
            return  isMurder(w)
  else :
    kill = [wordnet.synset('kill.v.01'),wordnet.synset('killer.n.01'),wordnet.synset('killing.n.02')]
    suicide =wordnet.synset('suicide.n.01')
    #first we check that it is not a word for suicide
    for s in synsets:
        if suicide==s:
            return False
        for h in s.common_hypernyms(suicide):
          if suicide==h:
            return  False 
    for s in synsets:
      for k in kill:
        for h in s.common_hypernyms(k):
          if k==h:
            return True
  return False

def isAPerson(word):
  word = word.replace(" ","_")
  synsets=wordnet.synsets(word)
  persons =[wordnet.synset('people.n.01'),wordnet.synset('person.n.01')]
  for s in synsets:
    for p in persons:
        for h in s.common_hypernyms(p): 
            if p==h:
                return True
  
  return False
