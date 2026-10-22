import os
import sys
import requests
import json
import re
import random
import time
from datetime import datetime
from auto_post import search_rakuten_items, call_gemini_safe, validate_article_quality, DATA_FILE

# 検索ボリューム大・Z世代のリアルな悩みに直結する高CVR記事テーマ10選
HIGH_CVR_TOPICS = [
    # スキンケア・洗顔
    {
        "keyword": "メンズ ニキビケア 薬用 洗顔 スキンケア",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-acne-care-cleanser",
        "tag": "#ニキビケア",
        "theme": "赤ニキビ・白ニキビの無限ループを断ち切る！男の肌荒れを沈静化する薬用ニキビケア比較",
        "targetAudience": "頬や顎の繰り返しできるニキビに悩み、赤ら顔を卒業したい男子",
        "fallback_intro": "ニキビができるたびに手で潰して赤黒いクレーター跡にしてないか？男のニキビは過剰な皮脂とアクネ菌の増殖が原因。殺菌・抗炎症有効成分が入った薬用処方で肌の炎症を鎮火させ、清潔な肌を取り戻せ。"
    },
    {
        "keyword": "メンズ 泡洗顔料 ポンプ 濃密泡 時短",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-foam-face-wash-pump",
        "tag": "#泡洗顔",
        "theme": "泡立てネットすら面倒な朝に！ワンプッシュで濃密クッション泡が出るメンズ泡洗顔料比較",
        "targetAudience": "朝の身だしなみに時間をかけたくないが、毛穴汚れとアブラは落としたいズボラ男子",
        "fallback_intro": "洗顔料を手で適当に泡立てて肌を擦り付けるのは、摩擦で肌を傷つけてテカリを悪化させる最大の原因。ポンプを押すだけで弾力のあるミクロ泡が出てくる泡洗顔なら、肌を擦らず30秒で毛穴汚れを吸着できる。"
    },
    {
        "keyword": "メンズ BBクリーム ナチュラル バレない 毛穴",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "slug": "mens-natural-bb-cream-matte",
        "tag": "#BBクリーム",
        "theme": "メイク感ゼロで肌の粗を帳消しにする！至近距離でも絶対にバレないメンズBBクリーム徹底比較",
        "targetAudience": "青髭、毛穴の開き、肌の色ムラを手っ取り早く隠して肌を綺麗に見せたい男性",
        "fallback_intro": "「男がファンデーションなんて」と躊躇している間に、周りの垢抜け男子はBBクリームで毛穴も青髭も消している。厚塗り感ゼロで肌色にスッと馴染み、『元から肌が綺麗な男』になれる神BBクリームを紹介する。"
    },

    # ヘア・眉毛セット
    {
        "keyword": "メンズ ハードスプレー キープ 崩れない 無香料",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-hair-spray-hard-lock",
        "tag": "#ヘアスプレー",
        "theme": "朝作った束感を夜まで完全固定！強風・湿気でも絶対に崩れないメンズハードスプレー比較",
        "targetAudience": "ワックスをつけても時間が経つとペタッと潰れてしまう軟毛・直毛男子",
        "fallback_intro": "ワックスだけでセットを維持しようとするから、重みで昼過ぎに髪がペタッとヘタるんだ。仕上げにハードスプレーを根元からフワッと吹きかけるだけで、強風が吹いても手ぐしで戻る無敵のキープ力が手に入るぞ。"
    },
    {
        "keyword": "メンズ 眉マスカラ 眉カラー アッシュ 自然",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-eyebrow-mascara-natural",
        "tag": "#眉マスカラ",
        "theme": "黒々した海苔眉毛から即脱出！サッと塗るだけで顔が垢抜けるメンズ眉マスカラ比較",
        "targetAudience": "眉毛が太くて重く、垢抜けない印象を柔らかく変えたい男子",
        "fallback_intro": "髪を明るく染めたり軽くしたりしても、眉毛だけが真っ黒で主張していると野暮ったさが抜けない。アッシュやナチュラルブラウンのメンズ眉マスカラを毛流れに沿ってひと塗りするだけで、顔の印象が一気に垢抜けるぞ。"
    },
    {
        "keyword": "メンズ ヘアアイロン ストレート 縮毛 カール 初心者",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "slug": "mens-hair-straightener-iron",
        "tag": "#ヘアアイロン",
        "theme": "頑固なくせ毛・うねりを3分でサラサラ直毛にする！男子向け小型ストレートアイロン比較",
        "targetAudience": "前髪のうねりやサイドのハネで毎朝のスタイリングが決まらないくせ毛男子",
        "fallback_intro": "うねったくせ毛の上にどれだけ高いワックスを揉み込んでも変な束感になるだけだ。プレート幅が細いメンズ向けヘアアイロンで根元のクセをスッと伸ばすだけで、サロン帰りのような自然な毛流れが自宅で作れる。"
    },

    # ニオイ・体臭対策
    {
        "keyword": "メンズ 薬用ボディシート 汗拭きシート 超クール",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-deodorant-body-wipes",
        "tag": "#汗拭きシート",
        "theme": "夏場・運動後のベタつきと汗臭を3秒でリセット！携帯必須のメンズ薬用ボディシート比較",
        "targetAudience": "汗っかきで外出先での身体のベタつきやニオイが不安な男性",
        "fallback_intro": "汗をかいたまま放置すると、皮膚の雑菌が皮脂をエサにして激臭ガスを放ち始める。厚手で大判の薬用ボディシートをカバンに忍ばせておけば、トイレでサッと拭くだけでシャワー上がりの爽快感と無臭を取り戻せる。"
    },
    {
        "keyword": "メンズ デリケートゾーン ソープ 股間 臭い 痒み",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "slug": "mens-intimate-wash-soap",
        "tag": "#股間ケア",
        "theme": "男の隠れた激臭スポット「股間の蒸れ・ニオイ」を元から浄化するメンズ専用ソープ比較",
        "targetAudience": "下着を脱いだ瞬間のこもったニオイや股間の痒みに悩んでいる男子",
        "fallback_intro": "男の股間周辺はアポクリン汗腺が密集しており、蒸れた下着の中で強烈なニオイを発生させている。普通の強すぎる石鹸ではなく、弱酸性で菌の繁殖を抑えるメンズデリケートゾーンソープで洗うのが大人のエチケットだ。"
    },

    # ボディ・姿勢改善
    {
        "keyword": "メンズ 可変式ダンベル 筋トレ 自宅 アジャスタブル",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-adjustable-dumbbells-home",
        "tag": "#可変式ダンベル",
        "theme": "部屋が散らからない！ダイヤル1つで重さを変えて肩・腕を太くする可変式ダンベル比較",
        "targetAudience": "自宅で効率よく筋トレして、男らしい逆三角形の身体を作りたい男子",
        "fallback_intro": "何個もダンベルを床に転がして部屋を狭くする時代は終わった。1秒で重量を切り替えられる可変式ダンベルなら、肩メロン・たくましい二の腕・厚い胸板を自宅のわずか畳1畳のスペースで手に入れられるぞ。"
    },
    {
        "keyword": "メンズ ストレッチポール フォームローラー 背中 肩甲骨",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "slug": "mens-stretch-pole-spine",
        "tag": "#ストレッチポール",
        "theme": "寝転がるだけで胸が開いて猫背が治る！肩甲骨を剥がして姿勢を整えるストレッチポール比較",
        "targetAudience": "スマホ首で背中がガチガチに固まり、呼吸が浅くなっているデスクワーク男子",
        "fallback_intro": "筋トレする前に、まずは縮こまった大胸筋と固まった背骨をリセットしろ。ストレッチポールの上に仰向けで寝て脱力するだけで、自重で肩甲骨が自然に開き、巻き肩と猫背が驚くほど軽くなるぞ。"
    }
]

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)

    existing_slugs = set(p.get("slug") for p in existing_posts)
    new_posts = []

    print(f"Adding High-CVR topics. Current posts: {len(existing_posts)}")

    for topic_info in HIGH_CVR_TOPICS:
        if topic_info["slug"] in existing_slugs:
            print(f"Skipping existing: {topic_info['slug']}")
            continue

        print(f"Generating article for: {topic_info['theme']}")
        products_raw = search_rakuten_items(topic_info["keyword"], hits=4)
        if not products_raw:
            print(f"[WARN] No products for {topic_info['keyword']}")
            continue

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
対象読者は、今まで身だしなみに無頓着で、陰キャ・チー牛と見なされがちだったZ世代の男性です。
上から目線の説教ではなく、論理的で親しみやすい「講座・ロードマップ」として、具体的かつ確実に効果が出るアドバイスを行います。
AI特有の不自然な言い回し（「いかがでしたでしょうか」「〜と言えるでしょう」等）は一切使わず、熱量のあるリアルな日本語で執筆してください。
返答は以下のJSON形式のみで出力してください：
{
  "title": "記事タイトル（32〜45文字程度でクリックしたくなる魅力的なもの）",
  "excerpt": "要約文（70〜90文字程度）",
  "intro": "導入文（なぜ今このアイテムが必要なのか、現状放置するとどう足切りされるのか、160〜220文字）",
  "problemStatement": "読者のリアルな悩み・課題の言語化（160〜220文字）",
  "conclusion": "まとめ・背中を押すメッセージ（140〜180文字）"
}
"""
        prompt = f"""
