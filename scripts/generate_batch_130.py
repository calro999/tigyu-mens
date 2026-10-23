import os
import requests
import json
import time
import random
import re
import urllib.parse
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

# ユーザー規則に基づく最新対応Geminiモデルローテーション（1.5系は完全廃止・禁止）
GEMINI_ROTATION_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

NEW_BATCH_TOPICS = [
    {
        "slug": "mens-facial-cleansing-brush-sonic",
        "keyword": "洗顔ブラシ メンズ 音波 電動 シリコン",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#音波洗顔ブラシ",
        "theme": "手洗い洗顔はもう古い！音波振動で毛穴の奥の黒ずみと角栓を叩き出すメンズ電動洗顔ブラシ比較",
        "user_intent": "ゴシゴシ手洗いしても小鼻の黒ずみやアブラっぽさが取れず、肌を傷めずにツルツルにしたい男子向け"
    },
    {
        "slug": "mens-compression-inner-posture-shirt",
        "keyword": "加圧シャツ メンズ 着圧インナー 姿勢 補正",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#加圧インナー",
        "theme": "着た瞬間にお腹凹み＆背筋ピン！服の下に着込むだけでチー牛体型を即引き締める加圧インナーシャツ比較",
        "user_intent": "ぽっこりお腹や丸まった背中が服の上から目立ち、即効でスタイルを引き締めたい男子向け"
    },
    {
        "slug": "mens-medicated-acne-body-mist",
        "keyword": "背中ニキビ メンズ スプレー 薬用 ミスト",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#背中ニキビスプレー",
        "theme": "手の届かない背中ニキビ＆ザラつきを撃退！逆さ噴射できる薬用アクネボディミスト徹底比較",
        "user_intent": "脱衣所や海・温泉で背中の赤いブツブツや色素沈着を見られるのがコンプレックスな男子向け"
    },
    {
        "slug": "mens-foam-roller-myofascial-release",
        "keyword": "フォームローラー 筋膜リリース メンズ ストレッチ",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#フォームローラー",
        "theme": "ガチガチ背中と巻き肩を一撃ほぐし！1日3分ゴロゴロするだけで姿勢改善する筋膜リリースローラー比較",
        "user_intent": "長時間のPC作業やスマホで肩甲骨周りや太ももが固まり、体が重だるく姿勢が歪んでいる男子向け"
    },
    {
        "slug": "mens-tinted-sunscreen-bb-stick",
        "keyword": "日焼け止め スティック メンズ UV スティック",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#UVスティック",
        "theme": "手を汚さず直塗り5秒！外出先でもテカらず紫外線ガードできるメンズUVサンスティック比較",
        "user_intent": "日焼け止めのベタつきや手が白くなるのが嫌いで、持ち歩いてノールックで塗り直したい男子向け"
    },
    {
        "slug": "mens-scented-hand-cream-clean",
        "keyword": "ハンドクリーム メンズ いい匂い ベタつかない",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#メンズハンドクリーム",
        "theme": "スマホ触ってもベタつかない！すれ違いざまに上品な清潔感がフワッと香るメンズ神ハンドクリーム比較",
        "user_intent": "カサカサの手荒れやささくれは見苦しいが、ヌルヌルして作業の邪魔になるのが嫌な男子向け"
    },
    {
        "slug": "mens-hard-water-pomade-barber",
        "keyword": "ポマード 水性 メンズ バーバースタイル 水性ポマード",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#水性ポマード",
        "theme": "シャンプー1発オフでガチガチ固定！男の色気とツヤ感を爆上げするバーバー御用達水性ポマード比較",
        "user_intent": "油性ポマードやジェルでは洗髪が大変だが、崩れないホールド力とウェットな色気を出したい男子向け"
    },
    {
        "slug": "mens-mouthwash-breath-stain-remover",
        "keyword": "マウスウォッシュ 口臭 薬用 汚れが見える メンズ",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#マウスウォッシュ",
        "theme": "うがいでドロドロ汚れが目に見えて落ちる！口臭とネバつきを20秒でリセットする薬用マウスウォッシュ比較",
        "user_intent": "朝起きたときの口内のネバつきや、人と話す前の至近距離口臭を瞬時に一掃したい男子向け"
    },
    {
        "slug": "mens-ab-roller-wheel-rebound",
        "keyword": "腹筋ローラー アブローラー 膝マット アシスト 初心者",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#腹筋ローラー",
        "theme": "腰痛ゼロでチー牛腹をシックスパックへ！自動リバウンド機能付き超安定型腹筋ローラー徹底比較",
        "user_intent": "普通の腹筋運動ではお腹が割れず、腹筋ローラーは腰を痛めそうで怖い筋トレ初心者男子向け"
    },
    {
        "slug": "mens-point-hair-stick-ahoge-fixer",
        "keyword": "まとめ髪 スティック アホ毛 マスカラ メンズ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#アホ毛スティック",
        "theme": "トップのピョンピョン跳ねるアホ毛を一撫で抹消！清潔感のディテールを極めるポイントキープブラシ比較",
        "user_intent": "セット後に頭頂部や前髪から飛び出すピンピンした毛のせいで寝癖っぽく見えてしまうのを直したい男子向け"
    }
]

