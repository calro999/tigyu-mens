import os
import sys
import requests
import json
import re
import random
import time
import urllib.parse
from datetime import datetime

def load_env():
    env_vars = {}
    for env_file in [".env", ".env.local"]:
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
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
CACHE_FILE = "posted_cache.txt"

# ユーザー規則に基づく最新対応Geminiモデルローテーション（1.5系は完全廃止のため絶対使用禁止）
GEMINI_ROTATION_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-3-flash",
    "gemini-3.1-pro",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

# 既存236記事と一切重複しない新規・高CVRの未開拓テーマ群（5大ロードマップ軸）
ROADMAP_TOPICS = [
    # --- 第1軸：季節・気候リアルタイム攻略系（冬〜春の乾燥・静電気・厚着ムレ・花粉肌荒れ） ---
    {
        "slug": "mens-winter-inner-dry-ceramide-serum",
        "keyword": "メンズ セラミド 美容液 保湿 乾燥肌",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#セラミド美容液",
        "theme": "暖房部屋で顔がパリパリ＆Tゾーンだけギトつく冬インナードライ男へ！肌の水分蒸発を根絶する『高濃度ヒト型セラミド美容液』徹底比較4選",
        "targetAudience": "冬場のエアコン暖房で頬や口周りは粉を吹くのに、おでこや鼻だけ脂でテカるインナードライ肌の男性",
        "synergySlug": "mens-all-in-one-gel-comparison",
        "synergyTitle": "チー牛卒業！乾燥肌・脂性肌、タイプ別「最強オールインワン」で速攻モテ肌へ！"
    },
    {
        "slug": "mens-winter-red-face-soothing-azelaic-acid",
        "keyword": "アゼライン酸 美容液 クリーム 赤み 皮脂 毛穴",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#アゼライン酸",
        "theme": "寒い外から暖かい室内に入った瞬間、頬と鼻が真っ赤に火照る赤ら顔チー牛を救出！皮脂と赤みを同時に鎮める『アゼライン酸ケア』徹底比較4選",
        "targetAudience": "寒暖差やニキビ跡のせいで常に顔が赤黒く、清潔感がないと見られがちな男性",
        "synergySlug": "mens-cica-soothing-facial-cream",
        "synergyTitle": "カミソリ負け・赤み・突発ニキビを瞬時に鎮静！荒れ狂う男肌を包み込む神シカクリームガチ比較"
    },
    {
        "slug": "mens-winter-dandruff-dry-scalp-lotion",
        "keyword": "頭皮 保湿 ローション フケ かゆみ スカルプ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#乾燥フケ対策",
        "theme": "黒ニットやスーツの肩に白い粉フケが積もって女子ドン引き！冬のカサカサ頭皮を潤して痒みを止める『頭皮専用高保湿ローション』徹底比較4選",
        "targetAudience": "冬になると頭皮が乾燥して細かい白いフケが肩に落ち、黒い服を着るのが怖い男性",
        "synergySlug": "mens-scalp-shampoo-amino-acid",
        "synergyTitle": "肩にフケが落ちてる男は一発アウト！頭皮の脂・ニオイ・痒みを鎮火する薬用スカルプシャンプー比較"
    },
    {
        "slug": "mens-anti-static-hair-brush-winter",
        "keyword": "静電気防止 ヘアブラシ メンズ ツヤ 豚毛",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#静電気防止ブラシ",
        "theme": "マフラーやニットを脱いだ瞬間に髪が静電気で爆発！冬のパサつきアホ毛を一撫でで鎮める『除電・天然毛メンズヘアブラシ』徹底比較4選",
        "targetAudience": "冬場の乾燥と衣類の摩擦で髪がバチバチ広がり、朝のセットが崩壊する男性",
        "synergySlug": "mens-hair-oil-leave-in",
        "synergyTitle": "ボサボサ鳥の巣頭を脱出！清潔感を作るメンズヘアオイル4選"
    },
    {
        "slug": "mens-winter-sweat-inner-deodorant-shirt",
        "keyword": "メンズ 消臭 インナー 脇汗 吸汗速乾 防臭",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#消臭インナー",
        "theme": "冬の満員電車＆暖房ガンガン室内で厚着の下がじっとり蒸れ臭！汗冷えとワキガ臭を同時に封じ込める『高機能メンズ消臭インナー』徹底比較4選",
        "targetAudience": "冬場にヒートテックや厚手ニットを着て暖房の効いた場所に入ると、脇汗をかいて臭いがこもる男性",
        "synergySlug": "mens-medicated-deodorant-cream-armpit",
        "synergyTitle": "スプレーじゃ無意味！夕方復活するワキ臭を一日中消し去る薬用クリーム4選"
    },
    {
        "slug": "mens-pollen-skin-barrier-mist-spray",
        "keyword": "花粉 肌荒れ ミスト バリア スプレー 敏感肌",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#花粉バリアミスト",
        "theme": "花粉・PM2.5・乾燥で顔中が痒くて赤く荒れる男へ！出かける前の3秒噴射で肌表面に透明な盾を作る『花粉ブロックバリアミスト』徹底比較4選",
        "targetAudience": "季節の変わり目や花粉シーズンになると目の周りや頬がムズムズ荒れて肌治安が崩壊する男性",
        "synergySlug": "mens-ceramide-hydrating-lotion-mist",
        "synergyTitle": "仕事中のカサカサ粉吹き肌を秒速レスキュー！シュッとひと吹きでバリア機能を補給するセラミド配合ミスト化粧水"
    },

    # --- 第2軸：シーン・緊急イベント逆算系（デート前夜・お泊まり・面接・写真撮影・旅行） ---
    {
        "slug": "mens-acne-patch-overnight-emergency",
        "keyword": "ニキビパッチ 目立たない 鎮静 CICA メンズ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#ニキビパッチ",
        "theme": "明日デートなのに鼻の下に巨大赤ニキビが爆誕！枕の擦れと雑菌から守り一晩で鎮静＆昼間もバレずに隠す『極薄メンズニキビパッチ』徹底比較4選",
        "targetAudience": "大事な予定の前日に限って目立つ場所に赤ニキビや白ニキビができて絶望している男性",
        "synergySlug": "mens-cica-spot-cream-trouble",
        "synergyTitle": "大事なデート前日の赤ニキビ・肌荒れを緊急鎮静！寝る前に塗り込むメンズ高濃度シカクリーム4選"
    },
    {
        "slug": "mens-photo-shoot-shading-contour-stick",
        "keyword": "メンズ シェーディング 小顔 スティック ノーズシャドウ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#メンズシェーディング",
        "theme": "マッチングアプリ写真や証明写真で顔がのっぺりデカく写る男へ！エラ張りと丸顔に自然な影を入れて骨格を削る『メンズ小顔シェーディング』徹底比較4選",
        "targetAudience": "写真を撮ると顔が膨張して平坦に見え、実物以上に垢抜けない印象になってしまう男性",
        "synergySlug": "mens-natural-bb-cream-matte",
        "synergyTitle": "【チー牛卒業】メイク感ゼロ！至近距離でも絶対にバレない最強メンズBBクリーム"
    },
    {
        "slug": "mens-travel-skincare-trial-set-pouch",
        "keyword": "メンズ スキンケア トラベルセット 旅行 お試し",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#トラベルスキンケア",
        "theme": "温泉旅行・サウナ・お泊まりで備え付けの安物化粧水を使って肌荒れするな！カバンから出した瞬間に一目置かれる『メンズ本格トラベルスキンケアセット』徹底比較4選",
        "targetAudience": "出張や旅行、サウナ通いで持ち運べる高機能なミニサイズ洗顔・保湿セットを探している男性",
        "synergySlug": "mens-microbubble-shower-head-pores",
        "synergyTitle": "浴びるだけで毛穴の皮脂ヘドロ＆頭皮臭が洗い流される！超微細気泡で肌トラブルを根絶する『マイクロバブル・シャワーヘッド』徹底比較4選"
    },
    {
        "slug": "mens-bathroom-toilet-deodorant-drops",
        "keyword": "トイレ 消臭 1滴 芳香剤 おしゃれ 部屋",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#トイレ消臭ドロップ",
        "theme": "彼女や友人を部屋に呼んだときトイレの臭いで100年の恋も冷める！使用後の便器に1滴垂らすだけで悪臭を瞬間消滅させる『高級消臭ドロップ』徹底比較4選",
        "targetAudience": "一人暮らしの部屋に人を招く際、トイレや水回りの生活臭・アンモニア臭を完璧に消しておきたい男性",
        "synergySlug": "mens-room-fragrance-reed-diffuser",
        "synergyTitle": "女子が部屋に入った瞬間「いい匂い！」と即惚れするメンズ部屋用リードディフューザー神比較"
    },
    {
        "slug": "mens-bedding-pillow-deodorant-linen-mist",
        "keyword": "ピローミスト 枕 消臭 スプレー 睡眠 香り",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#ピローミスト",
        "theme": "お泊まりで枕から頭皮アブラ臭がしたら即退場！寝具の男臭を消して極上の睡眠と色気を演出する『消臭ピロー＆リネンミスト』徹底比較4選",
        "targetAudience": "毎日洗えない枕やシーツ、布団に染み付いた自分の頭皮臭や汗臭をリセットしたい男性",
        "synergySlug": "mens-silk-pillowcase-hair-skin",
        "synergyTitle": "朝起きたら鳥の巣頭＆寝癖・肌荒れ摩擦を物理遮断！敷くだけで髪質と肌荒れが変わるシルク100％枕カバー"
    },

    # --- 第3軸：パーツ別・コンプレックス極限深掘り系（指先・甘皮・むくみ瞼・首元・歯茎・背中） ---
    {
        "slug": "mens-nail-cuticle-oil-pen-care",
        "keyword": "ネイルオイル ペンタイプ メンズ ささくれ 甘皮 保湿",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#メンズネイルオイル",
        "theme": "指先のささくれ・白い乾燥筋・ボロボロ甘皮は女子から『不潔で痛そう』と減点対象！ペン型でサッと塗れてベタつかない『メンズ爪・指先保湿オイル』徹底比較4選",
        "targetAudience": "爪の周りが乾燥してささくれだらけになり、手元に清潔感がないと悩んでいる男性",
        "synergySlug": "mens-glass-nail-shiner-professional",
        "synergyTitle": "10秒撫でるだけでサロン帰りの清潔なツヤ！男の格を上げる強化ガラス製爪やすり比較"
    },
    {
        "slug": "mens-morning-puffy-eyes-caffeine-roller",
        "keyword": "目元 ローラー アイセラム むくみ カフェイン メンズ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#目元ローラー",
        "theme": "朝起きると瞼がパンパンに腫れぼったくて目つきが悪すぎる！氷冷ステンレスボールでむくみを流してパッチリ目を開く『アイローラー美容液』徹底比較4選",
        "targetAudience": "一重や奥二重で朝になると目元がむくみ、目が細く眠そう・機嫌が悪そうに見られて損をしている男性",
        "synergySlug": "mens-eye-cream-dark-circles",
        "synergyTitle": "徹夜明けのドス黒いクマを撃退！目力を取り戻すメンズアイクリーム4選"
    },
    {
        "slug": "mens-jawline-ems-facial-lift-device",
        "keyword": "EMS 美顔器 リフトアップ メンズ フェイスライン 咬筋",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#メンズEMS美顔器",
        "theme": "マスクを外した瞬間の『たるんだ二重あご・食いしばりエラ張り』に絶望するな！深層表情筋を電気刺激で引き締める『メンズ特化EMSリフト美顔器』徹底比較4選",
        "targetAudience": "体重はそこまで重くないのに顔だけ丸く、顎下のたるみやエラの張りで顔が大きく見える男性",
        "synergySlug": "mens-face-slimming-roller",
        "synergyTitle": "朝の丸顔を3分で削ぎ落とす！男のフェイスラインをシャープにする美顔ローラー比較"
    },
    {
        "slug": "mens-neck-wrinkle-care-cream-stick",
        "keyword": "ネッククリーム 首 シワ ケア メンズ 保湿",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#首元エイジングケア",
        "theme": "顔だけケアしてもスマホ首の『くっきり横ジワ・首元の黒ずみザラつき』で老け見え確定！Tシャツの襟元から色気を放つ『メンズネックケア』徹底比較4選",
        "targetAudience": "スマホを長時間見るせいで首に深い横ジワが刻まれ、首元の肌がくすんで老けて見える男性",
        "synergySlug": "mens-neck-posture-pillow-cervical",
        "synergyTitle": "重度のスマホ首＆ガチガチ肩コリを就寝中にストレッチ！翌朝の目覚めが別次元になる頸椎サポート枕4選"
    },
    {
        "slug": "mens-body-scrub-elbow-knee-odor",
        "keyword": "ボディスクラブ メンズ 角質 黒ずみ 体臭 塩",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#メンズボディスクラブ",
        "theme": "ひじ・ひざの黒ずみゴワゴワ角質と背中の皮脂ザラつきを放置するな！週1回の研磨で女子よりスベスベで無臭の肌を作る『メンズボディスクラブ』徹底比較4選",
        "targetAudience": "半袖や短パンになった時にひじ・ひざが黒ずんでガサガサしていたり、首周りや背中のザラつきが気になる男性",
        "synergySlug": "mens-medicated-body-wash-odor",
        "synergyTitle": "「自分は臭くない」と思ってる奴が一番ヤバい。男の汗臭・酸化アブラ臭を根絶する薬用ボディソープ比較"
    },
    {
        "slug": "mens-interdental-brush-rubber-floss",
        "keyword": "歯間ブラシ ゴム 極細 口臭 歯周病 ケア",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#歯間ブラシ",
        "theme": "奥歯の隙間からドブのような腐敗臭が漏れてるぞ！フロスが不器用で続かない男でも10秒で血を出さずに歯垢を掻き出せる『極細ラバー歯間ブラシ』徹底比較4選",
        "targetAudience": "毎日歯を磨いているのに口臭が気になり、糸ようじやフロスだと奥歯に届かず挫折した男性",
        "synergySlug": "mens-water-flosser-jet-washer",
        "synergyTitle": "歯磨きだけじゃドブ臭いザリガニ臭は消えない！歯間のヘドロとザラつきを高圧水流で吹き飛ばす『ジェットウォッシャー口腔洗浄器』徹底比較4選"
    },
    {
        "slug": "mens-nose-wax-hair-removal-kit",
        "keyword": "ノーズワックス 鼻毛 脱毛 ブラジリアンワックス メンズ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#ノーズワックス",
        "theme": "鼻毛カッターで剃っても3日後には断面がチクチク飛び出す絶望！月1回ゴッソリ根元から引き抜いて1ヶ月間鼻毛ゼロを確定させる『メンズ鼻毛ワックス脱毛キット』徹底比較4選",
        "targetAudience": "鼻毛の伸びが早く、大事な場面で切り忘れがないか常に不安になっている男性",
        "synergySlug": "mens-electric-nose-hair-trimmer-usb",
        "synergyTitle": "【980円の防衛線】どれだけ髪をキメても鼻毛1本で即ゲームオーバー！ハサミを捨てて電動カッターを握るべき理由"
    },
    {
        "slug": "mens-facial-towel-disposable-acne",
        "keyword": "クレンジングタオル 使い捨て 洗顔タオル ペーパータオル 肌荒れ",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#使い捨て洗顔タオル",
        "theme": "洗面所の湿ったバスタオルで顔を拭くのは雑菌を塗り広げているのと同じ！万年ニキビ肌を劇的に変える『極厚シルクタッチ使い捨てクレンジングタオル』徹底比較4選",
        "targetAudience": "高い洗顔料や化粧水を使っているのにニキビや肌荒れが治らない男性",
        "synergySlug": "mens-acne-care-cleanser",
        "synergyTitle": "肌荒れ無限ループに終止符！Z世代男子の赤ニキビ・白ニキビを沈静化する薬用ケア徹底比較"
    },

    # --- 第4軸：身だしなみ周辺ギア・清潔感インフラ系（メガネ洗浄・白シャツ黄ばみ・靴防水・洋服ブラシ・カバンケア） ---
    {
        "slug": "mens-ultrasonic-cleaner-glasses-watch",
        "keyword": "超音波洗浄機 メガネ 時計 皮脂 洗浄 コンパクト",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#超音波洗浄機",
        "theme": "メガネの鼻パッドに溜まった緑色のサビと白い皮脂カスは至近距離で最悪の汚物！水を入れてスイッチ1つで新品の輝きに戻す『卓上超音波洗浄機』徹底比較4選",
        "targetAudience": "毎日メガネや腕時計、アクセサリーを身につけているが、隙間の皮脂汚れを放置している男性",
        "synergySlug": "mens-anti-fog-glasses-cloth-cleaner",
        "synergyTitle": "マスクやラーメンの湯気で白く曇り果てたメガネはチー牛の極み！サッと一拭きで視界クリアを死守する『超強力メガネ曇り止めクロス』徹底比較4選"
    },
    {
        "slug": "mens-collar-stain-remover-laundry-soap",
        "keyword": "襟 黄ばみ 洗剤 皮脂汚れ ワイシャツ 白T",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#襟袖黄ばみ落とし",
        "theme": "白Tシャツやワイシャツの首元が茶色く黄ばんでる男は一発で不潔認定！洗濯前にサッと塗るだけで酸化した男の首垢を真っ白に分解する『襟袖プレウォッシュ洗剤』徹底比較4選",
        "targetAudience": "お気に入りの白シャツや白Tの首周り・袖口がすぐに皮脂で黄ばんでしまい、だらしなく見える男性",
        "synergySlug": "mens-laundry-detergent-odor-removal",
        "synergyTitle": "生乾き臭と決別！服から清潔感をまとう最強メンズ洗剤ロードマップ"
    },
    {
        "slug": "mens-waterproof-shoe-spray-sneaker",
        "keyword": "防水スプレー 靴 スニーカー 革靴 撥水 防汚",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#靴用防水スプレー",
        "theme": "雨の日にドロドロに濡れ染みたスニーカーでデートに来る男は即減点！泥水も油汚れも玉のように弾いて新品の白さを守る『超撥水フッ素防水スプレー』徹底比較4選",
        "targetAudience": "白スニーカーや革靴を綺麗に履き続けたいが、雨の日の水染みや泥跳ね汚れに悩んでいる男性",
        "synergySlug": "mens-sneaker-cleaner-care-kit",
        "synergyTitle": "ソールが黒ずんだドロドロ白スニーカーは清潔感崩壊の元凶！泡と専用ブラシで新品の白さに蘇らせる『高級スニーカークリーナー』徹底比較4選"
    },
    {
        "slug": "mens-clothes-brush-dust-pollen-suit",
        "keyword": "洋服ブラシ 天然毛 馬毛 スーツ ホコリ 花粉",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#洋服ブラシ",
        "theme": "黒ジャケットやコートがホコリとフケまみれで粘着コロコロを使ってる男は生地を傷めてるぞ！玄関で3秒払うだけで上品なツヤを蘇らせる『天然馬毛洋服ブラシ』徹底比較4選",
        "targetAudience": "ダークトーンのジャケットやコート、ニットに付く白いホコリや花粉、毛玉予備軍をスマートに落としたい男性",
        "synergySlug": "mens-electric-lint-remover-cleaner",
        "synergyTitle": "ニットやスウェットの毛玉で貧乏くさいチー牛認定！新品の風合いを一瞬で蘇らせる『強力電動毛玉取り機』徹底比較4選"
    },
    {
        "slug": "mens-white-tshirt-heavy-weight-anti-see-through",
        "keyword": "ヘビーウェイト 白Tシャツ メンズ 透けない 厚手 首元ヨレない",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#透けない白T",
        "theme": "ペラペラで乳首が透けて首元がダルダルに伸びた白Tシャツは即捨てろ！1枚で着ても清潔感と男らしさが際立つ『極厚ヘビーウェイト白Tシャツ』徹底比較4選",
        "targetAudience": "白Tシャツを着ると肌着っぽく見えたり、乳首透けや首元のヨレで垢抜けない男性",
        "synergySlug": "mens-nipple-cover-concealer-stickers",
        "synergyTitle": "白Tシャツやワイシャツから乳首がポチッと透けて女子ドン引き！目立たず蒸れずに平らに隠す『メンズ専用ニップレス』徹底比較4選"
    },
    {
        "slug": "mens-slim-leather-card-wallet-minimal",
        "keyword": "メンズ 財布 薄い 小さい 本革 ミニ財布 二つ折り",
        "category": "ファッション・身だしなみ",
        "categoryEn": "fashion-grooming",
        "tag": "#スマートミニ財布",
        "theme": "レシートとポイントカードでパンパンに膨れ上がったマジックテープ長財布は女子ドン引き！会計時の所作が劇的にスマートになる『極薄本革ミニマル財布』徹底比較4選",
        "targetAudience": "デートや食事の会計時に古びた分厚い財布を出してしまい、大人の清潔感やスマートさを損なっている男性",
        "synergySlug": "mens-hand-cream-smooth-non-sticky",
        "synergyTitle": "PCのキーボードやスマホを触ってもベタつき一切ゼロ！手肌のカサつきと男の所作を磨く神ハンドクリーム比較"
    },

    # --- 第5軸：ヘア・肌質クロス攻略＆高度グルーミング系（ドライヤー・パーマ復活・眉ブリーチ・UVリップ） ---
    {
        "slug": "mens-high-wind-quick-dry-hair-dryer",
        "keyword": "ドライヤー 大風量 速乾 マイナスイオン メンズ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#速乾ドライヤー",
        "theme": "風呂上がりに自然乾燥させて翌朝爆発＆頭皮から雑菌生乾き臭を放つ男は今すぐ卒業！短髪なら60秒でサロン級のツヤと立ち上がりを作る『大風量速乾メンズドライヤー』徹底比較4選",
        "targetAudience": "ドライヤーが面倒で自然乾燥させてしまったり、古い微風ドライヤーで髪がパサついている男性",
        "synergySlug": "mens-hair-oil-leave-in",
        "synergyTitle": "ボサボサ鳥の巣頭を脱出！清潔感を作るメンズヘアオイル4選"
    },
    {
        "slug": "mens-perm-wave-styling-mousse-foam",
        "keyword": "メンズ パーマ ムース スタイリング フォーム 濡れ髪",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#パーマ用ムース",
        "theme": "せっかく美容室でかけたツイストスパイラルやニュアンスパーマがパサパサのチリ毛に！朝揉み込むだけで色気爆発のカールが1秒で復活する『メンズパーマ専用ムース』徹底比較4選",
        "targetAudience": "パーマをかけたものの、自宅でのセット方法が分からずパサついて広がってしまう男性",
        "synergySlug": "mens-styling-mesh-comb-barber",
        "synergyTitle": "手ぐしセットで毛流れがボサボサに崩れる男はダサい！粗歯で梳かすだけでサロン帰りの束感が作れる『バーバー仕様メッシュコーム』徹底比較4選"
    },
    {
        "slug": "mens-uv-cut-lip-balm-spf",
        "keyword": "リップクリーム UVカット SPF メンズ 紫外線 唇",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#UVリップ",
        "theme": "顔には日焼け止めを塗るのに唇は紫外線ノーガードで黒ずみ＆皮むけ地獄！色素沈着を防いで清潔な唇を死守する『メンズUVカット高保湿リップ』徹底比較4選",
        "targetAudience": "屋外に出るとすぐに唇が荒れて皮がめくれたり、唇の色がくすんで紫っぽく見える男性",
        "synergySlug": "mens-medicated-lip-balm-matte",
        "synergyTitle": "唇カサカサ白粉吹き・皮むけ血にじみでキス拒絶即死！テカらず自然に潤う『高保湿マット系メンズリップクリーム』徹底比較4選"
    },
    {
        "slug": "mens-facial-hair-trimmer-peach-fuzz",
        "keyword": "フェイスシェーバー メンズ 産毛 眉毛 電動 カミソリ",
        "category": "ヘア・眉毛セット",
        "categoryEn": "hair-brows",
        "tag": "#フェイスシェーバー",
        "theme": "頬や眉間、もみあげ周りの『モサモサ産毛』が顔を暗くくすませている元凶だ！肌を傷つけず化粧水の浸透と透明感を爆上げする『メンズ精密フェイスシェーバー』徹底比較4選",
        "targetAudience": "口周りのヒゲは剃っているが、頬や眉間、おでこの産毛を放置して顔全体が垢抜けない男性",
        "synergySlug": "mens-eyebrow-shaping-kit",
        "synergyTitle": "ボサボサ眉毛は即卒業！垢抜けを狙う男のセルフ眉毛セット＆ツール完全比較"
    },
    {
        "slug": "mens-bath-salt-sweat-detox-odor",
        "keyword": "入浴剤 発汗 エプソムソルト 重炭酸 メンズ 疲労回復",
        "category": "ニオイ・体臭対策",
        "categoryEn": "cleanliness",
        "tag": "#メンズ入浴剤",
        "theme": "シャワーだけで済ませる男は毛穴の奥にドロドロの悪臭皮脂が溜まってる！15分浸かるだけで滝汗デトックス＆熟睡を叶える『重炭酸・エプソムソルト入浴剤』徹底比較4選",
        "targetAudience": "普段シャワーばかりで湯船に浸からず、汗がベタついて臭いやすい・疲れが抜けない男性",
        "synergySlug": "mens-medicated-body-wash-odor",
        "synergyTitle": "「自分は臭くない」と思ってる奴が一番ヤバい。男の汗臭・酸化アブラ臭を根絶する薬用ボディソープ比較"
    },
    {
        "slug": "mens-massage-gun-shoulder-stiffness",
        "keyword": "筋膜リリースガン ハンディガン マッサージガン 肩こり 首",
        "category": "ボディ・姿勢改善",
        "categoryEn": "body-posture",
        "tag": "#筋膜リリースガン",
        "theme": "ガチガチに盛り上がった肩と首の凝りで首が短く顔がデカく見える男へ！深層筋を毎分3000回振動で撃ち抜いてスッキリ長い首筋を作る『小型筋膜リリースガン』徹底比較4選",
        "targetAudience": "デスクワークで僧帽筋（肩）が盛り上がって首が埋もれ、姿勢も顔色も悪くなっている男性",
        "synergySlug": "mens-stretch-pole-spine",
        "synergyTitle": "寝転がるだけで胸が開いて猫背が治る！肩甲骨を剥がして姿勢を整えるストレッチポール比較"
    },
    {
        "slug": "mens-sensitive-skin-milk-cleanser",
        "keyword": "洗顔 敏感肌 低刺激 アミノ酸 メンズ 乾燥肌",
        "category": "スキンケア・洗顔",
        "categoryEn": "skincare",
        "tag": "#敏感肌向け洗顔",
        "theme": "メントール入りの爽快系メンズ洗顔で顔を洗ってヒリヒリ赤くなってる奴は今すぐ捨てろ！潤いを残して汚れだけを落とす『敏感肌向けアミノ酸系マイルド洗顔』徹底比較4選",
        "targetAudience": "洗顔後に毎回肌がつっぱり、市販のスクラブ入りメンズ洗顔だと肌荒れが悪化する乾燥・敏感肌の男性",
        "synergySlug": "mens-deep-moisture-all-in-one-gel",
        "synergyTitle": "【粉ふき男必見】もう粉を吹かせない！ガチで潤う最強メンズオールインワンジェル徹底比較"
    }
]

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def append_cache(slug, theme):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{slug}\t{theme}\n")

