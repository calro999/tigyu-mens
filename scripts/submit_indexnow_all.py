import urllib.request
import json
import os
import ssl

INDEXNOW_KEY = "e2c39515949d4791a87b926411d73507"
HOST = "tigyu-mens.vercel.app"
KEY_LOCATION = f"https://{HOST}/{INDEXNOW_KEY}.txt"

# 1. publicキーファイルの存在担保
os.makedirs("public", exist_ok=True)
with open(f"public/{INDEXNOW_KEY}.txt", "w") as f:
    f.write(INDEXNOW_KEY)

# 2. 全固定ページおよび全236記事URLを抽出
url_list = [
    f"https://{HOST}/",
    f"https://{HOST}/curriculum",
    f"https://{HOST}/reviews",
    f"https://{HOST}/ranking",
    f"https://{HOST}/profile",
    f"https://{HOST}/contact",
    f"https://{HOST}/privacy",
    f"https://{HOST}/sitemap.xml",
    f"https://{HOST}/robots.txt"
]

if os.path.exists("data/posts.json"):
    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
    for p in posts:
        url_list.append(f"https://{HOST}/posts/{p['slug']}")

# 重複排除
url_list = list(dict.fromkeys(url_list))
print(f"Total target URLs to submit: {len(url_list)}")

payload = {
    "host": HOST,
    "key": INDEXNOW_KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": url_list
}

data_json = json.dumps(payload).encode("utf-8")
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "IndexNow-Client/2.0"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# IndexNowプロトコル対応エンドポイント（Bing, Yandex, Naver, Seznam, DuckDuckGo等のネットワーク）
endpoints = [
    ("api.indexnow.org", "https://api.indexnow.org/indexnow"),
    ("Bing", "https://www.bing.com/indexnow"),
    ("Yandex", "https://yandex.com/indexnow"),
    ("Naver Search Advisor", "https://searchadvisor.naver.com/indexnow"),
    ("Seznam.cz", "https://search.seznam.cz/indexnow")
]

print("\n--- Submitting via IndexNow Protocol ---")
for name, ep in endpoints:
    req = urllib.request.Request(ep, data=data_json, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            print(f"[{name}] Status: {resp.status} (Success)")
    except urllib.error.HTTPError as e:
        # IndexNow仕様: 200, 202は受付成功。
        print(f"[{name}] HTTP Status: {e.code} ({e.reason})")
    except Exception as e:
        print(f"[{name}] Connection Error: {e}")

# 3. Google / Bing サイトマップ Ping 通知
print("\n--- Pinging Sitemaps to Global Search Engines ---")
sitemap_url = f"https://{HOST}/sitemap.xml"
ping_targets = [
    ("Google Sitemap Ping", f"https://www.google.com/ping?sitemap={sitemap_url}"),
    ("Bing Sitemap Ping", f"https://www.bing.com/ping?sitemap={sitemap_url}")
]

for name, ping_url in ping_targets:
    req = urllib.request.Request(ping_url, headers={"User-Agent": "Mozilla/5.0"}, method="GET")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            print(f"[{name}] Status: {resp.status} (Ping delivered)")
    except urllib.error.HTTPError as e:
        print(f"[{name}] HTTP Status: {e.code} ({e.reason})")
    except Exception as e:
        print(f"[{name}] Note: {e}")

print("\nAll IndexNow & Crawler notifications completed!")
