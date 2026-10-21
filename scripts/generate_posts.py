import os
import sys
import requests
import json
import re
import random
import time
from datetime import datetime

# Load .env
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

CATEGORIES = [
    {"name": "スキンケア・洗顔", "en": "SKINCARE", "tag": "#スキンケア"},
    {"name": "ヘア・眉毛セット", "en": "HAIR & BROWS", "tag": "#ヘア眉毛"},
    {"name": "ボディ・姿勢改善", "en": "BODY & POSTURE", "tag": "#ボディメイク"},
    {"name": "ニオイ・体臭対策", "en": "CLEANLINESS", "tag": "#ニオイ対策"},
]

ARTICLE_TOPICS = [
    {
        "keyword": "メンズ オールインワン ジェル 保湿",
        "category": "スキンケア・洗顔",
        "categoryEn": "SKINCARE",
        "tag": "#スキンケア",
        "theme": "もう化粧水選びで迷わない！乾燥肌・脂性肌別の最強オールインワン比較",
        "heroImage": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?q=80&w=800&auto=format&fit=crop"
    },
    {
        "keyword": "メンズ コンシーラー 青髭 クマ",
        "category": "スキンケア・洗顔",
        "categoryEn": "SKINCARE",
        "tag": "#青髭",
        "theme": "青髭・夕方の泥棒ヒゲをゼロにする！肌色別の最強メンズコンシーラー厳選",
        "heroImage": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=800&auto=format&fit=crop"
    },
    {
        "keyword": "メンズ 眉毛 アイブロウ ペンシル キット",
        "category": "ヘア・眉毛セット",
        "categoryEn": "HAIR & BROWS",
        "tag": "#眉毛",
        "theme": "ボサボサ眉毛は今すぐ卒業！清潔感2倍のセルフ眉毛セット＆ツール徹底比較",
        "heroImage": "https://images.unsplash.com/photo-1592647420148-faccb4ce0d1e?q=80&w=800&auto=format&fit=crop"
    },
    {
        "keyword": "メンズ ヘアワックス ハード マット 束感",
        "category": "ヘア・眉毛セット",
        "categoryEn": "HAIR & BROWS",
        "tag": "#ヘアセット",
        "theme": "ノーセット髪は足切り対象！朝5分で決まる髪質別メンズワックス徹底解説",
        "heroImage": "https://images.unsplash.com/photo-1593702275687-f8b402bf1fb5?q=80&w=800&auto=format&fit=crop"
    },
    {
        "keyword": "メンズ デオドラント ロールオン 制汗剤",
        "category": "ニオイ・体臭対策",
        "categoryEn": "CLEANLINESS",
        "tag": "#体臭",
        "theme": "「無臭の男」こそ最強の清潔感！男のワキ汗・汗臭を元から断つ制汗剤比較",
        "heroImage": "https://images.unsplash.com/photo-1621607512214-68297480165e?q=80&w=800&auto=format&fit=crop"
    },
    {
        "keyword": "メンズ フォームローラー 姿勢 矯正 ストレッチ",
        "category": "ボディ・姿勢改善",
        "categoryEn": "BODY & POSTURE",
        "tag": "#自重トレ",
        "theme": "猫背・巻き肩チー牛を即座に直す！姿勢改善＆自重トレ名品ギア比較",
        "heroImage": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=800&auto=format&fit=crop"
    }
]

def search_rakuten_items(keyword, hits=4):
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
                if img:
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

def build_post(topic_info, index):
    print(f"Generating post for: {topic_info['theme']}")
    products_raw = search_rakuten_items(topic_info["keyword"], hits=4)
    
    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    
    comparisons = []
    for i, p in enumerate(products_raw):
        st = skin_types[i % len(skin_types)]
        comparisons.append({
            "name": p["name"],
            "brand": p["brand"],
            "category": topic_info["category"],
            "targetSkin": st,
            "feature": f"{st}の悩みに特化した設計。伸びが良く、ベタつきのない使用感で毎日のケアに馴染みやすい注目アイテム。",
            "price": p["price"],
            "pros": ["肌なじみが良い", "清潔感UP", "コスパ良好"],
            "cons": ["香りの好みが分かれる場合あり"],
            "imageUrl": p["imageUrl"],
            "affiliateUrl": p["affiliateUrl"],
            "rating": round(random.uniform(4.2, 4.8), 1),
            "reviewCount": random.randint(120, 1500)
        })

    # AIに記事本文（Z世代に刺さるチー牛脱却コスメ塾トーン）を書かせる
    sys_msg = """
あなたは「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の塾長です。
対象読者は、今まで身だしなみに無頓着で、陰キャ・チー牛と見なされがちだったZ世代の男性です。
上から目線の説教ではなく、論理的で親しみやすい「講座・ロードマップ」として、具体的かつ確実に効果が出るアドバイスを行います。
AI特有の不自然な言い回し（「いかがでしたでしょうか」「〜と言えるでしょう」等）は一切使わず、熱量のあるリアルな日本語で執筆してください。
返答は以下のJSON形式のみで出力してください（Markdownの```jsonなどの囲みは付けないか、純粋なJSONで返してください）：
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
上記のテーマで記事本文の構成をJSONで作成してください。
"""

    ai_res = call_gemini(prompt, sys_msg)
    data = {}
    if ai_res:
        cleaned = re.sub(r'```(?:json)?', '', ai_res).strip()
        try:
            data = json.loads(cleaned)
        except Exception as e:
            print("JSON parse error:", e)
    
    slug = f"post-{index+1}-{topic_info['categoryEn'].lower().replace(' ', '-')}"
    now_str = datetime.now().strftime("%Y.%m.%d")
    
    post = {
        "slug": slug,
        "title": data.get("title", topic_info["theme"]),
        "excerpt": data.get("excerpt", "清潔感を手に入れてチー牛を脱却するための徹底比較ガイド。肌質別の最適アイテムと選び方を解説。"),
        "category": topic_info["category"],
        "categoryEn": topic_info["categoryEn"],
        "date": now_str,
        "readTime": f"{random.randint(3, 6)} min read",
        "heroImage": topic_info["heroImage"],
        "tags": [topic_info["tag"], "#チー牛脱却", "#メンズコスメ", "#清潔感"],
        "intro": data.get("intro", "「スキンケアなんて女がやるもの」と思っていませんか？男性の肌は女性よりも皮脂が多く水分が少ないため、放置するとテカリと毛穴の黒ずみで一気に老け見えします。まずは基本を押さえましょう。"),
        "targetAudience": "スキンケアや身だしなみを何から始めればいいか分からない高校生〜20代男性",
        "problemStatement": data.get("problemStatement", "夕方になると顔がギトギトになる、あるいは冬になると粉を吹く。ドラッグストアに行っても何を選べばいいか分からない。そんな悩みを解決するために、乾燥肌向け・オイリー肌向けを厳選しました。"),
        "comparisonTable": comparisons,
        "conclusion": data.get("conclusion", "身だしなみへの投資は、見た目だけでなく自信を劇的に変えてくれます。まずは自分の肌質に合った1本を手に入れて、明日の朝から実践してみてください。"),
        "views": random.randint(1200, 4800)
    }
    return post

def main():
    existing_posts = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_posts = json.load(f)
        except Exception:
            existing_posts = []

    # 初回、またはトピック全件を生成
    posts = []
    for i, topic in enumerate(ARTICLE_TOPICS):
        p = build_post(topic, i)
        posts.append(p)
        time.sleep(1)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {len(posts)} posts into {DATA_FILE}")

if __name__ == "__main__":
    main()
