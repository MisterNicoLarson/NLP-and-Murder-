#!/usr/bin/env python
# coding: utf-8

# In[307]:


# -*- coding: utf-8 -*-
from lxml import html
from lxml import etree
from nltk import word_tokenize
import xml.etree.ElementTree  as ET 
def recuperationText(path):
    # Entree : string qui est le chemin vers nos données XML
    # Sortie : l'objet de la balise soit un texte
    # Objectif : recuper un texte XML et le transformer en texte de string
    
    #Etape 1 : l'extraction des balise textes
    tree = etree.parse(path) # c'est le dossier dans lequel on a du XML
    root = tree.getroot() # permet de recuperer la racine
    childrenRoot = root.getchildren()
    liste = []
    for rdc in childrenRoot:
        for etage in rdc:
            #print(elt1.getchildren())
            captureText = etage.findall("{http://www.mediawiki.org/xml/export-0.10/}text")# captureText est une liste
            for textBalise in captureText:
                liste.append(textBalise.text)
    
    # Etape 2 : transformer la liste de texte en super texte
    megaText = " ".join(liste)
    
    #Renvoie le texte
    return megaText
#return list of sentences
def purge(doc):
    
    result = "";
    flag = True;
    
    for mot in doc:
        
        #on enlève les contenues informatiques du style {%fbhjeiud} ou <ref></ref>
        if mot == '{' or mot == '<':
            flag = False;
        elif mot == '}' or mot == '>':
            flag = True;
        elif flag:
            
            if (mot not in ['\'','[',']','=','|','*']):
                result += mot;
            
            #on retire ensuite les ponctuations inutiles
            #if mot not in [ ';' , ':' , '\'']:
                
    
    #le texte est enfin "nettoyé"
    #print(result)
    sentences=result.split('\n')
    return sentences
pathFile = "essai.xml"
path = "WhoKilledWho/listSerialKiller.xml"
text = recuperationText(path)
sentences=purge(text)


# In[308]:


import nltk
from semantic_tests import isALocation
from nltk import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
def secondPurgeAndTokenize(list_of_sentences):
    tok_sentences=[]
    for s in list_of_sentences :
        #delete the empty lines and tokenize the sentences
        if len(s)>0:
            tok_sentences.append(nltk.word_tokenize(s))
    return tok_sentences
sentences=secondPurgeAndTokenize(sentences)


# In[309]:


def sortByCountries(list_tok_sentences):#takes a list of tokenized sentences and return a dictionnary with cases indexed by countries
    liste=[]
    index='none'
    dicti={}
    for t in list_tok_sentences:
        #we store murder cases in a temporary list
        #we make a semantic test to check if the expression is not a location (country, city...)
        #In our corpus murders are presented by countries, so if we find a new single counrty name (like 'The Bahamas')
        #it means we have now the murders in Bahamas, so we store our list of murder in the dictionnary, 
        #indexed with the country which came before and we empty the list
        if isALocation('_'.join(t)): 
            #if the country is already in the list
            if index in dicti:
                dicti[index].extend(liste)
            else:
                dicti[index]=liste
            liste=[]
            index=' '.join(t) 
        else:
             liste.append(t)
    #we delete the introduction of the corpus (everything written before the first country) 
    del dicti['none']
    return dicti
def postagAll(list_tok_sentences):#postag a list of tokenized sentences
    tagged_sentences=[]
    for t in list_tok_sentences:
        tagged_sentences.append(nltk.pos_tag(t))
    return tagged_sentences
cases= sortByCountries(sentences)
copy_dict={}
for country in cases :
    copy_dict[country]=postagAll(cases[country])
    
cases=copy_dict


# In[310]:


#we are trying to tag Numbers which seems to be a year
def tagYEAR(tagged_sentence):
    copy=[]
    last_Prep=False#boolean to store if the word before the number is a Preposition or subordinating conjunction
    last_number=False #to store if we just found a number
    year=""
    for word in tagged_sentence:
        if last_Prep:#if we found a preposition then a number ther is a growing chance that this is a year
            if word[1]=="CD":
                last_number=True
                year= word[0]#we store the word
            elif last_number:
                if word[1]not in["NN","NNS","NNP","NNPS","JJ","JJS",'JJR']:# no noun or adjectives after to avoid expression like "in 12 cities"
                    copy.append((year,"YEAR"))#if there is no noun/adj after we tag it with "Year"
                    copy.append(word)
                else :#there is a noun/adj we tag it normally
                    last_number=False
                    last_Prep=False
                    copy.append((year,'CD'))
                    copy.append(word)            
            else: 
                last_Prep=False
                copy.append(word)
        elif word[1]in["IN",'TO']:
            last_Prep=True
            copy.append(word)
        else:
            copy.append(word)
    return copy
    
                    


# In[311]:


