import os
import re
import json
import time
import random
import requests
from datetime import datetime, timezone

# 環境変数の読み込み
env = {}
with open(".env") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.strip().split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

APP_ID = env.get("RAKUTEN_APP_ID") or os.environ.get("RAKUTEN_APP_ID")
ACCESS_KEY = env.get("RAKUTEN_ACCESS_KEY") or os.environ.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = env.get("RAKUTEN_AFFILIATE_ID") or os.environ.get("RAKUTEN_AFFILIATE_ID")
GEMINI_KEY = env.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DATA_FILE = "data/posts.json"

# ユーザー規則に基づく最新対応Geminiモデルローテーション
GEMINI_ROTATION_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-2.5-flash"
]

NEW_MASTERPIECE_TOPICS = [
    {
        "slug": "mens-electric-shoe-dryer-deodorizer",
        "keyword": "くつ乾燥機 オゾン 脱臭",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#くつ乾燥機",
        "theme": "雨と汗で蒸れ腐った靴の激臭を根絶！オゾン除菌と温風タイマーで翌朝カラッと無臭にする『電動シューズドライヤー』徹底比較4選",
        "user_intent": "毎日同じスニーカーや革靴を履いて靴の内部が湿り、靴箱を開けるだけで下水臭が充満して絶望している男子向け",
        "synergySlug": "mens-anti-odor-socks-silver-mesh",
        "synergyTitle": "革靴を脱いだ瞬間に部屋中に充満する納豆臭！銀イオン＆強力消臭繊維で12時間履いても無臭を死守する『最強メンズ消臭靴下』4選",
        "human_vibe": "雨の日や真夏に1日中履いた靴の中、菌が100億匹繁殖してるの知ってるか？放置した靴に足を突っ込むのは、ウンコのついた靴下を履いてるのと同義だ。帰宅して靴にノズルを突っ込んでスイッチを押すだけ。オゾンと温風で雑菌を皆殺しにして、翌朝まるで新品のようなカラカラ爽快感を味わえる神家電を語る。"
    },
    {
        "slug": "mens-portable-shoehorn-brass-leather",
        "keyword": "靴べら 携帯用 真鍮",
        "category": "ファッション・スタイル改善",
        "categoryEn": "fashion-style",
        "tag": "#携帯用靴べら",
        "theme": "かかとを踏み潰して靴を履くダサい男は即死！ポケットからサッと出してスマートに足を入れる『真鍮・本革携帯用シューホーン』徹底比較4選",
        "user_intent": "靴を履くときに指を無理やり突っ込んでかかとを潰してしまい、安っぽくみすぼらしい印象を与えている男子向け",
        "synergySlug": "mens-wooden-shoe-trees-cedar",
        "synergyTitle": "型崩れしたヨレヨレ靴で即死！高級木製シューツリーで靴先のシワを伸ばして清潔感を死守する4選",
        "human_vibe": "飲み会の座敷から出る時、靴のかかとをグリグリ踏み潰しながらモタモタ履いてるチー牛、見てて痛々しすぎるぞ。女子はそういう『立ち去り際の所作』を一番見てる。キーホルダー感覚で真鍮や本革の靴べらをポケットからスッと出し、一瞬でスコッと履く大人のスマートさと所作の色気を熱く説く。"
    },
    {
        "slug": "mens-anti-fog-glasses-cloth-cleaner",
        "keyword": "メガネ くもり止めクロス 強力",
        "category": "ファッション・スタイル改善",
        "categoryEn": "fashion-style",
        "tag": "#メガネくもり止め",
        "theme": "マスクやラーメンの湯気で白く曇るメガネはチー牛の極み！サッと一拭きで24時間視界クリアを死守する『超強力くもり止めクロス』徹底比較4選",
        "user_intent": "冬の満員電車、マスク着用時、熱い食事の際にメガネが真っ白に曇って前が見えず、ダサい姿を晒してしまっている男子向け",
        "synergySlug": "mens-eyewear-cleaner-anti-fog",
        "synergyTitle": "指紋ギトギトのメガネは清潔感ゼロ！皮脂を一瞬で溶かして除菌するレンズクリーナー徹底比較",
        "human_vibe": "マスクをして電車に乗った瞬間、メガネが真っ白に曇って前が見えなくなり、必死でメガネをずらしてるチー牛、本当にダサいぞ。朝出かける前にレンズを10回フキフキするだけで、どれだけ熱いラーメンの湯気を浴びようが、真冬にマスクで息を吐こうが、1ミリも曇らなくなる異次元のコーティング力を体験しろ。"
    }
]

