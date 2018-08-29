import re
import sys



def writeToOutputFile():
    for k, v in sorted(wordDict.items()):
        outputF.write(k + ' ' + str(v) + '\n')

def createWordDict():
    wordDict = {}

    for word in wordList:
        if word not in wordDict:
            wordDict[word] = wordList.count(word)
    return wordDict

def createWordList():
    regExp = r'\b\w+\b'
    wordList = re.findall(regExp, fileStr)
    return wordList

def setupFiles():
    inputFileName = sys.argv[1:][0]
    outputFileName = sys.argv[1:][1]

    try:
        inputF = open(inputFileName, 'r')
    except FileNotFoundError:
        print('Oops, input file not found')
        exit()
    outputF = open(outputFileName, 'w')

    return inputF, outputF

inputF , outputF = setupFiles()
fileStr = inputF.read().lower()

wordList = createWordList()
wordDict = createWordDict()
writeToOutputFile()

inputF.close()
outputF.close()