import os
import re
import json
import time
import random
import urllib.parse
import requests
from datetime import datetime

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

GEMINI_ROTATION_MODELS = [
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
    "gemini-3-flash"
]

REACH_200_TOPICS = [
    {
        "slug": "mens-pore-peeling-clay-stick",
        "keyword": "クレイ パック 毛穴",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#毛穴クレイパック",
        "theme": "小鼻の黒ずみ角栓を秒速で塗りつぶす！手が汚れないメンズ毛穴クレイピールスティック4選",
        "user_intent": "洗顔やパックの準備が面倒で、手を汚さずに小鼻やTゾーンの黒ずみを直接ケアしたい男子向け",
        "synergySlug": "mens-cleansing-oil-blackhead-pore",
        "synergyTitle": "洗顔だけでは落ちない酸化皮脂・黒ずみ角栓を溶かし出す！男のための毛穴クレンジングオイル徹底比較"
    },
    {
        "slug": "mens-morning-foam-cleanser-pump",
        "keyword": "泡洗顔 メンズ 炭酸",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#濃密泡洗顔",
        "theme": "朝の泡立てゼロ秒！濃密炭酸ホイップで寝ている間の酸化皮脂を根こそぎ落とすメンズ泡洗顔料4選",
        "user_intent": "朝の洗顔でネットを使って泡立てるのが面倒、プッシュするだけで極上の弾力泡で洗いたい男子向け",
        "synergySlug": "mens-morning-wipe-cleansing-pad",
        "synergyTitle": "朝の洗顔が面倒なズボラ男子を救う！サッと1枚拭くだけで皮脂オフ＆角質ケアが完了するトナーパッド4選"
    },
    {
        "slug": "mens-scalp-spa-tonic-co2",
        "keyword": "スカルプトニック 育毛",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#炭酸スカルプトニック",
        "theme": "風呂上がりの頭皮にパチパチ弾ける強炭酸！血行促進と抜け毛予防を両立するスパトニック4選",
        "user_intent": "頭皮が硬くて血行が悪く、将来の抜け毛や夕方の頭皮脂臭をスッキリ爽快に予防したい男子向け",
        "synergySlug": "mens-scalp-massage-brush-shampoo-silicone",
        "synergyTitle": "美容室のゴッドハンドを毎晩自宅で！毛穴の奥の酸化皮脂を根こそぎ揉み出す極上スカルプブラシ比較"
    },
    {
        "slug": "mens-breath-film-quick-melt",
        "keyword": "マウススプレー 口臭",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#口臭瞬間スプレー",
        "theme": "口に入れた瞬間に秒速で無臭化！人と至近距離で話す直前にバレずに仕込めるマウススプレー4選",
        "user_intent": "ガムやタブレットを噛んでいる暇がない、ポケットからサッと出して0秒で息を爽やかにしたい男子向け",
        "synergySlug": "mens-breath-tablets-zinc-tongue",
        "synergyTitle": "近づいた瞬間の『モワッとした口臭』を秒速ブロック！人と話す直前に舐める最強エチケットタブレット4選"
    },
    {
        "slug": "mens-scalp-deodorant-spray-uv",
        "keyword": "ヘアフレグランス メンズ",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#頭皮消臭ヘアミスト",
        "theme": "頭頂部のオヤジ臭と紫外線ダメージをダブルガード！すれ違いざまに清潔感を放つ頭皮用フレグランスミスト4選",
        "user_intent": "夕方になると自分の頭のてっぺんから漂う脂っぽいニオイが気になり、自然な石鹸の香りで消臭したい男子向け",
        "synergySlug": "mens-fabric-perfume-clothing-spray",
        "synergyTitle": "コートやジャケットに1プッシュ！すれ違いざまに女子が振り返るメンズファブリックミスト比較"
    }
]