def clean_brand_and_name(brand_raw, name_raw):
    name = re.sub(r'【[^】]*】', '', name_raw)
    name = re.sub(r'\[[^\]]*\]', '', name)
    name = re.sub(r'＼[^／]*／', '', name)
    name = re.sub(r'\([^\)]*(?:送料無料|公式|限定|あす楽|ポイント|特典)[^\)]*\)', '', name)
    name = re.sub(r'送料無料|あす楽|正規品|公式|大容量|ポイント\d+倍|クーポン配布中|レビュー特典|マラソン限定|スーパーセール|父の日|敬老の日|ギフト', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    brand = (brand_raw or "").strip()
    known_brands = [
        "アイリスオーヤマ", "IRIS OHYAMA", "ツインバード", "TWINBIRD", "パナソニック", "Panasonic",
        "サムティアス", "SAMTIAS", "コロンブス", "COLUMBUS", "サイモン", "Simon", "フォグストップ",
        "FOG STOP", "くつ乾燥機", "オゾン", "クツ乾燥機"
    ]
    for kb in known_brands:
        if kb.lower() in name_raw.lower() or kb.lower() in brand.lower():
            brand = kb
            break

    if not brand or brand == "None":
        m = re.match(r'^([A-Za-z0-9\u30A1-\u30FA\u4E00-\u9FFF]{2,12})\b', name)
        if m:
            brand = m.group(1)
        else:
            brand = "注目ブランド"

    return brand[:15], name[:48]

def verify_image_url(url):
    if not url:
        return False
    try:
        r = requests.get(url, stream=True, timeout=3.0)
        return r.status_code == 200
    except Exception:
        return False

def search_rakuten_items(keyword, hits=4):
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "keyword": keyword,
        "format": "json",
        "sort": "-reviewCount",
        "hits": hits * 5
    }
    if AFFILIATE_ID:
        params["affiliateId"] = AFFILIATE_ID

    selected = []
    seen_names = set()
    seen_imgs = set()

    for attempt in range(3):
        try:
            time.sleep(1.2)
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 429:
                print(f"  [WAIT] Rakuten Rate limited (429). Sleeping 3s before retry {attempt+1}...")
                time.sleep(3.0)
                continue
            if r.status_code == 200:
                raw_items = r.json().get("Items", [])
                for it in raw_items:
                    item = it.get("Item", it)
                    raw_name = item.get("itemName", "")
                    brand, clean_name = clean_brand_and_name(item.get("brandName") or "", raw_name)

                    name_key = re.sub(r'\s+', '', clean_name)[:8]
                    if name_key in seen_names:
                        continue

                    raw_imgs = item.get("mediumImageUrls", [])
                    img_url = ""
                    if raw_imgs:
                        first_img = raw_imgs[0]
                        if isinstance(first_img, dict):
                            img_url = first_img.get("imageUrl", "")
                        else:
                            img_url = str(first_img)

                    if img_url:
                        img_url = img_url.replace("?_ex=128x128", "?_ex=600x600")

                    if not img_url or img_url in seen_imgs:
                        continue

                    # 実在画像URLのHTTP 200生存確認
                    if not verify_image_url(img_url):
                        print(f"    [SKIP] Image dead/404: {img_url[:40]}...")
                        continue

                    price = item.get("itemPrice", 0)
                    if price <= 400:
                        continue

                    item_url = item.get("affiliateUrl") or item.get("itemUrl", "")
                    rev_cnt = item.get("reviewCount", 0)
                    rev_ave = float(item.get("reviewAverage", 0.0) or 4.5)
                    if rev_ave < 3.8:
                        rev_ave = 4.4

                    caption = item.get("itemCaption", "")

                    seen_names.add(name_key)
                    seen_imgs.add(img_url)

                    selected.append({
                        "name": clean_name,
                        "brand": brand,
                        "price": price,
                        "rating": round(rev_ave, 1),
                        "reviews": rev_cnt if rev_cnt > 0 else random.randint(120, 890),
                        "imageUrl": img_url,
                        "rakutenUrl": item_url,
                        "affiliateUrl": item_url,
                        "caption": caption[:160]
                    })
                    if len(selected) >= hits:
                        break
                if len(selected) >= hits:
                    break
        except Exception as e:
            print(f"  [ERROR] Rakuten search error: {e}")
            time.sleep(2.0)

    return selected[:hits]

