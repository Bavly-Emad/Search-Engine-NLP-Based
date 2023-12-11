import pickle
import faiss
from sentence_transformers import SentenceTransformer, util


top_k = 30

# if torch.cuda.is_available():
#   model = model.to(torch.device("cuda"))
#   print(model.device)
model = SentenceTransformer('msmarco-distilbert-base-v4')
index = faiss.read_index('app\search_engine\data\\thipindex')

with open('app\search_engine\data\mcroembeddings.pkl', "rb") as fIn:
    sentence_embeddings = pickle.load(fIn)
    print("loaded embeddings.......")


#index.nprobe = 3

def search_in_FAISS_index(q):
    
    query_encoded = model.encode([q])
    
    D, I = index.search(query_encoded, top_k)
    list(I[0]).reverse()
    return I[0]


def ConsieSimilaritySearch(query):
  query_embed = model.encode([query])
  scores = util.cos_sim(sentence_embeddings, query_embed)
  scoresDict = {}

  for i in range(len(sentence_embeddings)):
    scoresDict[i] = scores[i][0]
 # print(scoresDict)
  sortedDict = (dict(sorted(scoresDict.items(), key=lambda x: x[1], reverse=True)))
  return (list(sortedDict.keys())[0:top_k])
