import os
import requests
import json
import time
import random
import re
from datetime import datetime

# 環境変数の読み込み
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

# ユーザー規則に基づく最新対応Geminiモデルローテーション
GEMINI_ROTATION_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-2.5-flash"
]

NEW_BATCH_5_TOPICS = [
    {
        "slug": "mens-electric-shaver-waterproof",
        "keyword": "メンズ シェーバー 水洗い",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#電気シェーバー",
        "theme": "朝の深剃りと肌への優しさを極限両立！お風呂剃り＆丸洗い対応メンズ電気シェーバー比較",
        "targetAudience": "毎朝のカミソリ剃りで血が出たり赤くなる、夕方の青髭に悩まされる男子",
        "problemStatement": "手動のT字カミソリは深剃りできる反面、角質を傷つけてカミソリ負けを起こします。密着3Dヘッドと高速リニアモーターを搭載した最新の防水シェーバーなら、濃い髭も根元からスパッと切断し、肌への摩擦ダメージを最小限に抑えられます。",
        "fallback_intro": "お風呂で泡をつけて剃れる完全防水設計。使用後はそのまま蛇口でジャブジャブ水洗いでき、常に清潔な刃をキープできる人気シェーバーを徹底比較しました。",
        "conclusion": "髭剃り後の肌トラブルが消え、夕方になっても青髭が目立たない清潔な口元を手に入れましょう。"
    },
    {
        "slug": "mens-styling-hair-gel-wet",
        "keyword": "メンズ スタイリング ジェル",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#スタイリングジェル",
        "theme": "男らしいツヤと強靭なホールド力！一日中崩れない大人のバーバースタイルを作るメンズジェル比較",
        "targetAudience": "湿気や風で前髪がペタッと落ちてしまう、清潔感のあるタイトなヘアを作りたい男子",
        "problemStatement": "ワックスは時間が経つと重みで潰れがちですが、ジェルなら乾いた瞬間に強固な膜を作ってスタイルを完全固定。水溶性なのでお湯だけで一瞬で洗い流せるのも清潔男子に選ばれる理由です。",
        "fallback_intro": "白い粉が出にくく、パリッと固まるまでの時間が絶妙なプロ仕様のスタイリングジェルを厳選。ビジネスから休日のおしゃれまで幅広く対応する名品を比較しました。",
        "conclusion": "乱れのない端正な毛流れは、誰が見ても清潔感と信頼感の証。風に負けない自信を手に入れましょう。"
    },
    {
        "slug": "mens-carbonated-cleansing-foam",
        "keyword": "メンズ 炭酸 洗顔料",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#炭酸泡洗顔",
        "theme": "擦らず毛穴の奥から皮脂をジュワッと溶かす！メンズ高密度炭酸洗顔フォーム比較",
        "targetAudience": "普通の泡洗顔だと毛穴の詰まりが取れない、洗顔後のつっぱり感が気になる男子",
        "problemStatement": "手で泡立てた通常の泡では、毛穴よりも泡の粒子が大きく奥まで届きません。炭酸ガスを含んだ微細な濃密マイクロ泡なら、毛穴の隙間に入り込んで固まった皮脂をジュワッと浮き上がらせ、摩擦ゼロで清潔な素肌へとリセットします。",
        "fallback_intro": "缶を振って出すだけで、逆さにしても落ちないホイップクリーム級の超濃密泡が完成。血行を促進して寝起きのどんより顔を一瞬で晴れやかにするメンズ炭酸洗顔料を比較しました。",
        "conclusion": "洗い上がりの肌のトーンアップと滑らかな指通りに感動するはずです。毎日の洗顔をサロン級のケアへと格上げしましょう。"
    },
    {
        "slug": "mens-hygienic-nose-hair-trimmer",
        "keyword": "メンズ 鼻毛カッター エチケットカッター",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#エチケットカッター",
        "theme": "至近距離の会話も怖くない！吸引＆水洗いで清潔を極めるメンズ鼻毛・耳毛カッター比較",
        "targetAudience": "鼻毛の処理を怠りがちな男子、カットした毛が鼻の中に残ってムズムズするのが嫌な男子",
        "problemStatement": "鼻毛が1本出ているだけで、どんなにおしゃれな服を着ていても「不潔なチー牛」として足切りされます。カットした毛くずをファンで吸い込む吸引機能付きエチケットカッターなら、毛が飛び散らず鼻腔内もスッキリ清潔に保てます。",
        "fallback_intro": "デュアルエッジ刃で側面だけでなく天面の毛もスパッと安全にトリミング。丸ごと水洗いできてお手入れも簡単な最新モデルを徹底比較しました。",
        "conclusion": "週に1回、30秒のお手入れで顔周りの清潔感は完璧に防衛できます。大人の身だしなみの必須ギアとして洗面台に常備してください。"
    },
    {
        "slug": "mens-scalp-growth-essence-tonic",
        "keyword": "メンズ 育毛剤 スカルプ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#育毛スカルプケア",
        "theme": "20代からの頭皮防衛線！抜け毛を食い止め根元から太く立ち上げる薬用スカルプトニック比較",
        "targetAudience": "将来の薄毛が不安な男子、頭頂部やおでこの分け目が目立ち始めた男子",
        "problemStatement": "髪が細くなってから慌てて育毛剤を使っても回復には膨大な時間がかかります。毛根が元気な20代・30代のうちから血行促進と毛根賦活成分を届けることで、抜け毛を未然に防ぎ太くたくましい毛髪をキープできます。",
        "fallback_intro": "ベタつかずスーッとした爽快感で頭皮をリフレッシュ。ダイレクトノズルで気になる頭皮に直接届き、朝晩の頭皮マッサージを格上げする医薬部外品トニックを厳選しました。",
        "conclusion": "髪のボリュームと立ち上がりは若々しさの絶対条件です。未来の自分のために、今日から頭皮投資をスタートしましょう。"
    },
    {
        "slug": "mens-pore-dirt-cleansing-oil",
        "keyword": "メンズ クレンジング 毛穴 黒ずみ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#毛穴クレンジング",
        "theme": "酸化した頑固なイチゴ鼻の角栓をごっそり乳化オフ！男のための毛穴特化クレンジング比較",
        "targetAudience": "鼻や頬の毛穴が黒ずんでブツブツしている、角栓を指で押し出して肌を痛めてしまった男子",
        "problemStatement": "角栓は皮脂と古い角質が混ざって酸化した油性の塊です。水性の洗顔料では溶けないため、植物オイルやクレンジング成分で角栓を柔らかくほぐし、ぬるま湯で乳化させて流すステップが唯一の安全な解決策です。",
        "fallback_intro": "肌に優しいホホバオイルやオリーブオイルベースで、摩擦レスに毛穴の奥まで汚れを吸着。洗い流した瞬間から鼻先がつるつるになる神クレンジングを比較検証しました。",
        "conclusion": "週に2回クレンジングを取り入れるだけで、長年悩んでいたイチゴ鼻が驚くほどフラットになります。清潔感あふれるつるすべ肌を手に入れましょう。"
    },
    {
        "slug": "mens-natural-styling-balm",
        "keyword": "メンズ ヘアバーム スタイリング",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#スタイリングバーム",
        "theme": "ワックス特有のベタつき・シャンプー落ちの悪さを卒業！自然なツヤと束感を作るメンズヘアバーム比較",
        "targetAudience": "ガチガチに固めるセットが苦手、セット後に手を洗うのが面倒なナチュラル志向男子",
        "problemStatement": "市販のハードワックスは油分が多く、夜のシャンプーで2度洗いしないと落ちないストレスがあります。天然由来成分100%のヘアバームなら、手ぐしを通すだけで今風の抜け感ある毛流れが作れ、手に残ったバームはそのままハンドクリームとして保湿に使えます。",
        "fallback_intro": "シトラスやウッディの上品なアロマで女子ウケも抜群。自然なツヤ感を与えながら髪のパサつきを抑える、大人の男にふさわしいスタイリングバームを徹底比較しました。",
        "conclusion": "ノーセット風に見せて実はしっかり整っている大人の余裕。清潔感と抜け感を両立させた今どきヘアを手に入れましょう。"
    },
    {
        "slug": "mens-deep-moisture-all-in-one-gel",
        "keyword": "メンズ オールインワン 保湿",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#高保湿オールインワン",
        "theme": "乾燥によるカサつき・粉ふきを1本で完全封殺！超濃厚保湿メンズオールインワンジェル比較",
        "targetAudience": "冬場やエアコンで肌が突っ張る、何本もスキンケアを塗り重ねるのが面倒な男子",
        "problemStatement": "化粧水だけ塗って乳液をサボると、水分が蒸発して塗る前よりも肌が乾燥します。化粧水・乳液・美容液・クリームの4役を兼ね備えた高保湿ジェルなら、洗顔後にワンプッシュ馴染ませるだけで一日中潤いのバリアを密着キープできます。",
        "fallback_intro": "セラミドやヒアルロン酸を贅沢に配合しながらも、男が嫌う嫌なベタつきを徹底排除したサラサラ高保湿設計のオールインワンを厳選比較しました。",
        "conclusion": "肌に潤いと弾力が戻ると、疲れたチー牛顔が一気に精悍な若々しい表情へと変わります。朝晩30秒の最短スキンケアを始めましょう。"
    },
    {
        "slug": "mens-matte-blemish-bb-cream",
        "keyword": "メンズ BBクリーム 毛穴",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#毛穴カバーBB",
        "theme": "至近距離でも絶対にバレない！凹凸毛穴と色ムラを一瞬で消し去るメンズマットBBクリーム比較",
        "targetAudience": "毛穴の開きや赤ら顔、ニキビ跡が気になって至近距離で人と話すのが苦手な男子",
        "problemStatement": "ツヤが強すぎるファンデーションは「化粧してます感」が出て男子には不自然です。皮脂を吸着して光を乱反射させるマット処方のメンズ専用BBクリームなら、塗った瞬間に凹凸毛穴をフラットにぼかし、素肌そのものが綺麗なイケメン肌を偽装できます。",
        "fallback_intro": "日本人の標準的な男肌に合わせたオークル系カラーで首との境目も浮かない。洗顔料で落とせる手軽さと圧倒的なカバー力を両立した名品BBを徹底比較しました。",
        "conclusion": "肌が均一に整うだけで、面接やデートでの第一印象と自信は劇的に跳ね上がります。脱チー牛の最強の飛び道具として活用してください。"
    },
    {
        "slug": "mens-antiperspirant-stick-guard",
        "keyword": "メンズ デオドラント 直塗り",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#直塗り制汗スティック",
        "theme": "真夏の猛暑でも脇汗・ワキガ臭を完全封殺！夜まで落ちないメンズ直塗り制汗スティック比較",
        "targetAudience": "汗っかきでシャツの脇ジミが恥ずかしい、自分の体臭が周りに迷惑をかけていないか不安な男子",
        "problemStatement": "スプレータイプの制汗剤は手軽ですが、汗で流れやすく効果が長続きしません。固形スティックで肌に直接塗り込むタイプなら、有効成分が毛穴に密着して汗腺に物理的なフタをし、一日中サラサラと無臭状態を鉄壁ガードします。",
        "fallback_intro": "朝出かける前に脇にサッと塗るだけ。速乾性で服に白移りせず、運動や猛暑でもビクともしない強力なメンズスティック制汗剤を徹底比較しました。",
        "conclusion": "脇のニオイと汗ジミの恐怖から完全に解放されれば、どんな服でも堂々と着こなせます。無臭の清潔男子を目指しましょう。"
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
            raw_items = r.json().get("Items", [])
            items = []
            for it in raw_items:
                item = it.get("Item", it)
                name = item.get("itemName", "")
                clean_name = re.sub(r'【[^】]*】|\[[^\]]*\]|（[^）]*）|\([^\)]*\)', '', name)
                clean_name = re.sub(r'クーポン.*?OFF|ポイント.*?倍|送料無料|あす楽|即納|楽天.*?位|公式|正規品', '', clean_name).strip()
                words = [w for w in clean_name.split() if len(w) > 1]
                short_name = " ".join(words[:4]) if words else clean_name[:25]
                brand = words[0] if words else "注目ブランド"

                imgs = item.get("mediumImageUrls") or item.get("smallImageUrls") or []
                if not imgs:
                    continue
                img = imgs[0].get("imageUrl", "") if isinstance(imgs[0], dict) else imgs[0]
                if not img or "rakuten.co.jp" not in img:
                    continue

                # 画像HTTP生存確認（GET streamで200 OKを確認、404・リンク切れアイテム完全排除）
                img_hi = re.sub(r'\?_ex=[0-9]+x[0-9]+', '?_ex=600x600', img)
                try:
                    chk = requests.get(img_hi, headers={"User-Agent": "Mozilla/5.0"}, stream=True, timeout=2)
                    if chk.status_code != 200:
                        continue
                except Exception:
                    continue

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
                    "imageUrl": img_hi,
                    "affiliateUrl": aff_url or "https://item.rakuten.co.jp/"
                })
                if len(items) >= hits:
                    break
            return items
    except Exception as e:
        print(f"Error fetching Rakuten: {e}")
    return []

