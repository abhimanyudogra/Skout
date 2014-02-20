'''
Created on 06-Feb-2014

@author: Abhimanyu
'''
import os
class Filesize():   
    
    def __init__(self, path):
        self.total_lines=0  
        self.total_lines_calculator(path)
        
    def file_len(self,fname):
        """Calculates number of lines in a file.
        """
        i = -1
        with open(fname) as f:
            for i,l in enumerate(f):
                pass
            
        return i + 1
    
    def total_lines_calculator(self,path):        
        """Takes filepath as an argument. Calculates the number of lines in all the files present in the directories inside the path and their subdirectories.
        """
        if os.path.isdir(path):                       
            for f in os.listdir(path):
                self.total_lines_calculator(os.path.join(path,f))
        else:
            if os.path.isfile(os.path.join(path)):
                self.total_lines += self.file_len(path) 
        

class ProgressBar:
    """ Tool to create a dynamic progress bar in the shell.
    """
    def __init__(self):
        
        self.prog_bar = '[]'
        self.fill_char = '#'
        self.width = 40
        self.update_amount(0)    

    def update_amount(self, new_amount):
        """ Updates the progress bar.
        """
        percent_done = new_amount
        all_full = self.width - 2
        num_hashes = int(round((percent_done / 100.0) * all_full))
        self.prog_bar = '[' + self.fill_char * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) / 2) - len(str(percent_done))
        pct_string = '%d%%' % percent_done
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])

    def __str__(self):
        return str(self.prog_bar)
    
    
if __name__=="__main__":
    p = ProgressBar()
    p.update_amount(20)
    print str(p) + chr(27) + '[A'
    
    