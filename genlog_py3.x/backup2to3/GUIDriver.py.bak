'''
Created on 13-Feb-2014

@author: Abhimanyu
'''

import logProcessor
import os
import utilities

class Driver():
    
    def __init__(self, window, condition_object, root_path):        
        self.success_count = 0  
        self.mainwindow = window
        self.line_number = 0
        self.eligible_lines = 0
        self.error = {"DivideByZero": 0, "ValueType": 0 }
        self.flag = True
        self.lv = condition_object
        self.files_processed = 0
        self.files_found = 0 
        self.directories_processed = 0
        
        self.mainwindow.progresslabel.setText("Calculating size of search location.")
        temp = utilities.Filesize(root_path)
        self.total_lines = temp.total_lines
        
        self.crawler(root_path)
        self.mainwindow.progresslabel.setText("Search complete.")
        self.print_statistics()
        
        
        
    def search(self, filepath):
        """Finds and prints the lines passing all the search, regex, rule conditions.
        """
        
        self.files_processed += 1
        #self.total_lines += utilities.Filesize.file_len(filepath)
        logStream = open(filepath,'r')        
        
        progress_text = "Searching file %s "%(filepath)  
        self.mainwindow.progresslabel.setText(progress_text)
        file_found_flag = False
        
        for line in logStream:
            self.line_number += 1  
            self.mainwindow.progressbar.setValue(int(float(self.line_number)/float(self.total_lines)*100))
            lp = logProcessor.LogProcessor(line)  
                   
            if lp.lineofInterest(str(self.mainwindow.searchbox.text()),str(self.mainwindow.regexbox.text())):
                self.eligible_lines += 1
                if self.mainwindow.conditionbox.text():
                    keyInfo = lp.infoExtracter()                 
                    try: 
                        self.flag = self.lv.logMatcher(keyInfo)      
                    except ZeroDivisionError:
                        self.error["DivideByZero"] += 1                     
                        self.flag = False             
                    except (ValueError, TypeError):   
                        self.error["ValueType"] += 1     
                        self.flag = False
                    
                if self.flag:  
                    if not file_found_flag:
                        self.mainwindow.resultbox.append("<font color = blue>Line(s) found at : " + filepath + "</font>")                        
                    self.mainwindow.resultbox.append(line)                                                                          
                    self.success_count += 1  
                    file_found_flag = True                 
                    
        if file_found_flag:
            self.files_found +=1
            print ""
               
            
    def crawler(self,filepath):
        """Recursively calls itself for each directory and calls the search function for each file
        """     
                
        
        if os.path.isdir(filepath):
            self.directories_processed += 1           
            for f in os.listdir(filepath):
                self.crawler(os.path.join(filepath,f))
        else:
            if os.path.isfile(os.path.join(filepath)):
                self.search(filepath) 
            
           
            
    def print_statistics(self):  
        """Prints results summary.
        """
        self.mainwindow.statsbox.append("____________________RESULT-STATISTICS_____________________________________________")
        self.mainwindow.statsbox.append("<font color=blue>Total lines processed :</font> %d" %(self.total_lines))
        self.mainwindow.statsbox.append("<font color=blue>Total files processed :</font> %d" %(self.files_processed))
        self.mainwindow.statsbox.append("<font color=blue>Total directories processed:</font> %d" %(self.directories_processed))
        self.mainwindow.statsbox.append("<font color=blue>Total files having lines matching the conditions:</font> %d" %(self.files_found))
        self.mainwindow.statsbox.append("<font color=blue>Total lines eligible according to search string / regex pattern (-s) : </font>%d" %(self.eligible_lines))

        if self.success_count == 0:        
            self.mainwindow.statsbox.append("<font color=red>No log found. Please check your condition / search string</font>")        
        else:
            self.mainwindow.statsbox.append("<font color=blue>Total eligible lines satisfying all the conditions :</font>%d" %(self.success_count))      
        
        self.mainwindow.statsbox.append("____________________ERROR-STATISTICS______________________________________________")        
        if self.error["DivideByZero"]:
            self.mainwindow.statsbox.append("<font color=red>!!ERROR :The script was made to divide by zero in %d instances. Those lines were skipped. !!</font>" % self.error["DivideByZero"])
        if self.error["ValueType"]:
            self.mainwindow.statsbox.append("<font color=red>!!ERROR :Value Error or Type Error was raised %d times.\nThis usually happens when there is no such variable/ keyword as mentioned in the rulestring.\nArithematic operators are applied on unsupported data like a string.\nThis can also happen when the datetime/time/date pattern in configuration file does not match the input.\nThose lines were skipped.!!</font>" % self.error["ValueType"])
        if (not self.error["DivideByZero"]) &  (not self.error["ValueType"]) :
            self.mainwindow.statsbox.append("<font color=green>No errors encountered.</font>")
            
    