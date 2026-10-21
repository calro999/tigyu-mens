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
APP_ID = env.get("RAKUTEN_APP_ID") or os.environ.get("RAKUTEN_APP_ID")
ACCESS_KEY = env.get("RAKUTEN_ACCESS_KEY") or os.environ.get("RAKUTEN_ACCESS_KEY")
AFFILIATE_ID = env.get("RAKUTEN_AFFILIATE_ID") or os.environ.get("RAKUTEN_AFFILIATE_ID")
GEMINI_KEY = env.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

DATA_FILE = "data/posts.json"
CACHE_FILE = "posted_cache.txt"

# SEO的に強いキーワードスラッグを定義
CANDIDATE_TOPICS = [
    {
        "keyword": "メンズ オールインワン ジェル 保湿",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-all-in-one-gel-recommend",
        "tag": "#オールインワン",
        "theme": "朝の支度30秒！乾燥とテカリを同時に防ぐメンズオールインワン傑作選"
    },
    {
        "keyword": "メンズ 洗顔料 毛穴 泥 泡",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-pore-face-wash-ranking",
        "tag": "#洗顔料",
        "theme": "毛穴の黒ずみ・イチゴ鼻を撲滅！泥洗顔＆濃密泡メンズ洗顔料比較"
    },
    {
        "keyword": "メンズ コンシーラー スティック クマ 青髭",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-beard-concealer-stick",
        "tag": "#青髭",
        "theme": "バレずに青髭・目の下のクマを完全消去！メンズスティックコンシーラー検証"
    },
    {
        "keyword": "メンズ 眉毛 アイブロウ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-eyebrow-pencil-trimmer",
        "tag": "#眉毛",
        "theme": "眉毛ボサボサは一発で足切り！失敗しないセルフアイブロウ＆トリマー比較"
    },
    {
        "keyword": "メンズ ヘアワックス ハード マット 束感",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-hair-wax-matte-hard",
        "tag": "#ワックス",
        "theme": "ノーセットのペタ髪を脱出！一日中キープできるメンズワックス＆グリース比較"
    },
    {
        "keyword": "メンズ スカルプシャンプー 薬用 頭皮",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-scalp-shampoo-care",
        "tag": "#頭皮ケア",
        "theme": "頭皮の脂ギッシュ＆抜け毛予防！今から始めるメンズスカルプシャンプー厳選"
    },
    {
        "keyword": "メンズ デオドラント ロールオン 制汗剤",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-deodorant-roll-on-block",
        "tag": "#制汗剤",
        "theme": "男のワキ汗＆すれ違いのニオイを1日完全ブロックするメンズデオドラント比較"
    },
    {
        "keyword": "メンズ 香水 練り香水 シトラス ソープ 清潔感",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-solid-perfume-clean-soap",
        "tag": "#フレグランス",
        "theme": "香水臭い男は嫌われる！「お風呂上がりの石鹸」香るメンズ練り香水比較"
    },
    {
        "keyword": "メンズ フォームローラー 姿勢 矯正 ストレッチ",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-posture-foam-roller",
        "tag": "#猫背改善",
        "theme": "チー牛姿勢・巻き肩を自宅で破壊！姿勢矯正＆筋膜リリースローラー比較"
    },
    {
        "keyword": "メンズ アブローラー 腹筋 筋トレ 自宅",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-ab-roller-core-workout",
        "tag": "#自重トレ",
        "theme": "だらしないぽっこり腹を割る！自宅1日3分で効くメンズ腹筋ローラー比較"
    }
]

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def append_cache(theme):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{theme}\n")

def search_rakuten_items(keyword, hits=4):
    if not APP_ID or not ACCESS_KEY:
        print("[WARN] RAKUTEN_APP_ID or RAKUTEN_ACCESS_KEY not set.")
        return []

    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "keyword": keyword,
        "format": "json",
        "hits": hits * 2
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

                img = re.sub(r'\?_ex=[0-9]+x[0-9]+', '?_ex=600x600', img)

                price_val = item.get("itemPrice", 0)
                price_str = f"¥{price_val:,}" if price_val else "オープン価格"

                aff_url = item.get("affiliateUrl")
                if not aff_url and item.get("itemUrl"):
                    import urllib.parse
                    enc = urllib.parse.quote(item["itemUrl"], safe="")
                    aff_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={enc}&m={enc}" if AFFILIATE_ID else item["itemUrl"]

                items.append({
                    "name": short_name,
                    "brand": brand,
                    "price": price_str,
                    "imageUrl": img,
                    "affiliateUrl": aff_url or "https://item.rakuten.co.jp/",
                    "rawCaption": item.get("itemCaption", "")[:120]
                })
                if len(items) >= hits:
                    break
            return items
    except Exception as e:
        print(f"Error fetching Rakuten: {e}")
    return []

