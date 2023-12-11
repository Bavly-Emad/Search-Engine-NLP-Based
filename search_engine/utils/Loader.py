import json, pickle

def loadInvertedIndexes():
    wordIndex = {}
    docIndex = {}
    with open('D:\Search engine\\app\search_engine\data\satuareted.json', 'r') as openfile:
        wordIndex = json.load(openfile)
    with open('D:\Search engine\\app\search_engine\data\docindexFF.json', 'r') as openfile:
        docIndex = json.load(openfile)
    return wordIndex, docIndex

def loadInvertedIndex():

    wordIndex = {}
    with open('app\search_engine\data\satuareted.json', 'r') as openfile:
        wordIndex = json.load(openfile)
    return wordIndex

# dict = {"docId": vector}
def loadEmbeddings():
  with open('app\search_engine\data\mcroembeddings.pkl', "rb") as fIn:
    sentence_embeddings = pickle.load(fIn)
    print("loaded embeddings.......")
    return sentence_embeddings


def getDocs():
    from Database import getAllDocs
    
    
    cursor = getAllDocs() #print(Rawdocs[0]["content"])
    
    i = 0
    while cursor:
        try:
            cursor[i]["_id"]
            cursor[i]['imdb_id']
            cursor[i]['original_title']
            cursor[i]["overview"]
            cursor[i]['poster_path']
            cursor[i]['release_date']
            i+=1
        # https://image.tmdb.org/t/p/w500//vzmL6fP7aPKNKPRTFnZmiUfciyV.jpg
        # https://www.imdb.com/title/tt0478970/           
        except:
            break