#We will try to handle issues with the preposition "of"
#so we creat a special tag for it
def tagOF(tagged_sentence):
    copy=[]
    for word in tagged_sentence:
        if word[0]in['de','of','von']:
            copy.append((word[0],'OF'))#creation of a special tag "OF" because there were a lot of issues in association 
            #like for exemple : (NP trial/NN)(CIRC for/IN (NP the/DT murders/NNS))(CIRC of/IN (NP five/CD elderly/JJ people/NNS)) "of five elderly peopleshould be associated with murder"
            #or Madame Truc de/von Machin                     
        else:
            copy.append(word)
    return copy


# In[312]:


copy_dict3={}
for country in cases:
    temp_list=[]
    for sentence in cases[country]:
        sentence=tagOF(sentence)
        sentence=tagYEAR(sentence)
        temp_list.append(sentence)
    copy_dict3[country]=temp_list
    


# In[313]:


cases=copy_dict3


# In[314]:


#As we have some problem with nltk.ne_chunks() we will try to build our own Named Entities Recognizer
#Therefore we'll use Regexp
#We also used it to analyse the structure of the sentence

#From nltk.org
#We  consider Named-Entities as a sequence of proper nouns
#But we can consider that if the name is with a determiner, a noun or a foreign word it is part of the name Exemple : Jack the Ripper

def analyseSentence(sentence):
    pattern = r"""
        NE: {<NNP|NNPS>+}
        NE: {<DT|JJ|JJS><NNP|NNPS|NE>+}
        NE: {<NE|NNP|NNPS><OF><NE|NNP|NNPS>}

        NP: {<DT|PP\$|CD>?<JJ|JJS>*<NN|NNS>+} #chunk determiner/possessive, adjectives and noun
        NP: {<DT|PP\$|CD><NP>+}    
        NP: {<NP><CC><NP>}#Defined separately so that two NP already found and bound by a CC can be considered as one NP
        NP : {<NP><OF><NP>}
        NE: {<NE><NP>}        
        CIRC :{<IN><DT>?<CD|NP|YEAR|NE>(<TO|CC><CD|NP|YEAR|NE>)*}#get the circumstance of the action
        
        VP:{<VBS|VBN|VBZ|VBG|VB|VBD>}
        VP:{<VP><CC><VP>}
        VP :{<VP><TO|OF>*<NP|NE>}
        VP : {<VP><CIRC>+}

    """
    cp = nltk.RegexpParser(pattern)
    return cp.parse(sentence)

#

#It would be interesting to detect the expression "also known as" to find the murderer nickname


# In[315]:


copy_dict4={}
for country in cases:
    liste=[]
    for sentence in cases[country]:   
        liste.append(analyseSentence(sentence))
    copy_dict4[country]=liste
    


# In[316]:


cases=copy_dict4


# In[317]:


def getVerbPhrases(analysed_sentence):
    verb_phrase=[]
    last_label_VP=False#We will avoid having several time the same verbphrase because an other one is intricated on a bigger one
    for a in analysed_sentence.subtrees():
        if a.label()=="VP":
            if not last_label_VP:
                verb_phrase.append(a)
            last_label_VP=True
        else:
            last_label_VP=False

    return verb_phrase


# In[318]:


from semantic_tests import isMurder,isALocation,isATimeIndicator
def getMurderInfo(analysed_sentence):#we will find and keep only the verb_phrases about the murders
    list_verb_phrases=getVerbPhrases(analysed_sentence)
    murders=[]#we can store several verb-phrases in case some criminal have been really...busy
    for a in list_verb_phrases:
        killed=False    #boolean storing if this verb phrase describe a murder
        if a.label()=="VP":
            for w in a.leaves():
                if isMurder(w[0]):
                    killed=True   
            if killed :
                murders.append(a)
    return murders
murders={}
for country in cases:
    liste=[]
    for sentence in cases[country]:
        liste.append(getMurderInfo(sentence))
    murders[country]=liste


# In[319]:


def getCircumstances(analysed_sentence):
    circ=[]
    last_label_CIRC=False#We will avoid having several time the same verbphrase because an other one is intricated on a bigger one
    for a in analysed_sentence.subtrees():
        if a.label()=="CIRC":
            if not last_label_CIRC:
                circ.append(a.leaves())
            last_label_CIRC=True
        else:
            last_label_CIRC=False

    return circ
circ ={}
for country in murders:
    liste=[]
    for facts in murders[country]:
        for f in facts:
            liste.extend(getCircumstances(f))
    circ[country]=liste


# In[320]:


def getPlaces(analysed_verbphrase):
    places=[]
    for a in analysed_verbphrase.subtrees():
        place_name=[]
        if a.label()=="CIRC":#we get all the circumstancial complement like 'In Ohahio','between 2001 and 2018'
            for s in a.subtrees():#We check the named entities
                if s.label()=="NE":
                    for w in s.leaves():
                        place_name.append(w[0])
                    if isALocation(' '.join(place_name)):#we found a location
                        place_name=[]
                        for word in a.leaves():
                            place_name.append(word[0])
                        places.append(' '.join(place_name))
                        
    return places  
places={}
for country in murders:
    liste=[]
    for facts in murders[country]:
        for f in facts:
            liste.append(getPlaces(f))
    places[country]=liste


# In[321]:


