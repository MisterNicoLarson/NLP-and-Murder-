# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
import xml.etree.ElementTree  as ET 

"""Fonction"""

def recuperationText(path):
    # Entree : string qui est le chemin vers nos données XML
    # Sortie : l'objet de la balise soit un texte
    
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

"""Traitement de l'information""" 

pathFile = "essai.xml"
path = "listSerialKiller.xml"
texte = recuperationText(path)
print(texte)