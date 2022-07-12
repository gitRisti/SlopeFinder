#Results class for handling multiple results

#EasyGUI for file explorer handling
import easygui
import os
import csv
from Result import Result

import matplotlib.pyplot as plt
from scipy.stats import linregress

def retrieveFile():
    files = easygui.fileopenbox(default = "*.itc",multiple=True)
    return files
 
if __name__ == "__main__":
    
    results = []  
    #Get .itc files
    files = retrieveFile()
    
    for file in files:
        
        #Import ITC results text file and convert to list object
        with open(file) as f:
            content = csv.reader(f,delimiter=',')
            contentList = list(content)
        #basename -> get filename with extension
        #splitext -> split filename and extension
        result = Result(os.path.splitext(os.path.basename(file))[0],contentList)
        results.append(result)
    
    for result in results:
        plt.scatter(result.x,result.y)
        fit = linregress(result.x,result.y)
        plt.axline((0,0),slope=fit.slope)
        plt.text(1,-0.2,f'R2: {fit.rvalue}\n slope: {fit.slope*4.184}')
        plt.show()
    
    


    


