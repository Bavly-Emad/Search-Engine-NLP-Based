
# class Cache:
#     cache = {}

#     def add_query_to_cache(self, query, docIds):
#         if len(self.cache) >= 50:
#             self.removeFirst20()

#         self.cache[query] = docIds
    
#     def get_cached_query(self, query):
#         return self.cache.get(query, [])

#     def removeFirst20(self):
#         for key in self.cache.keys():
#             del self.cache[key]
