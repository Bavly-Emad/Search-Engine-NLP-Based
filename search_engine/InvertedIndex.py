from utils.Preprocessing import cleanText
import math
import time  
import json
import pandas as pd 


df = pd.read_csv('app\search_engine\data\movies_data.csv',  usecols= ['_id', 'overview', 'original_title', 'release_date'])
print(str(df["overview"][0]))
#print(str(df['original_title'][1])+ ". " + str(df['overview'][1]))

wordIndex = {}
# Old version: wordIndex["cat"]=  {"idf": 5, "docs": {"doc1": 3, "doc2": 5}}
# current version: wordIndex["cat"]=  [idf, {"doc1": 523, "doc2": 3}]

# docIndex = {"documentID": lengthOfDocument}
docIndex = {}

N = len(df)


titleWeight = 5
dateWeight = 3
paragraphWeight = 1



def calculateIDF():
    
    for word in wordIndex.keys():
        nq = len(wordIndex[word][1])
        wordIndex[word][0] = math.log((N - nq + 0.5 / nq + .5) + 1 )
        


# build vocab and calcuaiton tf 
def buildVocab(doc): 

    docTextArray = doc["text"]
    a= set(doc["text"])


    document = ' '.join(docTextArray).split('hhh')
  #  print(document)
    for word in a:
        if word != 'hhh':
            try:
                wordIndex[word][1][doc["id"]] =  (titleWeight * document[0].count(word)) + (paragraphWeight * document[1].count(word)) + (dateWeight * document[2].count(word))
            except:
                wordIndex[word] = [0, {}]
                wordIndex[word][1][doc["id"]] = (titleWeight * document[0].count(word)) + (paragraphWeight * document[1].count(word)) + (dateWeight * document[2].count(word))


def saveIndex():
    with open('app\search_engine\data\invertedindexFF.json', 'w') as outfile:
        json.dump(wordIndex, outfile)
    with open('app\search_engine\data\docindexFF.json', 'w') as outfile:
        json.dump(docIndex, outfile)
    print(len(wordIndex), 'terms and ', len(docIndex), ' docs have been indexed and saved.')


###############################################


def buildInvertedIndex():
    
    s = time.time()

    doc = {}
    for i in range(N): 
        #print(doc, doc["id"])
        doc["id"] = i 
        #doc["text"] = cleanText(str(df['original_title'][i])+ ". " + str(df['overview'][i]) + ". " + str(df['release_date'][i])[0:4])
        doc["text"] = cleanText(str(df['original_title'][i])+ " hhh " + str(df['overview'][i]) + " hhh " + str(df['release_date'][i])[0:4])
        docIndex[doc["id"]] = len(doc["text"]) -1  # the hhh
        buildVocab(doc)    
  
    
    calculateIDF()

    saveIndex()    
    print("indexing process took ", ((time.time() - s)), 'seconds')


    
buildInvertedIndex()
 

#print(wordIndex)
###############################################################

			










# from utils.Preprocessing import cleanText
# import math
# import time  
# import json
# import pandas as pd 


# df = pd.read_csv('app\search_engine\data\movies_data.csv',  usecols= ['_id', 'overview', 'original_title', 'release_date'])
# print(str(df["overview"][0]))
# #print(str(df['original_title'][1])+ ". " + str(df['overview'][1]))

# wordIndex = {}
# # Old version: wordIndex["cat"]=  {"idf": 5, "docs": {"doc1": 3, "doc2": 5}}
# # current version: wordIndex["cat"]=  [idf, {"doc1": 523, "doc2": 3}]

# # docIndex = {"documentID": lengthOfDocument}
# docIndex = {}

# N = len(df)




# def calculateIDF():
    
#     for word in wordIndex.keys():
#         nq = len(wordIndex[word][1])
#         wordIndex[word][0] = math.log((N - nq + 0.5 / nq + .5) + 1 )
        

# # build vocab and calcuaiton tf 
# def buildVocab(doc): 
    
#     a= set(doc["text"])
#     for word in a:
#         try:
#             wordIndex[word][1][doc["id"]] =  doc["text"].count(word)
#         except:
#             wordIndex[word] = [0, {}]
#             wordIndex[word][1][doc["id"]] = doc["text"].count(word)


# def saveIndex():
#     with open('app\search_engine\data\invertedindex1.json', 'w') as outfile:
#         json.dump(wordIndex, outfile)
#     with open('app\search_engine\data\docindex1.json', 'w') as outfile:
#         json.dump(docIndex, outfile)
#     print(len(wordIndex), 'terms and ', len(docIndex), ' docs have been indexed and saved.')


# ###############################################


# def buildInvertedIndex():
    
#     s = time.time()

#     doc = {}
#     for i in range(N): 
#         #print(doc, doc["id"])
#         doc["id"] = i 
#         #doc["text"] = cleanText(str(df['original_title'][i])+ ". " + str(df['overview'][i]) + ". " + str(df['release_date'][i])[0:4])
#         doc["text"] = cleanText(str(df['original_title'][i])+ ". " + str(df['overview'][i]))
#         docIndex[doc["id"]] = len(doc["text"])
#         buildVocab(doc)    
  
    
#     calculateIDF()

#     saveIndex()    
#     print("indexing process took ", ((time.time() - s)), 'seconds')


    
# buildInvertedIndex()
 

# #print(wordIndex)
# ###############################################################

			

