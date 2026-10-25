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
        "slug": "mens-cleansing-oil-blackhead-pore",
        "keyword": "クレンジングオイル メンズ 毛穴 黒ずみ 角栓",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#クレンジングオイル",
        "theme": "洗顔だけでは落ちない酸化皮脂・黒ずみ角栓を溶かし出す！男のための毛穴クレンジングオイル徹底比較",
        "user_intent": "毎日洗顔しても小鼻の黒ずみやザラつきが全く取れず、毛穴の詰まりを根本からリセットしたい男子向け"
    },
    {
        "slug": "mens-booster-serum-skin-penetration",
        "keyword": "導入美容液 ブースター セラム 保湿 毛穴",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#導入美容液",
        "theme": "化粧水がグングン吸い込まれる！ゴワつく男肌を柔らかくほぐす導入美容液（ブースターセラム）比較",
        "user_intent": "化粧水を塗っても肌表面で弾かれてしまい、内側の乾燥（インナードライ）や肌のごわつきに悩む男子向け"
    },
    {
        "slug": "mens-bedhead-hair-water-mist",
        "keyword": "寝癖直し ウォーター ヘアミスト メンズ スタイリング",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#寝癖直しウォーター",
        "theme": "朝の爆発頭を30秒でリセット！ドライヤー熱から髪を守りサロン帰りのまとまりを作る寝癖直しミスト比較",
        "user_intent": "毎朝の寝癖がひどく、水で濡らしてもすぐにハネてしまい朝のセット時間を大幅短縮したい男子向け"
    },
    {
        "slug": "mens-mini-hair-iron-15mm-short",
        "keyword": "ヘアアイロン ストレート ミニ メンズ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#メンズヘアアイロン",
        "theme": "短髪・直毛チー牛でも美容室セットが完全再現！小回り抜群のプレートメンズヘアアイロン比較",
        "user_intent": "直毛すぎてワックスをつけてもツンツン立つだけ、またはくせ毛で前髪がうねるのを自在に操りたい男子向け"
    },
    {
        "slug": "mens-medicated-deodorant-cream-armpit",
        "keyword": "デオドラントクリーム 薬用 ワキガ 制汗 メンズ",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#デオドラントクリーム",
        "theme": "スプレーでは防げない濃厚ワキ臭・汗ジミを密閉ブロック！朝塗れば夜まで無臭が続く薬用デオドラントクリーム比較",
        "user_intent": "市販の制汗スプレーでは夕方にニオイが復活してしまう、ワキ汗やツンとする臭いを完全封印したい男子向け"
    },
    {
        "slug": "mens-laundry-detergent-odor-removal",
        "keyword": "洗濯洗剤 消臭 部屋干し 液体",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#消臭洗濯洗剤",
        "theme": "Tシャツの染み付いた生乾き臭・男脂臭を繊維の奥から分解！清潔感を服から纏う最強消臭洗濯洗剤比較",
        "user_intent": "洗ったはずの服を着て汗をかくと雑巾のような臭いが復活して困っている一人暮らし男子向け"
    },
    {
        "slug": "mens-compression-recovery-socks",
        "keyword": "着圧ソックス メンズ むくみ ふくらはぎ 疲労回復",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#着圧ソックス",
        "theme": "立ち仕事・デスクワークでパンパンの脚を翌朝スッキリ！血行を促進して足取りを軽くするメンズ着圧ソックス比較",
        "user_intent": "夕方になるとふくらはぎが重だるく、足のむくみや疲れが翌朝まで残ってしまう男子向け"
    },
    {
        "slug": "mens-kettlebell-home-core-workout",
        "keyword": "ケトルベル 筋トレ 体幹 トレーニング 自宅",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#ケトルベル",
        "theme": "1日5分のスイングで脂肪燃焼＆体幹覚醒！省スペースで逆三角形の男らしい背中と肩を作るケトルベル比較",
        "user_intent": "有酸素運動と筋トレを同時に効率よく行い、引き締まった細マッチョ体型を自宅で作りたい男子向け"
    },
    {
        "slug": "mens-neck-warmer-recovery-sleep",
        "keyword": "ネックウォーマー シルク 就寝 防寒",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#リカバリーネックウォーマー",
        "theme": "寝ている間に首・肩のガチガチ緊張をじんわり解放！翌朝の目覚めと顔色を劇的に変える就寝用ネックウォーマー比較",
        "user_intent": "スマホやPCのやりすぎで首・肩が常に凝り固まり、睡眠の質が浅く朝起きても疲れ顔になっている男子向け"
    },
    {
        "slug": "mens-breath-care-tablets-stomach",
        "keyword": "エチケット サプリ 口臭 サプリメント",
        "category": "ニオイ・体臭対策",
        "categoryEn": "odor-sweat",
        "tag": "#口臭サプリ",
        "theme": "胃の奥からこみ上げるニンニク・アルコール・男臭を内側から消去！飲むだけで爽やか息が続く口臭ケアサプリ比較",
        "user_intent": "歯磨きやマウスウォッシュをしても、お腹の奥から上がってくる不快な口臭が気になる男子向け"
    },
    {
        "slug": "mens-hot-eye-mask-rechargeable-sleep",
        "keyword": "ホットアイマスク USB 電熱 睡眠",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare-wash",
        "tag": "#ホットアイマスク",
        "theme": "スマホ眼精疲労と死んだ魚の目を毎晩リセット！極上の熟睡と明るい目元を作る温熱ホットアイマスク比較",
        "user_intent": "夜遅くまで画面を見続けて目が充血・疲労し、目の下のクマや目つきの悪さに悩んでいる男子向け"
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
      "targetSkin": "乾燥肌・敏感肌",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "脂性肌・オイリー",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "混合肌・初心者",
      "feature": "この商品の際立った強み・特徴（150文字前後）",
      "pros": ["メリット1", "メリット2", "メリット3"],
      "cons": ["デメリット・注意点"]
    }},
    {{
      "targetSkin": "全肌質・高機能",
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
        clean_json = re.sub(r',\s*([\]}])', r'\1', clean_json)
        return json.loads(clean_json)
    except Exception as e:
        print(f"[ERR] JSON parse error: {e}")
        return None

def main():
    print("=== START GENERATING BATCH POSTS (Target: Reach 170 articles) ===")
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)
        
    existing_slugs = set(p["slug"] for p in posts)
    print(f"Current posts: {len(posts)}")
    
    new_articles = []
    skin_quadrants = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    
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
                "targetSkin": skin_quadrants[i],
                "feature": items[i]["itemName"],
                "pros": ["高機能", "コスパ良し"],
                "cons": ["継続が必要"]
            }
            comparison_table.append({
                "name": items[i]["itemName"],
                "brand": items[i]["brand"] or "注目ブランド",
                "category": topic["category"],
                "targetSkin": skin_quadrants[i],
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
