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
    link: "/posts/mens-all-in-one-gel-comparison",
    items: ["水洗顔禁止とぬるま湯洗顔の作法", "乾燥肌とオイリー肌の見極め方", "毛穴の黒ずみを溶かす洗顔法"],
  },
  {
    step: "STEP 02",
    tag: "EYEBROW & BEARD",
    title: "眉毛デザインと青髭カバー（顔印象の劇的改造）",
    desc: "顔の印象の8割は眉毛で決まります。ボサボサ眉毛をハサミとコームで整え、夕方の泥棒ヒゲ・青髭をメンズ用コンシーラーで自然に消すだけで、一気に清潔感あふれる爽やか男子に変貌します。",
    link: "/posts/mens-eyebrow-shaping-kit",
    items: ["失敗しないセルフ眉毛カットの黄金比", "青髭・クマを消すメンズコンシーラーの選び方", "自然に血色感を出すメンズリップ"],
  },
  {
    step: "STEP 03",
    tag: "HAIRSTYLE",
    title: "美容室オーダー法と朝5分のヘアセット",
    desc: "1000円カットで「短めで」と頼むのを卒業。ホットペッパービューティーでの美容室の選び方から、失敗しないオーダーのコツ、そして朝5分で束感と清潔感を出せるワックス・グリースの付け方を徹底マスターします。",
    link: "/posts/mens-hair-styling-wax-review",
    items: ["美容室で「おまかせ」と言ってはいけない理由", "軟毛・剛毛別のヘアスタイリング剤比較", "1日中キープするハードスプレー術"],
  },
  {
    step: "STEP 04",
    tag: "BODY & CLEANLINESS",
    title: "猫背矯正ストレッチと「完全無臭」エチケット",
    desc: "どんなに顔を整えても、猫背・巻き肩で服が似合わなかったり、汗臭・体臭が漂っていたら一発で足切り。自宅でできる自重トレ＆ストレッチと、香水に頼らない薬用デオドラント習慣で清潔感を完成させます。",
    link: "/posts/mens-body-odor-deodorant-best",
    items: ["猫背と巻き肩をリセットするストレッチ", "男臭・汗臭を24時間ブロックするロールオン制汗剤", "服の生乾き臭・体臭を防ぐ洗濯ルーティン"],
  },
];

export default function CurriculumPage() {
  return (
    <main className="subpage-container">
      <div className="subpage-header">
        <span className="subpage-en">ROADMAP & CURRICULUM</span>
        <h1 className="subpage-title">【必修】ゼロから始める垢抜けカリキュラム</h1>
        <p className="subpage-lead">
          ネット上の断片的な情報に惑わされるのはもう終わり。本塾が提唱する「最もコスパ良く劇的に変わる順番」で、清潔感を最短でインストールしましょう。
        </p>
      </div>

      <div>
        {STEPS.map((s, idx) => (
          <div key={idx} className="curriculum-card">
            <div className="curriculum-top">
              <div className="curriculum-tag-wrap">
                <span className="curriculum-step-badge">{s.step}</span>
                <span className="curriculum-en-label">{s.tag}</span>
              </div>
              <Link href={s.link} className="curriculum-link">
                推奨アイテム比較を見る →
              </Link>
            </div>

            <h2 className="curriculum-title">{s.title}</h2>
            <p className="curriculum-desc">{s.desc}</p>

            <div className="curriculum-points-box">
              <span className="curriculum-points-title">📌 このステップで習得する最重要ポイント:</span>
              <ul className="curriculum-points-list">
                {s.items.map((item, i) => (
                  <li key={i}>
                    <span>✔</span>
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
