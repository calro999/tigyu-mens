import requests
import json
import os

INDEXNOW_KEY = "e2c39515949d4791a87b926411d73507"
HOST = "tigyu-mens.vercel.app"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"

# Ensure IndexNow key file exists in public/
os.makedirs("public", exist_ok=True)
with open(f"public/{INDEXNOW_KEY}.txt", "w") as f:
    f.write(INDEXNOW_KEY)

# 全記事および固定ページを動的生成
url_list = [
    f"https://{HOST}/",
    f"https://{HOST}/curriculum",
    f"https://{HOST}/reviews",
    f"https://{HOST}/ranking",
    f"https://{HOST}/sitemap.xml"
]

if os.path.exists("data/posts.json"):
    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    for p in posts:
        url_list.append(f"https://{HOST}/posts/{p['slug']}")

print(f"Total URLs to submit via IndexNow: {len(url_list)}")

payload = {
    "host": HOST,
    "key": INDEXNOW_KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": url_list[:500]  # 最大500件まで一度に送信可能
}

headers = {
    "Content-Type": "application/json; charset=utf-8"
}

endpoints = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow"
]

for ep in endpoints:
    try:
        r = requests.post(ep, data=json.dumps(payload), headers=headers, timeout=15)
        print(f"Submitted {len(payload['urlList'])} URLs to {ep} -> Status: {r.status_code}")
    except Exception as e:
        print(f"Error submitting to {ep}: {e}")
