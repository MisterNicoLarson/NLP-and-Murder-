# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
from nltk import *
import re
import nltk
import xml.etree.ElementTree  as ET

kill = [ "kill" , "dismember" , "murder" , "strangle" , "assasinate"]
cible = [ "him" , "her" , "them" , "by" ]

"""Fonction"""

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

def tokenTag(doc):
    # Entree : un texte
    # Sortie : une liste de token avec leur tag
    # Objectif : transformer un texte en une liste de token pour pouvoir tagger cette liste
    doc = nltk.word_tokenize(doc)
    doc = nltk.pos_tag(doc)
    return doc


# on va retirer tout ce qui va compliquer inutilement la lecture
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
            
            if (mot not in ['\'','[',']','=']):
                result += mot;
            
            #on retire ensuite les ponctuations inutiles
            #if mot not in [ ';' , ':' , '\'']:
                
    
    #le texte est enfin "nettoyé"
    #print(result)
    return result


#Conserve et transforme les verbes et nom en léxème,
#Isole les noms propres et les associes en groupe
def tri(doc):
    
    nom_propre = ["NNP"]
    nom_commun = ["NNS"]
    verbes = ["VBS","VBN","VBZ","VBG","VB" , "VBD"]
    
    list1 = []
    list2 = []
    
    ING = re.compile('.*ing$',re.IGNORECASE)
    ED = re.compile('.*ed$',re.IGNORECASE)
    YY = re.compile('.*y$',re.IGNORECASE)
    
    KK = re.compile('.*k$',re.IGNORECASE)
    SS = re.compile('.*s$',re.IGNORECASE)
    VV = re.compile('.*v$',re.IGNORECASE)
    

    flag1 = False

    identite = ""

    nb = -1
    step = 0
    
    for mot in doc:
        
        nb += 1
        
        lexeme = mot[0]
        classe = mot[1]
        
        lien = re.compile('Category(:[0-9]{4})?',re.IGNORECASE)
        lien1 = re.compile('.*\|.*',re.IGNORECASE)
            
        
        if (not lien.match(lexeme)) and (not lien1.match(lexeme)) :
            
        
            #TRAITEMENT DES NOMS
            if classe in nom_commun:
                
                if SS.match(lexeme):
                    longueur4 = len(lexeme) - 1
                    lexeme = lexeme[:longueur4]
                    
                if ING.match(lexeme):
                        longueur1 = len(lexeme) - 3
                        lexeme = lexeme[:longueur1]
                
                
            #TRAITEMENT DES VERBES
            #on transforme en léxème tous les verbes
            if classe in verbes:

                    
                if ING.match(lexeme) or ED.match(lexeme):
                            
                    if ING.match(lexeme):
                        longueur1 = len(lexeme) - 3
                        lexeme = lexeme[:longueur1]
                                
                if YY.match(lexeme):
                    longueur2 = len(lexeme) - 1
                    lexeme = lexeme[:longueur2]
                    lexeme = lexeme + 'ie'
                                
                elif ED.match(lexeme):
                    longueur3 = len(lexeme) - 2
                    lexeme = lexeme[:longueur3]
                            
                if KK.match(lexeme) or SS.match(lexeme) or VV.match(lexeme):
                    lexeme = lexeme + 'e'
                            
                elif SS.match(lexeme):
                    longueur4 = len(lexeme) - 1
                    lexeme = lexeme[:longueur4]
            
                
                
            #TRAITEMENT DES NOMS_PROPRES
            if classe in nom_propre:
                if flag1 == False:
                    flag1 = True
                    identite = lexeme
                else:
                    identite += " " + lexeme
                    
            elif flag1:
                flag1 = False
                
                if (not list2):
                    list2.append(identite)
                    flag2 = True
                    
                    
                    if lexeme not in [',' , 'and']:
                        list1.append(list2)
                        list2 = []
                        flag2 = False
                    
                    
                else:
                        
                    if ((nb - step - 1) < 5):
                        list2.append(identite)
                        flag2 = True
                        
                    else:
                        list1.append(list2)
                        list2 = []
                        list2.append(identite)
                        flag2 = False
                
                step = nb
                  
                  
            if (lexeme in ['.' , ';' , ':' , 'by']):
                nb += 50
            
            #TRAITEMENT GENERAL
            if (lexeme in kill):
                flag2 = True
                if (flag1 == False):
                    list1.append(list2)
                    list2 = []
                    list2.append(lexeme)
                else:
                    list2.append(lexeme)
                    list1.append(list2)
                    list2 = []
            elif (lexeme in cible) and (flag2):
                flag2 = False
                if (not list2):
                    list2.append(lexeme)
                    list1.append(list2)
                    list2 = []
                else:
                    list1.append(list2)
                    list2 = []
                    list2.append(lexeme)
            else:
                flag2 = False
                

    return list1


def association(doc):
    victim = []
    result = []
    flag1 = False
    
    for group in doc:
        
            if (not group) == False:
                
                if len(group) > 1:
                    victim = group
                    
                elif (group[0] not in kill) and (group[0] not in cible):
                    victim = group
                    
                if flag1:
                    if (group[0] in cible):
                        result.extend(victim)
                    elif (group[0] not in kill):
                        result.extend(victim)
                
                flag1 = (group[0] in kill)
                
    return result
      
      
#Lecture de fichers en tapant le nom du tueur
"""
nom_tueur = input()
nom_tueur.strip()
txt = nom_tueur.replace(' ','_')
text1 = txt + '.xml'
"""
#text1 = "Chandrakant_Jha.xml"
text1 = "enSK.xml"


#Traitements...

text2 = purge(recuperationText(text1))
text3 = tokenTag(text2)
text4 = tri(text3)
text5 = association(text4)
print(text5)