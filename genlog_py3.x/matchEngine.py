'''
Created on 17-Jan-2014

@author: Abhimanyu
'''
import os
import types
import datetime 
from configparser import RawConfigParser
pattern = RawConfigParser()
pattern.read(os.path.dirname(os.path.abspath(__file__)) + '/patterns.cfg')


class LogVerifier():
    def __init__(self, tree):
        self.ruleTree = tree
        self.keyInfo = {}
    
    def isKey(self,arg):
        """Returns True if n belongs to "keyinfo" class variable.
        """
        if arg in list(self.keyInfo.keys()):
            return True
        else:
            return False   
        
    def equationSolver_single(self, arg, operator):
        """Takes two operators: arg and operator. Solves the euqation for unary operators.
        """
    
        if operator == "!":
            if self.isKey(arg):
                return not self.keyInfo[arg]
            else:
                return not arg    
        
    def equationSolver(self,arg1,arg2,operator):
        """ Takes 3  arguments which are supposed to be the operator and the operands . Returns the expected result of the expression for binary operators
        """
               
        if operator == '&':
            return arg1 and arg2
        
        elif operator == '|':
            return arg1 or arg2
        
        elif operator == '=':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] == self.keyInfo[arg2] 
                elif arg1 == "datetime":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatetimepattern"))  
                    return self.keyInfo[arg1] == arg2                    
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return self.keyInfo[arg1] == arg2
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()
                    return self.keyInfo[arg1] == arg2                                                 
                else:
                    return self.keyInfo[arg1] == arg2                           
            elif self.isKey(arg2):
                if arg2 == "datetime":
                    arg1 = datetime.datetime.strptime(arg1,pattern.get("usersettings","ruledatetimepattern"))
                    return arg1 == self.keyInfo[arg2]
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return arg1 == self.keyInfo[arg2]
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()
                    return arg1 == self.keyInfo[arg2] 
                else:
                    return arg1 == self.keyInfo[arg2]                           
            else: 
                return arg1 == arg2
            
        elif operator == '>':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] > self.keyInfo[arg2] 
                elif arg1 == "datetime":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatetimepattern"))  
                    return self.keyInfo[arg1] > arg2                    
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return self.keyInfo[arg1] > arg2
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()
                    return self.keyInfo[arg1] > arg2                                                 
                else:
                    return self.keyInfo[arg1] > arg2                           
            elif self.isKey(arg2):
                if arg2 == "datetime":
                    arg1 = datetime.datetime.strptime(arg1,pattern.get("usersettings","ruledatetimepattern"))
                    return arg1 > self.keyInfo[arg2]
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return arg1 > self.keyInfo[arg2]
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()
                    return arg1 > self.keyInfo[arg2] 
                else:
                    return arg1 > self.keyInfo[arg2]                           
            else: 
                return arg1 > arg2
            
        elif operator == '<':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] < self.keyInfo[arg2] 
                elif arg1 == "datetime":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatetimepattern"))  
                    return self.keyInfo[arg1] < arg2                    
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return self.keyInfo[arg1] < arg2
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()  
                    return self.keyInfo[arg1] < arg2                                                 
                else:
                    return self.keyInfo[arg1] < arg2                           
            elif self.isKey(arg2):
                if arg2 == "datetime":
                    arg1 = datetime.datetime.strptime(arg1,pattern.get("usersettings","ruledatetimepattern"))
                    return arg1 < self.keyInfo[arg2]
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return arg1 < self.keyInfo[arg2]
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()  
                    return arg1 < self.keyInfo[arg2] 
                else:
                    return arg1 < self.keyInfo[arg2]                           
            else: 
                return arg1 < arg2
            
        elif operator == '<=':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] <= self.keyInfo[arg2] 
                elif arg1 == "datetime":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatetimepattern"))  
                    return self.keyInfo[arg1] <= arg2                    
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return self.keyInfo[arg1] <= arg2
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()  
                    return self.keyInfo[arg1] <= arg2                                                 
                else:
                    return self.keyInfo[arg1] <= arg2                           
            elif self.isKey(arg2):
                if arg2 == "datetime":
                    arg1 = datetime.datetime.strptime(arg1,pattern.get("usersettings","ruledatetimepattern"))
                    return arg1 <= self.keyInfo[arg2]
                elif arg1 == "date":
                    arg2 = datetime.date.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return arg1 <= self.keyInfo[arg2]
                elif arg1 == "time":
                    arg2 = datetime.time.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time() 
                    return arg1 <= self.keyInfo[arg2] 
                else:
                    return arg1 <= self.keyInfo[arg2]                           
            else: 
                return arg1 <= arg2
            
        elif operator == '>=':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] >= self.keyInfo[arg2] 
                elif arg1 == "datetime":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatetimepattern"))  
                    return self.keyInfo[arg1] >= arg2                    
                elif arg1 == "date":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return self.keyInfo[arg1] >= arg2
                elif arg1 == "time":
                    arg2 = datetime.datetime.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time()  
                    return self.keyInfo[arg1] >= arg2                                                 
                else:
                    return self.keyInfo[arg1] >= arg2                           
            elif self.isKey(arg2):
                if arg2 == "datetime":
                    arg1 = datetime.datetime.strptime(arg1,pattern.get("usersettings","ruledatetimepattern"))
                    return arg1 >= self.keyInfo[arg2]
                elif arg1 == "date":
                    arg2 = datetime.date.strptime(arg2,pattern.get("usersettings","ruledatepattern")).date()
                    return arg1 >= self.keyInfo[arg2]
                elif arg1 == "time":
                    arg2 = datetime.time.strptime(arg2,pattern.get("usersettings","ruletimepattern")).time() 
                    return arg1 >= self.keyInfo[arg2] 
                else:
                    return arg1 >= self.keyInfo[arg2]                           
            else: 
                return arg1 >= arg2
        
        elif operator == '+':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] + self.keyInfo[arg2]                          
                else:
                    return self.keyInfo[arg1] + arg2                           
            elif self.isKey(arg2):
                    return arg1 + self.keyInfo[arg2]                           
            else: 
                return arg1 + arg2      
            
        elif operator == '-':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] - self.keyInfo[arg2]                           
                else:
                    return self.keyInfo[arg1] - arg2                           
            elif self.isKey(arg2):
                    return arg1 - self.keyInfo[arg2]                            
            else: 
                return arg1 - arg2  
        
        elif operator == '*':
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] * self.keyInfo[arg2]                           
                else:
                    return self.keyInfo[arg1] * arg2                           
            elif self.isKey(arg2):
                    return arg1 * self.keyInfo[arg2]                            
            else: 
                return arg1 * arg2  
            
        elif operator == '/':            
            if self.isKey(arg1):
                if self.isKey(arg2):
                    return self.keyInfo[arg1] / self.keyInfo[arg2]                           
                else:
                    return self.keyInfo[arg1] / arg2                         
            elif self.isKey(arg2):
                    return arg1 / self.keyInfo[arg2]                           
            else: 
                return arg1 / arg2 

       
        
    def treeSolver(self,rTree):        
        """Takes the tree generated by the lisTreeBuilder method of ruleEngine module and solves it by looking up the information extracted 
        from the log file by the infroExtracter method of the logProcessor module        
        """
        if len(rTree) == 3:                    
            if type(rTree[0]) == list:
                arg1=self.treeSolver(rTree[0])
            else :
                arg1=rTree[0]
            if type(rTree[2]) == list:
                arg2=self.treeSolver(rTree[2])
            else :
                arg2=rTree[2]
            return self.equationSolver(arg1, arg2, rTree[1])     
               
        elif len(rTree) == 2:
            if type(rTree[0]) == list:
                arg = self.treeSolver(rTree[0])
            else :
                arg = rTree[0]
            return self.equationSolver_single(arg, rTree[1])
                
            
                       
            
    def logMatcher(self,keyInfo):
        """Returns True if the line being examined matches the required specifications
            
        """        
        rtree = self.ruleTree
        self.keyInfo = keyInfo
        return self.treeSolver(rtree)
            
'''if __name__=="__main__":
    d = [[['LTP', '=', ['validBids', '*', 'validAsks']], '|', ['updateLevel', '=', '8']]]
    c = [[['LTP', '=', ['5','+','5']], '|', ['updateLevel', '=', '8']]]
    
    lv = LogVerifier(c)
    lv.keyInfo["datetime"] = datetime.datetime
    print lv.equationSolver_single(False ,'!')'''
     
        
        