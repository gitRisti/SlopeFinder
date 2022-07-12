class Result:
    
    def stringToFloat(self,string):
        splitString = string.split()
        value = float(splitString[1]) 
        return value
    
    def findListAverage(self,lst,start,end,index):
        avg = sum(float(i[index]) for i in lst[start:end])/len(lst[start:end])
        return avg
    
    def plotConcentration(self,sizes,concentration):
        concList = [0]
        for n in range(0,len(sizes)):
            concList.append(sizes[n]*concentration+concList[n]) 
        return concList
    
    #Handle calculation of average heat rates, data set and number of injections as input
    def findHeatRate(self,data,n):
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
        baseline = self.findListAverage(data,injectionIndices[1]-61,injectionIndices[1]-1,1)
        #Calculate average heat rates of injections
        for i in range(2,n+1,1):
            averageHeats.append((self.findListAverage(data,injectionIndices[i]-61,injectionIndices[i]-1,1)) - baseline)
        return averageHeats
    
    def findxy(self):
        injectionSizes = []
        numberOfInjections = 0
        #Define beginning of injection table
        for line in self.data:
          if 'ADC' in line[0]:
              injectionIndex = self.data.index(line) + 2
              
        #Create arrays containing injection volumes and spacings         
        for line in self.data[injectionIndex:]:
            #Find end of injection table
            if "# 0" in line[0]:
                break
            if numberOfInjections > 0:
                injectionSizes.append(self.__stringToFloat(line[0]))
            numberOfInjections += 1
            
        self.y = self.findHeatRate(self.data,numberOfInjections)
        self.x = self.plotConcentration(injectionSizes,1)  
        
    def __init__(self,name,data):
        self.name = name
        self.data = data
        self.findxy()

                  
        
    
        
        