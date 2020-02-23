# -*- coding: utf-8 -*-
from lxml import etree
import xml.etree.ElementTree  as ET 

""" Fonction script"""   
            
def arbreXML (pathDataFileXML):
    # Entree : string qui est le chemin vers nos données XML
    # Sortie : liste de string qui est le nom de balise XML
    tree = etree.parse(pathDataFileXML) # c'est le dossier dans lequel on a du XML
    root = tree.getroot() # permet de recuperer la racine
    #Boucle qui va donner a chaque fois le nom des elements dans les balises depuis root
    etage = [root.tag] # la base de notre arbre va etre sa racine root.tag
    for leaf in root:
        etage.append(leaf.tag)
        for leaf1 in leaf:
            etage.append(leaf1.tag)
            for leaf2 in leaf1 :
                etage.append(leaf2.tag)
    return etage

def cheminParcoursArbre(liste):
    # Objectif : obtenir ce chemin /mediawiki/page/revision/text
    # Entrée : une liste qui est notre arbre
    # Sortie : un chemin qui est le chemin de notre arbre
    # Methode : "/".join(liste) qui permet de transformer une liste en string
    way = "/"+"/".join(liste)
    return way

def nettoyageListe(liste):
    # Entree : liste
    # Sortie : liste nettoyée
    # Objectif : je reçois une liste de nom de balise et je vais la purger de tout ce qui est inutile
    listeClean = []
    listeClean.append(liste[0]) # ici on ajoute notre root
    page = liste.index("{http://www.mediawiki.org/xml/export-0.10/}page")
    revision = liste.index("{http://www.mediawiki.org/xml/export-0.10/}revision")
    text = liste.index("{http://www.mediawiki.org/xml/export-0.10/}text")
    listeClean.append(liste[page])
    listeClean.append(liste[revision])
    listeClean.append(liste[text])
    return listeClean

def textBaliseText(pathXML, pathArbre):
    # Entree : prends 2 variables string
    #           -> pathXML : c'est le chemin vers le dossier XML
    #           -> pathArbre : c'est le chemin dans l'arbre pour acceder au texte
    # Sortie : le texte dans la balise texte
    # Objectif : renvoyer le text qui est dans la balise text
    tree = etree.parse(pathXML)
    for elt in tree.xpath(pathArbre):
        print(elt.text)

"""Traitement de l'information""" 

pathFile = "listSerialKiller.xml"
listXML = arbreXML(pathFile)


listeClean = nettoyageListe(listXML)
for elt in listeClean:
    print(elt)
    
pathTree = cheminParcoursArbre(listeClean)
print("Voici le path que l'on recherche : "+pathTree)

textBaliseText(pathFile, pathTree)