# e5-search-demo
multilingual-E5モデル での 企業検索デモアプリ

日本語含む多言語にて企業情報のベクトル検索をする

バックエンドは Qdrant

https://github.com/tkys/e5-search-demo/assets/24400946/4439df41-2886-4b62-a00f-0f06a04f741d


model:[intfloat/multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small)


dataset:上場企業説明データ スクレイピングしたもの


---

```
.
├── csv2qdrant.py
├── list_company.csv
├── scrape_minkabu.py
├── search_vector.py
├── server-vectorsearch.py
└── updated_companies.csv

```

```
# データ収集
python scrape_minkabu.py


# ベクトルDB Qdrant 立てる
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant

 

# テキストをベクトル化してqdrantへ投入
python csv2qdrant.py


# 確認
`localhost:6000/dashboard/`にアクセスするとダッシュボード上で登録したコレクション情報が確認できる


```

```
# ベクトル検索テスト
python search_vector.py
```

```
# streamlitアプリ起動
streamlit run server-vectorsearch.py


# ベクトル検索アプリ確認
`localhost:8501/`にアクセスしてアプリ操作

```
