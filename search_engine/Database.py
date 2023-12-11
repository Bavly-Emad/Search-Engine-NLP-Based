#https://youtu.be/qWYx5neOh2s mongocrash
#from markupsafe import Markup
from pymongo import MongoClient


def connectDB():
    mongoDriver = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'
    client = MongoClient(mongoDriver)
    return client


client = connectDB()
db = client['testDB']
mycollection = db['movies']
crawlercollection = db['testCollection']


def InsertUrlObject(Url):
	mycollection.insert_one(Url)

# docs_ids = list(map(str,(range(0, 999))))

def isExistInDB(url):
    if  crawlercollection.find_one({"url": url}) is not None: return True
    else: return False



# alpha = range(0, 10000)
# alpha = list(map(str,alpha))

def getDocsByIds(docsIds):
    docs_ids = list(map(str ,docsIds))
    results= mycollection.find({"_id": {"$in": docs_ids}})
    return list(results)
    #display_resulsts(list(results))




def display_resulsts(docs):
    for doc in docs: 
        print(doc)
       # print(doc["_id"], doc["original_title"], '\n') #doc["overview"], '\n' )

#getDocsByIds([1, 3])
        
        
        

#getDocsByIds([1, 3, 4])
#print(display_resulsts(getAllDocs()))




# https://stackoverflow.com/questions/22797768/does-mongodbs-in-clause-guarantee-order
def getByIds(docsIds):
    listx = list(map(str ,docsIds))
    stack = []

    for i in range(len(listx), 0, -1):
        #print("hello", i)
        rec = {
            "$cond": [
                { "$eq": [ "$_id", listx[i-1] ] },
                i
            ]
        }
        if len(stack) == 0:
            rec["$cond"].append( i+1 )
        else:
            lval = stack.pop()
            rec["$cond"].append( lval )
    

        stack.append( rec )

    pipeline = [
        { "$match": { "_id": { "$in": listx } }},
        { "$project": { "weight": stack[0], "original_title": 1, "overview": 1, "release_date":1, "poster_path": 1, "imdb_id": 1}},
        { "$sort": { "weight": 1 } }
    ]
    result = mycollection.aggregate( pipeline )
    return list(result)

def getByIds2():
    return ""
    #list = [3, 5, 2, 8, 9']
    #things = list(db.things.find({'_id': {'$in': id_array}}))
    #things.sort(key=lambda thing: id_array.index(thing['_id']))
#rs = getByIds()
#print(list(rs))
