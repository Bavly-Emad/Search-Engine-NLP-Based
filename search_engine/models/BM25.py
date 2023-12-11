from utils.Loader import loadInvertedIndexes


# load indexes 
wordIndex = {}
docIndex = {}
wordIndex, docIndex =  loadInvertedIndexes()

      

# paramters 
b = 0.75
k = 1.2
epsilon=0.25
idf_sum = 0
average_idf = 0
#avgdl = sum(docIndex.values()) / len(docIndex)

# query, get dict of uniqie docs ids with score as 0

def getDocs(query):
    a = set()
    
    for q in query: 
        if wordIndex.get(q) is not None:
            a.update((wordIndex[q][1].keys()))
        else:
            print("the word (", q , ") is not in the index")
                
    return dict.fromkeys(list(a), 0)
    
# def all_query_terms_existInIndex(query):
#     for q in query:
#         if wordIndex.get(q, None) == None: 
#             return False
#     return True
# retyrbs sorted unique id by their socres 
def BM25(query):
    #  doc index = size 
    #docs_len = [getWordCount(doc) for doc in docs]
    #avgdl = sum(docs_len) / len(docs)
    # scores = []
    if not query: return []
    
    docs = getDocs(query) # {doc: score}

    if len(docs) is 0 : return []

    #print(docs)

    for docId in docs.keys():
        score = 0
        
        for q in query:
            if wordIndex.get(q) is not None:
                # # current version: wordIndex["cat"]=  [idf, {"doc1": 523, "doc2": 3}
                tf = (wordIndex[q][1].get(docId) or 0) # retirive tf of term in doctumet by docId 
                idf = wordIndex[q][0]
                CurrnetdocumentLenght = docIndex[docId]
                score += idf * ((tf * (k+1)))/ (tf + k * (1- b + (b*CurrnetdocumentLenght/ avgdl)))

            docs[docId] = score
    
    return sort(docs)



def BM25F(query):
    #  doc index = size 
    #docs_len = [getWordCount(doc) for doc in docs]
    #avgdl = sum(docs_len) / len(docs)
    # scores = []
    if not query: return []
    
    docs = getDocs(query) # {doc: score}

    if len(docs) is 0 : return []

    #print(docs)

    for docId in docs.keys():
        score = 0
        
        for q in query:
            if wordIndex.get(q) is not None:
                # # current version: wordIndex["cat"]=  [idf, {"doc1": 523, "doc2": 3}
                tf = (wordIndex[q][1].get(docId) or 0) # retirive tf of term in doctumet by docId 
                idf = wordIndex[q][0]
                score += idf * (tf / (k + tf))

            docs[docId] = score
    
    return sort(docs)

def sort(docs):
    top_k = 50
    docsSorted = list(dict(sorted(docs.items(), key=lambda x: x[1], reverse=True)).keys())
    if len(docsSorted) > top_k:
        return docsSorted[0:top_k]
    return docsSorted