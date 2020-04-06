# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
from nltk import *
import re
import nltk
import xml.etree.ElementTree  as ET

kill = [ "kill" , "dismember" , "murder" , "strangle" , "assasinate" , "shot" , "shoot"]
mouthDay = [ "Monday",
             "Tuesday",
             "Wednesday",
             "Thursday",
             "Friday",
             "Saturday",
             "Sunday",
             "January",
             "February",
             "March",
             "April",
             "May",
             "June",
             "July",
             "August",
             "September",
             "October",
             "November",
             "December",
             ]


cible = [ "him" , "her" , "them" , "by" ]
date = re.compile('^[0-9]{4}$',re.IGNORECASE)


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
    listAlpha = []
    
    ING = re.compile('.*ing$',re.IGNORECASE)
    ED = re.compile('.*ed$',re.IGNORECASE)
    YY = re.compile('.*y$',re.IGNORECASE)
    II = re.compile('.*i$',re.IGNORECASE)
    
    KK = re.compile('.*k$',re.IGNORECASE)
    SS = re.compile('.*s$',re.IGNORECASE)
    VV = re.compile('.*v$',re.IGNORECASE)
    
    lien = re.compile('Category(:[0-9]{4})?',re.IGNORECASE)
    lien1 = re.compile('.*\|.*',re.IGNORECASE)
    
    flag0 = True
    flag1 = False
    
    #permet d'enregistrer et d'ajouter des noms propres (ex : "PRENOM NOM_DE_FAMILLE")
    identite = ""
    tueur_nom = ""
    
    #servent à marquer la position de lecture
    marqueur = -1
    nb = -1 
    step = 0
    
    for mot in doc:
        
        #tueur_nom = ""
        
        marqueur += 1
        nb += 1
        
        lexeme = mot[0]
        classe = mot[1]
        
        
        
            
        #on supprime des mots inutiles comme Catégorie ou de forme XX|XX
        if (not lien.match(lexeme)) and (not lien1.match(lexeme)) :
            
        
            #TRAITEMENT DES NOMS : si le mot est un nom commun
            if classe in nom_commun:
                
                #s'il y a un 's' à la fin, on le retire
                if SS.match(lexeme):
                    longueur4 = len(lexeme) - 1
                    lexeme = lexeme[:longueur4]
                
                #s'il y a un 'ing' à la fin, on le retire
                if ING.match(lexeme):
                        longueur1 = len(lexeme) - 3
                        lexeme = lexeme[:longueur1]
                
                
            #TRAITEMENT DES VERBES : si le mot est un verbe
            #on transforme en léxème tous les verbes
            if classe in verbes:

                #s'il y a un 'ing' ou 'ed' à la fin, on le retire    
                #if ING.match(lexeme) or ED.match(lexeme):
                
                if SS.match(lexeme):
                    longueur4 = len(lexeme) - 1
                    lexeme = lexeme[:longueur4]
                    
                if ING.match(lexeme):
                    longueur1 = len(lexeme) - 3
                    lexeme = lexeme[:longueur1]
                    
                if ED.match(lexeme):
                    longueur3 = len(lexeme) - 2
                    lexeme = lexeme[:longueur3]    
                    
                #s'il y a un 'y' à la fin, on le remplace par 'ie'
                if YY.match(lexeme):
                    longueur2 = len(lexeme) - 1
                    lexeme = lexeme[:longueur2]
                    lexeme = lexeme + 'ie'
                #s'il y a un 'i' à la fin, on le remplace par 'y'
                elif II.match(lexeme):
                    longueur2 = len(lexeme) - 1
                    lexeme = lexeme[:longueur2]
                    lexeme = lexeme + 'y'
                                
                
                #s'il y a un 'v' à la fin, on ajoute un 'e'
                if VV.match(lexeme):
                    lexeme = lexeme + 'e'
                
                
            #TRAITEMENT DES NOMS_PROPRES : si le mot est un nom propre
            if (classe in nom_propre) and (identite not in mouthDay):
                
                #on enregistre le nom propre...
                #si on en avait pas lu, on démarre la lecture des noms propres :
                #chaque fois qu'on lira un nouveau nom propre, on l'ajoute à l'ancien avec un espace
                if flag1 == False:
                    flag1 = True
                    identite = lexeme
                else:
                    identite += " " + lexeme
            
            #si le mot n'est pas un nom propre, alors qu'on avait démaré leur lecture...
            #on vérifie aussi que ce n'est pas le nom du tueur (on cherche ses victimes)
            elif flag1 and (tueur_nom != identite) and (identite not in mouthDay):
                
                if flag0:
                    flag0 = False
                    tueur_nom = identite
                
                    
                #on enregistre aussi dans une autre liste, les noms propres avec leur position dans le texte
                stock = (identite,marqueur)
                listAlpha.append(stock)
                
                #on arrête cette lecture
                flag1 = False
                
                
                #on met le nom propre enregistré dans un groupe (et s'il est vide)
                #on signale que le groupe actuel est occupé par des noms propres
                if (not list2):
                    list2.append(identite)
                    flag2 = True
                    
                    #et si on ne lie pas un ',' ou 'and', le groupe est isolé : on l'enregistre et on en crée un nouveau (vide)
                    #on signale que le groupe actuel est vide
                    if lexeme not in [',' , 'and']:
                        list1.append(list2)
                        list2 = []
                        flag2 = False
                    
                #si le groupe n'est pas vide (c-a-d qu'on avait enregistré quelque chose auparavant)
                else:
                    
                    #si le mot est assez proche du dernier enregistré, alors on les met dans le même groupe
                    #on signale que le groupe actuel est occupé par des noms propres
                    if ((nb - step - 1) < 5):
                        list2.append(identite)
                        flag2 = True
                        
                    #sinon, on enregistre le groupe, on en crée un nouveau, et on y met le nom propre
                    #on signale que le groupe actuel n'est pas vide
                    else:
                        list1.append(list2)
                        list2 = []
                        list2.append(identite)
                        flag2 = False
                
                #dans tous les cas, on enregistre de la position de ce mot
                step = nb
                  
            #si le mot est un "séparateur", on ajoute artificiellement du pas, pour allonger la distances entre les mots suivants
            if (lexeme in ['.' , ';' , ':' , 'by']):
                nb += 50
            
            #TRAITEMENT GENERAL : si le mot est en rapport avec le meurtre, on le met dans un groupe et on l'enregistre
            #on gère alors certains paramètres pour éviter les groupes vides ou d'en mettre avec les noms propres
            if (lexeme in kill):
                
                flag2 = True
                
                #si on n'était pas en train de lire de noms propres, on crée un nouveau groupe pour mettre le mot
                if (flag1 == False):
                    list1.append(list2)
                    list2 = []
                    list2.append(lexeme)
                #si on était en train de lire de noms propres, on met le mot dans le groupe actuel : il est vide car ça été déjà traité auparavant
                else:
                    list2.append(lexeme)
                    list1.append(list2)
                    list2 = []
            #si le mot n'est pas en rapport avec le meurtre...
            #et si le mot peut servir et que le groupe actuel n'est pas occupé par des noms propres...
            elif (lexeme in cible) and (flag2):
                
                #on signale que le (nouveau) groupe ne sera plus occupé par des noms propres
                flag2 = False
                
                #et si le groupe est vide, alors on met directement le mot dedans
                if (not list2):
                    list2.append(lexeme)
                    list1.append(list2)
                    list2 = []
                #sinon on en crée un nouveau et on le met dedans (on enregistre l'ancien)
                else:
                    list1.append(list2)
                    list2 = []
                    list2.append(lexeme)
            else:
                #dans tous les cas, on signale que le (nouveau) groupe ne sera plus occupé par des noms propres
                flag2 = False
                
            if (date.match(lexeme)):
                stock = (lexeme,marqueur)
                listAlpha.append(stock)
            
            """    
            if (lexeme in ['.' , ';' , ':']):
                stock = (lexeme,marqueur)
                listAlpha.append(stock)
                marqueur += 50
            """    
    #on retourne une liste qui contient tous les groupes enregistrés
    #on retourne aussi une liste qui contient les noms propres associés à leur position dans le texte
    return list1,listAlpha,tueur_nom


