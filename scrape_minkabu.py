import requests
from bs4 import BeautifulSoup
import time 
import pandas as pd

# 企業の説明と業種を取得する関数
def get_company_description_and_industry(stock_code):
    # 企業情報ページのURLを構築
    url = f"https://minkabu.jp/stock/{stock_code}"
    
    # セッションを開始し、ページのHTMLを取得
    session = requests.Session()
    response = session.get(url)
    if response.status_code != 200:
        return "ページが見つからないか、エラーが発生しました。", "ページが見つからないか、エラーが発生しました。"
    
    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 特定のテキストを含む`<div>`を検索
    industry_div = soup.find('div', class_='ly_content_wrapper size_ss')
    
    if industry_div:
        # 業種テキストの取得
        industry_link = industry_div.find('a')
        if industry_link:
            industry_text = industry_link.get_text(strip=True)
        else:
            industry_text = "業種が見つかりません。"
        
        # 業種情報の次の`<div>`を取得
        company_description_div = industry_div.find_next('div', class_='ly_content_wrapper size_ss')
        if company_description_div:
            company_description = company_description_div.get_text(strip=True)
        else:
            company_description = "企業説明が見つかりません。"
    else:
        industry_text = "業種情報が見つかりません。"
        company_description = "企業説明が見つかりません。"
    
    return industry_text, company_description

# CSVファイルを読み込む
df = pd.read_csv('list_company.csv')  # CSVファイルのパスを指定

# 新しい列を追加するための空のリストを作成
company_industries = []
company_descriptions = []

# 各行に対して企業の説明と業種を取得
for stock_code in df['stock_code']:
    industry, description = get_company_description_and_industry(stock_code)
    company_industries.append(industry)
    company_descriptions.append(description)
    time.sleep(0.5)  # サーバーへの負荷を減らすために遅延
    print(f"{stock_code}: {industry}, {description}")

# 新しい列として追加
df['industry'] = company_industries
df['company_description'] = company_descriptions

# 結果を新しいCSVファイルに保存
df.to_csv('updated_companies.csv', index=False)
