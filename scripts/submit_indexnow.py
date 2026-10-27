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

# Post URLs to submit
url_list = [
    f"https://{HOST}/",
    f"https://{HOST}/posts/mens-electric-shaver-fast-charge-waterproof",
    f"https://{HOST}/posts/dr-ci-labo-enrich-medicalift-duo-serum",
    f"https://{HOST}/posts/mens-electric-nose-hair-trimmer-usb",
    f"https://{HOST}/posts/everskin-scalp-shampoo-treatment-set",
    f"https://{HOST}/posts/willclense-medicated-deodorant-stick",
    f"https://{HOST}/posts/nile-scalp-hair-lotion-mens",
    f"https://{HOST}/sitemap.xml"
]

payload = {
    "host": HOST,
    "key": INDEXNOW_KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": url_list
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
        r = requests.post(ep, data=json.dumps(payload), headers=headers, timeout=10)
        print(f"Submitted to {ep} -> Status: {r.status_code}")
    except Exception as e:
        print(f"Error submitting to {ep}: {e}")