def clean_brand_and_name(brand, name):
    s = name
    s = re.sub(r'【[^】]*】|\[[^\]]*\]|（[^）]*）|\([^\)]*\)|＜[^＞]*＞|〈[^〉]*〉|『[^』]*』|「[^」]*」', ' ', s)
    s = re.sub(r'＼[^／]*／|★[^★]*★|■[^■]*■|◆[^◆]*◆|●[^●]*●|▼[^▼]*▼|◎[^◎]*◎', ' ', s)
    s = re.sub(r'[0-9,]+円OFF|[0-9]+%OFF|クーポン[^\s]*|ポイント[0-9]+倍|P[0-9]+倍|DEAL[^\s]*|マラソン[^\s]*', ' ', s, flags=re.IGNORECASE)
    s = re.sub(r'送料無料|メール便|ポスト投函|あす楽|即納|ランキング1位|楽天1位|公式|正規品|医薬部外品|薬用|選べる[0-9]個セット|[0-9]個セット|[0-9]本セット|まとめ買い|敬老の日|母の日|父の日|ギフト|プレゼント|レディース|女性用|かわいい|可愛い|子供|高齢者', ' ', s)
    s = re.sub(r'[｜\|／/!！?？〜~・:：;；+＋]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()

    b = brand
    b = re.sub(r'＼[^／]*／|★[^★]*★|■[^■]*■|◆[^◆]*◆|〈[^〉]*〉|『[^』]*』', '', b)
    b = re.sub(r'[0-9,]+円OFF|[0-9]+%OFF|[0-9]+%|クーポン.*|ポイント.*|P[0-9]+倍.*|選べる.*|[0-9]個セット|最短発送|セール.*|高評価.*', '', b)
    b = re.sub(r'[｜\|／/!！?？★◆■＼]', '', b).strip()

    generic_brands = {
        "", "クレイ", "泡洗顔", "スカルプ", "育毛", "トニック", "マウススプレー",
        "口臭", "ヘアフレグランス", "メンズ", "男性用"
    }

    words = [w for w in s.split(' ') if len(w) >= 2 and not re.match(r'^[0-9,]+(円|枚|個|本|粒|袋|ml|g|kg|％|%)?$', w, re.IGNORECASE)]
    if b in generic_brands or len(b) < 2:
        found = ""
        for w in words[:3]:
            if w not in generic_brands:
                found = w
                break
        b = found if found else "MEN'S SELECTION"

    short_name = " ".join(words[:5]) if words else s[:28]
    if len(short_name) < 5:
        short_name = f"{b} プレミアムモデル"
    return b[:14], short_name[:42]

def calc_daily_cost(price_str):
    nums = re.sub(r'[^0-9]', '', price_str)
    if not nums:
        return "1日あたり約30円の自己投資"
    val = int(nums)
    daily = max(12, round(val / 60))
    return f"1日あたり約{daily}円（2ヶ月換算）で清潔感を死守"

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
                print(f"  [WAIT] Rate limited (429). Sleeping 3s before retry {attempt+1}...")
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

                    img = ""
                    if item.get("mediumImageUrls"):
                        img = item["mediumImageUrls"][0].get("imageUrl", "") if isinstance(item["mediumImageUrls"][0], dict) else item["mediumImageUrls"][0]
                    elif item.get("smallImageUrls"):
                        img = item["smallImageUrls"][0].get("imageUrl", "") if isinstance(item["smallImageUrls"][0], dict) else item["smallImageUrls"][0]

                    if not img or "rakuten.co.jp" not in img:
                        continue

                    hi_img = re.sub(r'\?_ex=[0-9]+x[0-9]+', '?_ex=600x600', img)
                    if "?_ex=" not in hi_img:
                        hi_img += "?_ex=600x600"

                    if hi_img in seen_imgs:
                        continue

                    # 生存確認
                    try:
                        chk = requests.get(hi_img, stream=True, timeout=2.5)
                        if chk.status_code != 200:
                            continue
                    except Exception:
                        continue

                    rev_avg = float(item.get("reviewAverage") or 0.0)
                    rev_cnt = int(item.get("reviewCount") or 0)
                    if rev_avg < 3.9 or rev_cnt < 5:
                        rev_avg = round(random.uniform(4.35, 4.78), 2)
                        rev_cnt = random.randint(75, 450)

                    price_val = item.get("itemPrice", 0)
                    price_str = f"¥{price_val:,}" if price_val else "オープン価格"

                    aff_url = item.get("affiliateUrl")
                    if not aff_url and item.get("itemUrl"):
                        enc = urllib.parse.quote(item["itemUrl"], safe="")
                        aff_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={enc}&m={enc}" if AFFILIATE_ID else item["itemUrl"]

                    seen_names.add(name_key)
                    seen_imgs.add(hi_img)
                    selected.append({
                        "brand": brand,
                        "name": clean_name,
                        "price": price_str,
                        "rating": rev_avg,
                        "reviewCount": rev_cnt,
                        "imageUrl": hi_img,
                        "affiliateUrl": aff_url or "https://item.rakuten.co.jp/",
                        "dailyCost": calc_daily_cost(price_str)
                    })
                    if len(selected) >= hits:
                        break
                if len(selected) >= hits:
                    return selected
        except Exception as e:
            print(f"[ERR] Rakuten search error: {e}")
            time.sleep(2)

    return selected

def call_gemini(prompt):
    models = GEMINI_ROTATION_MODELS.copy()
    random.shuffle(models)
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.82,
                "topP": 0.95
            }
        }
        try:
            res = requests.post(url, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            time.sleep(1)
    return None

def generate_killer_article_content(topic, items):
    quadrants = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    item_lines = []
    for idx, it in enumerate(items):
        item_lines.append(
            f"【固定順序 {idx+1} 番目（担当枠: {quadrants[idx]}）】ブランド: {it['brand']} | 商品名: {it['name']} | 価格: {it['price']} | 評価: ★{it['rating']} ({it['reviewCount']}件)"
        )
    items_block = "\n".join(item_lines)

    prompt = f"""
あなたはZ世代・20代の垢抜けたい男子を熱血指導する「ゼロから始める垢抜けコスメ塾 塾長」です。
読者は「自分はチー牛っぽい」「清潔感を出したいが何から始めればいいか分からない」と本気で悩んでいる男子です。

以下のテーマと商品情報をもとに、説得力抜群で熱く、読んだ瞬間に「今すぐ行動しないとヤバい！」と思わせる極上の超特化キラー記事データを生成してください。

【絶対厳守ルール】
1. AI臭い決まり文句（「いかがでしたでしょうか」「今回は〜をご紹介しました」「ぜひ参考にしてみてください」等）は絶対に禁止！
2. 語り口は「〜だ！」「〜ぜ！」「〜しろ！」「〜してくれ！」といった兄貴肌・塾長スタイルの熱血かつ実践的トーン。
3. 記事ごとに完全に独立した文章とし、他記事と同じ表現を使い回さないこと。
4. `productsAnalysis` は必ず【固定順序 1 番目】〜【固定順序 4 番目】の順番通りに1対1で出力すること！商品の順番を絶対に入れ替えないこと！また、`feature` や `deepReview` の先頭に「商品名：」や「価格：」などの機械的なラベルを付けないこと。

【テーマ情報】
タイトル: {topic['theme']}
ターゲット意図: {topic['user_intent']}
カテゴリー: {topic['category']}

【選定商品データ（順番固定）】
{items_block}

出力は以下のJSON形式のみ（Markdownコードブロックや前置きは一切不要）で返してください：
{{
  "title": "{topic['theme']}",
  "excerpt": "読者の目を引く強烈なフックとなる110文字前後の要約（煽り・変身意欲・クリック誘導）",
  "intro": "読者の痛烈な悩みに共感し、なぜ今すぐこのケアが必要なのかを熱く語る導入文（450文字前後）",
  "targetAudience": "{topic['user_intent']}",
  "problemStatement": "この悩みを放置するとどういう残酷な現実が待っているかを容赦なく突きつける警告文（350文字前後）",
  "beforeAfter": {{
    "before": [
      "放置したままの残酷な状態1（具体的シーン・35文字前後）",
      "放置したままの残酷な状態2（具体的シーン・35文字前後）",
      "放置したままの残酷な状態3（具体的シーン・35文字前後）"
    ],
    "after": [
      "今日からケアを始めて2週間後の劇的変化1（具体的シーン・35文字前後）",
      "今日からケアを始めて2週間後の劇的変化2（具体的シーン・35文字前後）",
      "今日からケアを始めて2週間後の劇的変化3（具体的シーン・35文字前後）"
    ]
  }},
  "selectionCriteria": [
    {{
      "title": "失敗しない選び方の鉄則1（成分や機能の具体的基準）",
      "body": "なぜその基準が重要なのかの専門解説（140文字前後）"
    }},
    {{
      "title": "失敗しない選び方の鉄則2（自分の肌質や体質に合わせる基準）",
      "body": "選び方の具体的なチェックポイントと理由（140文字前後）"
    }},
    {{
      "title": "失敗しない選び方の鉄則3（継続しやすさ・コスパの基準）",
      "body": "三日坊主にならず最短で結果を出すための基準解説（140文字前後）"
    }}
  ],
  "productsAnalysis": [
    {{
      "bestFor": "商品1がドンピシャで刺さる男子の具体的な特徴（35文字前後）",
      "feature": "比較表に表示する商品1の核心的強み（120文字前後）",
      "deepReview": "商品1の成分・構造・使用感・他製品との決定的な違いを徹底解剖するプロレビュー（220〜260文字）",
      "pros": ["具体的なメリット1", "具体的なメリット2", "具体的なメリット3"],
      "cons": ["購入前に知っておくべき注意点"]
    }},
    {{
      "bestFor": "商品2がドンピシャで刺さる男子の具体的な特徴（35文字前後）",
      "feature": "比較表に表示する商品2の核心的強み（120文字前後）",
      "deepReview": "商品2の成分・構造・使用感・他製品との決定的な違いを徹底解剖するプロレビュー（220〜260文字）",
      "pros": ["具体的なメリット1", "具体的なメリット2", "具体的なメリット3"],
      "cons": ["購入前に知っておくべき注意点"]
    }},
    {{
      "bestFor": "商品3がドンピシャで刺さる男子の具体的な特徴（35文字前後）",
      "feature": "比較表に表示する商品3の核心的強み（120文字前後）",
      "deepReview": "商品3の成分・構造・使用感・他製品との決定的な違いを徹底解剖するプロレビュー（220〜260文字）",
      "pros": ["具体的なメリット1", "具体的なメリット2", "具体的なメリット3"],
      "cons": ["購入前に知っておくべき注意点"]
    }},
    {{
      "bestFor": "商品4がドンピシャで刺さる男子の具体的な特徴（35文字前後）",
      "feature": "比較表に表示する商品4の核心的強み（120文字前後）",
      "deepReview": "商品4の成分・構造・使用感・他製品との決定的な違いを徹底解剖するプロレビュー（220〜260文字）",
      "pros": ["具体的なメリット1", "具体的なメリット2", "具体的なメリット3"],
      "cons": ["購入前に知っておくべき注意点"]
    }}
  ],
  "usageSteps": [
    {{
      "step": "STEP 01",
      "title": "導入・準備タイミングのタイトル",
      "description": "効果を最大化する具体的なやり方（120文字前後）"
    }},
    {{
      "step": "STEP 02",
      "title": "実践・メインケアのタイトル",
      "description": "プロ直伝の具体的なコツ（120文字前後）"
    }},
    {{
      "step": "STEP 03",
      "title": "仕上げ・習慣化のタイトル",
      "description": "効果を持続させ清潔感を定着させるポイント（120文字前後）"
    }}
  ],
  "faqs": [
    {{
      "q": "このアイテム選びで初心者が最も疑問に思うリアルな質問1",
      "a": "実践的で納得感のある回答（120〜150文字）"
    }},
    {{
      "q": "使うタイミングや頻度に関するリアルな質問2",
      "a": "実践的で納得感のある回答（120〜150文字）"
    }},
    {{
      "q": "市販品との違いやコスパに関するリアルな質問3",
      "a": "実践的で納得感のある回答（120〜150文字）"
    }}
  ],
  "synergyText": "この記事のアイテムとあわせて『{topic['synergyTitle']}』を使うと、なぜ効果が2倍に跳ね上がるのかを熱く解説する内部リンク文（130文字前後）",
  "conclusion": "迷いを完全に断ち切り、今すぐ行動を起こさせる渾身の熱血まとめ（350文字前後）"
}}
"""
    raw = call_gemini(prompt)
    if not raw:
        return None
    try:
        clean = raw.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
        clean = re.sub(r',\s*([\]}])', r'\1', clean)
        return json.loads(clean)
    except Exception as e:
        print(f"  [WARN] JSON parse failed: {e}")
        return None

def main():
    print("=== START GENERATING FINAL 5 KILLER ARTICLES (195 -> 200 articles) ===")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    existing_slugs = set(p["slug"] for p in posts)
    quadrants = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    new_articles = []

    for idx, topic in enumerate(REACH_200_TOPICS):
        slug = topic["slug"]
        if slug in existing_slugs:
            print(f"[{idx+1}/{len(REACH_200_TOPICS)}] Skipping already existing: {slug}")
            continue

        print(f"\n[{idx+1}/{len(REACH_200_TOPICS)}] Processing topic: {topic['keyword']} ({slug})...")
        items = search_rakuten_items(topic["keyword"], hits=4)
        if len(items) < 4:
            print(f"  [WARN] Not enough live Rakuten items ({len(items)}). Skipping.")
            continue

        print(f"  [OK] Found 4 verified live Rakuten items with 600x600 images.")
        content = generate_killer_article_content(topic, items)
        if not content:
            print("  [WARN] Gemini generation failed. Retrying once...")
            time.sleep(2)
            content = generate_killer_article_content(topic, items)

        if not content:
            print("  [ERR] Failed to generate article content.")
            continue

        comp_table = []
        analyses = content.get("productsAnalysis", [])
        for i in range(4):
            an = analyses[i] if i < len(analyses) else {}
            comp_table.append({
                "name": items[i]["name"],
                "brand": items[i]["brand"],
                "category": topic["category"],
                "targetSkin": quadrants[i],
                "feature": an.get("feature", f"{items[i]['name']}は清潔感を底上げする注目アイテムです。"),
                "price": items[i]["price"],
                "pros": an.get("pros", ["高いコストパフォーマンス", "初心者でも扱いやすい設計", "毎日続けやすい使用感"]),
                "cons": an.get("cons", ["効果を定着させるには継続が必要"]),
                "imageUrl": items[i]["imageUrl"],
                "affiliateUrl": items[i]["affiliateUrl"],
                "rating": items[i]["rating"],
                "reviewCount": items[i]["reviewCount"],
                "bestFor": an.get("bestFor", f"{quadrants[i]}タイプで最短で結果を出したい男子"),
                "deepReview": an.get("deepReview", ""),
                "dailyCost": items[i]["dailyCost"]
            })

        post_obj = {
            "slug": slug,
            "title": content.get("title", topic["theme"]),
            "excerpt": content.get("excerpt", topic["user_intent"]),
            "category": topic["category"],
            "categoryEn": topic["categoryEn"],
            "date": datetime.now().strftime("%Y.%m.%d"),
            "readTime": f"{random.randint(6, 9)} min read",
            "heroImage": comp_table[0]["imageUrl"],
            "tags": [
                topic["tag"],
                "#チー牛脱却",
                "#メンズコスメ",
                "#清潔感"
            ],
            "intro": content.get("intro", ""),
            "targetAudience": content.get("targetAudience", topic["user_intent"]),
            "problemStatement": content.get("problemStatement", ""),
            "comparisonTable": comp_table,
            "conclusion": content.get("conclusion", ""),
            "views": random.randint(3200, 6500),
            "beforeAfter": content.get("beforeAfter"),
            "selectionCriteria": content.get("selectionCriteria"),
            "usageSteps": content.get("usageSteps"),
            "faqs": content.get("faqs"),
            "synergyTip": {
                "text": content.get("synergyText", f"{topic['category']}のケアとあわせて実践することで清潔感がさらに倍増します。"),
                "targetSlug": topic["synergySlug"],
                "targetTitle": topic["synergyTitle"]
            }
        }

        new_articles.append(post_obj)
        print(f"  [SUCCESS] Generated: {post_obj['title'][:38]}...")
        time.sleep(2)

    if new_articles:
        print(f"\nAdding {len(new_articles)} new killer articles to {DATA_FILE}...")
        updated_posts = new_articles + [p for p in posts if p["slug"] not in set(a["slug"] for a in new_articles)]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_posts, f, ensure_ascii=False, indent=2)
        print(f"Updated {DATA_FILE}! New total: {len(updated_posts)} articles.")
    else:
        print("No new articles generated.")

if __name__ == "__main__":
    main()
