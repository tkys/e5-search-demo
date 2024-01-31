import streamlit as st
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, Range

# カスタムスタイル
st.markdown("""
    <style>
    .card {
        margin-bottom: 20px;
        padding: 20px;
        border-radius: 10px;
        background-color: #f2f2f2;
        color: #333;
        box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
    }
    .card-title {
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .card-text {
        font-size: 16px;
        margin-bottom: 10px;
    }
    .card-image {
        max-width: 100px;
        margin-bottom: 15px;
    }
    .streamlit-input-container {
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# モデルのロード
model_name = "intfloat/multilingual-e5-small"
model = SentenceTransformer(model_name)

# Qdrantクライアントの初期化
client = QdrantClient(host="localhost", port=6333)

def search_similar_vectors(collection_name, query_vector, limit=10):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )
    return search_result

st.title("ニュースキーワード×企業検索")

# ユーザー入力
query_text = st.text_input("ニュースキーワードを入力してください")
limit = st.number_input("表示する結果の数", min_value=1, max_value=10, value=10)

if st.button("検索"):
    query_vector = model.encode(str(query_text))
    results = search_similar_vectors("companies", query_vector, limit)

    # タイル形式で結果を表示
    col_num = 5  # 一行に表示するタイルの数
    cols = st.columns(col_num)

    for index, result in enumerate(results):
        with cols[index % col_num]:
            # カードスタイルのコンテンツ
            st.markdown(f"""
                <div class="card">
                    <img src="{result.payload.get('company_logo_url', '')}" class="card-image">
                    <div class="card-title">{result.payload['company_name']}</div>
                    <div class="card-text">Score: {result.score}</div>
                    <div class="card-text">StockCode: {result.payload['stock_code']}</div>
                    <div class="card-text">{result.payload['company_description']}</div>
                </div>
            """, unsafe_allow_html=True)
