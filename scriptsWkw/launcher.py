# -*- coding: utf-8 -*-
from wkwGUI import *
from WhoKillWho5 import *

print("Bonjour Harry que puis je pour vous ? ")
print('\nDesirez vous une anayse rapide de la situation ou une analyse plus avancée ?')
print("\nPour une analyse rapide tapez 1 pour une analyse avancée tapez 2")
reponse = input()
while reponse != str(1) and reponse !=str(2):
    reponse = input()

    #Methode par ligne
if reponse == str(1):
    executionScript()
    
    #Methode par interface graphique
if reponse == str(2):
    GUITest()