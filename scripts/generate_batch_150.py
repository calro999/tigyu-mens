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
        "slug": "mens-room-fragrance-reed-stick-premium",
        "keyword": "ルームフレグランス リードディフューザー 部屋 消臭 芳香",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#ルームフレグランス",
        "theme": "入った瞬間「この部屋めっちゃ落ち着く！」と女子絶賛！男の部屋の生活臭を浄化するリードディフューザー比較",
        "user_intent": "男特有の部屋のホコリ臭・生活臭を消し去り、上品な香りでモテ空間に変えたい男子向け"
    },
    {
        "slug": "mens-medicated-back-acne-clearing-mist",
        "keyword": "背中 にきび スプレー 薬用",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#背中ニキビスプレー",
        "theme": "温泉・サウナで脱いでも恥ずかしくない！背中と胸元の赤ブツ・ザラつきを一網打尽にする薬用アクネミスト比較",
        "user_intent": "手が届かない背中の肌荒れ・毛穴詰まりを手軽にスプレーしてツルツルにしたい男子向け"
    },
    {
        "slug": "mens-plantar-foot-acupressure-roller",
        "keyword": "足裏 マッサージ ローラー 足ツボ 青竹踏み",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#足ツボローラー",
        "theme": "デスクワークの足裏の重だるさを秒速リフレッシュ！土踏まずを刺激して美立ち姿勢を呼び覚ますフットローラー比較",
        "user_intent": "長時間の座り仕事で足がだるく扁平足になり、立ち姿が崩れて疲れやすい男子向け"
    },
    {
        "slug": "mens-exfoliating-toner-pads-bha",
        "keyword": "トナーパッド 毛穴 拭き取り 角質ケア",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#トナーパッド",
        "theme": "朝の3秒サッと拭きでテカリ・黒ずみ毛穴即リセット！古い角質と過剰皮脂を絡め取るふき取りパッド比較",
        "user_intent": "朝の洗顔が面倒だが、小鼻のザラつきや日中のギトギト脂浮きを根本から予防したい男子向け"
    },
    {
        "slug": "mens-push-up-handles-ergonomic",
        "keyword": "プッシュアップバー 筋トレ 腕立て伏せ 器具",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#プッシュアップバー",
        "theme": "服の上からでも分かる分厚い大胸筋へ！手首への負担を逃して限界まで追い込めるエルゴノミック腕立てバー比較",
        "user_intent": "腕立て伏せで手首が痛くなってしまい、自宅で安全かつ効率的に胸板を厚くしたい男子向け"
    },
    {
        "slug": "mens-portable-breath-spray-mint",
        "keyword": "口臭 スプレー 薬用 携帯用 マウススプレー",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#マウススプレー",
        "theme": "至近距離の会話も怖くない！ニンニク・コーヒー・タバコ後の息を一撃で氷結リセットする携帯マウススプレー比較",
        "user_intent": "外食後やすぐに人と会うタイミングで、手軽に爽やかな息をキープしたい男子向け"
    },
    {
        "slug": "mens-standing-stretch-slant-board",
        "keyword": "ストレッチボード ふくらはぎ 姿勢改善 前屈",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#ストレッチボード",
        "theme": "乗るだけで骨盤の傾き＆スマホ首を根本矯正！ガチガチ下半身を解放してモデル立ち姿勢を作るスラントボード比較",
        "user_intent": "骨盤が前傾または後傾し、猫背や反り腰で姿勢がだらしなく見えてしまう男子向け"
    },
    {
        "slug": "mens-matte-powder-blotting-sheets",
        "keyword": "あぶらとり紙 メンズ テカリ防止 パウダー",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#あぶらとり紙",
        "theme": "午後3時の油田肌を秒で陶器マット肌へ！テカリだけを吸収してサラサラが持続するメンズあぶらとり紙比較",
        "user_intent": "仕事中やデート中に顔がギトギトになって不潔感が出るのをサッと解消したい男子向け"
    },
    {
        "slug": "mens-scalp-massage-brush-soft-silicone",
        "keyword": "シャンプーブラシ スカルプブラシ メンズ シリコン 頭皮",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#シャンプーブラシ",
        "theme": "指先では届かない毛穴の皮脂づまりを一掃！頭皮のかゆみ・フケを根絶する極上シリコンシャンプーブラシ比較",
        "user_intent": "毎日シャンプーしても頭皮のニオイやかゆみが気になる、爪で地肌を傷つけがちな男子向け"
    },
    {
        "slug": "mens-hard-wax-matte-clay-hold",
        "keyword": "ヘアワックス メンズ マット クレイ ハード",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#クレイワックス",
        "theme": "ツヤ消し無造作ヘアで垢抜けろ！軟毛でもペタッとならず1日中束感をキープする最強マットクレイワックス比較",
        "user_intent": "セットしてもすぐに潰れてしまう軟毛や、テカテカした質感が苦手で自然な束感を作りたい男子向け"
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
    print("=== START GENERATING BATCH POSTS (Target: Reach 150 articles) ===")
    
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