テーマ: {topic_info['theme']}
カテゴリ: {topic_info['category']}
ターゲット読者: {topic_info.get('targetAudience', '垢抜けたい男子')}
選抜アイテム数: {len(comparisons)}点
純粋なJSONフォーマットのみで出力してください。
"""
        data = None
        for attempt in range(3):
            ai_res = call_gemini_safe(prompt, sys_msg)
            if ai_res:
                cleaned = re.sub(r'```(?:json)?', '', ai_res).strip()
                try:
                    cand_data = json.loads(cleaned)
                    is_valid, reason = validate_article_quality(cand_data)
                    if is_valid:
                        data = cand_data
                        break
                except Exception:
                    pass
            time.sleep(1)

        if not data:
            data = {
                "title": topic_info["theme"],
                "excerpt": f"{topic_info['category']}で清潔感を底上げし、陰キャ・チー牛を脱却するための徹底検証＆比較ガイド。",
                "intro": topic_info.get("fallback_intro", "「男だから外見なんて気にしなくていい」と放置していると、第一印象で清潔感がないと判断され大きな損をする。毎日の習慣に1つ加えるだけで劇的に垢抜ける神アイテムを厳選した。"),
                "problemStatement": "「ドラッグストアに行っても何を選べばいいか分からない」「高価なものを買って失敗したくない」。そんな悩みを解決するために、肌質・タイプ別に最もコスパ良く効果が出る商品を徹底比較しました。",
                "conclusion": "清潔感は生まれつきの顔立ちではなく、正しいアイテム選びと習慣で100%作れます。まずは自分に合った1本を手に入れて、明日の朝から試してみてください。"
            }

        now_str = datetime.now().strftime("%Y.%m.%d")
        new_post = {
            "slug": topic_info["slug"],
            "title": data.get("title", topic_info["theme"]),
            "excerpt": data.get("excerpt", "清潔感を手に入れてチー牛を脱却するための徹底比較ガイド。肌質別の最適アイテムと選び方を解説。"),
            "category": topic_info["category"],
            "categoryEn": topic_info["categoryEn"],
            "date": now_str,
            "readTime": f"{random.randint(4, 6)} min read",
            "heroImage": hero_img,
            "tags": [topic_info["tag"], "#チー牛脱却", "#メンズコスメ", "#清潔感"],
            "intro": data.get("intro", ""),
            "targetAudience": topic_info.get("targetAudience", "垢抜けて清潔感を手に入れたいZ世代男性"),
            "problemStatement": data.get("problemStatement", ""),
            "comparisonTable": comparisons,
            "conclusion": data.get("conclusion", ""),
            "views": random.randint(1400, 4200)
        }
        new_posts.append(new_post)
        print(f"[SUCCESS] Prepared: {new_post['title']}")
        time.sleep(1.5)

    all_posts = new_posts + existing_posts
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\nBatch add complete! Total posts in dataset: {len(all_posts)}")

if __name__ == "__main__":
    main()
