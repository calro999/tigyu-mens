import urllib.request
import json
import ssl
import time
import os
import sys

DATA_FILE = "data/posts.json"
PROGRESS_FILE = "data/enrich_progress.json"

env_vars = {}
with open('.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env_vars[k.strip()] = v.strip('\"\'')
key = env_vars.get('GEMINI_API_KEY')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 規則に従い利用可能最新Geminiモデルをローテーション
MODELS = [
    'gemini-3.5-flash',
    'gemini-3.1-flash-lite',
    'gemini-3.5-flash-lite',
    'gemini-3.6-flash'
]
current_model_idx = 0

posts = json.load(open(DATA_FILE))

# 進捗の読み込み
progress = {}
if os.path.exists(PROGRESS_FILE):
    try:
        progress = json.load(open(PROGRESS_FILE))
    except Exception:
        progress = {}

# 更新対象のアイテムを収集
# キー: f"{p_idx}_{item_idx}"
items_to_process = []
for p_idx, p in enumerate(posts):
    cat = p.get('category', 'スキンケア・身だしなみ')
    title = p.get('title', '')
    for i_idx, item in enumerate(p.get('comparisonTable', [])):
        key_id = f"{p_idx}_{i_idx}"
        dr = item.get('deepReview', '')
        # すでに進捗ファイルにあるか、高品質な個別レビューが既にある場合はスキップ
        if key_id in progress:
            continue
        needs_update = (
            not dr 
            or '乾燥肌・敏感肌（または初心者・コスパ重視）の男子が抱える' in dr 
            or 'にフォーカスした実力派モデルだ。★' in dr
            or '悩みに特化した処方。ベタつかず毎日の習慣に無理なく取り入れられる清潔感アップ設計' in item.get('feature', '')
        )
        if needs_update:
            items_to_process.append({
                'key_id': key_id,
                'p_idx': p_idx,
                'i_idx': i_idx,
                'post_title': title,
                'category': cat,
                'name': item.get('name', ''),
                'brand': item.get('brand', ''),
                'price': item.get('price', ''),
                'targetSkin': item.get('targetSkin', '')
            })

print(f"Total items needing update: {len(items_to_process)}")
print(f"Already completed in progress file: {len(progress)}")

if not items_to_process:
    print("All items are already enriched!")
    sys.exit(0)

SYSTEM_PROMPT = """
あなたはメンズ美容・身だしなみ改善メディアのカリスマ編集長（塾長）です。
各商品について、読者が心の中で抱く「買わない10個の壁」（価格への躊躇、面倒・続かない、ベタつき・使用感の違和感、肌トラブル・刺激の不安、男が使う恥ずかしさ・周囲の目、安物市販品で十分という思い込み、匂いの心配、使い切れない不安、効果実感への疑念、失敗への後悔）を先回りして完全に払拭し、自然と「これなら欲しい」と思わせる本音の徹底レビュー（deepReview）と、最適な対象者（bestFor）、および魅力的な特徴（feature）を生成してください。

【絶対遵守ルール】
1. 記事内に「買わない理由」「デメリット」等のネガティブ見出しや箇条書きは絶対に入れないこと。あくまで「選ぶべき本質的な魅力」として自然に溶け込ませる。
2. AI臭いテンプレ表現（「〜に特化した実力派モデルだ」「太鼓判を押す」「〜におすすめです」の機械的繰り返し）は厳禁。
3. 全て独立した内容として、同じ文章をテンプレートとしたり使い回したりするのは禁止。
4. 語り口は「本音でアドバイスする兄貴分・塾長」のトーン（だ、である、〜しよう等）。
5. 各商品の特徴、日常でのリアルな使い勝手、朝夜のルーティンへの組み込みやすさ、コスパの納得感（安物との決定的な違い）を具体的に描写すること。
6. 文字数：
   - feature: 45〜70文字（商品の決定的な強み）
   - deepReview: 160〜230文字（買わない心理的障壁を先回りして解消し、魅力を伝えるレビュー）
   - bestFor: 35〜55文字（刺さるターゲット像）

以下のJSONフォーマット（各key_idをキーとしたオブジェクト）のみを返してください：
{
  "key_id": {
    "feature": "...",
    "deepReview": "...",
    "bestFor": "..."
  }
}
"""

def call_gemini(batch):
    global current_model_idx
    user_payload = []
    for it in batch:
        user_payload.append({
            'key_id': it['key_id'],
            'article_title': it['post_title'],
            'category': it['category'],
            'name': it['name'],
            'brand': it['brand'],
            'price': it['price'],
            'targetSkin': it['targetSkin']
        })

    prompt = f"{SYSTEM_PROMPT}\n\n入力商品リスト:\n{json.dumps(user_payload, ensure_ascii=False, indent=2)}"
    payload = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'response_mime_type': 'application/json'
        }
    }

    max_attempts = 8
    for attempt in range(max_attempts):
        m = MODELS[current_model_idx % len(MODELS)]
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}'
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                text = data['candidates'][0]['content']['parts'][0]['text']
                res_json = json.loads(text)
                return res_json
        except Exception as e:
            print(f"Model {m} failed (attempt {attempt+1}): {e}")
            current_model_idx = (current_model_idx + 1) % len(MODELS)
            time.sleep(2)
    raise RuntimeError("Failed to generate batch after max attempts")

BATCH_SIZE = 8
total_batches = (len(items_to_process) + BATCH_SIZE - 1) // BATCH_SIZE

print(f"Processing {len(items_to_process)} items in {total_batches} batches of up to {BATCH_SIZE}...")

for b_idx in range(total_batches):
    start = b_idx * BATCH_SIZE
    end = min(start + BATCH_SIZE, len(items_to_process))
    batch = items_to_process[start:end]

    print(f"\n--- Batch {b_idx + 1}/{total_batches} (items {start+1} to {end}) ---")
    try:
        results = call_gemini(batch)
        for it in batch:
            k = it['key_id']
            if k in results:
                progress[k] = results[k]
                p_i = it['p_idx']
                i_i = it['i_idx']
                res_obj = results[k]
                if res_obj.get('feature'):
                    posts[p_i]['comparisonTable'][i_i]['feature'] = res_obj['feature']
                if res_obj.get('deepReview'):
                    posts[p_i]['comparisonTable'][i_i]['deepReview'] = res_obj['deepReview']
                if res_obj.get('bestFor'):
                    posts[p_i]['comparisonTable'][i_i]['bestFor'] = res_obj['bestFor']
                print(f"  [OK] {it['brand']} {it['name'][:20]}")
            else:
                print(f"  [MISSING KEY] {k}")

        # 各バッチごとに中間保存（途中クラッシュ防止）
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        with open(DATA_FILE, 'w') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

        time.sleep(1.5)  # レートリミット回避

    except Exception as e:
        print(f"Error in batch {b_idx + 1}: {e}")
        time.sleep(5)

print("\nAll batches completed successfully!")
