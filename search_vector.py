from sentence_transformers import SentenceTransformer

#model_name = "all-MiniLM-L12-v2"
model_name = "intfloat/multilingual-e5-small"

# モデルのロード
model = SentenceTransformer(model_name)



from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, Range

# Qdrantクライアントの初期化
client = QdrantClient(host="localhost", port=6333)  # qdratは先に起動させておくこと

def search_similar_vectors(collection_name, query_vector, limit=3):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )
    return search_result

# 例えば、以下のクエリベクトルを使用して検索を実行する
query_vector = model.encode("プリント基板 CAD ")
results = search_similar_vectors("companies", query_vector, limit=3)

print(results)
