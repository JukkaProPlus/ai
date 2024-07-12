from FlagEmbedding import FlagModel
sentences_1 = ["我爱你", "我恨你","给我冲一杯咖啡吧","我的口渴了","今天天气真好", "热死我了"]
sentences_2 = ["我讨厌你", "我喜欢你"]
model = FlagModel('BAAI/bge-large-zh-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
embeddings_1 = model.encode(sentences_1)
embeddings_2 = model.encode(sentences_2)
similarity = embeddings_1 @ embeddings_2.T
print(similarity)
print("------------------------------------")
# for s2p(short query to long passage) retrieval task, suggest to use encode_queries() which will automatically add the instruction to each query
# corpus in retrieval task can still use encode() or encode_corpus(), since they don't need instruction

# queries = ['query_1']#--, 'query_2']
# passages = ["样例文档-1"]#, "样例文档-2"]

# queries = ['query_1', 'query_2']
# passages = ["样例文档-1"]#, "样例文档-2"]

# q_embeddings = model.encode_queries(queries)
# p_embeddings = model.encode(passages)
# scores = q_embeddings @ p_embeddings.T
# print(scores)
