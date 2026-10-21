import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "基礎カリキュラム | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "脱チー牛のための完全ロードマップ。STEP1スキンケアからSTEP4ニオイ対策まで、迷わず垢抜ける必修カリキュラム。",
};

const STEPS = [
  {
    step: "STEP 01",
    tag: "SKINCARE",
    title: "洗顔と保湿の土台作り（肌の治安回復）",
    desc: "「顔がギトつくから水だけで洗う」「ベタつくのが嫌で何も塗らない」は最悪の悪循環。まずはドラッグストアでも揃う正しい洗顔料と、乾燥肌・オイリー肌別に特化したオールインワンで肌の赤み・毛穴・テカリを撲滅する基礎を固めます。",
    link: "/posts/post-1-skincare",
    items: ["水洗顔禁止とぬるま湯洗顔の作法", "乾燥肌とオイリー肌の見極め方", "毛穴の黒ずみを溶かす洗顔法"],
  },
  {
    step: "STEP 02",
    tag: "EYEBROW & BEARD",
    title: "眉毛デザインと青髭カバー（顔印象の劇的改造）",
    desc: "顔の印象の8割は眉毛で決まります。ボサボサ眉毛をハサミとコームで整え、夕方の泥棒ヒゲ・青髭をメンズ用コンシーラーで自然に消すだけで、一気に清潔感あふれる爽やか男子に変貌します。",
    link: "/posts/post-2-skincare",
    items: ["失敗しないセルフ眉毛カットの黄金比", "青髭・クマを消すメンズコンシーラーの選び方", "自然に血色感を出すメンズリップ"],
  },
  {
    step: "STEP 03",
    tag: "HAIRSTYLE",
    title: "美容室オーダー法と朝5分のヘアセット",
    desc: "1000円カットで「短めで」と頼むのを卒業。ホットペッパービューティーでの美容室の選び方から、失敗しないオーダーのコツ、そして朝5分で束感と清潔感を出せるワックス・グリースの付け方を徹底マスターします。",
    link: "/posts/post-4-hair-brows",
    items: ["美容室で「おまかせ」と言ってはいけない理由", "軟毛・剛毛別のヘアスタイリング剤比較", "1日中キープするハードスプレー術"],
  },
  {
    step: "STEP 04",
    tag: "BODY & CLEANLINESS",
    title: "猫背矯正ストレッチと「完全無臭」エチケット",
    desc: "どんなに顔を整えても、猫背・巻き肩で服が似合わなかったり、汗臭・体臭が漂っていたら一発で足切り。自宅でできる自重トレ＆ストレッチと、香水に頼らない薬用デオドラント習慣で清潔感を完成させます。",
    link: "/posts/post-5-cleanliness",
    items: ["猫背と巻き肩をリセットするストレッチ", "男臭・汗臭を24時間ブロックするロールオン制汗剤", "服の生乾き臭・体臭を防ぐ洗濯ルーティン"],
  },
];

export default function CurriculumPage() {
  return (
    <main className="max-w-[1000px] mx-auto px-5 py-12">
      <div className="mb-10 text-center">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          ROADMAP & CURRICULUM
        </span>
        <h1 className="text-3xl sm:text-4xl font-black text-[#f4f4f5] mb-4">
          【必修】ゼロから始める垢抜けカリキュラム
        </h1>
        <p className="text-sm text-[#a1a1aa] max-w-2xl mx-auto leading-relaxed">
          ネット上の断片的な情報に惑わされるのはもう終わり。本塾が提唱する「最もコスパ良く劇的に変わる順番」で、清潔感を最短でインストールしましょう。
        </p>
      </div>

      <div className="space-y-8">
        {STEPS.map((s, idx) => (
          <div
            key={idx}
            className="bg-[#18181b] border border-[#27272a] hover:border-[#3f3f46] rounded-xl p-6 sm:p-8 transition-colors"
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4 pb-4 border-b border-[#27272a]">
              <div className="flex items-center gap-3">
                <span className="bg-[#ccff00] text-black font-black text-xs px-3 py-1 rounded">
                  {s.step}
                </span>
                <span className="text-xs text-[#a1a1aa] font-bold">{s.tag}</span>
              </div>
              <Link
                href={s.link}
                className="text-xs font-bold text-[#ccff00] hover:underline self-start sm:self-auto"
              >
                このステップの推奨比較を見る →
              </Link>
            </div>

            <h2 className="text-xl sm:text-2xl font-black text-[#f4f4f5] mb-3">
              {s.title}
            </h2>
            <p className="text-sm text-[#a1a1aa] leading-relaxed mb-5">{s.desc}</p>

            <div className="bg-[#09090b] border border-[#27272a] p-4 rounded-lg">
              <span className="text-xs font-bold text-[#f4f4f5] block mb-2">
                📌 このステップで習得する最重要ポイント:
              </span>
              <ul className="space-y-1 text-xs text-[#a1a1aa]">
                {s.items.map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className="text-[#ccff00] font-bold">✔</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
