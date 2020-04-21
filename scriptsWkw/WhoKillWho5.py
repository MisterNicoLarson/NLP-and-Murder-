# -*- coding: utf-8 -*-
from lxml import etree
from lxml import html
from nltk import *
import re
import nltk
from nltk.corpus import wordnet
import xml.etree.ElementTree  as ET
from file import *

#cette liste contient les mots avec le champ lexical du meurtre.
kill = [ "kill" , "dismember" , "murder" , "strangle" , "assasinate" , "shot" , "shoot"]

#cette liste contient tous les noms en rapport avec la date (jour de la semaine et mois)
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

#cette liste contient des mots qui peuvent indiquer des sujets (comme les pronoms relatifs)
cible = [ "him" , "her" , "them" , "by" ]

#permet de savoir si un mot est une année (4 chiffres)
date = re.compile('^[0-9]{4}$',re.IGNORECASE)


"""Fonction"""



#Indique si le mot en paramètre est un nom de lieu
def isALocation(word):
    #on enlève les signes "_"
    word = word.replace(" ","_")
    
    #on tague le mot pour ensuite analyser sa nature
    synsets = wordnet.synsets(word)
    location = wordnet.synset('location.n.01')
    
    #si la nature de ce mot (ou de ses composants) est une localisation,
    #alors on renvoie "True"
    for s in synsets:
        for h in s.common_hypernyms(location):
            if location==h:
                return True
      
    #sinon on renvoie "False"
    return False

#Permet de taguer un texte : renvoie une liste contenant chaque mot de ce texte, associé à un tag (nom commun, verbe, etc.)
def tokenTag(doc):
    # Entree : un texte
    # Sortie : une liste de token avec leur tag
    # Objectif : transformer un texte en une liste de token pour pouvoir tagger cette liste
    doc = nltk.word_tokenize(doc)
    doc = nltk.pos_tag(doc)
    return doc


#Va retirer tout ce qui va compliquer inutilement la lecture
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
            #on enlève aussi les signes comme :  ' , [ , ] , = .
            if (mot not in ['\'','[',']','=']):
                result += mot;
            
                
    #la fonction renvoie enfin le texte "nettoyé"
    return result


#Conserve et transforme les verbes et nom en léxème,
#Isole les noms propres et les associes en groupe
def tri(doc):
    
    nom_propre = ["NNP"]
    nom_commun = ["NNS"]
    verbes = ["VBS","VBN","VBZ","VBG","VB" , "VBD"]
    
    list1 = []
    list2 = []
    listAlpha = []  #cette liste contiendra les mots et les dates, associés chacun avec leur localisation dans le texte
    listBeta = []   #cette liste contiendra les mots et les lieux, associés chacun avec leur localisation dans le texte
    
    ING = re.compile('.*ing$',re.IGNORECASE)    #indique si un mot se termine par "ing"
    ED = re.compile('.*ed$',re.IGNORECASE)      #indique si un mot se termine par "ed"
    YY = re.compile('.*y$',re.IGNORECASE)       #indique si un mot se termine par "y"
    II = re.compile('.*i$',re.IGNORECASE)       #indique si un mot se termine par "i"        
    KK = re.compile('.*k$',re.IGNORECASE)       #indique si un mot se termine par "k"
    SS = re.compile('.*s$',re.IGNORECASE)       #indique si un mot se termine par "s"
    VV = re.compile('.*v$',re.IGNORECASE)       #indique si un mot se termine par "v"
    
    lien = re.compile('Category(:[0-9]{4})?',re.IGNORECASE)       #indique les mots contenant "Catégorie:"
    lien1 = re.compile('.*\|.*',re.IGNORECASE)                    #indique les mots avec un pipe |
    
    flag0 = True
    flag1 = False
    
    #permet d'enregistrer et d'ajouter des noms propres (ex : "PRENOM NOM_DE_FAMILLE")
    identite = ""
    tueur_nom = ""
    
    #servent à marquer la position de lecture
    marqueur = -1
    nb = -1 
    step = 0
    
    #on parcourt tout le texte en paramètre...
    for mot in doc:
        
        
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
            if (classe in nom_propre) and (lexeme not in mouthDay):
                
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
                
                """
                Quand les VRAIS noms propres seront reconnu:
                    -faire la reconnaissance des dates et des lieux (if / else) ailleurs et remettre le paragraphe
                    qui suit dans l'ordre
                """
                if isALocation(identite) and (flag0 == False):
                    stock1 = (identite,marqueur)
                    listBeta.append(stock1)
                
                else:
                    
                    #on enregistre aussi dans une autre liste, les noms propres avec leur position dans le texte
                    stock = (identite,marqueur)
                    listAlpha.append(stock)
                    listBeta.append(stock)
                    
                    
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
                
                  
            #SEPARATEUR : Si le mot est un "séparateur", on ajoute artificiellement du pas, pour allonger la distances entre les mots suivants
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
            
            #s'il s'agit d'une date, on l'enregistre dans la seconde liste (avec sa localisation)
            if (date.match(lexeme)):
                stock = (lexeme,marqueur)
                listAlpha.append(stock)

    #on retourne une liste qui contient tous les groupes enregistrés
    #on retourne aussi une liste qui contient les noms propres associés à leur position dans le texte
    return list1,listAlpha,listBeta,tueur_nom