#associe les noms propres à un indice temporel
def temporel(doc):
    
    result = []
    listNom = []
    date1 = ""
    date2 = ""
    
    
    for groupe in doc:

        #si on lie une date...
        if date.match(groupe[0]):
            
            #et si c'est la première qu'on rencontre et qu'on n'a pas encore rencontré de noms propres,
            #alors on enregistre la date
            if (not listNom) and (date1 == ""):
                date1 = groupe
                
            #et si c'est la première qu'on rencontre et si on avait rencontré des noms propres auparavant,
            #alors on les associe à cette date (et on vide la liste des noms propres rencontrés)
            elif ((not listNom) == False) and (date1 == ""):
                
                for raw in listNom:
                    result.append((raw[0],groupe[0]))
                
                listNom = []
                           
            #et si c'est la deuxième date qu'on rencontre et si on avait rencontré des noms propres auparavant,
            #alors on compare la distance entre cette date et le premier nom propre enregistré, avec
            #la distance entre la première date enregistrée et le premier nom propre enregistré:
            #on attribut aux noms propres enregistrés, la date la plus proche du premier nom propre enregistré
            #(et on vide la liste des noms propres rencontrés)
            elif ((not listNom) == False) and (date1 != ""):

                distance1 = listNom[0][1] - date1[1]
                distance2 = groupe[1] - listNom[0][1]
                             
                if( distance1 > distance2 ):
                    for raw in listNom:
                        result.append((raw[0],groupe[0]))
                        date1 == ""
                                
                else:
                    for raw in listNom:
                        result.append((raw[0],date1[0]))
            
                listNom = []
                
        #si on lie un nom propre, on l'enregistre dans une liste
        elif groupe[0] not in ['.' , ';' , ':' , ',']:
            listNom.append(groupe)              
    
    #une fois la lecture terminée, on retourne une liste contenant les noms propres, associés chacun à une date
    return result
            
