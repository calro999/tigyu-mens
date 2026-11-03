import os
import re
import json
import time
import random
import requests
from datetime import datetime

env = {}
with open(".env") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

APP_ID = env.get("RAKUTEN_APP_ID")
ACCESS_KEY = env.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = env.get("RAKUTEN_AFFILIATE_ID")
GEMINI_KEY = env.get("GEMINI_API_KEY")

DATA_FILE = "data/posts.json"

topic = {
    "slug": "mens-styling-mesh-comb-barber",
    "keyword": "メッシュコーム",
    "category": "ヘアスタイル・頭皮ケア",
    "categoryEn": "hair-scalp",
    "tag": "#メッシュコーム",
    "theme": "手ぐしセットで毛流れがボサボサに崩れる男はダサい！粗歯で梳かすだけでサロン帰りの束感が作れる『バーバー仕様メッシュコーム』徹底比較4選",
    "user_intent": "センターパートやマッシュ、ツーブロックのスタイリングで手ぐしだと毛束が太くなりすぎたり均一に毛流れが作れず悩んでいる男子向け",
    "synergySlug": "mens-hair-styling-wax-review",
    "synergyTitle": "ノーセット髪はもう限界！朝5分で人生が変わる髪質別メンズワックス徹底比較4選",
    "human_vibe": "ワックスを適当につけた後、手ぐしだけで適当に散らして『なんかボサボサで決まらない』って頭抱えてないか？美容師やバーバーがやってるプロの毛流れは、目の粗いメッシュコームを通すだけで10秒で作れるんだ。ワックスの馴染みと束感の美しさが別次元になる、1000円前後の最強神アイテムを熱く語る。"
}

def clean_brand_and_name(brand_raw, name_raw):
    name = re.sub(r'【[^】]*】|\[[^\]]*\]|＼[^／]*／', '', name_raw)
    name = re.sub(r'\([^\)]*(?:送料無料|公式|限定|あす楽|ポイント|特典)[^\)]*\)', '', name)
    name = re.sub(r'送料無料|あす楽|正規品|公式|大容量|ポイント\d+倍|クーポン配布中|レビュー特典|マラソン限定|スーパーセール|父の日|敬老の日|ギフト', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    brand = "iMii" if "imii" in name_raw.lower() else "バーバーコーム"
    return brand, name[:48]

def search_items():
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "keyword": topic["keyword"],
        "format": "json",
        "sort": "-reviewCount",
        "hits": 20
    }
    r = requests.get(url, params=params, timeout=10)
    items = []
    seen = set()
    for it in r.json().get("Items", []):
        item = it.get("Item", it)
        brand, clean_name = clean_brand_and_name("", item.get("itemName", ""))
        key = clean_name[:10]
        if key in seen:
            continue
        raw_imgs = item.get("mediumImageUrls", [])
        if not raw_imgs:
            continue
        img = (raw_imgs[0].get("imageUrl") if isinstance(raw_imgs[0], dict) else str(raw_imgs[0])).replace("?_ex=128x128", "?_ex=600x600")
        try:
            if requests.get(img, timeout=2.5).status_code != 200:
                continue
        except Exception:
            continue
        seen.add(key)
        items.append({
            "name": clean_name,
            "brand": brand,
            "price": item.get("itemPrice", 990),
            "rating": round(float(item.get("reviewAverage", 4.6)), 1),
            "reviews": item.get("reviewCount", 100),
            "imageUrl": img,
            "rakutenUrl": item.get("itemUrl", ""),
            "affiliateUrl": item.get("itemUrl", ""),
            "caption": item.get("itemCaption", "")[:160]
        })
        if len(items) >= 4:
            break
    return items

items = search_items()
print("Found items:", len(items))

items_desc = ""
for i, it in enumerate(items):
    items_desc += f"""
商品{i+1}:
- ブランド: {it['brand']}
- 名称: {it['name']}
- 価格: 約{it['price']:,}円
- 特徴概要: {it['caption']}
"""

