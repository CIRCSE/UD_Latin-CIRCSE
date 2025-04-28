import networkx as nx
import io



class Speaker:
    def __init__(self,name):
        self.name = name
        self.speeches = []
        return
    

    def __str__(self):
        return self.name    

    def __repr__(self):
        return self.name    

    
    def appendSpeech(self,speech):
        self.speeches.append(speech)
        return
    
    def getAllTokenCount(self):
        allTokens = 0
        for speech in self.speeches:
            allTokens += speech.getTotalOfToken()
        return allTokens


class SpeakerSpeech:

    def __init__(self):
        self.speechRawText = []
        self.conlluLines = []
        self.sentences = []
    
    def appendTokenToSpeech(self,token):
        self.conlluLines.append(token)


    def appendSentenceToSpeech (self):
        if (len(self.conlluLines) > 0):
            self.sentences.append(self.conlluLines)
        self.conlluLines = []
    
    def getSentenceText(self,sentence):
        skiptokenList = []
        sentenceText = []
        uniqueTokens = set()
        for token in sentence: # ciclo su ogni token della frase
            if  type(token["id"]) is tuple:
                firstPosition = token["id"][0]
                lastPosition = token["id"][2]
                for skipTokenId in range(firstPosition,lastPosition+1):
                    skiptokenList.append(skipTokenId)
            if token["id"] not in skiptokenList:
                sentenceText.append(token["form"])
                uniqueTokens.add(token["form"].lower())
        return(" ".join(sentenceText))


    def getSpeechText(self):
        sentenceText = []
        uniqueTokens = set()
        for sentence in self.sentences: # ciclo sulle frasi e uso la variabile sentence per ogni frase
            # sentenceIdMapping = {} # creo un dizionario che mi mapperà ogni riga della frase con il rispettivo id 
            skiptokenList = []
            for token in sentence: # ciclo su ogni token della frase
                if  type(token["id"]) is tuple:
                    firstPosition = token["id"][0]
                    lastPosition = token["id"][2]
                    for skipTokenId in range(firstPosition,lastPosition+1):
                        skiptokenList.append(skipTokenId)
                if token["id"] not in skiptokenList:
                    sentenceText.append(token["form"])
                    uniqueTokens.add(token["form"].lower())
        return(" ".join(sentenceText), (len(uniqueTokens) / len(sentenceText)))

    def getNumberOfSentences(self):
        return len(self.sentences)
    

    def getSpeechSentenceTreeDepth(self,sentence):
        G = nx.DiGraph()
        mapping = {}
        for token in sentence: # ciclo su ogni token della frase
                if  type(token["id"]) is not tuple:
                    nodeName = str(token["id"])+ "_"+token["form"]
                    G.add_node(nodeName)
                    mapping[token["id"]] = nodeName
                    #tree.create_node(token["form"], token["id"])
        
        for token in sentence:
            if  type(token["id"]) is not tuple:
                if token["head"] in mapping:
                    source = mapping[token["head"]]
                    target = str(token["id"])+ "_"+token["form"]
                    G.add_edge(source, target)
                elif token["head"] not in mapping and token["head"] != 0: 
                    source = "external_node_"+str(token["head"])
                    target = str(token["id"])+ "_"+token["form"]
                    G.add_edge(source, target)
        UG = G.to_undirected()
        # extract subgraphs
        sub_graphs = nx.connected_components(UG)
        numberOfGraph = sum(1 for x in sub_graphs)

        if numberOfGraph > 1 :
            #print("******** multigraph ********")
            sub_graphs = nx.connected_components(UG)
          
            theTree = ""
            f = io.StringIO("")
            nx.write_network_text(G,path=f)   
            theTree =f.getvalue()
            f.close()

            maxDepth = 0
            for i, sg in enumerate(sub_graphs):
                dg = G.subgraph(sg)
 
                len(nx.dag_longest_path(dg))-1
                if len(nx.dag_longest_path(dg))-1 > maxDepth: 
                    maxDepth = len(nx.dag_longest_path(dg))-1

            return maxDepth,theTree
        else:
            if nx.is_tree(G):
                theTree = ""
                f = io.StringIO("")
                nx.write_network_text(G,path=f)   
                theTree =f.getvalue()
                f.close()
                return len(nx.dag_longest_path(G))-1,theTree
            else:
                return None


    
    


    

    def getTotalOfToken(self):
        countAll = 0
        for sentence in self.sentences:
            countAll += len(sentence)
        return countAll