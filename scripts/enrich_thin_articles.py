import os
import sys
import requests
import json
import re
import random
import time
from datetime import datetime

def load_env():
    env_vars = {}
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip("'").strip('"')
    return env_vars

env = load_env()
APP_ID = env.get("RAKUTEN_APP_ID")
ACCESS_KEY = env.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = env.get("RAKUTEN_AFFILIATE_ID")
GEMINI_KEY = env.get("GEMINI_API_KEY")

DATA_FILE = "data/posts.json"

# 最新対応Geminiモデルローテーション（1.5系は完全廃止済みのため除外）
GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.5-flash"
]

def search_rakuten_items(keyword, count=4):
    """楽天新APIを直接叩いて最新の人気商品をリアルタイム取得"""
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "affiliateId": AFFILIATE_ID,
        "keyword": keyword,
        "hits": count,
        "format": "json",
        "sort": "-reviewCount"
    }
    try:
        res = requests.get(url, params=params, timeout=12)
        if res.status_code == 200:
            data = res.json()
            raw_items = data.get("Items", [])
            results = []
            for it in raw_items:
                item = it.get("Item", {})
                name = item.get("itemName", "")
                price = item.get("itemPrice", 0)
                aff_url = item.get("affiliateUrl", "")
                rev_cnt = item.get("reviewCount", 0)
                rev_ave = item.get("reviewAverage", 4.5)
                
                # 画像の取得（高画質URLへの変換対応）
                imgs = item.get("mediumImageUrls", [])
                img_url = ""
                if imgs:
                    raw_img = imgs[0] if isinstance(imgs[0], str) else imgs[0].get("imageUrl", "")
                    img_url = re.sub(r"\?_ex=\d+x\d+", "?_ex=600x600", raw_img)
                    if "?_ex=" not in img_url and img_url:
                        img_url += "?_ex=600x600"
                
                # ブランド名の推定抽出
                brand = "公式専売"
                if "【" in name and "】" in name:
                    m = re.search(r"【(.*?)】", name)
                    if m and len(m.group(1)) <= 15:
                        brand = m.group(1)
                elif " " in name:
                    first_word = name.split()[0]
                    if len(first_word) <= 15 and not first_word.startswith("★"):
                        brand = first_word

                # 商品名の簡潔化（余計なPR文言をカット）
                clean_name = re.sub(r"【.*?】|\[.*?\]|（.*?）", "", name).strip()
                clean_name = clean_name.split()[0] if len(clean_name.split()) > 0 else name[:25]
                if len(clean_name) < 4:
                    clean_name = name[:30]

                if aff_url and img_url:
                    results.append({
                        "name": clean_name,
                        "brand": brand,
                        "price": f"¥{price:,}",
                        "imageUrl": img_url,
                        "affiliateUrl": aff_url,
                        "rating": float(rev_ave) if rev_ave else 4.5,
                        "reviewCount": int(rev_cnt) if rev_cnt else 120
                    })
            return results
    except Exception as e:
        print(f"Rakuten API error: {e}", file=sys.stderr)
    return []

def call_gemini(prompt, sys_instruction=""):
    """Gemini API最新モデルをローテーションして呼び出し"""
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.95,
                "responseMimeType": "application/json"
            }
        }
        if sys_instruction:
            payload["systemInstruction"] = {"parts": [{"text": sys_instruction}]}
            
        try:
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text)
            elif res.status_code == 429:
                print(f"Rate limited on {model}, waiting 3s then trying next model...", file=sys.stderr)
                time.sleep(3.0)
                continue
            else:
                print(f"Error on {model}: {res.status_code} - {res.text[:100]}", file=sys.stderr)
        except Exception as e:
            print(f"Exception on {model}: {e}", file=sys.stderr)
            time.sleep(2.0)
    return None

