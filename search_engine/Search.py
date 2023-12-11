from Database import getByIds
from models.BM25 import BM25, BM25F
from models.BertModel import search_in_FAISS_index, ConsieSimilaritySearch
from utils.Preprocessing import cleanText
from utils.spellcheck import spellCheck

#print(spellCheck(cleanText('ii')), 'ahahah')

def search(query="", searchType="k"):

    if not query: return []

    docsIds = []
    

    if searchType == "k":
        print("keyword search: ")

        if query.startswith('"') and query.endswith('"'):
            query = cleanText(query[1:-1])
        else:
            query = spellCheck(cleanText(query))
            
        docsIds = BM25F(query)

    else:
        print("semantic search: ")
        #docsIds = search_in_FAISS_index(query)
        docsIds = ConsieSimilaritySearch(query)
            
    print(docsIds)     
        
    
    if len(docsIds) == 0: #return []
        print("couldn't find results.")
        return []
    else:
        return getByIds(docsIds)


console = 0

if console:
    while True: 
        query = input("Enter your search query: \n")
        searchType = input("enter your search type. s = sematnic, k = keyword (s/k): ")
        print(search(query, searchType))
    

#from utils.cache import Cache

# caching queries with results
#cache = Cache()



# def search(query="", searchType="a"):
#     s = time.time()
#     # 1- check misepllings 

#     rawquery = query+searchType 
#     docsIds = cache.get_cached_query(rawquery)
    
    
    
#     if not docsIds:
#         print("not in chace")
#         if searchType == "k":
#             print("keyword")
#             query = cleanText(query)
#             docsIds = BM25(query)
#         else:
#             docsIds = search_in_FAISS_index(query)
            
#         print(docsIds)     
            

        
#     e = time.time()
#     print("time took to retreive: ", round((e- s)/1000, 4), "ms")
    
#     if len(docsIds) is 0: #return []
#         return "couldn't find results"
#     else:
#         cache.add_query_to_cache(rawquery, docsIds)
#         return getDocsByIds(docsIds)
    