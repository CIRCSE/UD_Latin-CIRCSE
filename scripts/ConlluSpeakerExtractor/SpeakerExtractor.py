import sys
from io import open
from conllu import parse
import argparse
from collections import defaultdict
from Classes import Speaker,SpeakerSpeech

def assignATokenToSpeaker(speakerList,token):
    
    speaker = ""
    tokenForm = ""
    for speakerElement in speakerList:
        if type(speakerElement) is not str:
            
            interval = (int(speakerElement[1].split("-")[0]),int(speakerElement[1].split("-")[1]))
            
            tokenId = token["id"]
            if  type(token["id"]) is tuple:
                tokenId = token["id"][0]

            if tokenId >= interval[0] and tokenId <= interval[1]:
                tokenForm = token['form']
                speaker = speakerElement[0]
        else:
            speaker = speakerElement
            tokenForm = token['form']
    return speaker,tokenForm


def assignATokenToSpeakerNew(speakerList,token):
    
    speaker = ""
    for speakerElement in speakerList:
        if type(speakerElement) is not str:
            
            interval = (int(speakerElement[1].split("-")[0]),int(speakerElement[1].split("-")[1]))
            
            if token["id"] >= interval[0] and token["id"] <= interval[1]:
                tokenForm = token['form']
                speaker = speakerElement[0]

        else:
            speaker = speakerElement
            tokenForm = token['form']
    return speaker,tokenForm
    
  

def elemetAnalyzer(stringa):
    speaker =""
    otherElement = ""
    if "(" in stringa:
        stringElements = stringa.split("(")
        speaker = stringElements[0].strip()
        otherElement = stringElements[1].replace(")","").strip()
        if "token" in otherElement.lower():
            otherElement = otherElement.lower().replace("token","").strip()
        else:
            otherElement = otherElement.strip()

    return speaker,otherElement
        



SINGLE_INDENT ="* "
DOUBLE_INDENT ="   * "
TRIPLE_INDENT ="      * "
QUAD_INDENT ="         * "
QUAD_TAB ="         "

# aFile = "localfile
# data_file = open(aFile, "r", encoding="utf-8") 

data_file = open(sys.argv[1], "r", encoding="utf-8") 
file_content = data_file.read() 
sentences = parse(file_content) 

senteceBySpeaker = defaultdict(list)

speakerObjectlist = list()

currentSpeech = SpeakerSpeech()
currentSpeaker = ""
for sentence in sentences: # ciclo sulle frasi e uso la variabile sentence per ogni frase
    speaker = sentence.metadata['speaker']
    speakerElements = speaker.split(",")
    
    speakerList = []
    if len(speakerElements) > 1: 
        for element in speakerElements:
            speaker,otherElement = elemetAnalyzer(element)
            speakerList.append((speaker,otherElement))
            if not any(speakObj.name == speaker.strip() for speakObj in speakerObjectlist):
                newSpeaker = Speaker(speaker.strip())
                speakerObjectlist.append(newSpeaker)
          
    elif "(" in speakerElements[0]:
        speaker,otherElement = elemetAnalyzer(speakerElements[0])
        if not any(speakObj.name == speaker.strip() for speakObj in speakerObjectlist):
            newSpeaker = Speaker(speaker.strip())
            speakerObjectlist.append(newSpeaker)
        speakerList.append(speaker)
    else:
        if not any(speakObj.name == speaker.strip() for speakObj in speakerObjectlist):
            newSpeaker = Speaker(speaker.strip())
            speakerObjectlist.append(newSpeaker)
        speakerList.append(speaker.strip())
    


    sentenceText = []



    
    for token in sentence:
        if  type(token["id"]) is tuple:

         
            speaker,form = assignATokenToSpeaker(speakerList,token)
            
           

            if len(currentSpeaker) == 0:
                currentSpeaker = speaker

            


            if speaker != currentSpeaker:
                speakerObj = next((x for x in speakerObjectlist if x.name == currentSpeaker), None)
                currentSpeech.appendSentenceToSpeech()
                speakerObj.appendSpeech(currentSpeech)

                currentSpeech = SpeakerSpeech()
                currentSpeech.appendTokenToSpeech(token)
                
                currentSpeaker = speaker
            else:
                currentSpeech.appendTokenToSpeech(token)


        else:
            if len(currentSpeaker) == 0:
                currentSpeaker = speaker

            speaker,form = assignATokenToSpeaker(speakerList,token)




            if speaker != currentSpeaker:


                speakerObj = next((x for x in speakerObjectlist if x.name == currentSpeaker), None)
                currentSpeech.appendSentenceToSpeech()
                speakerObj.appendSpeech(currentSpeech)
               

                currentSpeech = SpeakerSpeech()
                currentSpeech.appendTokenToSpeech(token)
                
                currentSpeaker = speaker
            else:
                currentSpeech.appendTokenToSpeech(token)



    currentSpeech.appendSentenceToSpeech()

speakerObj = next((x for x in speakerObjectlist if x.name == currentSpeaker), None)
currentSpeech.appendSentenceToSpeech()
speakerObj.appendSpeech(currentSpeech)

for speaker in speakerObjectlist:
    speaker.getAllTokenCount()

    print("## "+str(speaker) + " ("+str(speaker.getAllTokenCount())+" token with multiword)") 
    print("* Number of speeches: "+str(len(speaker.speeches)))
    for idxSpeec,speech in enumerate(speaker.speeches):

        speechText, ttr = speech.getSpeechText()
        print(SINGLE_INDENT + "Speech no. " + str(idxSpeec+1))
        print(SINGLE_INDENT + "TTR: " + str(round(ttr, 3)))
        print(DOUBLE_INDENT + speechText)
        print(DOUBLE_INDENT + "Sentences :" + str(speech.getNumberOfSentences()))
        for sentenceidx,sentence in enumerate(speech.sentences):
            print(TRIPLE_INDENT + "Sentence: " + str(sentenceidx+1))
            print(QUAD_INDENT + speech.getSentenceText(sentence))
            treeDepth,tree = speech.getSpeechSentenceTreeDepth(sentence)
            print(QUAD_INDENT + "Sentence depth: "+ str(treeDepth))
            print(QUAD_TAB + "```")
            treeLines = tree.split("\n")
            for treeLine in treeLines:
                print(QUAD_TAB + treeLine)
            print(QUAD_TAB + "```")
            
    print()