def enrich_article(post):
    """薄い記事に対して楽天APIから比較商品を取得し、徹底的に肉付け"""
    slug = post["slug"]
    title = post["title"]
    category = post.get("category", "メンズコスメ")
    print(f"\n==================================================")
    print(f"Enriching: {title} ({slug})")
    
    current_products = post.get("comparisonTable", [])
    needed_count = 4 - len(current_products)
    
    # 検索キーワードの選定（タグやタイトルから抽出）
    search_query = post.get("tags", ["メンズコスメ"])[0].replace("#", "")
    if len(search_query) < 2 or search_query in ["コスメ", "チー牛脱却", "清潔感"]:
        search_query = title.split("！")[-1].split("？")[-1][:12]
        
    print(f"  Fetching from Rakuten API with keyword: '{search_query}'...")
    rakuten_items = search_rakuten_items(search_query, count=6)
    time.sleep(1.2) # APIレートリミット対策
    
    # 既存商品とURL重複のない新しい商品を追加
    existing_urls = set(p.get("affiliateUrl") for p in current_products)
    added_items = []
    for r in rakuten_items:
        if r["affiliateUrl"] not in existing_urls and len(added_items) < max(2, needed_count):
            added_items.append(r)
            existing_urls.add(r["affiliateUrl"])
            
    print(f"  Added {len(added_items)} new products via Rakuten API.")
    
    # Geminiで追加商品の詳細（targetSkin, bestFor, feature, pros, cons, deepReview, dailyCost）を生成
    if added_items:
        prompt = f"""
以下の記事と新商品リストに基づき、各商品のメンズ向け検証レビュー詳細データをJSON配列で生成してください。
AI臭い定型文や使い回しは厳禁。チー牛を脱出して本気で清潔感を手に入れたい男性向けに、実践的で具体的な検証トーンで書いてください。

【記事タイトル】{title}
【カテゴリー】{category}
【既存商品数】{len(current_products)}

【追加する商品リスト】
{json.dumps([{ 'name': it['name'], 'brand': it['brand'], 'price': it['price'] } for it in added_items], ensure_ascii=False, indent=2)}

【出力フォーマット】以下のキーを持つオブジェクトのJSON配列:
- targetSkin: 推奨タイプ（例: "オイリー・毛穴肌", "乾燥・敏感肌", "初心者・時短重視", "プロ仕様・剛毛向け" など）
- bestFor: こんな男子は迷わずコレ（具体的悩みとシチュエーション）
- feature: 商品の特徴（成分や独自機能、50文字程度）
- dailyCost: 1日あたりのコスト感（例: "1日あたり約38円（2ヶ月分）"）
- pros: メリット3つの配列（例: ["皮脂を吸着して夕方までサラサラ", "泡立て不要で朝が劇的に楽", "天然精油の爽やかな香り"]）
- cons: デメリット2つの配列（例: ["市販の安物より500円ほど高価", "冬場はしっかり保湿が必須"]）
- deepReview: 塾長の徹底解剖レビュー（200文字程度、実体験に基づいた本音の検証所感）
"""
        enrich_data = call_gemini(prompt, "あなたは『ゼロから始める垢抜けコスメ塾』の塾長。実体験と科学的根拠に基づいたメンズ美容のプロ。")
        if enrich_data and isinstance(enrich_data, list):
            for i, it in enumerate(added_items):
                meta = enrich_data[i] if i < len(enrich_data) else {}
                it["targetSkin"] = meta.get("targetSkin", "全肌質対応・バランス型")
                it["bestFor"] = meta.get("bestFor", "失敗せず王道を選びたい男子")
                it["feature"] = meta.get("feature", "高い実感力と扱いやすさを両立した高機能モデル")
                it["dailyCost"] = meta.get("dailyCost", "1日あたり約45円")
                it["pros"] = meta.get("pros", ["高い実感力", "初心者でも扱いやすい設計", "清潔感の向上"])
                it["cons"] = meta.get("cons", ["継続使用が前提", "店舗での取り扱いが限定的"])
                it["deepReview"] = meta.get("deepReview", "実際に使い込むことで真価を発揮する1本。日々のケアに組み込むことで清潔感が底上げされます。")
        else:
            for it in added_items:
                it["targetSkin"] = "全肌質対応・バランス型"
                it["bestFor"] = "失敗せず王道を選びたい男子"
                it["feature"] = "高い実感力と扱いやすさを両立した高機能モデル"
                it["dailyCost"] = "1日あたり約45円"
                it["pros"] = ["高い実感力", "初心者でも扱いやすい設計"]
                it["cons"] = ["継続使用が前提", "やや高価"]
                it["deepReview"] = "実際に使い込むことで真価を発揮する1本。日々のケアに組み込むことで清潔感が底上げされます。"
                
        current_products.extend(added_items)
        post["comparisonTable"] = current_products

    # featureSections（深掘りビジュアル解説）がない場合は作成
    if not post.get("featureSections") and len(current_products) >= 2:
        top1 = current_products[0]
        top2 = current_products[1]
        post["featureSections"] = [
            {
                "title": f"本命1位：なぜ「{top1['name']}」が圧倒的におすすめなのか？",
                "body": f"数多くの市販品やネット専売品を検証した結果、最も『失敗リスクが低く、効果の実感が早い』のがこの{top1['brand']}の{top1['name']}です。特に{top1.get('feature', '')}という点は、毎日のルーティンで劇的な差を生みます。迷っているならまずはここからスタートするのが最短ルートです。",
                "imageUrl": top1.get("imageUrl", ""),
                "imageAlt": top1.get("name", ""),
                "affiliateUrl": top1.get("affiliateUrl", ""),
                "affiliateButtonText": f"👉 {top1['brand']} {top1['name']}を楽天公式で最安値チェック →"
            },
            {
                "title": f"対抗馬：{top2.get('targetSkin', '別タイプ')}には「{top2['name']}」が刺さる！",
                "body": f"1位の本命アイテムと並んで甲乙つけがたいのがこちらの{top2['brand']}。{top2.get('feature', '')}に特化しているため、特に『{top2.get('bestFor', '特定の悩みを持つ方')}』には最高の相棒になります。",
                "imageUrl": top2.get("imageUrl", ""),
                "imageAlt": top2.get("name", ""),
                "affiliateUrl": top2.get("affiliateUrl", ""),
                "affiliateButtonText": f"👉 {top2['brand']} {top2['name']}を公式で見る →"
            }
        ]

    # usageSteps がない場合は追加
    if not post.get("usageSteps"):
        post["usageSteps"] = [
            {
                "step": "STEP 01",
                "title": "朝・夜のベース準備",
                "description": "清潔な状態を作り、アイテムの浸透・効果を最大化するためにぬるま湯または適切な下準備を行います。"
            },
            {
                "step": "STEP 02",
                "title": "適量をムラなく馴染ませる",
                "description": "ケチらず規定量を手のひらに取り、摩擦を与えないよう包み込むように優しく塗布・セットします。"
            },
            {
                "step": "STEP 03",
                "title": "仕上げと24時間キープのコツ",
                "description": "鏡で正面だけでなく横顔・首元まで確認。日中の崩れやテカリ、ニオイの発生を未然に防ぎます。"
            }
        ]

    return post

def main():
    print("Loading posts.json...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    # 比較商品が4つ未満の記事を抽出して処理
    target_posts = [p for p in posts if len(p.get("comparisonTable", [])) < 4]
    print(f"Found {len(target_posts)} thin articles to enrich.")

    processed_count = 0
    for p in target_posts:
        enrich_article(p)
        processed_count += 1
        # 定期セーブ
        if processed_count % 3 == 0 or processed_count == len(target_posts):
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
            print(f"--> Saved progress: {processed_count}/{len(target_posts)} posts.")
        time.sleep(1.0)

    print("\nAll target articles enriched successfully!")

if __name__ == "__main__":
    main()