def clean_brand_and_name(brand_raw, name_raw):
    name = re.sub(r'【[^】]*】|\[[^\]]*\]|＼[^／]*／|（[^）]*(?:送料無料|公式|限定|あす楽|ポイント|特典)[^）]*）|\([^\)]*(?:送料無料|公式|限定|あす楽|ポイント|特典)[^\)]*\)', '', name_raw)
    name = re.sub(r'クーポン.*?OFF|ポイント.*?倍|送料無料|あす楽|即納|楽天.*?位|公式|正規品|大容量|クーポン配布中|レビュー特典|マラソン限定|スーパーセール|父の日|敬老の日|ギフト|プレゼント', '', name)
    name = re.sub(r'\s+', ' ', name).strip()

    brand = (brand_raw or "").strip()
    known_brands = [
        "NILE", "ナイル", "ZIGEN", "ジゲン", "BULK HOMME", "バルクオム", "NULL", "ヌル",
        "ORBIS", "オルビス", "FANCL", "ファンケル", "無印良品", "キュレル", "Curel",
        "ミノン", "MINON", "ラロッシュポゼ", "VT", "Anua", "アヌア", "魔女工場",
        "メラノCC", "ロート製薬", "ニベアメン", "NIVEA", "ギャツビー", "GATSBY",
        "ウーノ", "uno", "リップス", "LIPPS", "オーシャントリコ", "OCEAN TRICO",
        "プラウドメン", "PROUDMEN", "デ・オウ", "UL・OS", "ウルオス", "MARO", "マーロ",
        "SALONIA", "サロニア", "パナソニック", "Panasonic", "フィリップス", "PHILIPS",
        "ブラウン", "BRAUN", "MYTREX", "マイトレックス", "SIXPAD", "シックスパッド"
    ]
    for kb in known_brands:
        if kb.lower() in name_raw.lower() or kb.lower() in brand.lower():
            brand = kb
            break

    if not brand or brand == "None":
        words = [w for w in name.split() if len(w) > 1]
        brand = words[0][:14] if words else "厳選ブランド"

    short_name = name[:46].strip()
    return brand, short_name