def getTimes(analysed_verbphrase):
    times=[]
    for a in analysed_verbphrase.subtrees():
        time=False
        period=[]
        if a.label()=="CIRC":#we get all the circumstancial complement like 'In Ohahio','between 2001 and 2018'
            for w in a.leaves():
                if (isATimeIndicator(w[0])or w[1]=="YEAR")and w[1]!="IN" :#if there is a time indicator or a year tag
                    time=True#We also check that we are not analysing the semantic of a preposition becaus
                    
            if time:
                for w in a.leaves():
                    period.append(w[0])
                times.append(' '.join(period))   
    return times 
times={}
for country in murders:
    liste=[]
    for facts in murders[country]:
        for f in facts:
            liste.append(getTimes(f))
    times[country]=liste


# In[322]:


def getNounPhrases(analysed_sentence):
    noun_phrase=[]
    last_label_NP=False#We will avoid having several time the same nounphrase because an other one is intricated on a bigger one
    for a in analysed_sentence.subtrees():
        if a.label()=="NP":
            if not last_label_NP:
                content=[]
                for w in a.leaves():
                    content.append(w[0])
                noun_phrase.append(content)
            last_label_NP=True
        else:
            last_label_NP=False

    return noun_phrase
def getObject(analysed_verbphrase):#we get all the noun phrases which are not in a circumstancial complement
    NP=getNounPhrases(analysed_verbphrase)#used to find the victim as the object of the action of killing
    verb_object=[]
    for a in analysed_verbphrase.subtrees():
        name=[]
        if a.label()in['CIRC'] :        
            for word in a.leaves():
                for n in NP:
                    found=False
                    if word[0] in n:
                        found=True
    for n in NP:
        verb_object.append(' '.join(n))
        
            
    return verb_object
    


# In[323]:


victims={}
for country in murders:
    liste=[]
    for killer in murders[country]:
        for facts in killer:
            liste.append(getObject(facts))
    victims[country]=liste
    


# In[324]:


print(victims['France'])


# In[325]:


#In English the common way to write a sentence is Subject Verb Complement 
def getNE(analysed_sentence):
    named_entities=[]
    last_label_NE=False#We will avoid having several time the same verbphrase because an other one is intricated on a bigger one
    for a in analysed_sentence.subtrees():
        if a.label()=="NE":
            if not last_label_NE:
                name=[]
                for w in a.leaves():
                    name.append(w[0])
                named_entities.append(name)
            last_label_NE=True
        else:
            last_label_NE=False

    return named_entities


# In[326]:


print(getNE(cases['France'][5]))
print(cases['France'][5])


# In[327]:


def getSubject(analysed_sentence):
    NE=getNE(analysed_sentence)
    subject=[]
    for a in analysed_sentence.subtrees():
        name=[]
        if a.label()in['CIRC','VP'] :        
            for word in a.leaves():
                for n in NE:
                    found=False
                    if word[0] in n:
                        found=True
            

    return NE
    


# In[328]:


print(getSubject(cases['France'][5]))


# In[329]:


boolean=True
for c in ['Chambet']:
    boolean= boolean and(c in['Ludivine', 'Chambet'])
boolean


# In[330]:


copy_dict5={}
for country in cases:
    small_dict={}
    for murders in cases[country]:
        killer=getSubject(murders) #we choose the first named entity as the nameof our Murderer
        if(len(killer)>0):
            small_dict[' '.join(killer[0])]=murders
    copy_dict5[country]=small_dict


# In[331]:


for country in copy_dict5:
    for killer in copy_dict5[country]:
        print(killer+':')
        print(copy_dict5[country][killer])


# In[332]:


cases=copy_dict5


# In[333]:


file={}
for country in cases :
    country_file={}
    for killer in cases[country]:
        killer_file={}
        murder_info=getMurderInfo(cases[country][killer])
        crime_time=''
        crime_place='in '+country+' '
        victims=''
        for m in murder_info:
            crime_time+=" , ".join(getTimes(m))
            crime_place+=" , ".join(getPlaces(m))
            victims+=" , ".join(getObject(m))
                
        killer_file['crime_time']=crime_time
        killer_file['crime_place']=crime_place
        killer_file['victims']=victims
        country_file[killer]=killer_file
    file[country]=country_file
            
        


# In[334]:


for country in file:
    for killer in file[country]:
        print(killer+" murdered "+file[country][killer]['victims']+",PLACE "+file[country][killer]['crime_place']+" ,TIME "+file[country][killer]['crime_time'])


# In[335]:


def pickALetter(letter):
    letter=letter.upper()
    for country in cases:
        for killer in cases[country]:
            goodFirstLetter=False
            tok_name=nltk.word_tokenize(killer)
            for word in tok_name:
                if word[0].upper()==letter:
                    goodFirstLetter=True
            if goodFirstLetter:
                print(killer+" murdered "+file[country][killer]['victims']+",PLACE "+file[country][killer]['crime_place']+" ,TIME "+file[country][killer]['crime_time'])


# In[336]:


pickALetter('J')


# In[299]:


print(cases['Antigua and Barbuda']['John Baughman'])


# In[ ]:




