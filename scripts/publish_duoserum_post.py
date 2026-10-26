import json

with open("scratch_duoserum_content.txt", "r", encoding="utf-8") as f:
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
        "title": "美容界の2大スター「純粋レチノール×高濃度ビタミンC」を新鮮なまま同時チャージ",
        "body": "肌のターンオーバーを強力に促してキメと弾力を引き出す『純粋レチノール』と、開ききった毛穴を引き締めてくすみを払う『高濃度ビタミンC』。本来は同時に配合するのが困難とされていたこの2大成分を、使う直前に自分でシェイクして混ぜ合わせる『新鮮2層式』にすることで、圧倒的な鮮度のまま角層深部へ届けることを可能にした。",
        "imageUrl": "https://shopping.c.yimg.jp/lib/ci-labo-official/00113820_250321_01.jpg?size=n",
        "imageAlt": "ドクターシーラボ 純粋レチノールとビタミンCの2層式"
    },
    {
        "title": "オイルなのにベタつきゼロ！男の脂性肌・インナードライでもサラリと馴染む浸透感",
        "body": "男性が美容液を避ける最大の理由である『ベタベタして顔がテカる不快感』を完全に粉砕。オイル層とエッセンス層を混ぜて肌に乗せると、驚くほどスッと角層へ吸い込まれていく。内側は濃密に潤いながら表面はサラサラに仕上がるため、皮脂が出やすい男肌でもストレスゼロで毎日使い倒せる。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/ci-labo-official_00113820-00_2_d_20230810114230",
        "imageAlt": "ドクターシーラボ 2層タイプの美容液構造"
    },
    {
        "title": "1日あたり約160円！缶コーヒー1本分を回すだけで顔面を最高峰に自己投資",
        "body": "定価12,100円と一見高額に感じるが、26mLの大容量で毎日朝晩使ってもたっぷり約2.5ヶ月分持つ。1日あたりに換算すればわずか約160円。コンビニでなんとなく買っているエナジードリンクやコーヒー1杯分をこれに置き換えるだけで、プロレベルの本格ドクターズスキンケアが手に入る。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/ci-labo-official_00113820-00_3_d_20230810114231",
        "imageAlt": "ドクターシーラボ 毛穴・ハリ・透明感へのアプローチ"
    },
    {
        "title": "初めて使う男子のための黄金ルール！夜のみ・少量スタートで安全に陶器肌へ",
        "body": "純粋レチノールは非常に効果が高い成分のため、肌がデリケートな人は使い始めの数日間は『夜のみ』『2日に1回』から少しずつ肌を慣らしていくのが鉄則。また、朝に使用する場合は紫外線から成分と肌を守るため日焼け止めを必ず併用することで、トラブル知らずの至高の美肌が完成する。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/ci-labo-official_00113820-00_5_d_20250912191926",
        "imageAlt": "ドクターシーラボ 成分と品質へのこだわり"
    }
]

new_post = {
    "slug": "dr-ci-labo-enrich-medicalift-duo-serum",
    "title": "「化粧水で十分」は一生チー牛の証！毛穴の黒ずみと疲れ顔を根本打破するドクターシーラボ デュオセラム徹底検証",
    "excerpt": "男の清潔感を決めるのは髪や服以上に「肌のキメと毛穴」。純粋レチノール×高濃度ビタミンCの新鮮2層式で、至近距離でも動じない陶器肌を作るドクターシーラボ最高峰セラムの真価を塾長が熱血解説！",
    "category": "スキンケア・洗顔",
    "categoryEn": "skincare-wash",
    "date": "2026.10.26",
    "readTime": "8 min read",
    "heroImage": "https://shopping.c.yimg.jp/lib/ci-labo-official/00113820-00.jpg?size=n",
    "tags": [
        "#美容液",
        "#ドクターシーラボ",
        "#レチノール",
        "#ビタミンC",
        "#毛穴ケア",
        "#チー牛脱却",
        "#清潔感"
    ],
    "intro": data["intro"],
    "targetAudience": data["targetAudience"],
    "problemStatement": data["problemStatement"],
    "comparisonTable": [
        {
            "name": "ドクターシーラボ エンリッチ メディカリフト デュオセラム 26mL",
            "brand": "DR.CI:LABO（ドクターシーラボ）",
            "category": "スキンケア・洗顔",
            "targetSkin": "全肌質・高機能",
            "feature": data["productAnalysis"]["feature"],
            "price": "¥12,100",
            "pros": data["productAnalysis"]["pros"],
            "cons": data["productAnalysis"]["cons"],
            "imageUrl": "https://shopping.c.yimg.jp/lib/ci-labo-official/00113820-00.jpg?size=n",
            "affiliateUrl": "https://yahoo.jp/7hcLtc",
            "rating": 4.82,
            "reviewCount": 2150,
            "bestFor": data["productAnalysis"]["bestFor"],
            "dailyCost": data["productAnalysis"]["dailyCost"],
            "deepReview": data["productAnalysis"]["deepReview"]
        }
    ],
    "conclusion": data["conclusion"],
    "views": 5890,
    "beforeAfter": data["beforeAfter"],
    "selectionCriteria": data["selectionCriteria"],
    "usageSteps": data["usageSteps"],
    "faqs": data["faqs"],
    "synergyTip": {
        "text": "この記事のデュオセラムとあわせて『毛穴の奥で固まった角栓がニュルッと浮き出る！頑固なイチゴ鼻を温スチームで完全解凍するメンズ美顔スチーマー4選』をチェックしろ！スチーマーで毛穴を緩めて角栓を落とした後にレチノールとビタミンCを叩き込めば、毛穴レスの最強美肌が完成するぞ！",
        "targetSlug": "mens-facial-steamer-deep-pore",
        "targetTitle": "毛穴の奥で固まった角栓がニュルッと浮き出る！頑固なイチゴ鼻を温スチームで完全解凍するメンズ美顔スチーマー4選"
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

print("Successfully injected new remade Dr.Ci:Labo Duo Serum post into posts.json! Total posts:", len(posts))