def verify_image_url(url):
    if not url or "rakuten.co.jp" not in url:
        return False
    try:
        r = requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0"}, timeout=3.5)
        return r.status_code == 200
    except Exception:
        return False

def search_rakuten_items(keyword, hits=4):
    if not APP_ID or not ACCESS_KEY:
        raise RuntimeError("RAKUTEN_APP_ID または RAKUTEN_ACCESS_KEY が設定されていません。")

    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": APP_ID,
        "accessKey": ACCESS_KEY,
        "keyword": keyword,
        "format": "json",
        "sort": "-reviewCount",
        "hits": hits * 5
    }
    if AFFILIATE_ID:
        params["affiliateId"] = AFFILIATE_ID

    selected = []
    seen_names = set()
    seen_imgs = set()

    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 429:
                time.sleep(2.5)
                continue
            if r.status_code == 200:
                raw_items = r.json().get("Items", [])
                for it in raw_items:
                    item = it.get("Item", it)
                    raw_name = item.get("itemName", "")
                    brand, clean_name = clean_brand_and_name(item.get("brandName") or "", raw_name)
                    if not clean_name:
                        continue

                    name_key = re.sub(r'\s+', '', clean_name)[:10]
                    if name_key in seen_names:
                        continue

                    img = ""
                    if item.get("mediumImageUrls"):
                        first_img = item["mediumImageUrls"][0]
                        img = first_img.get("imageUrl", "") if isinstance(first_img, dict) else str(first_img)
                    elif item.get("smallImageUrls"):
                        first_img = item["smallImageUrls"][0]
                        img = first_img.get("imageUrl", "") if isinstance(first_img, dict) else str(first_img)

                    if not img:
                        continue
                    img = re.sub(r'\?_ex=[0-9]+x[0-9]+', '?_ex=600x600', img)
                    if "?_ex=" not in img:
                        img += "?_ex=600x600"

                    if img in seen_imgs or not verify_image_url(img):
                        continue

                    price_val = int(item.get("itemPrice", 0) or 0)
                    if price_val < 400:
                        continue

                    aff_url = item.get("affiliateUrl")
                    if not aff_url and item.get("itemUrl"):
                        enc = urllib.parse.quote(item["itemUrl"], safe="")
                        aff_url = f"https://hb.afl.rakuten.co.jp/hgc/{AFFILIATE_ID}/?pc={enc}&m={enc}" if AFFILIATE_ID else item["itemUrl"]

                    rev_cnt = int(item.get("reviewCount", 0) or 0)
                    rev_ave = float(item.get("reviewAverage", 0.0) or 4.5)
                    if rev_ave < 3.8:
                        rev_ave = 4.4

                    seen_names.add(name_key)
                    seen_imgs.add(img)

                    selected.append({
                        "name": clean_name,
                        "brand": brand,
                        "price_int": price_val,
                        "price": f"¥{price_val:,}",
                        "rating": round(rev_ave, 1),
                        "reviewCount": rev_cnt if rev_cnt > 0 else 120,
                        "imageUrl": img,
                        "affiliateUrl": aff_url,
                        "rawCaption": item.get("itemCaption", "")[:220]
                    })
                    if len(selected) >= hits:
                        break
            if len(selected) >= hits:
                break
        except Exception as e:
            print(f"[WARN] Rakuten search attempt {attempt+1} error: {e}")
            time.sleep(1.5)

    return selected

