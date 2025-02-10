import requests

# 服务的 URL
BASE_URL = "http://127.0.0.1:8000"  # 根据实际情况修改端口

def test_embed():
    sentences = ["你好，世界！", "今天天气不错。"]
    response = requests.post(f"{BASE_URL}/embed/", json={"sentences":sentences})
    
    if response.status_code == 200:
        print("嵌入结果:", response.json())
    else:
        print("嵌入请求失败:", response.status_code, response.text)

def test_similarity():
    sentences_1 = ["你好，世界！", "今天天气不错。"]
    sentences_2 = ["世界，你好！", "今天天气很好。"]
    response = requests.post(f"{BASE_URL}/similarity/", json={"sentences_1": sentences_1, "sentences_2": sentences_2})
    
    if response.status_code == 200:
        print("相似度结果:", response.json())
    else:
        print("相似度请求失败:", response.status_code, response.text)

if __name__ == "__main__":
    test_embed()
    # test_similarity()