#Associe les noms propres à un indice temporel
def temporel(doc):
    
    result = []
    listNom = []
    date1 = ""
    date2 = ""
    
    #on parcourt une liste contenant des mots et des dates, associés à leur localisation dans le texte de départ
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
            

#associe les noms propres à un indice de lieu
def localisation(doc):
    
    result = []
    listNom = []
    lieu1 = ""
    lieu2 = ""
    
    #on parcourt une liste contenant des mots et des lieux, associés à leur localisation dans le texte de départ
    for groupe in doc:

        #si on lie un lieu...
        if isALocation(groupe[0]):
            
            #et si c'est le premier qu'on rencontre et qu'on n'a pas encore rencontré de noms propres,
            #alors on enregistre le lieu
            if (not listNom) and (lieu1 == ""):
                lieu1 = groupe
                
            #et si c'est le premier qu'on rencontre et si on avait rencontré des noms propres auparavant,
            #alors on les associe à ce lieu (et on vide la liste des noms propres rencontrés)
            elif ((not listNom) == False) and (lieu1 == ""):
                
                for raw in listNom:
                    result.append((raw[0],groupe[0]))
                
                listNom = []
                           
            #et si c'est le deuxième lieu qu'on rencontre et si on avait rencontré des noms propres auparavant,
            #alors on compare la distance entre ce lieu et le premier nom propre enregistré, avec
            #la distance entre le premier lieu enregistré et le premier nom propre enregistré:
            #on attribut aux noms propres enregistrés, le lieu le plus proche du premier nom propre enregistré
            #(et on vide la liste des noms propres rencontrés)
            elif ((not listNom) == False) and (lieu1 != ""):

                distance1 = listNom[0][1] - lieu1[1]
                distance2 = groupe[1] - listNom[0][1]
                             
                if( distance1 > distance2 ):
                    for raw in listNom:
                        result.append((raw[0],groupe[0]))
                        lieu1 == ""
                                
                else:
                    for raw in listNom:
                        result.append((raw[0],lieu1[0]))
            
                listNom = []
                
        #si on lie un nom propre, on l'enregistre dans une liste
        elif groupe[0] not in ['.' , ';' , ':' , ',']:
            listNom.append(groupe)              
    
    #une fois la lecture terminée, on retourne une liste contenant les noms propres, associés chacun à un lieu
    return result


            
#Associe les noms propres aux victimes du tueur (suivant les mots en rapport avec le meurtre)
def association(doc):
    victim = []
    result = []
    flag1 = False
    
    #on parcourt une liste de mots...
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


#Associe les noms propres associés à une date, avec la liste des vrai victimes
def deduction1(doc1,doc2):
    result = []
    
    for raw1 in doc1:
        flag = False
        
        for raw2 in doc2:
            if raw1[0] == raw2:
                flag = True
        
        if flag:
            result.append(raw1)
        
    return result

#Associe les noms propres associés à un lieu, avec la liste des vrai victimes (associées à une date)
def deduction2(doc1,doc2):
    result = []
    for raw1 in doc1:
        flag = True
        for raw2 in doc2:
            if raw1[0] == raw2[0]:
                flag = False
                stock = ( raw1[0], raw1[1] , raw2[1] )
                result.append(stock)
        if flag:
            stock = ( raw1[0], raw1[1] , "" )
            result.append(stock)
                
    return result


#Enleve tous les doublons
def nettoyage(doc):
    
    original = []
    result = []
    
    for mot in doc:
        if mot[0] not in original:
            original.append(mot[0])
            result.append(mot)
            
    return result
    
#Traite un texte donné puis renvoie :
#  - le nom du tueur de ce texte
#  - ses victimes avec :
#       • leur nom
#       • leur date
#       • leur lieu (si possible)
def execution(text1):
    
    #on nettoie le texte, puis on le tague
    text2 = purge(text1)
    text3 = tokenTag(text2)
    
    #on en récupère des listes et le nom du tueur
    text4,textA,textB,tueur_nom = tri(text3)
    
    #une liste va permettre de retrouver le nom des victimes (text4)
    text5 = association(text4)
    
    #une liste va permettre de retrouver la date de leur meurtre  (textA)
    textA1 = temporel(textA)
    
    #une liste va permettre de retrouver le lieur de leur meurtre  (textB)
    textB1 = localisation(textB)
    
    #on joint le nom des victimes avec la date de leur meurtre
    textFA1 = deduction1(textA1,text5)
    textFA2 = nettoyage(textFA1)
    
    #on joint le nom des victimes avec la lieu de leur meurtre
    textFB1 = deduction1(textB1,text5)
    textFB2 = nettoyage(textFB1)
    
    #on joint le nom des victimes, la date de leur meurtre et leur lieu
    textFF = deduction2(textFA2,textFB2)
    
    #on renvoie le résultat
    return textFF,tueur_nom

    
    
