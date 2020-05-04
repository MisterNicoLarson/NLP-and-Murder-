#!/usr/bin/env python
# coding: utf-8

# In[307]:
import syntaxical_analysis,text_pretreatment
import nltk


def pickALetter(letter,text):
    sentences=text_pretreatment.purge(text) 
    sentences=text_pretreatment.secondPurgeAndTokenize(sentences)
    #We now have a tokenized text without all the XML structure elements
    cases= text_pretreatment.sortByCountries(sentences)
    copy_dict={}
    for country in cases :
        copy_dict[country]=syntaxical_analysis.postagAll(cases[country])   
    cases=copy_dict

    copy_dict3={}
    for country in cases:
        temp_list=[]
        for sentence in cases[country]:
            sentence=syntaxical_analysis.tagOF(sentence)
            sentence=syntaxical_analysis.tagYEAR(sentence)
            temp_list.append(sentence)
        copy_dict3[country]=temp_list
    cases=copy_dict3


    copy_dict4={}
    for country in cases:
        liste=[]
        for sentence in cases[country]:   
            liste.append(syntaxical_analysis.analyseSentence(sentence))
        copy_dict4[country]=liste
    cases=copy_dict4

    murders={}
    for country in cases:
        liste=[]
        for sentence in cases[country]:
            liste.append(syntaxical_analysis.getMurderInfo(sentence))
            #for each sentence we collect the verb-phrase about a murder
        murders[country]=liste



    copy_dict5={}
    for country in cases:
        small_dict={}
        for murders in cases[country]:
            killer=syntaxical_analysis.getSubject(murders) #we choose the first named entity as the nameof our Murderer
            if(len(killer)>0):
                small_dict[' '.join(killer[0])]=murders
        copy_dict5[country]=small_dict


    cases=copy_dict5


    # In[333]:


    file={}
    for country in cases :
        country_file={}
        for killer in cases[country]:
            killer_file={}
            murder_info=syntaxical_analysis.getMurderInfo(cases[country][killer])
            crime_time=''
            crime_place='in '+country+' '
            victims=''
            for m in murder_info:
                crime_time+=" , ".join(syntaxical_analysis.getTimes(m))
                crime_place+=" , ".join(syntaxical_analysis.getPlaces(m))
                victims+=" , ".join(syntaxical_analysis.getVictims(m))
                    
            killer_file['crime_time']=crime_time
            killer_file['crime_place']=crime_place
            killer_file['victims']=victims
            country_file[killer]=killer_file
        file[country]=country_file
                
            


    letter=letter.upper()
    data=""
    for country in cases:
        for killer in cases[country]:
            goodFirstLetter=False
            tok_name=nltk.word_tokenize(killer)
            for word in tok_name:
                if word[0].upper()==letter:
                    goodFirstLetter=True
            if goodFirstLetter:
                data+=(killer+" murdered "+file[country][killer]['victims']+", "+file[country][killer]['crime_place']+" , "+file[country][killer]['crime_time'])+"\n"
                    
    return data

# In[336]:

text = text_pretreatment.recuperationText('../M0M0/WhoKilledWho/listSerialKiller.xml')
print(pickALetter('J', text))
