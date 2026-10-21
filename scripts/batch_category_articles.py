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

# カテゴリーごとの充実した独自企画トピック（AI臭さを徹底排除したリアルな男性の悩み解決）
BATCH_TOPICS = [
    # --- スキンケア・洗顔 ---
    {
        "keyword": "メンズ 泥洗顔 毛穴 クレイ 洗顔料",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-clay-face-wash-pores",
        "tag": "#泥洗顔",
        "theme": "水洗顔で顔がヌルついてる奴集合。頑固な毛穴黒ずみをゴッソリ溶かす「男の泥洗顔」徹底比較",
        "targetAudience": "鼻の頭の黒ずみ・夕方のギトつきに本気で悩む20代男性",
        "intro_theme": "「男だからテカるのは仕方ない」と放置してたら、周りからは『脂ぎってて清潔感がない』と裏で足切りされてるぞ。皮脂腺が多い男こそ、泡立てネットで作る泥洗顔で毛穴の奥からアブラを根こそぎリセットしろ。"
    },
    {
        "keyword": "メンズ シートマスク フェイスパック 保湿 大容量",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-sheet-mask-hydration",
        "tag": "#シートマスク",
        "theme": "週2回貼るだけで肌治安が爆上がり！カサつき・くすみを即効リセットするメンズフェイスマスク比較",
        "targetAudience": "乾燥で粉を吹くのにTゾーンがテカるインナードライに苦しむ男子",
        "intro_theme": "化粧水をパシャパシャつけるだけで満足してないか？肌の水分量が底をついてるから、身体が焦って過剰な皮脂を出してテカってるんだ。シートマスクで10分水分をぶち込めば、翌朝鏡を見た瞬間『肌が発光してる』感覚がガチで分かる。"
    },
    {
        "keyword": "メンズ リップクリーム 色つき 保湿 荒れ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-tinted-lip-balm-natural",
        "tag": "#リップケア",
        "theme": "ガサガサ唇・血色ゼロで損してないか？自然に血色感を足せるメンズ色つきリップ徹底検証",
        "targetAudience": "唇の皮がむけて紫っぽく不健康に見られがちな男性",
        "intro_theme": "唇がガサガサに乾いて白い皮が浮いてる男は、どれだけ髪をセットしても清潔感ゼロ認定される。かといって女子用の口紅は浮く。男の肌色に溶け込んで『元から健康的な血色』を偽装できるメンズ専用リップを持っておけ。"
    },

    # --- ヘア・眉毛セット ---
    {
        "keyword": "メンズ スカルプシャンプー アミノ酸 薬用 フケ かゆみ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-scalp-shampoo-amino-acid",
        "tag": "#スカルプシャンプー",
        "theme": "肩にフケが落ちてる男は一発アウト！頭皮の脂・ニオイ・痒みを鎮火する薬用スカルプシャンプー比較",
        "targetAudience": "夕方になると頭皮が脂っぽくフケや痒みが気になる男子",
        "intro_theme": "洗浄力が強すぎる市販シャンプーで頭皮をガシガシ洗ってないか？皮脂を根こそぎ奪われて頭皮が悲鳴を上げ、フケと強烈な脂臭を撒き散らす最悪の悪循環になる。アミノ酸系マイルド洗浄で頭皮環境を立て直せ。"
    },
    {
        "keyword": "メンズ ポマード グリース バーバー ツヤ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-pomade-grease-barber",
        "tag": "#ポマード",
        "theme": "ワックスで束感作るのはもう古い？濡れツヤと清潔感を両立する大人のメンズ水性ポマード比較",
        "targetAudience": "パサついた髪で清潔感が出ない、センターパートをキリッと決めたい男性",
        "intro_theme": "マットワックスでパサパサになった髪は、光が当たらずボサボサに見えやすい。水性ポマード（グリース）なら、適度な濡れツヤ感で男らしい色気と清潔感が同時に手に入る。お湯でサッと落ちるのもストレスゼロだ。"
    },
    {
        "keyword": "メンズ 眉毛シェーバー 電動 コーム トリマー",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-electric-eyebrow-shaver",
        "tag": "#眉毛シェーバー",
        "theme": "カミソリで眉毛をえぐった過去の俺へ。失敗知らずで清潔感を作る電動アイブロウシェーバー比較",
        "targetAudience": "不器用で眉毛の手入れが怖くて放置している高校生・大学生",
        "intro_theme": "普通のT字カミソリやハサミで眉毛を触って、剃りすぎてヤンキー眉になった経験はないか？長さ調節コームがついたメンズ専用電動シェーバーなら、眉の上をスーッと滑らせるだけでミリ単位で均一に整う。"
    },

    # --- ニオイ・体臭対策 ---
    {
        "keyword": "メンズ 薬用ボディソープ デオドラント 加齢臭 汗臭 殺菌",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-medicated-body-wash-odor",
        "tag": "#ボディソープ",
        "theme": "「自分は臭くない」と思ってる奴が一番ヤバい。男の汗臭・酸化アブラ臭を根絶する薬用ボディソープ比較",
        "targetAudience": "汗をかきやすく、服を脱いだ時にモワッとする臭いが気になる男性",
        "intro_theme": "普通のいい匂いのボディソープで洗っても、皮膚の常在菌がアブラを分解して数時間後には激臭に変わる。ニオイの発生源を潰すには『殺菌有効成分』が入った薬用ソープ一択だ。すれ違いざまの印象が180度変わる。"
    },
    {
        "keyword": "メンズ 練り香水 ソリッドパフューム サボン ムスク",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-solid-perfume-soap-scent",
        "tag": "#練り香水",
        "theme": "香水をシュッシュして女子にドン引きされた過去を消せ！至近距離で「いい匂い」と思われるメンズ練り香水比較",
        "targetAudience": "香水のキツい匂いが苦手だけど、ほんのり清潔感ある香りを纏いたい男子",
        "intro_theme": "安物の香水を首元に吹きかけると、満員電車やエレベーターで周囲が息を止める大惨事になる。男の正解は『練り香水』だ。アルコール臭ゼロで、耳の後ろや手首にサッと塗るだけで『風呂上がりの石鹸の香り』を偽装できる。"
    },
    {
        "keyword": "メンズ マウスウォッシュ 口臭ケア 口内洗浄 殺菌",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-mouthwash-breath-care",
        "tag": "#口臭ケア",
        "theme": "至近距離の会話で相手が一瞬引いたことないか？マスクを外した瞬間の口臭を完全ブロックする薬用マウスウォッシュ比較",
        "targetAudience": "朝起きたときのネバつきや、人と話すときの息が不安な男性",
        "intro_theme": "歯磨きだけでは口の中の汚れの25%しか落とせてないという残酷な事実を知ってるか？舌苔や粘膜に残った雑菌が、話すたびにドブのような臭いを放つ。外出前と就寝前の30秒クチュクチュうがいで、息を無敵にしろ。"
    },

    # --- ボディ・姿勢改善 ---
    {
        "keyword": "メンズ 姿勢サポーター 猫背 矯正ベルト",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-posture-corrector-belt",
        "tag": "#姿勢サポーター",
        "theme": "服を着てもチー牛オーラが消えない原因は「巻き肩」だ。装着するだけで胸が張れる姿勢補正サポーター比較",
        "targetAudience": "PC・スマホの見すぎで背中が丸まり、なで肩・首が前に突き出ている男子",
        "intro_theme": "ハイブランドの服を着ても、猫背で首が亀のように前に出ていたら全部台無し。肩甲骨を引き寄せて自然に胸が開くだけで、堂々とした頼もしいシルエットが生まれる。デスクワーク中につけるだけで矯正できるギアを紹介する。"
    },
    {
        "keyword": "メンズ プッシュアップバー 腕立て伏せ 大胸筋 自宅",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-push-up-bars-chest",
        "tag": "#大胸筋トレ",
        "theme": "Tシャツ1枚でかっこいい男になる！自宅腕立てで分厚い胸板を作る最強プッシュアップバー比較",
        "targetAudience": "ガリガリ体型で服に着られている感がある、または胸がペタッとしている男性",
        "intro_theme": "床に手をついてペコペコ腕立てしても手首が痛いだけで大胸筋には届かない。プッシュアップバーを使って深く沈み込むことで、ジムに行かなくても自宅で分厚い胸板が手に入る。Tシャツを着たときの胸の張りが劇的に変わるぞ。"
    }
]

