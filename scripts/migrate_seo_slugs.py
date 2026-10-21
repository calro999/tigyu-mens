import json

DATA_FILE = "data/posts.json"

# 各記事の内容・検索クエリに最適化されたSEOスラッグマッピング
SEO_SLUG_MAP = {
    "腹筋ローラー": "mens-ab-roller-workout",
    "オールインワン": "mens-all-in-one-gel-comparison",
    "コンシーラー": "mens-beard-concealer-guide",
    "眉毛": "mens-eyebrow-shaping-kit",
    "ワックス": "mens-hair-styling-wax-review",
    "無臭": "mens-body-odor-deodorant-best",
    "猫背": "mens-posture-corrector-roller"
}

with open(DATA_FILE, "r", encoding="utf-8") as f:
    posts = json.load(f)

for p in posts:
    title = p.get("title", "")
    assigned = False
    for keyword, seo_slug in SEO_SLUG_MAP.items():
        if keyword in title:
            p["slug"] = seo_slug
            assigned = True
            break
    if not assigned:
        p["slug"] = "mens-cosme-" + p.get("categoryEn", "care").lower()

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Updated slugs:")
for p in posts:
    print(f" - {p['slug']} : {p['title'][:35]}")