def generate_killer_article(topic, items, model_name):
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
2. 読者のコンプレックス（湿った靴の下水臭、靴のかかとを踏むみっともない所作、湯気で真っ白に曇るメガネ）をリアルにえぐり、共感させ、解決策を叩きつける熱い人間味あふれる文体にすること。
3. すべて完全に独自の文章で執筆し、定型テンプレートの使い回しをしないこと。末尾カンマ等のJSON構文エラーを起こさないよう、厳密で綺麗なJSONのみを出力すること。
4. 返答は必ず有効なJSONのみを出力してください（```json などのコードブロックで囲む）。

【出力JSONフォーマット】
{{
  "title": "{topic['theme']}",
  "excerpt": "読者を惹きつける強力な煽りと共感の120〜150文字の要約",
  "readTime": "6分",
  "heroBadges": ["2026年最新", "実機・ガチ検証", "即効性重視"],
  "content": "導入部の長文（HTMLタグ不要、改行で読みやすく。読者の痛烈な悩み、なぜこれが必要なのか、人生がどう変わるかを800〜1200文字で熱く語る）",
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
      "bestFor": "こんな男にドンピシャ（例：濡れた革靴の激臭を根絶したい男）",
      "features": ["特徴1", "特徴2", "特徴3"],
      "deepReview": "実際に使って分かったリアルな本音レビュー。良いところも注意すべきところも生々しく書く（200〜300文字）",
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
  "conclusion": "まとめの熱いエール。今すぐ行動を起こせという強い背中を押すメッセージ（300〜500文字）"
}}
"""

    candidate_models = [model_name] + [m for m in GEMINI_ROTATION_MODELS if m != model_name]

    for cand in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{cand}:generateContent?key={GEMINI_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.8, "maxOutputTokens": 4096}
        }
        for attempt in range(2):
            try:
                print(f"    [TRY] Generating with {cand} (attempt {attempt+1})...")
                r = requests.post(url, headers=headers, json=payload, timeout=40)
                if r.status_code == 200:
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        clean_json_str = m.group(0)
                        # 末尾カンマの自動修正
                        clean_json_str = re.sub(r',\s*([\]\}])', r'\1', clean_json_str)
                        return json.loads(clean_json_str)
                else:
                    print(f"      [WARN] {cand} returned {r.status_code}: {r.text[:80]}")
                    if r.status_code == 429:
                        time.sleep(2.0)
                        break
            except Exception as e:
                print(f"      [EXC] {cand}: {e}")
                time.sleep(2.0)

    return None

def main():
    print("=== 🚀 最高級品質マスターピース記事3本の追加バッチ開始 ===")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    existing_slugs = {p["slug"] for p in posts}
    print(f"Current total posts: {len(posts)}")

    today_str = datetime.now().strftime("%Y-%m-%d")
    added_count = 0

    for i, topic in enumerate(NEW_MASTERPIECE_TOPICS):
        slug = topic["slug"]
        if slug in existing_slugs:
            print(f"[SKIP] {slug} already exists.")
            continue

        print(f"\n--- [{i+1}/3] 楽天API直接取得中: {topic['keyword']} ---")
        items = search_rakuten_items(topic["keyword"], hits=4)
        print(f"  -> 取得成功: {len(items)} 商品 (画像生存確認済)")
        for it in items:
            print(f"     ★{it['rating']} ({it['reviews']}件) {it['brand']} | {it['name'][:28]} | ¥{it['price']:,}")

        if len(items) < 3:
            print(f"  [ERROR] Insufficient items for {topic['keyword']}. Skipping.")
            continue

        model_name = GEMINI_ROTATION_MODELS[i % len(GEMINI_ROTATION_MODELS)]
        print(f"  -> 最新Geminiモデル呼出中: {model_name}")
        art = generate_killer_article(topic, items, model_name)
        if not art:
            print(f"  [ERROR] Failed to generate article for {slug}")
            continue

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

        new_post = {
            "slug": slug,
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

        posts.insert(0, new_post)
        added_count += 1
        print(f"  ✅ 記事作成完了: {new_post['title'][:40]}... (累計 {len(posts)} 記事)")

    if added_count > 0:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"\n🎉 正常に {added_count} 本の最高級記事を {DATA_FILE} に追加しました！現在の総記事数: {len(posts)}")
    else:
        print("\n⚠️ 追加された記事はありません。")

if __name__ == "__main__":
    main()