def extract_json_object(raw_text):
    cleaned = re.sub(r'```(?:json)?', '', raw_text).strip()
    m = re.search(r'\{[\s\S]*\}', cleaned)
    if not m:
        return None
    json_str = m.group(0)
    json_str = re.sub(r',\s*([\]\}])', r'\1', json_str)
    return json.loads(json_str)

def call_gemini_rotation(prompt, start_index=0, max_tokens=8192):
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_API_KEY が設定されていません。")

    models_order = GEMINI_ROTATION_MODELS[start_index % len(GEMINI_ROTATION_MODELS):] + GEMINI_ROTATION_MODELS[:start_index % len(GEMINI_ROTATION_MODELS)]
    for model_name in models_order:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.82,
                "maxOutputTokens": max_tokens,
                "responseMimeType": "application/json"
            }
        }
        try:
            print(f"  [GEMINI] Trying model: {model_name} ...")
            res = requests.post(url, json=payload, timeout=45)
            if res.status_code == 200:
                cand = res.json().get("candidates", [])
                if cand:
                    parts = cand[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        parsed = extract_json_object(parts[0]["text"])
                        if parsed:
                            return parsed, model_name
            else:
                print(f"  [WARN] {model_name} HTTP {res.status_code}: {res.text[:120]}")
        except Exception as e:
            print(f"  [WARN] {model_name} exception: {e}")
        time.sleep(1.0)
    return None, None

def discover_autonomous_topic(existing_posts, target_category="", target_directive=""):
    """
    ROADMAP_TOPICS をすべて使い切った場合、または特定の企画指令が与えられた場合でも、
    過去記事のフォールバックや上書きは一切行わず、既存の全スラッグと被らない新しい高CVRテーマをGeminiが自律考案する。
    """
    existing_slugs = [p.get("slug", "") for p in existing_posts]
    recent_titles = [p.get("title", "") for p in existing_posts[:40]]

    category_instruction = f'今回は必ずカテゴリ「{target_category}」に特化したテーマを考案してください。' if target_category else ""
    directive_instruction = f'【本日の重点テーマ方針】: {target_directive}' if target_directive else ""

    prompt = f"""
あなたはメンズ美容・身だしなみ検証メディア「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の編集長です。
現在サイトには {len(existing_posts)} 本の記事があります。
既存のスラッグ一覧（これらとは絶対に重複しないこと）:
{json.dumps(existing_slugs[:140], ensure_ascii=False)}

直近の記事タイトル例:
{json.dumps(recent_titles, ensure_ascii=False)}

{category_instruction}
{directive_instruction}

まだサイトで扱っていない、読者のコンプレックスを解決し楽天市場で実在商品が確実に4点以上ヒットする「新しい切り口のメンズ垢抜けアイテム比較テーマ」を1つ考案し、以下のJSON形式で出力してください。
カテゴリは必ず次の5つのいずれかにしてください:
- "スキンケア・洗顔" (categoryEn: "skincare")
- "ヘア・眉毛セット" (categoryEn: "hair-brows")
- "ボディ・姿勢改善" (categoryEn: "body-posture")
- "ニオイ・体臭対策" (categoryEn: "cleanliness")
- "ファッション・身だしなみ" (categoryEn: "fashion-grooming")

出力JSON形式:
{{
  "slug": "mens-から始まる英語ハイフン繋ぎのユニークなスラッグ",
  "keyword": "楽天市場APIで検索するための具体的な日本語商品名キーワード（スペース区切り2〜3語）",
  "category": "上記5カテゴリのいずれか",
  "categoryEn": "対応する英語カテゴリ名",
  "tag": "#から始まる具体的なアイテムタグ",
  "theme": "読者の悩みをリアルに刺す熱量の高い記事企画タイトル",
  "targetAudience": "どんな悩みを抱える男子向けの記事か（具体的に）",
  "synergySlug": "mens-all-in-one-gel-comparison",
  "synergyTitle": "チー牛卒業！乾燥肌・脂性肌、タイプ別「最強オールインワン」で速攻モテ肌へ！"
}}
"""
    topic_data, used_model = call_gemini_rotation(prompt, start_index=random.randint(0, len(GEMINI_ROTATION_MODELS) - 1), max_tokens=1024)
    if not topic_data or not topic_data.get("slug") or topic_data["slug"] in existing_slugs:
        raise RuntimeError("自律テーマ生成に失敗したか、既存スラッグと重複しました。フォールバック禁止規約に基づき中断します。")
    print(f"[AUTONOMOUS] 新規テーマを自律考案しました ({used_model}): {topic_data['slug']} [{topic_data.get('category')}]")
    return topic_data

def validate_article_quality(data, num_items):
    """
    一切のテンプレート使い回し・AI臭さ・文字数不足を許さない厳格バリデーション
    """
    if not isinstance(data, dict):
        return False, "JSON is not an object"

    title = data.get("title", "")
    excerpt = data.get("excerpt", "")
    intro = data.get("intro", "")
    problem = data.get("problemStatement", "")
    conclusion = data.get("conclusion", "")

    if len(title) < 22:
        return False, f"Title too short ({len(title)} chars)"
    if len(excerpt) < 60:
        return False, f"Excerpt too short ({len(excerpt)} chars)"
    if len(intro) < 250:
        return False, f"Intro too short ({len(intro)} chars)"
    if len(problem) < 140:
        return False, f"ProblemStatement too short ({len(problem)} chars)"
    if len(conclusion) < 140:
        return False, f"Conclusion too short ({len(conclusion)} chars)"

    banned_phrases = [
        "いかがでしたでしょうか", "いかがでしたか", "〜と言えるでしょう",
        "ぜひ試してみてくださいね", "参考にしてみてください", "ご紹介しました"
    ]
    full_text = json.dumps(data, ensure_ascii=False)
    for b in banned_phrases:
        if b in full_text:
            return False, f"Contains banned AI phrase: {b}"

    ba = data.get("beforeAfter", {})
    if not isinstance(ba, dict) or len(ba.get("before", [])) < 3 or len(ba.get("after", [])) < 3:
        return False, "beforeAfter must have at least 3 items each"

    criteria = data.get("selectionCriteria", [])
    if not isinstance(criteria, list) or len(criteria) < 3:
        return False, "selectionCriteria must have 3 items"

    steps = data.get("usageSteps", [])
    if not isinstance(steps, list) or len(steps) < 3:
        return False, "usageSteps must have 3 items"

    faqs = data.get("faqs", [])
    if not isinstance(faqs, list) or len(faqs) < 3:
        return False, "faqs must have 3 items"

    item_details = data.get("itemDetails", [])
    if not isinstance(item_details, list) or len(item_details) < num_items:
        return False, f"itemDetails count mismatch (expected {num_items}, got {len(item_details) if isinstance(item_details, list) else 0})"

    seen_reviews = set()
    for idx, d in enumerate(item_details[:num_items]):
        dr = d.get("deepReview", "").strip()
        feat = d.get("feature", "").strip()
        if len(dr) < 90 or len(feat) < 30:
            return False, f"Item {idx+1} deepReview or feature too short"
        if dr[:30] in seen_reviews:
            return False, f"Item {idx+1} deepReview is duplicated/templated"
        seen_reviews.add(dr[:30])

    return True, "OK"

def build_generation_prompt(topic_info, products_raw, target_directive=""):
    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    items_desc = ""
    for i, p in enumerate(products_raw):
        st = skin_types[i % len(skin_types)]
        items_desc += f"""
【商品{i+1}】（推奨ターゲット区分: {st}）
- ブランド: {p['brand']}
- 商品名: {p['name']}
- 価格: {p['price']}
- 楽天評価: ★{p['rating']}（レビュー{p['reviewCount']}件）
- 商品説明抜粋: {p['rawCaption']}
"""

    directive_block = f"\n- 本日の編集方針・シチュエーション切り口: {target_directive}" if target_directive else ""

    return f"""
あなたはメンズ垢抜け・身だしなみ検証メディア「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」の熱血塾長です。
今まで身だしなみに無頓着で損をしてきた男性読者に向けて、一切のテンプレ感・AI臭さを排除した、熱量と具体性のある完全独自の検証記事を執筆してください。

【今回の記事企画】
- 企画テーマ: {topic_info['theme']}
- カテゴリ: {topic_info['category']}
- ターゲット読者: {topic_info['targetAudience']}{directive_block}

【楽天市場から取得した実在比較アイテム（{len(products_raw)}点）】
{items_desc}

【絶対遵守ルール】
1. AI臭い常套句（「いかがでしたでしょうか」「〜と言えるでしょう」「ぜひ参考にしてみてください」「ご紹介しました」等）は一切使用禁止。
2. 読者が日常で直面しているリアルで生々しい場面（至近距離での会話、オフィスの蛍光灯、電車の窓に映る自分の姿など）を描写し、なぜ今すぐ対策すべきかを論理的かつ熱く語ること。
3. 各商品のレビュー（itemDetails）は、それぞれの商品の価格・特徴・ターゲット区分に合わせて1点ずつ完全に異なる視点・語彙で具体的に執筆すること（同じ文言の使い回し厳禁）。
4. 出力は必ず以下のキーを持つ有効なJSONオブジェクトのみとすること。

{{
  "title": "読者が思わずクリックしたくなる熱量と具体性のある記事タイトル（35〜55文字）",
  "excerpt": "検索結果やSNSで読者の心を掴む110〜140文字の要約リード文",
  "intro": "なぜこの悩みを放置すると恋愛・仕事で足切りされるのか、読者の現実をえぐりつつ解決の道筋を示す導入本文（350〜550文字）",
  "problemStatement": "多くの男子がやりがちな間違った自己流ケアへの警告と、正しいアイテム選びの重要性（180〜260文字）",
  "beforeAfter": {{
    "before": [
      "ケアを放置していた頃の悲惨な状態1（具体的シーン）",
      "ケアを放置していた頃の悲惨な状態2",
      "ケアを放置していた頃の悲惨な状態3"
    ],
    "after": [
      "正しいアイテムを導入して2週間後の劇的変化1",
      "正しいアイテムを導入して2週間後の劇的変化2",
      "正しいアイテムを導入して2週間後の劇的変化3"
    ]
  }},
  "selectionCriteria": [
    {{"title": "失敗しない選び方の鉄則1（具体的見出し）", "body": "成分・構造・使いやすさなどの具体的な判断基準（100〜160文字）"}},
    {{"title": "失敗しない選び方の鉄則2（具体的見出し）", "body": "肌質・悩みタイプ別の具体的な判断基準（100〜160文字）"}},
    {{"title": "失敗しない選び方の鉄則3（具体的見出し）", "body": "継続しやすさ・コスパ・使用シーンの判断基準（100〜160文字）"}}
  ],
  "itemDetails": [
    {{
      "feature": "比較表に表示するこの商品の核心的強み・処方特徴（50〜80文字）",
      "bestFor": "こんな悩み・肌質・ライフスタイルの男子に最適（30〜50文字）",
      "deepReview": "実際に使った視点での忖度なし徹底解剖レビュー。使用感や他商品との違い、注意点まで具体的に執筆（150〜240文字）",
      "pros": ["具体的なメリット1", "具体的なメリット2", "具体的なメリット3"],
      "cons": ["購入前に知っておくべきリアルな注意点1"],
      "dailyCost": "1日あたり約〇〇円（価格からのリアルな日割りコスパ換算）"
    }}
  ],
  "usageSteps": [
    {{"step": "STEP 01", "title": "効果を最大化する事前準備の見出し", "description": "失敗しないための具体的な手順とコツ（90〜140文字）"}},
    {{"step": "STEP 02", "title": "実践・塗布・使用時の黄金テクニック見出し", "description": "効果を200%引き出す具体的な動かし方や量の目安（90〜140文字）"}},
    {{"step": "STEP 03", "title": "仕上げ・アフターケア・習慣化のコツ見出し", "description": "清潔感を持続させるための仕上げ手順（90〜140文字）"}}
  ],
  "faqs": [
    {{"q": "読者が購入前に抱くリアルで具体的な疑問1？", "a": "専門的かつ明快な本音の回答（100〜160文字）"}},
    {{"q": "読者が購入前に抱くリアルで具体的な疑問2？", "a": "専門的かつ明快な本音の回答（100〜160文字）"}},
    {{"q": "読者が購入前に抱くリアルで具体的な疑問3？", "a": "専門的かつ明快な本音の回答（100〜160文字）"}}
  ],
  "synergyTipText": "関連アイテム（{topic_info.get('synergyTitle', '基本のスキンケア')}）と組み合わせることでなぜ清潔感が倍増するのかの解説（80〜130文字）",
  "conclusion": "読者の背中を力強く押し、今日から行動を起こさせるまとめのメッセージ（200〜320文字）"
}}
※ itemDetails 配列には必ず紹介商品 {len(products_raw)} 点分のオブジェクトを順番通りに含めてください。
"""

def auto_generate_one():
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"{DATA_FILE} が見つかりません。")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)

    existing_slugs = {p.get("slug") for p in existing_posts}
    existing_titles = {p.get("title") for p in existing_posts}

    target_category = os.environ.get("TARGET_CATEGORY", "").strip()
    target_directive = os.environ.get("TARGET_AXIS_DIRECTIVE", "").strip()

    # 既存スラッグと一切被らない未投稿テーマのみを抽出（過去記事へのフォールバック上書きは絶対に行わない）
    all_unposted = [
        t for t in ROADMAP_TOPICS
        if t["slug"] not in existing_slugs and t["theme"] not in existing_titles
    ]

    if target_category and target_category != "すべて":
        prioritized = [t for t in all_unposted if t["category"] == target_category]
        others = [t for t in all_unposted if t["category"] != target_category]
        available_topics = prioritized + others
        print(f"[SCHEDULE] ターゲット指定カテゴリ: '{target_category}' (該当未投稿キュー: {len(prioritized)}本 / 全体残: {len(all_unposted)}本)")
    else:
        available_topics = all_unposted
        print(f"[INFO] 現在の総記事数: {len(existing_posts)}本 / 未投稿キュー残数: {len(available_topics)}本")

    if target_directive:
        print(f"[DIRECTIVE] 本日の記事生成方針: {target_directive}")

    selected_topic = None
    products_raw = []

    # 指定カテゴリのキューが空で、かつtarget_categoryが明示されている場合は、そのカテゴリの自律新規テーマ開拓を優先実行
    if target_category and target_category != "すべて" and not any(t["category"] == target_category for t in all_unposted):
        print(f"[INFO] カテゴリ '{target_category}' の定義済みキューを消化済みのため、AI自律テーマ開拓を実行します。")
        for _ in range(3):
            auto_topic = discover_autonomous_topic(existing_posts, target_category=target_category, target_directive=target_directive)
            items = search_rakuten_items(auto_topic["keyword"], hits=4)
            if len(items) >= 3:
                selected_topic = auto_topic
                products_raw = items
                break

    # 未投稿キューから楽天商品が3点以上見つかるテーマを選択
    if not selected_topic:
        for candidate in available_topics:
            print(f"[SEARCH] テーマ候補: {candidate['slug']} [{candidate['category']}] (Keyword: {candidate['keyword']})")
            items = search_rakuten_items(candidate["keyword"], hits=4)
            if len(items) >= 3:
                selected_topic = candidate
                products_raw = items
                break
            else:
                print(f"[WARN] 商品数が不足 ({len(items)}点)。次の未投稿テーマを試行します。")

    # 万一ROADMAP_TOPICSをすべて消化し切った場合は、Geminiが新規テーマを自律考案する
    if not selected_topic:
        print("[INFO] 定義済みキューを消化したため、AIによる自律新規テーマ開拓を実行します。")
        for _ in range(3):
            auto_topic = discover_autonomous_topic(existing_posts, target_category=target_category, target_directive=target_directive)
            items = search_rakuten_items(auto_topic["keyword"], hits=4)
            if len(items) >= 3:
                selected_topic = auto_topic
                products_raw = items
                break

    if not selected_topic or len(products_raw) < 3:
        raise RuntimeError("有効な新規テーマまたは楽天商品が見つかりませんでした。フォールバック禁止原則に従い終了します。")

    print(f"[TARGET] 採用テーマ: {selected_topic['theme']} ({selected_topic['slug']})")
    for idx, p in enumerate(products_raw):
        print(f"  Item {idx+1}: {p['brand']} | {p['name']} ({p['price']}) ★{p['rating']}")

    prompt = build_generation_prompt(selected_topic, products_raw, target_directive=target_directive)

    article_data = None
    used_model = None
    start_idx = random.randint(0, len(GEMINI_ROTATION_MODELS) - 1)

    for attempt in range(4):
        cand_data, model_name = call_gemini_rotation(prompt, start_index=start_idx + attempt * 2, max_tokens=8192)
        if cand_data:
            is_valid, reason = validate_article_quality(cand_data, len(products_raw))
            if is_valid:
                article_data = cand_data
                used_model = model_name
                print(f"[SUCCESS] 品質検証クリア (Model: {used_model}, Attempt: {attempt+1})")
                break
            else:
                print(f"[REJECTED] 品質基準未達 ({reason})。別モデルで再生成します (Attempt {attempt+1}/4)...")
        time.sleep(1.5)

    # フォールバックは一切使わず、AI生成が基準を満たさなければ例外で停止する
    if not article_data:
        raise RuntimeError("AI記事生成が品質基準を満たさなかったため、フォールバック禁止規約に基づき公開を中止しました。")

    skin_types = ["乾燥肌・敏感肌", "脂性肌・オイリー", "混合肌・初心者", "全肌質・高機能"]
    item_details = article_data["itemDetails"]
    comparisons = []

    for i, p in enumerate(products_raw):
        st = skin_types[i % len(skin_types)]
        detail = item_details[i]
        comparisons.append({
            "name": p["name"],
            "brand": p["brand"],
            "category": selected_topic["category"],
            "targetSkin": st,
            "feature": detail["feature"],
            "price": p["price"],
            "pros": detail.get("pros", [])[:3],
            "cons": detail.get("cons", [])[:2],
            "imageUrl": p["imageUrl"],
            "affiliateUrl": p["affiliateUrl"],
            "rating": p["rating"],
            "reviewCount": p["reviewCount"],
            "bestFor": detail.get("bestFor", ""),
            "deepReview": detail.get("deepReview", ""),
            "dailyCost": detail.get("dailyCost", "")
        })

    now_str = datetime.now().strftime("%Y.%m.%d")
    new_post = {
        "slug": selected_topic["slug"],
        "title": article_data["title"],
        "excerpt": article_data["excerpt"],
        "category": selected_topic["category"],
        "categoryEn": selected_topic["categoryEn"],
        "date": now_str,
        "readTime": "6 min read",
        "heroImage": products_raw[0]["imageUrl"],
        "tags": [selected_topic["tag"], "#チー牛脱却", "#メンズコスメ", "#清潔感"],
        "intro": article_data["intro"],
        "targetAudience": selected_topic["targetAudience"],
        "problemStatement": article_data["problemStatement"],
        "beforeAfter": article_data["beforeAfter"],
        "selectionCriteria": article_data["selectionCriteria"],
        "comparisonTable": comparisons,
        "usageSteps": article_data["usageSteps"],
        "faqs": article_data["faqs"],
        "synergyTip": {
            "text": article_data.get("synergyTipText", ""),
            "targetSlug": selected_topic.get("synergySlug", "mens-all-in-one-gel-comparison"),
            "targetTitle": selected_topic.get("synergyTitle", "チー牛卒業！乾燥肌・脂性肌、タイプ別「最強オールインワン」で速攻モテ肌へ！")
        },
        "conclusion": article_data["conclusion"],
        "views": random.randint(1200, 3400)
    }

    updated_posts = [new_post] + existing_posts
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_posts, f, ensure_ascii=False, indent=2)

    append_cache(new_post["slug"], new_post["title"])
    print(f"[PUBLISHED] 完全新規の独自記事を追加しました！ 総記事数: {len(updated_posts)}本")
    print(f"  Slug : {new_post['slug']}")
    print(f"  Title: {new_post['title']}")

if __name__ == "__main__":
    auto_generate_one()