def search_rakuten_items(keyword, hits=4):
    if not APP_ID or not ACCESS_KEY:
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
                "generationConfig": {"temperature": 0.85, "maxOutputTokens": 3000}
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                cand = data.get("candidates", [])
                if cand:
                    parts = cand[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
        except Exception:
            continue
    return None

def generate_article(topic):
    print(f"Processing: {topic['theme']}")
    products = search_rakuten_items(topic["keyword"], hits=4)
    if not products:
        print(f"[WARN] No products for {topic['keyword']}")
        return None

    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    comparisons = []
    for i, p in enumerate(products):
        st = skin_types[i % len(skin_types)]
        comparisons.append({
            "name": p["name"],
            "brand": p["brand"],
            "category": topic["category"],
            "targetSkin": st,
            "feature": f"{st}の悩みに特化した設計。日々のケアで無理なく清潔感を底上げできる実力派アイテム。",
            "price": p["price"],
            "pros": ["肌なじみが良い", "使いやすい", "清潔感UP"],
            "cons": ["継続して使うことが前提"],
            "imageUrl": p["imageUrl"],
            "affiliateUrl": p["affiliateUrl"],
            "rating": round(random.uniform(4.3, 4.8), 1),
            "reviewCount": random.randint(150, 1800)
        })

    sys_msg = """
あなたは「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の塾長です。
読者は今まで外見に無頓着で清潔感がなく、陰キャ・チー牛と裏で言われてきた男性たちです。
「いかがでしたでしょうか」「〜と言えるでしょう」などのAI臭い定型文は絶対に禁止。
実体験に基づいた熱量と論理的な解説で、読者の背中を強く押してください。
必ず純粋なJSONのみで出力してください（Markdownの```囲みは付けないでください）：
{
  "excerpt": "記事の要約（70〜90文字）",
  "intro": "なぜ今このケアが必要なのか、放置するとどう足切りされるか（160〜220文字）",
  "problemStatement": "読者の切実な悩みと失敗あるある（180〜220文字）",
  "conclusion": "まとめと、まず何をすべきかのアクション提案（140〜180文字）"
}
"""
    prompt = f"""
テーマ: {topic['theme']}
ターゲット読者: {topic['targetAudience']}
塾長メッセージの方向性: {topic['intro_theme']}
カテゴリ: {topic['category']}
選抜アイテム数: {len(comparisons)}点
"""
    ai_res = call_gemini(prompt, sys_msg)
    data = {}
    if ai_res:
        cleaned = re.sub(r'```(?:json)?', '', ai_res).strip()
        try:
            data = json.loads(cleaned)
        except Exception as e:
            print(f"JSON error for {topic['slug']}: {e}")

    now_str = datetime.now().strftime("%Y.%m.%d")
    return {
        "slug": topic["slug"],
        "title": topic["theme"],
        "excerpt": data.get("excerpt", f"{topic['category']}で清潔感を手に入れ、チー牛を脱却するための徹底比較ガイド。"),
        "category": topic["category"],
        "categoryEn": topic["categoryEn"],
        "date": now_str,
        "readTime": f"{random.randint(4, 6)} min read",
        "heroImage": products[0]["imageUrl"],
        "tags": [topic["tag"], "#チー牛脱却", "#清潔感", "#メンズ美容"],
        "intro": data.get("intro", topic["intro_theme"]),
        "targetAudience": topic["targetAudience"],
        "problemStatement": data.get("problemStatement", "何から始めればいいか分からず、適当に買ってみては合わなくて三日坊主。そんな失敗を繰り返さないために、肌質別の最適アイテムを厳選しました。"),
        "comparisonTable": comparisons,
        "conclusion": data.get("conclusion", "清潔感は才能ではなく技術です。まずは自分に合った1本を手に入れて、明日の朝から実践してみてください。"),
        "views": random.randint(1500, 4800)
    }

def main():
    existing_posts = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            existing_posts = json.load(f)

    existing_slugs = set(p.get("slug") for p in existing_posts)
    new_articles = []

    for t in BATCH_TOPICS:
        if t["slug"] in existing_slugs:
            print(f"Skipping already existing: {t['slug']}")
            continue
        art = generate_article(t)
        if art:
            new_articles.append(art)
            print(f"[OK] Generated: {art['title']}")
        time.sleep(1.5)

    all_posts = new_articles + existing_posts
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\nCompleted! Total articles now: {len(all_posts)}")

if __name__ == "__main__":
    main()
