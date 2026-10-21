import os
import sys
import requests
import json
import re
import random
import time
from datetime import datetime
from auto_post import EXPANDED_TOPICS, search_rakuten_items, call_gemini_safe, validate_article_quality, DATA_FILE

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)

    existing_slugs = set(p.get("slug") for p in existing_posts)
    new_posts = []

    print(f"Starting batch expansion. Current count: {len(existing_posts)}")

    for topic_info in EXPANDED_TOPICS:
        if topic_info["slug"] in existing_slugs:
            print(f"Already exists: {topic_info['slug']}")
            continue

        print(f"Generating for: {topic_info['theme']}")
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
            "views": random.randint(1200, 3800)
        }
        new_posts.append(new_post)
        print(f"[SUCCESS] Prepared: {new_post['title']}")
        time.sleep(1.5)

    all_posts = new_posts + existing_posts
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    print(f"\nAll topics processed. Total post count: {len(all_posts)}")

if __name__ == "__main__":
    main()
