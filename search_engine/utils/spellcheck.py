from rapidfuzz import process as rapidfuzz_process
from models.BM25 import wordIndex
from rapidfuzz.string_metric import levenshtein


# terms of inverted index 
index = list(wordIndex.keys())

threshold = 2 # min distance only 2

def spellCheck(query):

    if not query: return 

    for counter, q in enumerate(query): 
      if q not in index: 
        res = rapidfuzz_process.extract(q, index, limit=3,scorer=levenshtein, score_cutoff=threshold)
        print(res)
        if not res: continue
        suggestedWord = res[0][0]
        score = res[0][1]
        if score <= threshold: 
                query[counter] = suggestedWord

    return query 


 

 