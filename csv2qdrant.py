from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# CSVデータを読み込む
data = pd.read_csv('updated_companies.csv')

#不要データ削除
data = data[ data["company_description"]  != "ページが見つからないか、エラーが発生しました。" ].reset_index(drop=True)


# 使用する多言語モデルを選択
#model_name = "all-MiniLM-L12-v2"
model_name = "intfloat/multilingual-e5-small"

# モデルのロード
model = SentenceTransformer(model_name)
print(f"Done:Load model")

# 会社の説明をリストに変換
descriptions = data['company_description'].tolist()

# ベクトル化
vectors = model.encode(descriptions)
print(f"Done:model.encode")


#####
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Qdrantクライアントの初期化
client = QdrantClient(host="localhost", port=6333)

# Check if the collection exists
if client.get_collection(collection_name="companies"):
    # Delete the existing collection
    client.delete_collection(collection_name="companies")

# Then create the collection as before
client.create_collection(
    collection_name="companies",
    vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE)
)
print(f"Done:create_collection")


# ベクトルとペイロードの追加
for i, row in data.iterrows():
    payload = {
        "stock_code": str(row["stock_code"]),
        "company_name": row["company_name"],
        "company_description": row["company_description"]
    }
    #print(f"payload:{payload}")

    operation_info = client.upsert(
        collection_name="companies",
        points=[PointStruct(id=i, vector=vectors[i].tolist(), payload=payload)],
        wait=True
    )
print(f"Done:upsert_collection")

