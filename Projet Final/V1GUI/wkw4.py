de d # -*- coding: utf-8 -*-

from PyQt5 import *
from PyQt5.QtWidgets import QFileDialog
from ScriptFonction import *
import re

#####################################################################################"
"""Classe Python"""
class windowPrincipale(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 480)
        self.butChargerFichier = QtWidgets.QPushButton(Dialog)
        self.butChargerFichier.setGeometry(QtCore.QRect(50, 40, 131, 28))
        self.butChargerFichier.setObjectName("butChargerFichier")
        self.butTransformation = QtWidgets.QPushButton(Dialog)
        self.butTransformation.setGeometry(QtCore.QRect(260, 40, 161, 28))
        self.butTransformation.setObjectName("butTransformation")
        self.butAffichageWindow = QtWidgets.QPushButton(Dialog)
        self.butAffichageWindow.setGeometry(QtCore.QRect(500, 40, 93, 28))
        self.butAffichageWindow.setObjectName("butAffichageWindow")
        self.butQuitterWindow = QtWidgets.QPushButton(Dialog)
        self.butQuitterWindow.setGeometry(QtCore.QRect(280, 430, 93, 28))
        self.butQuitterWindow.setObjectName("butQuitterWindow")
        self.erreurFichierXML = QtWidgets.QLabel(Dialog)
        self.erreurFichierXML.setGeometry(QtCore.QRect(50, 90, 361, 16))
        self.erreurFichierXML.setText("")
        self.erreurFichierXML.setObjectName("erreurFichierXML")
        self.transformationXML = QtWidgets.QLabel(Dialog)
        self.transformationXML.setGeometry(QtCore.QRect(50, 120, 361, 16))
        self.transformationXML.setText("")
        self.transformationXML.setObjectName("transformationXML")
        self.labLettre = QtWidgets.QLabel(Dialog)
        self.labLettre.setGeometry(QtCore.QRect(50, 180, 171, 16))
        self.labLettre.setObjectName("labLettre")
        self.getLettre = QtWidgets.QLineEdit(Dialog)
        self.getLettre.setGeometry(QtCore.QRect(170, 180, 113, 22))
        self.getLettre.setObjectName("getLettre")
        self.getLettre.setMaxLength(1)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(50, 230, 541, 161))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 159))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.labAffRes = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labAffRes.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.labAffRes.setText("")
        self.labAffRes.setObjectName("labAffRes")
        self.scrollArea.setWidget(self.labAffRes) # on link la scroll bar au label qui va 

        #Action des bouttons :
        self.butChargerFichier.clicked.connect(self.recupererFichierXML)
        self.butTransformation.clicked.connect(self.recupFirstLettre)
        #self.butAffichageWindow.clicked.connect(self.quelclient_m)
        self.butQuitterWindow.clicked.connect(Dialog.close)
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Who Kill Who", "Who Kill Who"))
        self.butChargerFichier.setText(_translate("Dialog", "Charger le fichier"))
        self.butTransformation.setText(_translate("Dialog", "Transformation "))
        self.butAffichageWindow.setText(_translate("Dialog", "Affichage"))
        self.butQuitterWindow.setText(_translate("Dialog", "Quitter"))
        self.labLettre.setText(_translate("Dialog", "Entrer une lettre :"))
        
    def test3(self):
        self.labAffRes.setText("J'aime le poil")       
        self.labAffRes.adjustSize()
        print(self.getLettre.text())
        
    def recupererFichierXML(self):
        # Bouton : ouvre une boite de dialogue pour recuperer le path
       filename = QFileDialog.getOpenFileName(None,"Open File"," ","*.xml")
       print(filename)
   
    def recupFirstLettre(self):
        # Bouton : check la lettre et fait le traitement
        ftCaract = self.getLettre.text()
        boolean = checkAlpha(self,ftCaract)
          
############################################################################################
"""Methodes Principales"""
def GUI():   
    # But : lancer la GUI
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = windowPrincipale()
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec_())
        
def checkAlpha(self,lettre):
        #Entree : une lettre
        # Sortie : un boolean
        # But : verifier qu'on mettent bien un carcatère alphabetique
        exprReg = r"([a-zA-Z])"
        boolLettre = True
        if re.match(exprReg, lettre):
            self.erreurFichierXML.setText("Nous allons executer votre demande")
        else:
            self.erreurFichierXML.setText("Vous devez rentrer un caractère alphabetique")
            boolLettre = False
        print(boolLettre)
        return boolLettre
        
###################################################################""
GUI()