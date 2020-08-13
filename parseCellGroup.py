import re
import csv
import os

#inputFile = r'c:/Work/studty/ParsePrimaryCellGroup/rawMsg.txt'
#outputFile = r'c:/Work/studty/ParsePrimaryCellGroup/out.csv'

inputFile = input("Please insert file path: ")
outputFile = os.path.splitext(inputFile)[0] + '_out.csv'

#Example
#11:16:51.233 04-Aug-20 RRC DL DL-DCCH RadioBearerConfig DL-DCCH RadioBearerConfig
#. . . . . . . . . . . . . . . . . . . .moreThanOneRLC
#. . . . . . . . . . . . . . . . . . . . .primaryPath
#. . . . . . . . . . . . . . . . . . . . . .cellGroup: 1
#. . . . . . . . . . . . . . . . . . . . .ul-DataSplitThreshold: 8 ( b12800)

timePattern = r'[\d:\.]+\s[\w-]+-\d+'
cellGroupPattern = r'cellGroup:\s\d'
splitPattern = r'ul-DataSplitThreshold:[\s\d(\w]+\)'


#write to list of list
with open(inputFile) as file:
    finalList = []
    tempList = []
    for f in file:
        #find timestamp
        if bool(re.search(timePattern, f)):
            #only update finalList if  there are more than one cell group information is found.
            if(len(tempList) > 1):
                finalList.append(tempList)
                tempList = []
                tempList.append(re.search(timePattern, f)[0])
            else:
                tempList=[]
                tempList.append(re.search(timePattern, f)[0])
        #find cell group information
        if bool(re.search(cellGroupPattern, f)):
            tempList.append(re.search(cellGroupPattern, f)[0])
        #find ul split information
        if bool(re.search(splitPattern, f)):
            tempList.append(re.search(splitPattern, f)[0])



#write the finalList to csv
with open(outputFile, 'w', newline='') as outCsv:
    writer = csv.writer(outCsv)
    writer.writerows(finalList)

print("output file: ", outputFile)