def search_rakuten_items(keyword, hits=4):
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "keyword": keyword,
        "format": "json",
        "hits": hits * 3
    }
    if AFFILIATE_ID:
        params["affiliateId"] = AFFILIATE_ID

    try:
        r = requests.get(url, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            raw_items = data.get("Items", [])
            items = []
            for it in raw_items:
                item = it.get("Item", it)
                name = item.get("itemName", "")
                clean_name = re.sub(r'【[^】]*】|\[[^\]]*\]|（[^）]*）|\([^\)]*\)', '', name)
                clean_name = re.sub(r'クーポン.*?OFF|ポイント.*?倍|送料無料|あす楽|即納|楽天.*?位|公式|正規品', '', clean_name).strip()
                words = [w for w in clean_name.split() if len(w) > 1]
                short_name = " ".join(words[:4]) if words else clean_name[:25]
                brand = words[0] if words else "注目ブランド"

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

                # 画像の生存確認（404・405・リンク切れを完全排除）
                try:
                    chk = requests.get(hi_img, stream=True, timeout=2.5)
                    if chk.status_code != 200:
                        continue
                except Exception:
                    continue

                price_val = item.get("itemPrice", 0)
                price_str = f"¥{price_val:,}" if price_val else "オープン価格"

                aff_url = item.get("affiliateUrl")
                if not aff_url and item.get("itemUrl"):
                    enc = urllib.parse.quote(item["itemUrl"], safe="")
                    aff_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={enc}&m={enc}" if AFFILIATE_ID else item["itemUrl"]

                items.append({
                    "itemName": short_name,
                    "brand": brand,
                    "itemPrice": price_str,
                    "itemUrl": aff_url or "https://item.rakuten.co.jp/",
                    "reviewAverage": item.get("reviewAverage", 4.4),
                    "reviewCount": item.get("reviewCount", random.randint(120, 890)),
                    "imageUrl": hi_img
                })
                if len(items) >= hits:
                    break
            return items
    except Exception as e:
        print(f"[ERR] Rakuten search exception: {e}")
    return []

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
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
        except Exception:
            time.sleep(1)
    return None

def generate_article_content(topic, items):
    item_summaries = []
    for idx, it in enumerate(items):
        item_summaries.append(f"商品{idx+1}: {it['itemName']} | 価格: {it['itemPrice']} | レビュー評価: {it['reviewAverage']} (件数: {it['reviewCount']})")
    item_context = "\n".join(item_summaries)

    prompt = f"""
あなたはZ世代・20代の垢抜けたい男子を熱血指導する「垢抜けコスメ塾 塾長」です。
読者は「自分はチー牛っぽい」「清潔感を出したいが何から始めればいいか分からない」と本気で悩んでいる男子です。

以下のテーマと商品情報をもとに、説得力抜群で熱く、読んだ瞬間に「今すぐ行動しないとヤバい！」と思わせる極上の比較記事本文を生成してください。

【厳格なルール】
1. AI臭い決まり文句（「いかがでしたでしょうか」「今回は〜をご紹介しました」「ぜひ参考にしてみてください」「いかがでしたか？」等）は絶対に禁止！
2. 語り口は「〜だ！」「〜ぜ！」「〜しろ！」「〜してくれ！」といった兄貴肌・塾長スタイルの熱血かつ実践的トーン。
3. 記事ごとに完全に独立した文章とし、他記事と同じ表現を使い回さないこと。
4. 4つの商品に対して、それぞれ以下の肌質・ターゲット4象限に割り当てて詳細なメリット・デメリット・おすすめ理由を執筆してください：
   - 「乾燥肌・敏感肌」（または「初心者・コスパ重視」）
   - 「脂性肌・オイリー」（または「即効性・ガチ勢」）
   - 「混合肌・初心者」（または「バランス型・万人受け」）
   - 「全肌質・高機能」（または「最高峰・プレミアム」）

【テーマ情報】
タイトル案: {topic['theme']}
ターゲット意図: {topic['user_intent']}
カテゴリー: {topic['category']}

【選定商品データ】
{item_context}

出力は以下のJSON形式のみ（余計なMarkdownフェンスや前置きは一切不要）で返してください：
{{
  "title": "{topic['theme']}",
  "excerpt": "読者の目を引く強烈なフックとなる100文字前後の要約（煽り・変身意欲・クリック誘導）",
  "intro": "読者の痛烈な悩みに共感し、なぜ今すぐこのケアが必要なのかを熱く語る導入文（400文字前後）",
  "targetAudience": "{topic['user_intent']}",
  "problemStatement": "この悩みを放置するとどういう残酷な現実が待っているかを容赦なく突きつける警告文（350文字前後）",
  "selectionCriteria": [
    "選び方の重要ポイント1（理由つき）",
    "選び方の重要ポイント2（理由つき）",
    "選び方の重要ポイント3（理由つき）"
  ],
  "productsAnalysis": [
    {{
      "targetSkin": "乾燥肌・敏感肌（または初心者・コスパ重視）",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "脂性肌・オイリー（または即効性・ガチ勢）",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "混合肌・初心者（またはバランス型・万人受け）",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "全肌質・高機能（または最高峰・プレミアム）",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }}
  ],
  "conclusion": "最後にお前たちの背中をドカンと押す熱血まとめ。今日からできる最初のアクションを明確に提示する（300文字前後）"
}}
"""
    raw_response = call_gemini(prompt)
    if not raw_response:
        return None
        
    try:
        clean_json = raw_response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"[ERR] JSON parse error: {e}")
        return None

