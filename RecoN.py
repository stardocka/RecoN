from bs4 import BeautifulSoup
import requests
import re

#URL = input("URL: ")
URL = "https://www.portail-ie.fr/ressources/lexique/osint/"

def RequestWebPage():
    """ Request a web page and get the content """
    response = requests.get(URL)
    HTMLParsing = BeautifulSoup(response.text, "html.parser")
    elements = HTMLParsing.find_all(["h1", "h2", "h3", "h4", "p"])
    TextOnThePage = " ".join([el.get_text(separator=" ") for el in elements])
    CleanText = re.sub(r"\s+", " ", TextOnThePage).strip()
    return CleanText

wordlist = []
DicOccurrence = {}

def normalize(word):
    word = word.lower()
    word = re.sub(r"[.,;:!?()«»\"']", "", word)
    word = re.sub(r"^[ldjctsmn]’", "", word)
    return word


def DefineWordList():
    global wordlist
    WebContent = RequestWebPage()
    WordsList = WebContent.split(" ")

    for word in WordsList:
        NormalizeWord = normalize(word)
        if len(NormalizeWord) > 3 :
            wordlist.append(NormalizeWord)
    
    return wordlist

DefineWordList()

def Search4Occurrence():
    global DicOccurrence
    occ = 0

    for word in wordlist:
        for i in range(len(wordlist)):
            #print(word, wordlist[i])
            if word == str(wordlist[i]):
                occ+= 1
        DicOccurrence[word] = occ
        occ = 0
    return DicOccurrence

Search4Occurrence()

def Wordlist2BruteForce():
    FinalList = []
    SortedDico = sorted(DicOccurrence.items(), key=lambda x: x[1], reverse=True)
    for words in SortedDico:
        if words[1] > 2:
            FinalList.append(words[0])

    with open("RecoN-Wordlist.txt", "w", encoding="UTF-8") as file:
        for candidates in FinalList:
            file.write(candidates+"\n")

    print("=========================================")
    print("=           CANDIDATE WORD              =")
    print("=========================================")

    for i in range(len(FinalList)):
        print(f"{i}. {FinalList[i]}")
    
    print("=========================================")
    
    
    return FinalList

Wordlist2BruteForce()