#Indique si la première lettre du tueur et la même que celle recherchée
def identite(tueur_nom,lettre):
    
    #on sépare le(s) nom(s) (s'il est composé de plusieurs mots)
    liste = tueur_nom.split()
    courant = []
    listeListe = []
    
    #S'il y a un "and", on sépare les deux noms présents dans une liste respective (une partie)
    for raw in liste:
        
        courant.append(raw)
        
        if raw in ['and']:
            listeListe.append(courant)
            courant = []
            
    listeListe.append(courant)
    
    #Pour chaque partie, on compare la première lettre de chaque mot avec celle recherchée
    for partie in listeListe:
        
        #on ignore le premier mot car il s'agit normalement d'un prénom (et non d'un nom de famille)
        #si le nom du tueur est composé d'un seul mot, on fait exception à cette règle
        flag = ( len(partie) == 1 )
        
        for raw in partie:
            
            if flag == False:
                flag = True
            else:
                #la première lettre du mot est analisé pour savoir s'il s'agit bien d'une majuscule,
                #s'il s'agit de la lettre recherchée et si ce n'est pas d'un titre (comme Von ou Van)
                if (65 <= ord(raw[0])) and (ord(raw[0]) <= 90) and (raw[0] == lettre) and (raw not in ['Von','Van']) :
                    return True

    #si ses conditions n'ont pas été répondu au final, le programme renvoie False
    return False

#prend une lettre et va alors lire une liste de tueurs
def lectureList(lettre):
    txt1 = "XML/corpus.xml"
    txt2 = recuperationText(txt1)
    txt3 = ""
    nb = 0
    flag = False
    flag1 = False
    listFinal = []
    
    #on parcourt mot par mot cette liste, puis on les segmente en texte : chacun décrit un tueur en particulier
    
    for mot in txt2:
        

        #Chaque tueur commence avec une '*' et on ne lit qu'à partir de ce caractère (si on retire ce qu'il y a avant cette liste)
        if mot == '*' and ((not txt3) == False):
            
            #on traite chaque texte pour en extraire, le nom du tueur et celui de ses victimes (date et lieu)
            if flag:
                result,tueur_nom = execution(txt3)
                
                #on ne garde le résultat s'il n'est pas vide et si le tueur n'a pas un nom de lieu (ce qui génèrerait des effets indésirables)
                if ((not result) == False) and tueur_nom != "" and (isALocation(tueur_nom) == False):
                    #suivant la première lettre de son/ses nom(s) (de famille), on traite ce texte ou non
                    if identite(tueur_nom,lettre):
                        listFinal.append( (tueur_nom,result) )
                
                flag1 = False
            else:
                flag = True
            
            txt3 = ""
        else:
            if mot == '\n' and flag:
                flag1 = True
            
            if flag1 == False:
                txt3 += mot
    
    #le programme renvoie une liste, de listes contenant chacune le nom d'un tueur et une liste de ses victimes (nom, date et lieu)
    return listFinal

#prend une lettre et une liste de tueurs
def lectureListe(lettre,text):
    # Entree : une lettre et un texte brute
    # Sortie : un texte
    # But : on a une surcharge de la fonction lecturelist car celle ci va avoir pour but d'afficher les resultats dans le label labRes
   
    txt3 = ""
    nb = 0
    flag = False
    flag1 = False
    listFinal = []
    
    for mot in text:
        
        
        #Chaque tueur commence avec une '*' et on ne lit qu'à partir de ce caractère (si on retire ce qu'il y a avant cette liste)
        if mot == '*' and ((not txt3) == False):
            
            #on traite chaque texte pour en extraire, le nom du tueur et celui de ses victimes (date et lieu)
            if flag:
                
                result,tueur_nom = execution(txt3)
                
                #on ne garde le résultat s'il n'est pas vide et si le tueur n'a pas un nom de lieu (ce qui génèrerait des effets indésirables)
                if ((not result) == False) and tueur_nom != "" and (isALocation(tueur_nom) == False):
                    #suivant la première lettre de son/ses nom(s) (de famille), on traite ce texte ou non
                    if identite(tueur_nom,lettre):
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

    #le programme renvoie une liste, de listes contenant chacune le nom d'un tueur et une liste de ses victimes (nom, date et lieu)
    return listFinal


#Affiche le résultat du traitement de manière esthétique et présentable
def affichage(doc,lettre):
    aff = 'Voici tout les tueurs pour la lettre {} :\n'.format(lettre)
   
    for raw in doc:
        titre = '\n'+raw[0] + ' :\n'
        aff = aff + titre
        for mot in raw[1]:
            victime = "\t-" + mot[0] + " en " + mot[1]
            if (not mot[2]) == False:
                victime += " : " + mot[2]
            aff = aff+victime+'\n'
    return(aff)

def executionScript():
    print("Veuillez rentrer une lettre :")
    lettre = input()
    lettre = lettre.upper()
    print('\n')
    print("Merci d'attendre quelques secondes...")
    print('\n')
    result = lectureList(lettre)
    print("Liste de votre recherche :")
    final = affichage(result,lettre)
    print(final)
    