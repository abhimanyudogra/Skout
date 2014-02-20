'''
Created on 14-Jan-2014

@author: Abhimanyu
'''
import re
import os
from ConfigParser import SafeConfigParser
pattern = SafeConfigParser()
pattern.read(os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg')

class LogProcessor():   
    """This class deals with each line of logfile that is passed to it during initialization. Each line has one instance.
    """ 
    keyExtracter = re.compile(pattern.get("usersettings","searchpattern"),re.VERBOSE)
    idtimeExtracter= re.compile(pattern.get("usersettings","logtimepattern"), re.VERBOSE)
        
    def __init__(self,line):
        self.currentLine = line
        
   
    def lineofInterest(self, search_string, regex):
        """Returns true if the line being examined has vital information
        """
        
        if search_string:
            searchString = search_string
            searchString = re.escape(searchString)
            searchString = searchString.replace("\<\<alphas\>\>","[a-zA-Z]+") 
            searchString = searchString.replace("\<\<int\>\>","[0-9]+") 
            searchString = searchString.replace("\<\<alphanums\>\>","[a-zA-Z0-9]+") 
            searchString = searchString.replace("\<\<decimal\>\>","[0-9]+.[0-9]+")                                    
            searchExtracter = re.compile(searchString)  
               
            if regex:
                regex = re.compile(regex)
                
                if searchExtracter.search(self.currentLine) and regex.search(self.currentLine):
                    return True            
            else:
                if searchExtracter.search(self.currentLine):
                    return True     
        elif regex:
            regex = re.compile(regex)
            if regex.search(self.currentLine):
                return True 
            
        else:
            if self.keyExtracter.search(self.currentLine):
                    return True 
        

    def infoExtracter(self): 
        """Extracts relevent information and returns them as a dictionary.
        
        """            
        self.keyInfo = self.keyExtracter.findall(self.currentLine)
        keyDict = {}
        try:
            for element in self.keyInfo:
                keyDict[element[0]]=element[1]  
        except IndexError:
            pass      
        try:
            year, month, date, hours , minutes , seconds, milliseconds= self.idtimeExtracter.search(self.currentLine).groups()
            import datetime
            dtobj = datetime.datetime(int(year), int(month), int(date), int(hours), int(minutes), int(seconds), int(milliseconds), None)              
            keyDict["datetime"]= dtobj
            keyDict["date"] = dtobj.date()
            keyDict["time"] = dtobj.time()
        except (AttributeError, ValueError):
            pass    
        
        for key,value in keyDict.items():
            try:
                new_val = float(value)
            except (ValueError, TypeError):
                pass
            else:
                keyDict[key] = new_val            
                    
        return keyDict

if __name__=="__main__":
   
    log = open("singleLog")     
  
    for line in log:
        lp = LogProcessor(line)  
        if lp.lineofInterest(False, False)  :    
            keyInfo = lp.infoExtracter()
            print keyInfo
           

    
