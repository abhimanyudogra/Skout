'''
Created on 03-Feb-2014

@author: Abhimanyu

'''

from pyparsing import oneOf, Word, operatorPrecedence, opAssoc, alphanums, nums
import types
from datetime import datetime

def make_binary_tree(raw_list):
    ''' Takes a list generated as parsing result and converts it into a binary-tree list. That is -the result is a list of lists with each list having not more than 3 members (operand-operator-operand) or (operator-operand)
    '''    
    for element in raw_list:        
        if type(element) == list:
            make_binary_tree(element)

    size = len(raw_list)
    while size > 3:
        raw_list[:3] = [[i for i in raw_list[:3]]]
        size = len(raw_list)
    return raw_list
  
def parse_it(rule):    
    ''' Reads the string and forms a list of lists with each list representing an expression containing an  operands separated by operators according to precedence levels.
    '''   
    integer = Word(nums + ".").setParseAction(lambda t:float(t[0]))
    nonint = Word(alphanums + ":" + ".")
    operand = integer ^ nonint     
    #signop = oneOf('+ -')
    multop = oneOf('* /')
    plusop = oneOf('+ -')
    compop = oneOf('<= >= < > =')
    logiop  = oneOf('& |')
    rfactop = oneOf('!')
    lfactop = oneOf('%')
    expr = operatorPrecedence( operand,[
                             (rfactop, 1, opAssoc.LEFT),  
                             (lfactop, 1, opAssoc.RIGHT),    
                     #        (signop, 1, opAssoc.RIGHT),
                             (multop, 2, opAssoc.LEFT),
                             (plusop, 2, opAssoc.LEFT),
                             (compop, 2, opAssoc.LEFT),
                             (logiop, 2, opAssoc.LEFT),]
                              )

    return make_binary_tree(expr.searchString(rule)[0][0].asList())
       

'''if __name__=="__main__":
    
    a= parse_it("@today")
    print a'''

    