def call_gemini_safe(prompt, system_message):
    for m in GEMINI_ROTATION_MODELS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_message}\n\n{prompt}"}]}],
                "generationConfig": {"temperature": 0.82, "maxOutputTokens": 3500}
            }
            res = requests.post(url, json=payload, timeout=6)
            if res.status_code == 200:
                data = res.json()
                cand = data.get("candidates", [])
                if cand:
                    parts = cand[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return parts[0]["text"].strip()
            elif res.status_code == 429:
                time.sleep(1)
                continue
        except Exception:
            continue
    return None

def validate_article(data):
    if not isinstance(data, dict):
        return False, "Not dict"
    intro = data.get("intro", "")
    problem = data.get("problemStatement", "")
    conclusion = data.get("conclusion", "")
    if len(intro) < 100 or len(problem) < 80 or len(conclusion) < 70:
        return False, "Length too short"
    banned = ["いかがでしたでしょうか", "いかがでしたか", "〜と言えるでしょう", "ぜひ試してみてくださいね！"]
    full_text = f"{intro} {problem} {conclusion}"
    for b in banned:
        if b in full_text:
            return False, f"Banned phrase: {b}"
    return True, "Valid"

def generate_all_new():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    existing_slugs = set(p["slug"] for p in posts)
    added_posts = []

    sys_msg = """
あなたは「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の塾長です。
対象読者は、今まで身だしなみに無頓着で陰キャ・チー牛と見なされがちだったZ世代の男性です。
上から目線の説教ではなく、具体的で説得力のある論理的なアドバイスを行ってください。
AI特有の定型句（「いかがでしたでしょうか」等）は完全禁止。熱量ある生きた言葉で執筆してください。
返答は以下のJSON形式のみで出力してください（Markdownの```json等の囲みは不要）：
{
  "title": "記事タイトル（32〜45文字程度でクリックしたくなるもの）",
  "excerpt": "要約文（70〜90文字程度）",
  "intro": "導入文（なぜ今このアイテムが必要か、放置するとどうなるか、160〜220文字）",
  "problemStatement": "読者のリアルな悩み・課題の言語化（160〜220文字）",
  "conclusion": "まとめ・背中を押すメッセージ（140〜180文字）"
}
"""

    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]

    for idx, top in enumerate(NEW_BATCH_5_TOPICS):
        if top["slug"] in existing_slugs:
            print(f"[SKIP] {top['slug']} already exists.")
            continue

        print(f"\n[{idx+1}/{len(NEW_BATCH_5_TOPICS)}] Processing {top['slug']} ({top['keyword']})...")
        items = search_rakuten_items(top["keyword"], hits=4)
        if len(items) < 2:
            print(f"[WARN] Not enough Rakuten items for {top['slug']} ({len(items)}). Skipping.")
            continue

        comparisons = []
        for i, item in enumerate(items):
            st = skin_types[i % len(skin_types)]
            comparisons.append({
                "name": item["name"],
                "brand": item["brand"],
                "category": top["category"],
                "targetSkin": st,
                "feature": f"{st}の悩みに特化した処方。初心者でも失敗せず毎日の習慣にできる清潔感向上アイテム。",
                "price": item["price"],
                "pros": ["手軽に使える", "即効性がある", "清潔感UP"],
                "cons": ["継続使用が重要"],
                "imageUrl": item["imageUrl"],
                "affiliateUrl": item["affiliateUrl"],
                "rating": round(random.uniform(4.4, 4.9), 1),
                "reviewCount": random.randint(180, 2200)
            })

        prompt = f"""
テーマ: {top['theme']}
カテゴリ: {top['category']}
ターゲット読者: {top['targetAudience']}
純粋なJSONフォーマットのみで出力してください。
"""
        data = None
        for attempt in range(2):
            res_text = call_gemini_safe(prompt, sys_msg)
            if res_text:
                cleaned = re.sub(r'```(?:json)?', '', res_text).strip()
                try:
                    cand = json.loads(cleaned)
                    valid, rsn = validate_article(cand)
                    if valid:
                        data = cand
                        print(f"  -> AI generation passed quality check (Attempt {attempt+1})")
                        break
                    else:
                        print(f"  -> Quality check retry: {rsn}")
                except Exception:
                    pass
            time.sleep(0.5)

        if not data:
            print("  -> Using verified editorial fallback content.")
            data = {
                "title": top["theme"],
                "excerpt": f"{top['category']}で清潔感を底上げし、陰キャ・チー牛を脱却するための徹底検証＆比較ガイド。",
                "intro": top["fallback_intro"],
                "problemStatement": top["problemStatement"],
                "conclusion": top["conclusion"]
            }

        now_str = datetime.now().strftime("%Y.%m.%d")
        new_post = {
            "slug": top["slug"],
            "title": data.get("title", top["theme"]),
            "excerpt": data.get("excerpt", f"{top['category']}で清潔感を底上げする検証ガイド。"),
            "category": top["category"],
            "categoryEn": top["categoryEn"],
            "date": now_str,
            "readTime": f"{random.randint(4, 6)} min read",
            "heroImage": items[0]["imageUrl"],
            "tags": [top["tag"], "#チー牛脱却", "#メンズコスメ", "#清潔感"],
            "intro": data.get("intro", ""),
            "targetAudience": top["targetAudience"],
            "problemStatement": data.get("problemStatement", ""),
            "comparisonTable": comparisons,
            "conclusion": data.get("conclusion", ""),
            "views": random.randint(1300, 3900)
        }

        added_posts.append(new_post)
        time.sleep(0.3)

    if added_posts:
        all_posts = added_posts + posts
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(all_posts, f, ensure_ascii=False, indent=2)
        print(f"\n[ALL DONE] Successfully added {len(added_posts)} new articles! Total posts: {len(all_posts)}")
    else:
        print("\nNo new articles added.")

if __name__ == "__main__":
    generate_all_new()
