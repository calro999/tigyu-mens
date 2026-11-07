import os
import requests
import time

env = {}
with open(".env") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

APP_ID = env.get("RAKUTEN_APP_ID")
ACCESS_KEY = env.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = env.get("RAKUTEN_AFFILIATE_ID")

queries = [
    "ジェットウォッシャー 口腔洗浄器",
    "毛穴吸引器",
    "電動 頭皮ブラシ ヘッドスパ"
]

for q in queries:
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "affiliateId": AFFILIATE_ID,
        "keyword": q,
        "hits": 6,
        "format": "json",
        "sort": "-reviewCount"
    }
    res = requests.get(url, params=params, timeout=10)
    print(f"Query: {q} -> Status: {res.status_code}")
    if res.status_code == 200:
        items = res.json().get("Items", [])
        print(f"  Got {len(items)} items")
        for idx, it in enumerate(items[:3]):
            title = it.get("itemName", "")[:35]
            price = it.get("itemPrice", 0)
            rev_cnt = it.get("reviewCount", 0)
            rev_ave = it.get("reviewAverage", 0)
            img = it.get("mediumImageUrls", [""])[0]
            print(f"    [{idx+1}] {title} | ¥{price:,} | ★{rev_ave} ({rev_cnt}件) | Img: {bool(img)}")
    time.sleep(1.2)
