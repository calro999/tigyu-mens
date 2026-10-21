import os
import sys
import json
import random
import time
import re
import io
from datetime import datetime
import requests
from atproto import Client, client_utils
from PIL import Image

def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'").strip('"')
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

load_env_file()

BLUESKY_HISTORY_FILE = "bluesky_post_history.txt"
BLUESKY_TEXT_HISTORY_FILE = "bluesky_text_history.txt"
BLUESKY_ENGAGEMENT_FILE = "bluesky_engagement_history.txt"

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE", "tigyu-cosme.bsky.social")
BLUESKY_APP_PASSWORD = os.environ.get("BLUESKY_APP_PASSWORD", "")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash"
]

def load_posted_history():
    if os.path.exists(BLUESKY_HISTORY_FILE):
        with open(BLUESKY_HISTORY_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def record_posted_history(slug):
    with open(BLUESKY_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{slug}\n")

def load_text_history():
    if os.path.exists(BLUESKY_TEXT_HISTORY_FILE):
        with open(BLUESKY_TEXT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def record_text_history(text):
    cleaned = re.sub(r'\s+', ' ', text).strip()
    with open(BLUESKY_TEXT_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{cleaned}\n")

def is_similar_to_history(new_text, history_list):
    if not history_list:
        return False
    new_norm = re.sub(r'[\s、。！？!?,.]', '', new_text)
    for past in history_list[-20:]:
        past_norm = re.sub(r'[\s、。！？!?,.]', '', past)
        if len(new_norm) >= 16 and len(past_norm) >= 16:
            if new_norm[:16] == past_norm[:16]:
                return True
        if new_norm in past_norm or past_norm in new_norm:
            return True
    return False

def optimize_image_bytes(raw_bytes, max_bytes=800000):
    if len(raw_bytes) <= max_bytes:
        return raw_bytes
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        max_dim = 1200
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        quality = 85
        while quality >= 40:
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=quality, optimize=True)
            res = out.getvalue()
            if len(res) <= max_bytes:
                return res
            quality -= 10
        return res
    except Exception as e:
        print(f"[WARN] Image resize error: {e}")
        return raw_bytes[:max_bytes]

def fetch_image_bytes(image_url):
    if not image_url:
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(image_url, headers=headers, timeout=10)
        if res.status_code == 200 and len(res.content) > 500:
            return optimize_image_bytes(res.content)
    except Exception as e:
        print(f"[WARN] Failed to fetch image: {e}")
    return None

def generate_social_hook_text(article, item):
    title = article.get("title", "")
    item_name = item.get("name", "厳選アイテム")
    price = item.get("price", "")

    hooks = [
        f"「垢抜けたいならまずこれを見ろ！」{title}について本音で徹底比較したぞ。特に{item_name}（{price}）は清潔感爆上げの即効ギア。迷ったらまず記事の比較表をチェックしてくれ！",
        f"【チー牛脱却の決定版】{title}。適当に買って後悔する前に、肌質・タイプ別の比較を見てほしい。{item_name}はガチで人生変わるレベルで使いやすい逸品。",
        f"見た目の印象で損するの、もうやめにしないか？{title}をガチ検証。{item_name}（{price}）をルーティンに入れるだけで、一瞬で清潔感カンストするぞ。"
    ]

    past_texts = load_text_history()

    if GEMINI_KEY:
        sys_msg = "あなたはメンズ垢抜けメディア『もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾』の公式Bluesky運営者です。男の本音・熱量・煽りと親しみやすさを込め、AI臭い定型文（こんにちは、いかがでしょうか等）を一切排除した生々しいSNS投稿文を作成してください。"
        prompt = f"""
記事タイトル: {title}
おすすめ商品: {item_name}（{price}）
対象読者: {article.get('targetAudience', '清潔感を出したいZ世代男性')}

上記の内容を元に、読者の悩みに寄り添いつつ『まずこれ見とけ！』と記事を読みたくなるような、熱狂的で刺さる短い紹介文（80〜110文字程度）を作成してください。
※URLやハッシュタグは含めないでください。本文テキストのみを出力してください。
"""
        for m in GEMINI_MODELS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": f"{sys_msg}\n\n{prompt}"}]}],
                    "generationConfig": {"temperature": 0.9, "maxOutputTokens": 250}
                }
                res = requests.post(url, json=payload, timeout=10)
                if res.status_code == 200:
                    cand = res.json().get("candidates", [])
                    if cand:
                        text_cand = cand[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
                        text_cand = re.sub(r'https?://[^\s]+', '', text_cand).strip()
                        text_cand = re.sub(r'#[^\s]+', '', text_cand).strip()
                        if len(text_cand) >= 40 and not is_similar_to_history(text_cand, past_texts):
                            return text_cand
            except Exception:
                continue

    for h in hooks:
        if not is_similar_to_history(h, past_texts):
            return h
    return hooks[0]

def post_article_to_bluesky(article):
    if not BLUESKY_HANDLE or not BLUESKY_APP_PASSWORD:
        print("[WARN] BLUESKY_HANDLE or BLUESKY_APP_PASSWORD not set. Skipping Bluesky post.")
        return False

    client = Client()
    try:
        client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        print(f"[BLUESKY] Logged in successfully as @{BLUESKY_HANDLE}")
    except Exception as e:
        print(f"[ERROR] Bluesky login failed: {e}")
        return False

    # 記事内の代表商品
    comps = article.get("comparisonTable", [])
    rep_item = comps[0] if comps else {"name": article.get("title", ""), "price": "", "affiliateUrl": "https://www.rakuten.co.jp/"}
    site_article_url = f"https://tigyu-mens.vercel.app/posts/{article['slug']}"
    affiliate_url = rep_item.get("affiliateUrl") or "https://www.rakuten.co.jp/"

    post_text = generate_social_hook_text(article, rep_item)
    print(f"[BLUESKY-TEXT] {post_text}")

    # 画像取得（楽天画像）
    img_url = rep_item.get("imageUrl") or article.get("heroImage")
    image_bytes = fetch_image_bytes(img_url)

    # TextBuilderでリッチリンクとハッシュタグを構築
    tb = client_utils.TextBuilder()
    tb.text(post_text.strip() + "\n\n")

    tb.text("📖 徹底比較・詳細レビュー:\n")
    tb.link("👉 記事を読む", site_article_url)
    tb.text("\n\n")

    tb.text("🛒 楽天注目アイテム:\n")
    tb.link(f"👉 {rep_item.get('name', '商品詳細')[:20]}", affiliate_url)
    tb.text("\n\n")

    tags = ["垢抜け", "メンズコスメ", "清潔感", "チー牛脱却"]
    for i, t in enumerate(tags):
        tb.tag(f"#{t}", t)
        if i < len(tags) - 1:
            tb.text(" ")

    try:
        if image_bytes:
            print("[BLUESKY] Uploading high-res Rakuten product image...")
            upload = client.upload_blob(image_bytes)
            embed_images = [
                {
                    "alt": f"{article.get('title', 'メンズ垢抜け')} - {rep_item.get('name', '')}",
                    "image": upload.blob
                }
            ]
            response = client.send_post(tb, embed={"$type": "app.bsky.embed.images", "images": embed_images})
        else:
            response = client.send_post(tb)

        print(f"[SUCCESS] Bluesky post created! URI: {response.uri}")
        record_posted_history(article["slug"])
        record_text_history(post_text)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send Bluesky post: {e}")
        return False

def main():
    with open("data/posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    posted_history = load_posted_history()
    target_post = None

    for p in posts:
        if p["slug"] not in posted_history:
            target_post = p
            break

    if not target_post:
        # 全て投稿済みの場合は最新記事を投稿
        target_post = posts[0]
        print("[INFO] All posts posted at least once. Selecting latest article for promotion.")

    print(f"Target article to promote on Bluesky: {target_post['title']} ({target_post['slug']})")
    post_article_to_bluesky(target_post)

if __name__ == "__main__":
    main()
