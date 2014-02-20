'''
Created on 12-Feb-2014

@author: Abhimanyu
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import ruleParser
import matchEngine
from GUIDriver import Driver
import subprocess

from ConfigParser import RawConfigParser
pattern = RawConfigParser()
pattern.read(os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg')

class Terminal(QDialog):
    def __init__(self, parent = None):
        super(Terminal, self).__init__(parent)
        
        self.pathlabel = QLabel("File/ directory destination.")
        self.searchlabel = QLabel("Optional search filter: ") 
        self.regexlabel = QLabel("Optional regex filter: ") 
        self.conditionlabel = QLabel("Optional condition filter: ")
        self.progresslabel = QLabel("Click on Crunch button to initiate search procedure")  

        self.browsebutton = QPushButton("Browse the file system.")        
        self.searchbox = QLineEdit("")
        self.regexbox = QLineEdit("")
        self.conditionbox= QLineEdit("")
        self.resultbox = QTextBrowser()
        self.statsbox = QTextBrowser()
        self.submitbutton = QPushButton("Crunch.")
        self.configbutton = QPushButton("See/Edit configuration file")

        self.progressbar = QProgressBar()
        
        layout = QGridLayout()
        
        layout.addWidget(self.pathlabel, 0, 0)
        layout.addWidget(self.browsebutton, 0, 1, 1, 2)
        layout.addWidget(self.searchlabel, 1, 0,)
        layout.addWidget(self.searchbox, 1, 1, 1, 2)
        layout.addWidget(self.regexlabel, 2, 0)
        layout.addWidget(self.regexbox, 2, 1, 1, 2) 
        layout.addWidget(self.conditionlabel, 3, 0)
        layout.addWidget(self.conditionbox, 3, 1, 1, 2)         
        layout.addWidget(self.configbutton, 4, 2)              
        layout.addWidget(self.submitbutton, 4, 1)
        layout.addWidget(self.progresslabel, 5, 0, 1 , 1)
        layout.addWidget(self.progressbar, 5, 1, 1, 2)
        layout.addWidget(self.resultbox, 7, 0, 5, 3)
        layout.addWidget(self.statsbox, 12, 0, 2, 3)
        
        self.setLayout(layout)        
        self.setWindowTitle("GENLOG alpha version")
        self.progressbar.setRange(0, 100)
        
        self.connect(self.browsebutton, SIGNAL("clicked()"), self.file_browse )
        self.connect(self.configbutton, SIGNAL("clicked()"), self.open_cfg )
        self.connect(self.submitbutton, SIGNAL("clicked()"), self.ignition)
        
    def ignition(self):
        lv = None    
        self.resultbox.clear()
        self.statsbox.clear()
        if self.conditionbox.text():           
            self.progresslabel.setText("Parsing condition string")      
            ruleString = str(self.conditionbox.text())        
            try:    
                ruleTree = ruleParser.parse_it(ruleString)             
            except AttributeError:            
                self.resultbox.append("!!ERROR :Attribute error was raised. Check the condition string. Script was terminated.")
                exit()               
            lv = matchEngine.LogVerifier(ruleTree)  
                   
        Driver(window, lv, str(self.browsebutton.text()))
        
    def open_cfg(self):
        subprocess.call(['kate', os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg'])        
     
    def file_browse(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)     
       
        self.browsebutton.setText(str(dialog.getExistingDirectory()))
                 
        
app = QApplication(sys.argv)
window = Terminal()
window.resize(600, 1000)
window.show()

app.exec_()