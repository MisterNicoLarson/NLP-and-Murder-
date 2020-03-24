# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
from nltk import *
import xml.etree.ElementTree  as ET 

"""Fonction XML"""

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

"""Fonction pre-traitement"""
def tokenTag(doc):
    # Entree : un texte
    # Sortie : une liste de token avec leur tag
    # Objectif : transformer un texte en une liste de token pour pouvoir tagger cette liste
    doc = nltk.word_tokenize(doc)
    doc = nltk.pos_tag(doc)
    return doc

def verbeList(textTokenizer):
    # Entree : prends un texte tokenizer
    # Sortie : renvoie une liste de verbe 
    # Objectif : recuperer tout les verbes 
    listeVerbe = []
    for elt in textTokenizer:
        if elt[1] == "VB" :
            listeVerbe.append(elt[0])
        if elt[1] == "VBD" :
            listeVerbe.append(elt[0])
        if elt[1] == "VBG" :
            listeVerbe.append(elt[0])
        if elt[1] == "VBN" :
            listeVerbe.append(elt[0])
        if elt[1] == "VBP" :
            listeVerbe.append(elt[0])
        if elt[1] == "VBZ" :
            listeVerbe.append(elt[0])
    return listeVerbe