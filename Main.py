#EasyGUI for file explorer handling
import easygui
import os

#Prompt user to select file(s) for data analysis
#file = easygui.fileopenbox(default = "*.itc")
file = os.path.abspath("TestData\\220626 LEP4 1 TP0.itc")
print(file)
with open(file) as f:
    content = f.readlines()
    
#Obtain the injection table
with open("InjectionTable.txt",'w') as InjectionTable:
    for line in content[10:]:
        if "# 0" in line:
            break
        InjectionTable.write(line)
        print(line)
        
        
#LINE 11: Injection table