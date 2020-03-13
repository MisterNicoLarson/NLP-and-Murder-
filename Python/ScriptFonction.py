# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
from nltk import *
import xml.etree.ElementTree  as ET 

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