def call_gemini(prompt, system_message):
    models = ["gemini-2.5-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash"]
    for m in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_message}\n\n{prompt}"}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 3000}
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                cand = data.get("candidates", [])
                if cand:
                    parts = cand[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception as e:
            print(f"Model {m} failed: {e}")
            continue
    return None

def auto_generate_one():
    existing_posts = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    existing_slugs = set(p.get("slug") for p in existing_posts)
    cache = load_cache()
    available = [t for t in CANDIDATE_TOPICS if t["theme"] not in cache and t.get("slug") not in existing_slugs]
    if not available:
        available = CANDIDATE_TOPICS

    topic_info = random.choice(available)
    print(f"Target Theme: {topic_info['theme']}")

    products_raw = search_rakuten_items(topic_info["keyword"], hits=4)
    if not products_raw or len(products_raw) == 0:
        print("[WARN] No products retrieved from Rakuten. Aborting.")
        return

    hero_img = products_raw[0]["imageUrl"]

    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    comparisons = []
    for i, p in enumerate(products_raw):
        st = skin_types[i % len(skin_types)]
        comparisons.append({
            "name": p["name"],
            "brand": p["brand"],
            "category": topic_info["category"],
            "targetSkin": st,
            "feature": f"{st}の悩みに特化した処方。ベタつかず毎日の習慣に無理なく取り入れられる清潔感アップ設計。",
            "price": p["price"],
            "pros": ["肌なじみが良い", "清潔感UP", "コスパ良好"],
            "cons": ["香りの好みが分かれる場合あり"],
            "imageUrl": p["imageUrl"],
            "affiliateUrl": p["affiliateUrl"],
            "rating": round(random.uniform(4.2, 4.8), 1),
            "reviewCount": random.randint(120, 1500)
        })

    sys_msg = """
あなたは「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の塾長です。
対象読者は、今まで身だしなみに無頓着で、陰キャ・チー牛と見なされがちだったZ世代の男性です。
上から目線の説教ではなく、論理的で親しみやすい「講座・ロードマップ」として、具体的かつ確実に効果が出るアドバイスを行います。
AI特有の不自然な言い回し（「いかがでしたでしょうか」「〜と言えるでしょう」等）は一切使わず、熱量のあるリアルな日本語で執筆してください。
返答は以下のJSON形式のみで出力してください：
{
  "title": "記事タイトル（32〜45文字程度でクリックしたくなる魅力的なもの）",
  "excerpt": "要約文（70〜90文字程度）",
  "intro": "導入文（なぜ今このアイテムが必要なのか、現状放置するとどう足切りされるのか、150〜200文字）",
  "problemStatement": "読者のリアルな悩み・課題の言語化（200文字程度）",
  "conclusion": "まとめ・背中を押すメッセージ（150文字程度）"
}
"""
    prompt = f"""
テーマ: {topic_info['theme']}
カテゴリ: {topic_info['category']}
選抜アイテム数: {len(comparisons)}点
JSONフォーマットで出力してください。
"""
    ai_res = call_gemini(prompt, sys_msg)
    data = {}
    if ai_res:
        cleaned = re.sub(r'```(?:json)?', '', ai_res).strip()
        try:
            data = json.loads(cleaned)
        except Exception as e:
            print("JSON parse error:", e)

    # SEOクリーンなスラッグ
    base_slug = topic_info.get("slug") or f"mens-{topic_info['categoryEn']}-guide"
    slug = base_slug
    if slug in existing_slugs:
        slug = f"{base_slug}-{int(time.time())}"

    now_str = datetime.now().strftime("%Y.%m.%d")

    new_post = {
        "slug": slug,
        "title": data.get("title", topic_info["theme"]),
        "excerpt": data.get("excerpt", "清潔感を手に入れてチー牛を脱却するための徹底比較ガイド。肌質別の最適アイテムと選び方を解説。"),
        "category": topic_info["category"],
        "categoryEn": topic_info["categoryEn"],
        "date": now_str,
        "readTime": f"{random.randint(3, 5)} min read",
        "heroImage": hero_img,
        "tags": [topic_info["tag"], "#チー牛脱却", "#メンズコスメ", "#清潔感"],
        "intro": data.get("intro", "身だしなみへの投資は、最もリターンの高い自己投資です。放置すれば第一印象で足切りされるリスクを、毎日の簡単ケアでゼロにしましょう。"),
        "targetAudience": "垢抜けて清潔感を手に入れたいZ世代男性",
        "problemStatement": data.get("problemStatement", "肌荒れ、青髭、髪型の崩れなど、どこから手をつければいいか分からない。ドラッグストアで迷ってしまうあなたのために、肌質別の最適解を比較しました。"),
        "comparisonTable": comparisons,
        "conclusion": data.get("conclusion", "完璧を目指さず、まずは自分に合う1本を試すことからスタートしましょう。行動したその日から印象は劇的に変わり始めます。"),
        "views": random.randint(1000, 3500)
    }

    updated_posts = [new_post] + existing_posts[:49]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_posts, f, ensure_ascii=False, indent=2)

    append_cache(topic_info["theme"])
    print(f"[SUCCESS] Added new post: {new_post['title']} (slug: {new_post['slug']}) with SEO slug & Rakuten images.")

if __name__ == "__main__":
    auto_generate_one()
