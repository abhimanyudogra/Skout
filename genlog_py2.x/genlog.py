#! /path/to/python
'''
Created on 14-Jan-2014

@author: Abhimanyu
'''
import ruleParser
import argparse
import logProcessor
import matchEngine
import os
import utilities
from sys import exit

class Driver():
    
    def __init__(self, condition_object, root_path):        
        self.success_count = 0  
        
        self.line_number = 0
        self.eligible_lines = 0
        self.error = {"DivideByZero": 0, "ValueType": 0 }
        self.flag = True
        self.lv = condition_object
        self.files_processed = 0
        self.files_found = 0 
        self.directories_processed = 0
        
        temp = utilities.Filesize(root_path)
        self.total_lines = temp.total_lines
        
        self.crawler(root_path)
        self.print_statistics()
        
        
        
    def search(self, filepath):
        """Finds and prints the lines passing all the search, regex, rule conditions.
        """
        
        self.files_processed += 1
        #self.total_lines += utilities.Filesize.file_len(filepath)
        logStream = open(filepath,'r')
        p = utilities.ProgressBar()  
        print_path = filepath.split("/")
        print ">>> Searching file %s ......%s                                              " %("/".join(print_path[:4]) ,"/".join(print_path[-3:]))
        file_found_flag = False
        
        for line in logStream:
            self.line_number += 1  
            p.update_amount(int(float(self.line_number)/float(self.total_lines)*100))
            print str(p) + chr(27) + '[A'
            lp = logProcessor.LogProcessor(line)         
            if lp.lineofInterest(args.search,args.regex):
                self.eligible_lines += 1
                if args.condition:
                    keyInfo = lp.infoExtracter()                 
                    try: 
                        self.flag = lv.logMatcher(keyInfo)      
                    except ZeroDivisionError:
                        self.error["DivideByZero"] += 1                     
                        self.flag = False             
                    except (ValueError, TypeError):   
                        self.error["ValueType"] += 1     
                        self.flag = False
                    
                if self.flag:  
                    print "                                                       "
                    print chr(27) + '[A' + chr(27),           
                    print line                                                                          
                    self.success_count += 1  
                    file_found_flag = True 
                
                    
        if file_found_flag:
            self.files_found +=1
            print ""
        
        print chr(27) + '[A' + chr(27),
            
        
            
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
        print "                                                                                  "           
        print "____________________RESULT-STATISTICS_____________________________________________"
        print "Total lines processed : %d" %(self.total_lines)
        print "Total files processed : %d" %(self.files_processed)
        print "Total directories processed: %d" %(self.directories_processed)
        print "Total files having lines matching the conditions: %d" %(self.files_found)
        print "Total lines eligible according to search string / regex pattern (-s) : %d" %(self.eligible_lines)

        if self.success_count == 0:        
            print "No log found. Please check your condition / search string"        
        else:
            print "Total eligible lines satisfying the conditions (-c if provided) %d" %(self.success_count)            
        
        print "____________________ERROR-STATISTICS______________________________________________"        
        if self.error["DivideByZero"]:
            print "!!ERROR :The script was made to divide by zero in %d instances. Those lines were skipped. !!" % self.error["DivideByZero"]
        if self.error["ValueType"]:
            print "!!ERROR :Value Error or Type Error was raised %d times.\nThis usually happens when there is no such variable/ keyword as mentioned in the rulestring or\nArithematic operators are applied on unsupported variables like string. This can also happen when the datetime/time/date pattern in configuration file does not match the input.\nThose lines were skipped.!!" % self.error["ValueType"]
        if (not self.error["DivideByZero"]) &  (not self.error["ValueType"]) :
            print "No errors encountered."
            
    



if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description='Simple search script with advanced and customizable information extraction and processing capabilities' ,epilog ='Currently supported arithematic operators are: "+" "-" "*" "/" "<" ">=" "<=" "=" which can be combined with "!" (left assosiative),"&"(and) and "|"(or) logical operators. Time format for the log file as well as the rule string is specified in and can be modified from "patterns.cfg" configuration file. Time can be accessed using the "time" keyword and all operators work on time objects except for arithematic "*" "/" "+" "-". Example : (time<=11:49:00.000000). Use parenthesis only to override the pre-configured standard operator precedence as it slows down the parsing grammar.')
    parser.add_argument("-s","--search", metavar='', default =False, help="The lines of interest are found by searching for the specified string. Available special keywords are <<alphas>>: For matching any word. <<alphanums>>: For matching all word + number combinations. <<int>>: For matching all pure numbers. <<decimal>>: For matching decimal numbers. ")
    parser.add_argument("-r", "--regex", metavar='', default = False,  help="The lines of interest are found by matching the specified regular expression.")
    parser.add_argument("-c", "--condition", metavar='', default = False,  help="The lines of interest are further filtered by specified rules. Information for matching of the rule is extracted from the target file using a pattern mentioned in the configuration file. Default: always True")
    parser.add_argument("-f","--filepath", metavar='',default = os.getcwd(), help="Specify the log file name/relative path. Default : current directory")
    
    args = parser.parse_args() 
    
    lv = None
    
    if args.condition:           
        print "Parsing condition string..."        
        ruleString = args.condition         
        try:    
            ruleTree = ruleParser.parse_it(ruleString)             
        except AttributeError:            
            print "!!ERROR :Attribute error was raised. Check the condition string. Script was terminated." 
            exit()               
        lv = matchEngine.LogVerifier(ruleTree)  
               
    instance = Driver(lv, args.filepath)
    