def main():
    print("=== START GENERATING BATCH POSTS (Target: Expand to 130 articles) ===")
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    existing_slugs = set(p["slug"] for p in posts)
    print(f"Current posts: {len(posts)}")
    
    new_articles = []
    
    for idx, topic in enumerate(NEW_BATCH_TOPICS):
        slug = topic["slug"]
        if slug in existing_slugs:
            print(f"[{idx+1}/{len(NEW_BATCH_TOPICS)}] Skipping already existing slug: {slug}")
            continue
            
        print(f"\n[{idx+1}/{len(NEW_BATCH_TOPICS)}] Processing topic: {topic['keyword']} ({slug})...")
        items = search_rakuten_items(topic["keyword"])
        if len(items) < 4:
            print(f"  [WARN] Not enough live Rakuten items found ({len(items)}). Skipping.")
            continue
            
        print(f"  [OK] Found 4 verified Rakuten products with high-res images.")
        
        content = generate_article_content(topic, items)
        if not content:
            print("  [WARN] Gemini failed to generate valid content. Skipping.")
            continue
            
        comparison_table = []
        for i in range(4):
            analysis = content["productsAnalysis"][i] if i < len(content.get("productsAnalysis", [])) else {
                "targetSkin": "全タイプ",
                "feature": items[i]["itemName"],
                "pros": ["高機能", "コスパ良し"],
                "cons": ["継続が必要"]
            }
            comparison_table.append({
                "name": items[i]["itemName"],
                "brand": items[i]["brand"] or "注目ブランド",
                "category": topic["category"],
                "targetSkin": analysis.get("targetSkin", "おすすめ"),
                "feature": analysis.get("feature", "高品質なケアを実感できる注目アイテム。"),
                "price": items[i]["itemPrice"],
                "pros": analysis.get("pros", ["使いやすい", "清潔感UP"]),
                "cons": analysis.get("cons", ["継続が前提"]),
                "imageUrl": items[i]["imageUrl"],
                "affiliateUrl": items[i]["itemUrl"],
                "rating": items[i]["reviewAverage"],
                "reviewCount": items[i]["reviewCount"]
            })
            
        post_obj = {
            "slug": slug,
            "title": content.get("title", topic["theme"]),
            "excerpt": content.get("excerpt", topic["user_intent"]),
            "category": topic["category"],
            "categoryEn": topic["categoryEn"],
            "date": datetime.now().strftime("%Y.%m.%d"),
            "readTime": f"{random.randint(4, 6)} min read",
            "heroImage": items[0]["imageUrl"],
            "tags": [
                topic["tag"],
                "#チー牛脱却",
                "#メンズコスメ",
                "#清潔感"
            ],
            "intro": content.get("intro", ""),
            "targetAudience": content.get("targetAudience", topic["user_intent"]),
            "problemStatement": content.get("problemStatement", ""),
            "comparisonTable": comparison_table,
            "conclusion": content.get("conclusion", ""),
            "views": random.randint(1500, 3900)
        }
        
        new_articles.append(post_obj)
        print(f"  [SUCCESS] Generated: {post_obj['title'][:40]}...")
        time.sleep(2)
        
    if new_articles:
        print(f"\nAdding {len(new_articles)} new high-converting articles to {DATA_FILE}...")
        updated_posts = new_articles + [p for p in posts if p["slug"] not in set(a["slug"] for a in new_articles)]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_posts, f, ensure_ascii=False, indent=2)
        print(f"Updated {DATA_FILE}! New total: {len(updated_posts)} articles.")
    else:
        print("No new articles generated.")

if __name__ == "__main__":
    main()
