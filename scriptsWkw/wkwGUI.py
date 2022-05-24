# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wkwGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import *
from PyQt5.QtWidgets import QFileDialog,QtGui,QtCore,QtWidgets
from WhoKillWho5 import *
from file import *
from WkW import *


#######################################################################################################
###########################  Classe de la GUI  ########################################################
#######################################################################################################


class Ui_WhoKillWho(object):
    def setupUi(self, WhoKillWho):
        WhoKillWho.setObjectName("WhoKillWho")
        WhoKillWho.resize(800, 600)
        WhoKillWho.setWindowIcon(QtGui.QIcon('Image/logo.png'))

        self.butChgFileXML = QtWidgets.QPushButton(WhoKillWho)
        self.butChgFileXML.setGeometry(QtCore.QRect(130, 60, 161, 28))
        self.butChgFileXML.setObjectName("butChgFileXML")
        self.butTransfoXML = QtWidgets.QPushButton(WhoKillWho)
        self.butTransfoXML.setGeometry(QtCore.QRect(450, 60, 181, 28))
        self.butTransfoXML.setObjectName("butTransfoXML")
        self.butQuitter = QtWidgets.QPushButton(WhoKillWho)
        self.butQuitter.setGeometry(QtCore.QRect(330, 530, 93, 28))
        self.butQuitter.setObjectName("butQuitter")
        self.scrollRes = QtWidgets.QScrollArea(WhoKillWho)
        self.scrollRes.setGeometry(QtCore.QRect(50, 266, 711, 231))
        self.scrollRes.setWidgetResizable(True)
        self.scrollRes.setObjectName("scrollRes")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 709, 229))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.labRes = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labRes.setGeometry(QtCore.QRect(10, 10, 121, 31))
        self.labRes.setText("")
        self.labRes.setObjectName("labRes")
        self.scrollRes.setWidget(self.labRes)
        self.labGetLettre = QtWidgets.QLabel(WhoKillWho)
        self.labGetLettre.setGeometry(QtCore.QRect(60, 220, 181, 16))
        self.labGetLettre.setObjectName("labGetLettre")
        self.getLettre = QtWidgets.QLineEdit(WhoKillWho)
        self.getLettre.setGeometry(QtCore.QRect(170, 220, 113, 22))
        self.getLettre.setMaxLength(1)
        self.getLettre.setObjectName("getLettre")
        self.labInfo = QtWidgets.QLabel(WhoKillWho)
        self.labInfo.setGeometry(QtCore.QRect(120, 130, 501, 16))
        self.labInfo.setText("")
        self.labInfo.setObjectName("labInfo")

        self.retranslateUi(WhoKillWho)
        QtCore.QMetaObject.connectSlotsByName(WhoKillWho)
        
        #Action des bouttons :
        self.butChgFileXML.clicked.connect(self.chgtFichier) # permet de garder le path du fichier xml
        self.butTransfoXML.clicked.connect(self.transfoXML) # permet le traitement et l'affichage de se dossier xml
        self.butQuitter.clicked.connect(WhoKillWho.close)
        

#######################################################################################################
###########################  Fonctions pour boutons  ##################################################
#######################################################################################################

    def retranslateUi(self, WhoKillWho):
        _translate = QtCore.QCoreApplication.translate
        WhoKillWho.setWindowTitle(_translate("WhoKillWho", "Who Kill Who"))
        self.butChgFileXML.setText(_translate("WhoKillWho", "Charger Fichier"))
        self.butTransfoXML.setText(_translate("WhoKillWho", "Charger le resultat"))
        self.butQuitter.setText(_translate("WhoKillWho", "Quitter"))
        self.labGetLettre.setText(_translate("WhoKillWho", "Entrer une lettre :"))

    def chgtFichier(self):
        # Bouton : ouvre une boite de dialogue pour recuperer le path
        # 
       filename = QFileDialog.getOpenFileName(None,"Open File"," ","*.xml")# filename est un tuple
       svgStr(filename[0]) # on recupere dasn le tuple l'info en 0 qui correspond au path et le dans un fichier texte
       path = reedStr()
       text = recuperationText(path)
       self.labRes.setText(text) # on met le texte xml non oté dans notre labRes
       self.labRes.adjustSize()
       
    def transfoXML(self):
        # But : transformer le texte récupéré et afficher les resultats
        lettre = self.getLettre.text()
        
        cdtLettre = self.checkAlphabet(lettre)
        cdtRes = (self.labRes.text() == "")
        if (cdtLettre == True and cdtRes == False):
            self.labInfo.setText("Cela peut prendre quelquse minutes nous vous prions de patienter")
            texte = self.labRes.text()
            result = pickALetter(lettre,texte)# on recupere le texte xml non traité
            print("Voici result "+result)
            self.labRes.setText(result)
            self.labRes.adjustSize()
        else:
            self.labInfo.setText("Verifier que vous ayez bien charger un fichier et que vous ayez rentré une lettre ")
            self.labInfo.adjustSize()

    def checkAlphabet(self,lettre):
        #Entree : une lettre
        # Sortie : un boolean
        # But : verifier qu'on mettent bien un carcatère alphabetique
        exprReg = r"([a-zA-Z])"
        boolLettre = True
        if re.match(exprReg, lettre):
            self.labInfo.setText("Nous allons executer votre demande")
        else:
            self.labInfo.setText("Vous devez rentrer un caractère alphabetique")
            boolLettre = False
        return boolLettre
       
    
#######################################################################################################
###########################  Fonctions pour creer la GUI  #############################################
#######################################################################################################


       
def GUI():
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        WhoKillWho = QtWidgets.QDialog()
        ui = Ui_WhoKillWho()
        ui.setupUi(WhoKillWho)
        WhoKillWho.show()
        sys.exit(app.exec_())

def GUITest():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WhoKillWho = QtWidgets.QDialog()
    ui = Ui_WhoKillWho()
    ui.setupUi(WhoKillWho)
    WhoKillWho.show()
    sys.exit(app.exec_())
    
    
#GUI()