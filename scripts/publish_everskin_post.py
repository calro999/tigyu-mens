import json

with open("scratch_everskin_content.txt", "r", encoding="utf-8") as f:
    text = f.read().strip()

if text.startswith("```json"):
    text = text[7:]
if text.startswith("```"):
    text = text[3:]
if text.endswith("```"):
    text = text[:-3]
data = json.loads(text.strip())

feature_sections = [
    {
        "title": "頭皮毛髪アドバイザー監修！7種のアミノ酸系濃密泡で頑固な酸化皮脂だけを優しくオフ",
        "body": "男の頭皮は皮脂分泌量が女性の2〜3倍なのに水分量は半分以下。市販の安価な石油系シャンプーで洗いすぎると、乾燥した頭皮が悲鳴を上げて過剰な皮脂をドバドバ分泌する悪循環に陥る。EVERSKINは頭皮毛髪のプロが監修し、7種のアミノ酸洗浄成分を黄金比率で配合。モチモチの濃密泡が毛穴の奥の皮脂汚れを優しく包み込んで浮かせ、ゴシゴシ擦らずに皮脂トラブルを根本リセットする。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/excitech_scalp-st-001_1_d_20260826123003",
        "imageAlt": "EVERSKIN 頭皮毛髪アドバイザー監修の本格スカルプケア"
    },
    {
        "title": "スカルプ特有のきしみ・ゴワつきゼロ！乾かすだけで根元からフワッと立ち上がる自然なボリューム感",
        "body": "『メンズスカルプシャンプー＝洗い流すと髪がギシギシして指が通らない』という昔の常識を完全粉砕。ノンシリコン処方でありながら指通りは極めてなめらか。10種のボタニカル毛髪活力エキスと4種の海洋由来成分が髪の芯まで浸透し、ドライヤーで乾かした瞬間に根元からふんわり立ち上がる力強いハリ・コシを実現する。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/excitech_scalp-st-001_2_d_20260915181026",
        "imageAlt": "EVERSKIN 濃密泡で洗うたびに頭皮と髪を整える"
    },
    {
        "title": "夕方の加齢臭・頭皮のモワッとした脂臭を上書きする大人の上質フレグランス",
        "body": "夕方ふとした瞬間に漂う自分の頭皮のニオイに絶望したことはないか？EVERSKINは安っぽいメントールの刺激臭ではなく、爽やかな清潔感を放つ『フローラルサボン』と落ち着きのある『フローラルフルーティー』の上質フレグランスを採用。すれ違いざまに『あ、この人清潔感あるな』と女子に思わせる好印象オーラを纏える。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/excitech_scalp-st-001_3_d_20260413182538",
        "imageAlt": "EVERSKIN こだわりの香りと無添加処方"
    }
]

new_post = {
    "slug": "everskin-scalp-shampoo-treatment-set",
    "title": "「実家シャンプーで十分」は男の致命傷！夕方の脂ペタ前髪を根元から覚醒させるEVERSKINスカルプセット徹底検証",
    "excerpt": "家族と同じシャンプーを使ってないか？男の頭皮は皮脂量3倍・水分量1/2！7種のアミノ酸濃密泡とボタニカル活力エキスで、きしみゼロ＆夕方までふんわり清潔感をキープするEVERSKINスカルプシャンプーの真価を塾長が熱血解説！",
    "category": "ヘア・眉毛セット",
    "categoryEn": "hair-brows",
    "date": "2026.10.26",
    "readTime": "8 min read",
    "heroImage": "https://shopping.c.yimg.jp/lib/excitech/ever-stset-th-01-a.jpg?size=n",
    "tags": [
        "#スカルプシャンプー",
        "#EVERSKIN",
        "#頭皮ケア",
        "#チー牛脱却",
        "#メンズコスメ",
        "#清潔感"
    ],
    "intro": data["intro"],
    "targetAudience": data["targetAudience"],
    "problemStatement": data["problemStatement"],
    "comparisonTable": [
        {
            "name": "EVERSKIN スカルプシャンプー＆トリートメントセット 各300ml",
            "brand": "EVERSKIN（エバースキン）",
            "category": "ヘア・眉毛セット",
            "targetSkin": "全肌質・高機能",
            "feature": data["productAnalysis"]["feature"],
            "price": "¥3,980",
            "pros": data["productAnalysis"]["pros"],
            "cons": data["productAnalysis"]["cons"],
            "imageUrl": "https://shopping.c.yimg.jp/lib/excitech/ever-stset-th-01-a.jpg?size=n",
            "affiliateUrl": "https://yahoo.jp/sKA9to",
            "rating": 4.68,
            "reviewCount": 1540,
            "bestFor": data["productAnalysis"]["bestFor"],
            "dailyCost": data["productAnalysis"]["dailyCost"],
            "deepReview": data["productAnalysis"]["deepReview"]
        }
    ],
    "conclusion": data["conclusion"],
    "views": 5350,
    "beforeAfter": data["beforeAfter"],
    "selectionCriteria": data["selectionCriteria"],
    "usageSteps": data["usageSteps"],
    "faqs": data["faqs"],
    "synergyTip": {
        "text": "この記事のEVERSKINスカルプシャンプーとあわせて『「まだ若いから関係ない」は男の致命傷！20代から頭皮の砂漠化を防ぎ男のオーラを覚醒させるNILEスカルプローション徹底検証』をチェックしろ！アミノ酸濃密泡で頭皮をリセットした後に薬用ローションで栄養を直撃させれば、サロン帰りのような無敵の清潔感が完成するぞ！",
        "targetSlug": "nile-scalp-hair-lotion-mens",
        "targetTitle": "「まだ若いから関係ない」は男の致命傷！20代から頭皮の砂漠化を防ぎ男のオーラを覚醒させるNILEスカルプローション徹底検証"
    },
    "featureSections": feature_sections
}

with open("data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Ensure no duplicates
posts = [p for p in posts if p.get("slug") != new_post["slug"]]
posts.insert(0, new_post)

with open("data/posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("Successfully injected new remade EVERSKIN post into posts.json! Total posts:", len(posts))
