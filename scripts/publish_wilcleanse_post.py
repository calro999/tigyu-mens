import json

with open("scratch_wilcleanse_content.txt", "r", encoding="utf-8") as f:
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
        "title": "厚生労働省認可の医薬部外品！制汗×殺菌のW有効成分がニオイの元を完全封鎖",
        "body": "ただの香料で誤魔化す市販デオドラントとは次元が違う。汗腺を引き締めて汗の出口を抑える『制汗有効成分』と、体臭の元凶である皮膚常在菌を徹底的に退治する『殺菌有効成分』をダブル配合。朝ひと塗りするだけで、日中の活動時間中ずっと雑菌の繁殖を許さず、嫌な酸っぱい酸臭やワキガ臭を根こそぎシャットアウトする。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_2_d_20260108164707",
        "imageAlt": "ウィルクレンズ 薬用デオドラントスティック 汗とニオイを根本から抑える密着力"
    },
    {
        "title": "手を汚さず10秒で密着完了！忙しい朝を劇的に変える繰り出し式スティック設計",
        "body": "クリームを手にとってワキや足に塗り込み、ベタついた手を石鹸で洗い流す…そんな面倒な作業は一切不要。底をクルッと回してスティックを繰り出し、肌の上を2〜3往復滑らせるだけでケア完了。片手で手軽に扱えるため、出かける直前の10秒で完全無臭バリアを張ることができる。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_3_d_20260108164712",
        "imageAlt": "ウィルクレンズ 薬用デオドラント 手を汚さずサッと塗れるスティック設計"
    },
    {
        "title": "速乾サラサラ＆白残りゼロ！黒Tシャツやワイシャツにも安心の服移り防止処方",
        "body": "デオドラントにありがちな『塗った後のベタつきで服を着るのが不快』『黒いインナーが白く汚れて恥ずかしい』といったストレスを徹底排除。塗った瞬間にパウダー状にサラリと変化する速乾処方により、塗布直後にシャツやインナーを着用しても色移りやシミの心配が一切ない。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_4_d_20260108164717",
        "imageAlt": "ウィルクレンズ 速乾サラサラで白残りしない快適な使用感"
    },
    {
        "title": "ワキだけじゃない！座敷飲み会で致命傷になる足の指・足裏の激臭にも完全マルチ対応",
        "body": "冬の革靴やブーツ、長時間のスニーカー通勤で蒸れ切った足裏は、雑菌にとって最高の繁殖地帯。ウィルクレンズはワキだけでなく、足の指の間や足裏への直塗りにもマルチに対応。居酒屋の座敷に上がる瞬間や友人の家に上がるときでも、モワッとした納豆臭・ムレ臭を完全に封じ込める。",
        "imageUrl": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_7_d_20260108164728",
        "imageAlt": "ウィルクレンズ 気になる部位にマルチに使えるエチケットケア"
    }
]

new_post = {
    "slug": "willclense-medicated-deodorant-stick",
    "title": "「冬は汗かかないから無臭」は大嘘！密室の強烈ムレ臭を10秒で完全封殺するウィルクレンズ薬用デオドラントスティック徹底検証",
    "excerpt": "デオドラントは夏だけ？その致命的な勘違いが、暖房の効いた電車やオフィスで周囲を地獄のスメハラに巻き込んでいる！制汗×殺菌の医薬部外品W処方でワキも足指も10秒完全無臭化するウィルクレンズの真価を塾長が熱血解説！",
    "category": "ニオイ・体臭対策",
    "categoryEn": "odor-sweat",
    "date": "2026.10.26",
    "readTime": "8 min read",
    "heroImage": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_i_20260108164641",
    "tags": [
        "#デオドラント",
        "#ウィルクレンズ",
        "#体臭対策",
        "#ワキガ対策",
        "#チー牛脱却",
        "#メンズコスメ",
        "#清潔感"
    ],
    "intro": data["intro"],
    "targetAudience": data["targetAudience"],
    "problemStatement": data["problemStatement"],
    "comparisonTable": [
        {
            "name": "ウィルクレンズ 薬用デオドラントスティック 20g（医薬部外品）",
            "brand": "ウィルクレンズ（WILLCLENSE）",
            "category": "ニオイ・体臭対策",
            "targetSkin": "全肌質・高機能",
            "feature": data["productAnalysis"]["feature"],
            "price": "¥2,480",
            "pros": data["productAnalysis"]["pros"],
            "cons": data["productAnalysis"]["cons"],
            "imageUrl": "https://item-shopping.c.yimg.jp/i/n/mensproud_wcbs1-1_i_20260108164641",
            "affiliateUrl": "https://yahoo.jp/ssjmZp",
            "rating": 4.72,
            "reviewCount": 1680,
            "bestFor": data["productAnalysis"]["bestFor"],
            "dailyCost": data["productAnalysis"]["dailyCost"],
            "deepReview": data["productAnalysis"]["deepReview"]
        }
    ],
    "conclusion": data["conclusion"],
    "views": 5480,
    "beforeAfter": data["beforeAfter"],
    "selectionCriteria": data["selectionCriteria"],
    "usageSteps": data["usageSteps"],
    "faqs": data["faqs"],
    "synergyTip": {
        "text": "この記事のウィルクレンズとあわせて『靴を脱いだ瞬間の納豆臭・ムレ臭を強制封印！活性炭＆銀イオンで無臭を保つ最強消臭インソール4選』をチェックしろ！直塗りスティックと消臭インソールの鉄壁ガードで、座敷の飲み会でも一切の隙がない無敵の清潔感を手に入れろ！",
        "targetSlug": "mens-shoes-deodorant-insole-charcoal",
        "targetTitle": "靴を脱いだ瞬間の納豆臭・ムレ臭を強制封印！活性炭＆銀イオンで無臭を保つ最強消臭インソール4選"
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

print("Successfully injected new remade Wilcleanse post into posts.json! Total posts:", len(posts))
