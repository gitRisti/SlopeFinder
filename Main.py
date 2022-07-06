#EasyGUI for file explorer handling
import easygui
import os
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress

def stringToFloat(string):
    splitString = string.split()
    value = float(splitString[1]) 
    return value

def findListAverage(lst,start,end,index):
    avg = sum(float(i[index]) for i in lst[start:end])/len(lst[start:end])
    return avg

def plotConcentration(sizes,concentration):
    concList = [0]
    for n in range(0,len(sizes)):
        concList.append(sizes[n]*concentration+concList[n]) 
    print(concList)
    return concList

#Handle calculation of average heat rates, data set and number of injections as input
def findHeatRate(data,n):
    injectionLengths = []
    injectionIndices = []
    averageHeats = [0]
    #Find injection locations in data
    for i in range(1,n+1,1):
        for line in data:
            if f'@{i}' in line[0]:
                injectionLengths.append(int(float(line[3])))
                injectionIndices.append(data.index(line)+1)
    #Add virtual "last" injection
    injectionIndices.append(len(data)+1)
    #Calculate baseline
    baseline = findListAverage(data,injectionIndices[1]-61,injectionIndices[1]-1,1)
    #Calculate average heat rates of injections
    for i in range(2,n+1,1):
        averageHeats.append((findListAverage(data,injectionIndices[i]-61,injectionIndices[i]-1,1)) - baseline)
    return averageHeats
    

if __name__ == "__main__":
    #Prompt user to select file(s) for data analysis
    #file = easygui.fileopenbox(default = "*.itc")
    injectionSizes = []
    numberOfInjections = 0
    conc = 1
    file = os.path.abspath("TestData\\220625 LEP2 2 TP0.itc")
    
    #Import ITC results text file and convert to list object
    with open(file) as f:
        content = csv.reader(f,delimiter=',')
        contentList = list(content)
      
    #Obtain injection table
    with open(f'{str(file)} InjectionTable.txt','w') as InjectionTable:
          #Define beginning of injection table
        for line in contentList:
            if 'ADC' in line[0]:
                injectionIndex = contentList.index(line) + 2
           #Create arrays containing injection volumes and spacings         
        for line in contentList[injectionIndex:]:
            #Find end of injection table
            if "# 0" in line[0]:
                break
            if numberOfInjections > 0:
                injectionSizes.append(stringToFloat(line[0]))
            numberOfInjections += 1
            
            #Create InjectionTable text file
            for row in line:
                InjectionTable.write(row)
            InjectionTable.write('\n')
        y = findHeatRate(contentList,numberOfInjections)
        x = plotConcentration(injectionSizes,1)
        
        #Plot results
        plt.scatter(x,y)
        fit = linregress(x,y)
        plt.axline((0,0),slope=fit.slope)
        plt.text(1,-0.2,f'R2: {fit.rvalue}\n slope: {fit.slope*4.184}')
        plt.show()

    


