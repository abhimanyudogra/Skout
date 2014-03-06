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

from configparser import RawConfigParser
pattern = RawConfigParser()
pattern.read(os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg')

class Terminal(QDialog):
    def __init__(self, parent = None):
        super(Terminal, self).__init__(parent)
        
        self.filepathlabel = QLabel("Select file(s)")  
        self.dirpathlabel = QLabel("Select directory")      
        self.searchlabel = QLabel("Optional search filter: ") 
        self.regexlabel = QLabel("Optional regex filter: ") 
        self.conditionlabel = QLabel("Optional condition filter: ")
        self.progresslabel = QLabel("Click on Crunch button to initiate search procedure")  

        self.filebrowsebutton = QPushButton("Browse.")    
        self.dirbrowsebutton = QPushButton("Browse.")    
        self.searchbox = QLineEdit("")
        self.regexbox = QLineEdit("")
        self.conditionbox= QLineEdit("")
        self.resultbox = QTextBrowser()
        self.statsbox = QTextBrowser()
        self.submitbutton = QPushButton("Go")
        self.configbutton = QPushButton("See/Edit configuration file")

        self.progressbar = QProgressBar()
        
        layout = QGridLayout()
        
        layout.addWidget(self.filepathlabel, 0, 0)
        layout.addWidget(self.filebrowsebutton, 0, 1, 1, 2)
        layout.addWidget(self.dirpathlabel, 1, 0)
        layout.addWidget(self.dirbrowsebutton, 1, 1, 1, 2)
        layout.addWidget(self.searchlabel, 2, 0,)
        layout.addWidget(self.searchbox, 2, 1, 1, 2)
        layout.addWidget(self.regexlabel, 3, 0)
        layout.addWidget(self.regexbox, 3, 1, 1, 2) 
        layout.addWidget(self.conditionlabel, 4, 0)
        layout.addWidget(self.conditionbox, 4, 1, 1, 2)         
        layout.addWidget(self.configbutton, 5, 2)              
        layout.addWidget(self.submitbutton, 5, 1)
        layout.addWidget(self.progresslabel, 6, 0, 1 , 1)
        layout.addWidget(self.progressbar, 6, 1, 1, 2)
        layout.addWidget(self.resultbox, 8, 0, 5, 3)
        layout.addWidget(self.statsbox, 13, 0, 2, 3)
        
        self.setLayout(layout)        
        self.setWindowTitle("Skout! BETA")
        self.progressbar.setRange(0, 100)
        
        self.connect(self.filebrowsebutton, SIGNAL("clicked()"), self.file_browse )
        self.connect(self.dirbrowsebutton, SIGNAL("clicked()"), self.dir_browse)
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
        if self.dirbrowsebutton.text() == "NA" and self.filebrowsebutton.text() != "" :
            Driver(window, lv, str(self.filebrowsebutton.text()))
        elif self.filebrowsebutton.text() == "NA" and self.dirbrowsebutton.text() != "":
            Driver(window, lv, str(self.dirbrowsebutton.text()))
        else:
            self.statsbox.append("<font color='red'>Please select a file or a directory.</font>")

        
    def open_cfg(self):
        subprocess.call(['kate', os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg'])        
     
    def file_browse(self):
        dialog = QFileDialog(self)                
        self.filebrowsebutton.setText(str(dialog.getOpenFileName()))
        self.dirbrowsebutton.setText("NA")
        
    def dir_browse(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)         
        self.dirbrowsebutton.setText(str(dialog.getExistingDirectory()))
        self.filebrowsebutton.setText("NA")
                 
        
app = QApplication(sys.argv)
window = Terminal()
window.resize(600, 1000)
window.show()

app.exec_()