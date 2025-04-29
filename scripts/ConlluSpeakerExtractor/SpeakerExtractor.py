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
            
            intervals = speakerElement[1].split(";")
            for intervalRaw in intervals:

                beginEnd = intervalRaw.split("-")
                
                if len(beginEnd) > 1 :
                    interval = (int(beginEnd[0]),int(beginEnd[1]))
                else:
                    interval = (int(beginEnd[0]),int(beginEnd[0]))

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
    
  

def extractSpeakerList(speaker):
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


    return speakerList


def elemetAnalyzer(stringa):
    speaker =""
    otherElement = ""
    if "(" in stringa:
        stringElements = stringa.split("(")
        speaker = stringElements[0].strip()

        for i in range(1,len(stringElements)):
            otherElement = stringElements[i].replace(")","").strip()
            if "token" in otherElement.lower():
                otherElement = otherElement.lower().replace("token","").strip()
            else:
                otherElement = otherElement.strip()

    return speaker,otherElement
        
def initializeArgs():
    parser = argparse.ArgumentParser(prog='Speaker extractor',add_help=True, description='Tool for extracting and analyzing speeches in CoNLL-U format.')
    parser.add_argument('-i','--input', nargs='+',type=str,help='specify input file/files',required=False)
    parser.add_argument('-sc','--save_conllu', default=False, help='save the speaker conllu', action='store_true')

    args = parser.parse_args()


    return args




if __name__ == "__main__":

    program_arguments = initializeArgs()
    inputFiles  = program_arguments.input
    saveSpeakerConllu = program_arguments.save_conllu


    SINGLE_INDENT ="* "
    DOUBLE_INDENT ="   * "
    TRIPLE_INDENT ="      * "
    QUAD_INDENT ="         * "
    QUAD_TAB ="         "





    #aFile = "/Users/giovannimoretti/Downloads/UD_Latin-CIRCSE-main/conllu/01_Seneca_Hercules_Furens.conllu"
    #aFile = "/Users/giovannimoretti/Downloads/UD_Latin-CIRCSE-main/conllu/02_Seneca_Agamemnon.conllu"
    #aFile = "/Users/giovannimoretti/Downloads/UD_Latin-CIRCSE-main 2/conllu/04_Seneca_Oedipus.conllu"
    #inputFiles = []
    #inputFiles.append( "/Users/giovannimoretti/Downloads/UD_Latin-CIRCSE-main 2/conllu/04_Seneca_Oedipus.conllu")
    #data_file = open(aFile, "r", encoding="utf-8") 


    for file in inputFiles:
        data_file = open(file, "r", encoding="utf-8") 
        file_content = data_file.read() 
        sentences = parse(file_content) 

        senteceBySpeaker = defaultdict(list)

        speakerObjectlist = list()

        currentSpeech = SpeakerSpeech()
        currentSpeaker = ""
        for sentence in sentences: # ciclo sulle frasi e uso la variabile sentence per ogni frase
            senid = sentence.metadata['sent_id']
            speaker = sentence.metadata['speaker']

            speakerList = extractSpeakerList(speaker)

            sentenceText = []



            
            for token in sentence:
                if  type(token["id"]) is tuple:

                    speaker,form = assignATokenToSpeaker(speakerList,token)
                    
                    if len(currentSpeaker) == 0:
                        currentSpeaker = speaker

                    if speaker != currentSpeaker:
                        speakerObj = next((x for x in speakerObjectlist if x.name == currentSpeaker), None)
                        currentSpeech.appendSentenceToSpeech(senid)
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
                        currentSpeech.appendSentenceToSpeech(senid)
                        speakerObj.appendSpeech(currentSpeech)
                    

                        currentSpeech = SpeakerSpeech()
                        currentSpeech.appendTokenToSpeech(token)
                        
                        currentSpeaker = speaker
                    else:
                        currentSpeech.appendTokenToSpeech(token)



            currentSpeech.appendSentenceToSpeech(senid)

        speakerObj = next((x for x in speakerObjectlist if x.name == currentSpeaker), None)
        currentSpeech.appendSentenceToSpeech(senid)
        speakerObj.appendSpeech(currentSpeech)




        for speaker in speakerObjectlist:
            speaker.getAllTokenCount()

            if saveSpeakerConllu:
                f=  open(str(speaker)+".conllu", 'w')


            print("## "+str(speaker) + " ("+str(speaker.getAllTokenCount())+" token with multiword)") 
            print("* Number of speeches: "+str(len(speaker.speeches)))

            aggieggiFreq = {}




            for idxSpeec,speech in enumerate(speaker.speeches):

                speechText, ttr = speech.getSpeechText()
                print(SINGLE_INDENT + "Speech no. " + str(idxSpeec+1))
                print(SINGLE_INDENT + "TTR: " + str(round(ttr, 3)))
                print(DOUBLE_INDENT + speechText)
                print(DOUBLE_INDENT + "Sentences :" + str(speech.getNumberOfSentences()))

                if saveSpeakerConllu:
                    f.writelines([sentence.serialize() + "" for sentence in speech.sentences])


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


                    sentenceIdMapping = {} # creo un dizionario che mi mapperà ogni riga della frase con il rispettivo id 
                    for token in sentence: # ciclo su ogni token della frase
                        sentenceIdMapping[token["id"]] = token # uso come chiave per il dizionario l'id del token e come valore l'oggetto che rappresenta tutta la riga del conllu
                    for token in sentence: # ciclo su ogni token della frase
                        if (token["deprel"] != "_" and token["deprel"] != "punct" ): # sa la deprel è _ salto
                            aggeggio = ""
                            if token["head"] == 0:
                                aggeggio = "0->" + str(token["deprel"]) + "->" + str(sentenceIdMapping[token["id"]]["upos"])
                            elif token["head"] not in sentenceIdMapping:
                                aggeggio = (str(  token["head"] )  + "->" + str(token["deprel"]) + "->" + str(sentenceIdMapping[token["id"]]["upos"]))
                            else:
                                aggeggio = (str( sentenceIdMapping[token["head"]]["upos"])  + "->" + str(token["deprel"]) + "->" + str(sentenceIdMapping[token["id"]]["upos"])) 
                            # print(aggeggio)
                            if aggeggio not in aggieggiFreq:
                                aggieggiFreq[aggeggio] = 0
                            
                            aggieggiFreq[aggeggio] += 1
            
            print(SINGLE_INDENT + "Trigrammi speaker " + str(speaker))
            aggieggiFreq = dict(sorted(aggieggiFreq.items(), key=lambda item: item[1],reverse=True))
            for key in aggieggiFreq:
                print(DOUBLE_INDENT + key + "\t" + str(aggieggiFreq[key]))
            if saveSpeakerConllu:
                f.close()        
            print()