prompt = f"""
あなたは月間100万PVの超人気メンズ垢抜け・メンズ美容Webメディア「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の看板熱血編集長です。
読者は「身だしなみに無頓着で清潔感がなく、女子から生理的に無理と見下されていたが、本気で清潔感を手に入れて人生逆転したい男子」です。

テーマ: {topic['theme']}
スラッグ: {topic['slug']}
対象読者の悩み: {topic['user_intent']}
記事の人間味・世界観: {topic['human_vibe']}

紹介商品データ:
{items_desc}

【厳格ルール】
1. AI臭さ（「いかがでしたでしょうか」「是非参考にしてみてください」など）は絶対禁止。
2. 読者のコンプレックス（手ぐしでボサボサの髪型、ワックスつけてもキマらない苛立ち）をリアルにえぐり、共感させ、解決策を叩きつける熱い人間味あふれる文体にすること。
3. すべて完全に独自の文章で執筆し、定型テンプレートの使い回しをしないこと。末尾カンマ等のJSON構文エラーを起こさないよう、厳密で綺麗なJSONのみを出力すること。
4. 返答は必ず有効なJSONのみを出力してください（```json などのコードブロックで囲む）。

【出力JSONフォーマット】
{{
  "title": "{topic['theme']}",
  "excerpt": "読者を惹きつける強力な煽りと共感の120〜150文字の要約",
  "readTime": "6分",
  "heroBadges": ["2026年最新", "実機・ガチ検証", "即効性重視"],
  "content": "導入部の長文（800〜1200文字で熱く語る）",
  "beforeAfter": {{
    "before": ["チー牛時代の最悪な状態1", "チー牛時代の最悪な状態2", "チー牛時代の最悪な状態3"],
    "after": ["導入後の劇的改善1", "導入後の劇的改善2", "導入後の劇的改善3"]
  }},
  "selectionCriteria": [
    {{"title": "1. 鉄則1のタイトル", "body": "具体的で失敗しない選び方の解説"}},
    {{"title": "2. 鉄則2のタイトル", "body": "具体的で失敗しない選び方の解説"}},
    {{"title": "3. 鉄則3のタイトル", "body": "具体的で失敗しない選び方の解説"}}
  ],
  "itemDetails": [
    {{
      "bestFor": "こんな男にドンピシャ（例：センターパートの毛流れを一瞬で作りたい男）",
      "features": ["特徴1", "特徴2", "特徴3"],
      "deepReview": "実際に使って分かったリアルな本音レビュー（200〜300文字）",
      "dailyCost": "1日あたり約〇〇円（コスパ計算）"
    }},
    {{
      "bestFor": "こんな男にドンピシャ",
      "features": ["特徴1", "特徴2", "特徴3"],
      "deepReview": "実際に使って分かったリアルな本音レビュー（200〜300文字）",
      "dailyCost": "1日あたり約〇〇円"
    }},
    {{
      "bestFor": "こんな男にドンピシャ",
      "features": ["特徴1", "特徴2", "特徴3"],
      "deepReview": "実際に使って分かったリアルな本音レビュー（200〜300文字）",
      "dailyCost": "1日あたり約〇〇円"
    }},
    {{
      "bestFor": "こんな男にドンピシャ",
      "features": ["特徴1", "特徴2", "特徴3"],
      "deepReview": "実際に使って分かったリアルな本音レビュー（200〜300文字）",
      "dailyCost": "1日あたり約〇〇円"
    }}
  ],
  "usageSteps": [
    {{"step": "STEP 1: 準備", "title": "手順の要約", "description": "具体的な使い方と失敗しないコツ"}},
    {{"step": "STEP 2: 実践", "title": "手順の要約", "description": "具体的な使い方と失敗しないコツ"}},
    {{"step": "STEP 3: 仕上げ＆ケア", "title": "手順の要約", "description": "具体的な使い方と失敗しないコツ"}}
  ],
  "faqs": [
    {{"q": "読者が最も不安に思う疑問1？", "a": "プロとしての本音の回答"}},
    {{"q": "読者が最も不安に思う疑問2？", "a": "プロとしての本音の回答"}},
    {{"q": "読者が最も不安に思う疑問3？", "a": "プロとしての本音の回答"}}
  ],
  "conclusion": "まとめの熱いエール（300〜500文字）"
}}
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={GEMINI_KEY}"
headers = {"Content-Type": "application/json"}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.8, "maxOutputTokens": 4096}
}
r = requests.post(url, headers=headers, json=payload, timeout=40)
txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
clean_json_str = re.search(r'\{[\s\S]*\}', txt).group(0)
clean_json_str = re.sub(r',\s*([\]\}])', r'\1', clean_json_str)
art = json.loads(clean_json_str)

final_items = []
comparison_table = []
item_details = art.get("itemDetails", [])

for idx, it in enumerate(items):
    detail = item_details[idx] if idx < len(item_details) else {}
    features = detail.get("features", ["高機能", "高コスパ", "即効性"])
    best_for = detail.get("bestFor", "清潔感を爆上げしたい全ての男子")
    deep_review = detail.get("deepReview", f"{it['brand']}のこだわりが詰まった名機。毎日のケアに取り入れるだけで見違えるほどの変化を実感できる。")
    daily_cost = detail.get("dailyCost", f"1日あたり約{max(10, it['price']//180)}円")

    item_obj = {
        "name": it["name"],
        "brand": it["brand"],
        "price": it["price"],
        "rating": it["rating"],
        "reviews": it["reviews"],
        "imageUrl": it["imageUrl"],
        "rakutenUrl": it["rakutenUrl"],
        "affiliateUrl": it["affiliateUrl"],
        "features": features,
        "bestFor": best_for,
        "deepReview": deep_review,
        "dailyCost": daily_cost
    }
    final_items.append(item_obj)

    comparison_table.append({
        "name": it["name"],
        "brand": it["brand"],
        "price": f"¥{it['price']:,}",
        "rating": it["rating"],
        "reviewCount": it["reviews"],
        "features": features,
        "targetSkin": best_for,
        "imageUrl": it["imageUrl"],
        "rakutenUrl": it["rakutenUrl"],
        "affiliateUrl": it["affiliateUrl"],
        "pros": features[:2],
        "cons": ["人気のため在庫切れに注意"]
    })

today_str = datetime.now().strftime("%Y-%m-%d")
new_post = {
    "slug": topic["slug"],
    "title": art.get("title", topic["theme"]),
    "excerpt": art.get("excerpt", topic["user_intent"]),
    "date": today_str,
    "readTime": art.get("readTime", "6分"),
    "category": topic["category"],
    "categoryEn": topic["categoryEn"],
    "tag": topic["tag"],
    "tags": [topic["tag"]],
    "heroBadges": art.get("heroBadges", ["2026年最新", "実機検証", "コスパ最強"]),
    "content": art.get("content", ""),
    "beforeAfter": art.get("beforeAfter", {
        "before": ["チー牛時代の最悪な状態"],
        "after": ["導入後の劇的改善"]
    }),
    "selectionCriteria": art.get("selectionCriteria", []),
    "items": final_items,
    "comparisonTable": comparison_table,
    "usageSteps": art.get("usageSteps", []),
    "faqs": art.get("faqs", []),
    "synergyTip": {
        "text": f"さらに一段上の清潔感を目指すなら、{topic['synergyTitle']} と併用することで、隙のない完璧な爽やかさを手に入れられるぞ。",
        "targetSlug": topic["synergySlug"],
        "targetTitle": topic["synergyTitle"]
    },
    "conclusion": art.get("conclusion", "迷っている時間は一番の損失だ。今すぐ手に入れて、周囲の視線が変わる快感を味わえ！")
}

with open(DATA_FILE) as f:
    posts = json.load(f)

posts.insert(0, new_post)
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Successfully added comb article! Total posts:", len(posts))
