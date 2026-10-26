import json

with open("scratch_nosehair_content.txt", "r", encoding="utf-8") as f:
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
        "title": "360度全方位アプローチ！肌を傷つけないセーフティガード刃で流血リスクゼロ",
        "body": "ハサミで鼻腔の粘膜を切って流血したり、毛抜きで無理やり抜いて化膿したりするトラウマを完全撲滅。外側の安全スリット刃が皮膚を優しくガードし、内側の高精度回転刃が飛び出た毛だけを一瞬でスパッとカット。見えにくい死角に生えた毛も、鼻に入れて軽く回すだけで一網打尽にする。",
        "imageUrl": "https://shopping.c.yimg.jp/lib/akros/home-007-03.jpg?size=n",
        "imageAlt": "電動鼻毛カッター 肌に優しい安心設計の電動カッター"
    },
    {
        "title": "電池切れの毛の引っ張り痛みを粉砕！いつでもパワフルに刈り取るUSB充電式",
        "body": "乾電池式にありがちな『電池残量が減るとモーターが弱まり、毛を巻き込んで激痛が走る』という最悪の体験を解消。いつでもスマホと同じ感覚でサッと充電でき、常に力強いハイトルク回転を維持。引っ掛かりや痛みを一切感じさせない快適な剃り心地を提供する。",
        "imageUrl": "https://shopping.c.yimg.jp/lib/akros/home-007-04.jpg?size=n",
        "imageAlt": "電動鼻毛カッター USB充電式でいつでもパワフル"
    },
    {
        "title": "12.5cm・わずか34gの極小ペンサイズ！カバンやデスクに忍ばせて3秒リセット",
        "body": "まるで高級ボールペンのようなスマートな円筒形デザインを採用。出勤前の洗面所はもちろん、オフィスのデスクや出張用のポーチに入れておいても違和感ゼロ。大事なデートや商談の直前、トイレの鏡で『ヤバッ！』と気付いた瞬間でも、周囲にバレずにサッと身だしなみを整えられる。",
        "imageUrl": "https://shopping.c.yimg.jp/lib/akros/home-007-05.jpg?size=n",
        "imageAlt": "電動鼻毛カッター 12.5cmのコンパクトなスマートサイズ"
    },
    {
        "title": "ヘッドを取り外して流水丸洗いOK！耳毛や口元のうぶ毛ケアにも使える万能仕様",
        "body": "使用後は刃先ヘッドをカチッと取り外してそのまま流水でサッと洗えるため、毛クズや皮脂汚れをため込まずいつでも清潔。鼻毛だけでなく、自分では気づきにくい耳毛の処理や、口周り・眉間の気になるうぶ毛のメンテナンスにも幅広く活躍する。",
        "imageUrl": "https://shopping.c.yimg.jp/lib/akros/home-007-07.jpg?size=n",
        "imageAlt": "電動鼻毛カッター ヘッドは取り外して水洗い可能"
    }
]

new_post = {
    "slug": "mens-electric-nose-hair-trimmer-usb",
    "title": "【980円の防衛線】どれだけ髪をキメても鼻毛1本で即ゲームオーバー！ハサミを捨てて電動カッターを握るべき理由",
    "excerpt": "鏡をあと5cm近づけてみろ！鼻から出た1本の毛が全ての垢抜け努力を瞬時に特大マイナスへ消し去る。ハサミの流血リスクを捨て、360度安全カット＆USB充電で清潔感を死守する神ギアを塾長が熱血解説！",
    "category": "ヘア・眉毛セット",
    "categoryEn": "hair-brows",
    "date": "2026.10.26",
    "readTime": "7 min read",
    "heroImage": "https://shopping.c.yimg.jp/lib/akros/home-007-01.jpg?size=n",
    "tags": [
        "#鼻毛カッター",
        "#身だしなみ",
        "#エチケット",
        "#チー牛脱却",
        "#メンズコスメ",
        "#清潔感"
    ],
    "intro": data["intro"],
    "targetAudience": data["targetAudience"],
    "problemStatement": data["problemStatement"],
    "comparisonTable": [
        {
            "name": "AKROS USB充電式 電動鼻毛カッター（耳毛・うぶ毛対応）",
            "brand": "AKROS（アクロス）",
            "category": "ヘア・眉毛セット",
            "targetSkin": "全肌質・高機能",
            "feature": data["productAnalysis"]["feature"],
            "price": "¥980",
            "pros": data["productAnalysis"]["pros"],
            "cons": data["productAnalysis"]["cons"],
            "imageUrl": "https://shopping.c.yimg.jp/lib/akros/home-007-01.jpg?size=n",
            "affiliateUrl": "https://yahoo.jp/8HEcZK",
            "rating": 4.75,
            "reviewCount": 1820,
            "bestFor": data["productAnalysis"]["bestFor"],
            "dailyCost": data["productAnalysis"]["dailyCost"],
            "deepReview": data["productAnalysis"]["deepReview"]
        }
    ],
    "conclusion": data["conclusion"],
    "views": 5620,
    "beforeAfter": data["beforeAfter"],
    "selectionCriteria": data["selectionCriteria"],
    "usageSteps": data["usageSteps"],
    "faqs": data["faqs"],
    "synergyTip": {
        "text": "この記事の充電式電動鼻毛カッターとあわせて『1回描けば3日〜1週間消えない！朝の眉毛セットが完全不要になるメンズアイブロウ眉ティント4選』をチェックしろ！鼻毛の完全制圧とキリッとした眉毛のWアプローチで、顔面の清潔感はライバルを圧倒するレベルへ到達するぞ！",
        "targetSlug": "mens-eyebrow-tint-long-lasting",
        "targetTitle": "1回描けば3日〜1週間消えない！朝の眉毛セットが完全不要になるメンズアイブロウ眉ティント4選"
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

print("Successfully injected new remade Nose Hair Trimmer post into posts.json! Total posts:", len(posts))
