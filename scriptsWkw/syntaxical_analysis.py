
from semantic_tests import isMurder,isALocation,isATimeIndicator,isAPerson
import nltk
def postagAll(list_tok_sentences):#postag a list of tokenized sentences
    tagged_sentences=[]
    for t in list_tok_sentences:
        tagged_sentences.append(nltk.pos_tag(t))
    return tagged_sentences



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
    
def getVictims(analysed_VP):
    NP=getObject(analysed_VP)
    victims=[]
    for np in NP:
        person=False
        for word in nltk.word_tokenize(np):
            if isAPerson(word) or word[0].isupper():#if we find a word like people,children or a proper noun
                person=True
        if person:
            victims.append(np)
    return victims


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


# In[327]:


def getSubject(analysed_sentence):
    #we consider that the subject is a noun phrase which is not in a verb phrase or a circumstancial complement
    NE=getNE(analysed_sentence)
    for a in analysed_sentence.subtrees():
        if a.label()in['CIRC','VP'] :        
            for n in NE:
                found=True
                for word in n:
                    found=found and (word[0] in a.leaves())    #if we find the whole expression in the VP or CIRC found = true and we remove this named entity which is not the subject
                if found:
                    NE.remove(n)      
    return NE


