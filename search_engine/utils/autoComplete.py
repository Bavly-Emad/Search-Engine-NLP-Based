import pickle
from fast_autocomplete import AutoComplete
from fast_autocomplete.loader import WordValue

file_path = 'D:\Search engine\\app\search_engine\data\\autocomlist2'
# autocompatte index 
with open(file_path, 'rb') as fl:
    words = pickle.load(fl)
    print('loaded autocomplete list')



autocomplete = AutoComplete(words=words)

#print(autocomplete.words)

def getSuggestions(query):
    suggestsions = autocomplete.search(word=query,  max_cost=3, size=8)
    suggestsions = [suggestion[0] for suggestion in suggestsions]
    print(suggestsions)
    return suggestsions

def saveQuery(query):
    try:
        autocomplete.words[query]

        queryCount = autocomplete.get_count_of_word(query)
        print(queryCount, ' count before')
       # autocomplete.words[query] =  WordValue(context={}, display=query, count=queryCount+90, original_key=None)
        autocomplete.insert_word_branch(word=query, count=queryCount+1)
        autocomplete.insert_word_callback(word=query)
        print(queryCount, ' counter afer..any change?')

       # autocomplete.update_count_of_word(word=query, count=10000)
       # print(autocomplete.words)
        autocomplete.words[query] =WordValue(context={}, display=query, count=queryCount, original_key=None)
        print('updated count', autocomplete.words[query])
    except:
        autocomplete.insert_word_branch(word=query, count=1)
        autocomplete.insert_word_callback(word=query)
        autocomplete.words[query] =  WordValue(context={}, display=query, count=1, original_key=None)
        print('new query updated', autocomplete.words[query])



def saveAutoCompleteIndex():
    with open(file_path, 'wb') as fout:
        pickle.dump(autocomplete.words, fout)
        print('autocomplete list saved')


#print(saveQuery("agsdgda"))

#query = ""

# while query != 'x':
#     query = input("enter a query: ")
#     saveQuery(query)



