import json
import re

DATA_FILE = "data/posts.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    posts = json.load(f)

for i, post in enumerate(posts):
    # 安全なURL-safeスラッグに変換（& や % などの特殊文字を英字ハイフンに統一）
    old_slug = post.get("slug", "")
    new_slug = re.sub(r'[^a-zA-Z0-9\-]+', '-', old_slug).strip('-')
    new_slug = re.sub(r'-+', '-', new_slug)
    post["slug"] = new_slug

    # heroImageを楽天APIから取得した第1位（または高画質）商品画像に置換
    comparisons = post.get("comparisonTable", [])
    rakuten_img = ""
    for c in comparisons:
        img = c.get("imageUrl", "")
        if img and "rakuten.co.jp" in img:
            rakuten_img = img
            break
    
    if rakuten_img:
        post["heroImage"] = rakuten_img
    else:
        print(f"[WARN] No Rakuten image found for post {post['title']}")

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"Updated {len(posts)} posts with safe slugs and Rakuten images.")