#associe les noms propres aux victimes du tueur (en suivant les mots en rapport avec le meurtre)
def association(doc):
    victim = []
    result = []
    flag1 = False
    
    for group in doc:
        
            if (not group) == False:
                
                # si le groupe concerne des victimes, la liste est mise à jour
                if len(group) > 1:
                    victim = group
                    
                elif (group[0] not in kill) and (group[0] not in cible):
                    victim = group
                
                # si on avait lu un mot en relation avec le meurtre
                if flag1:
                    
                    #et si le prochain est de type "him", "her", etc.
                    #alors on prend le dernier groupe de victimes enregistré
                    if (group[0] in cible):
                        
                        if group[0] in ['him','her']:
                            result.append(victim[len(victim) - 1])
                            
                        else:
                            result.extend(victim)
                            
                    #ou si le prochain concerne des victimes, on les mets dans le résultat final
                    elif (group[0] not in kill):
                        result.extend(victim)
                
                #chaque fois qu'on lit un mot en relation avec le meurtre, on le signale (pour la lecture du prochain mot)
                flag1 = (group[0] in kill)
                
    return result

#garde les noms propres associés à une date, suivant la liste des victimes
def deduction(doc1,doc2):
    result = []
    
    for raw1 in doc1:
        flag = False
        
        for raw2 in doc2:
            if raw1[0] == raw2:
                flag = True
        
        if flag:
            result.append(raw1)
            
    return result


def nettoyage(doc):
    
    original = []
    result = []
    
    for mot in doc:
        if mot[0] not in original:
            original.append(mot[0])
            result.append(mot)
            
    return result
    

def execution(text1):
    #text1 = recuperationText(text0)
    text2 = purge(text1)
    text3 = tokenTag(text2)
    text4,textA,tueur_nom = tri(text3)
    textB = temporel(textA)
    text5 = association(text4)
    textF1 = deduction(textB,text5)
    textF2 = nettoyage(textF1)
    return textF2,tueur_nom
    



#Lecture de fichers en tapant le nom du tueur
"""
nom_tueur = input()
nom_tueur.strip()
txt = nom_tueur.replace(' ','_')
text1 = txt + '.xml'

text1 = "Chandrakant_Jha.xml"
"""

def lectureList(lettre):
    txt1 = "enSK.xml"
    txt2 = recuperationText(txt1)
    txt3 = ""
    nb = 0
    flag = False
    flag1 = False
    listFinal = []
    
    for mot in txt2:
        

        #Chaque tueur commence avec une '*' et on ne lit qu'à partir de ce caractère (si on retire ce qu'il y a avant cette liste)
        if mot == '*' and ((not txt3) == False):
            if flag:
                result,tueur_nom = execution(txt3)
                
                if ((not result) == False) and tueur_nom != "":
                    if tueur_nom[0] == lettre:
                        listFinal.append( (tueur_nom,result) )
                """
                titre = tueur_nom + ' :'
                print(titre)
                for raw in result:
                    print(raw)
                
                """
                
                flag1 = False
            else:
                flag = True
            
            txt3 = ""
        else:
            if mot == '\n' and flag:
                flag1 = True
            
            if flag1 == False:
                txt3 += mot
                
    return listFinal


def affichage(doc):
    print('\n')
    for raw in doc:
        titre = raw[0] + ' :'
        print(titre)
        for mot in raw[1]:
            victime = "\t-" + mot[0] + " en " + mot[1]
            print(victime)
        print('\n')


print("Veuillez rentrer une lettre :")
lettre = input()
print('\n')
print("Merci d'attendre quelques secondes...")
print('\n')
result = lectureList(lettre)
print("Liste de votre recherche :")
affichage(result)


"""
#Traitements...
text2 = purge(recuperationText(text1))
text3 = tokenTag(text2)
text4,textA = tri(text3)
textB = temporel(textA)
text5 = association(text4)
textF = deduction(textB,text5)
print(textF)
"""