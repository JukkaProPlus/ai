from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from FlagEmbedding import FlagModel

app = FastAPI()

# 加载模型
model = FlagModel('BAAI/bge-large-zh-v1.5', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True)

# 定义请求体
class EmbedRequest(BaseModel):
    sentences: List[str]

class SimilarityRequest(BaseModel):
    sentences_1: List[str]
    sentences_2: List[str]

@app.post("/embed/")
async def embed(request: EmbedRequest):
    try:
        embeddings = model.encode(request.sentences)
        return {"embeddings": embeddings.tolist()}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/similarity/")
async def similarity(request: SimilarityRequest):
    embeddings_1 = model.encode(request.sentences_1)
    embeddings_2 = model.encode(request.sentences_2)
    similarity = embeddings_1 @ embeddings_2.T
    results = []
    for i in range(similarity.shape[0]):
        for j in range(similarity.shape[1]):
            if similarity[i][j] > 0.7:
                results.append(f"'{request.sentences_1[i]}'和'{request.sentences_2[j]}'的意思是相似的")
    return {"similarity_results": results}

# 启动服务时使用命令: python -m uvicorn embedding_test_service:app --reload
