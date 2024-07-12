from VectorDBConnector import MyVectorDBConnector
from Tools import *

dbConnector = MyVectorDBConnector(collection_name="demo_vec_rrf", embedding_fn=embedding_fn)
result = dbConnector.search(query="坦克", top_n=5)
print(result)