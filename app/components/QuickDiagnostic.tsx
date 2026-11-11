"use client";

import { useState } from "react";
import Link from "next/link";

interface DiagnosticOption {
  id: string;
  label: string;
  icon: string;
  targetCategory: string;
  problem: string;
  bestItem: {
    name: string;
    brand: string;
    price: string;
    rating: number;
    reviewCount: number;
    imageUrl: string;
    affiliateUrl: string;
    articleSlug: string;
    recommendReason: string;
  };
}

const DIAGNOSTIC_OPTIONS: DiagnosticOption[] = [
  {
    id: "oil-skin",
    label: "顔のテカリ・毛穴・赤み",
    icon: "🧴",
    targetCategory: "スキンケア・洗顔",
    problem: "夕方になると顔がギトつく、毛穴の黒ずみ・赤みで清潔感がない",
    bestItem: {
      name: "薬用スキンケアウォッシュ（毛穴・殺菌処方）",
      brand: "メンズ高機能洗顔",
      price: "1,980円〜",
      rating: 4.8,
      reviewCount: 320,
      imageUrl: "https://thumbnail.image.rakuten.co.jp/@0_mall/goodyouth/cabinet/syouhingazou/facewash/facewash_main.jpg?_ex=600x600",
      affiliateUrl: "https://hb.afl.rakuten.co.jp/ichiba/4f05786b.d33190cb.4f05786c.6b5e0ee3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fgoodyouth%2Ffacewash%2F",
      articleSlug: "mens-medicated-acne-pore-face-wash",
      recommendReason: "皮脂吸着クレイと薬用有効成分で、テカリと毛穴黒ずみを根本からリセットする本塾No.1洗顔料。"
    }
  },
  {
    id: "beard-complex",
    label: "泥棒ヒゲ・青髭・クマ",
    icon: "🪒",
    targetCategory: "青髭・コンシーラー",
    problem: "剃っても残る青髭、目元のクマやニキビ跡のせいで老けて疲れて見える",
    bestItem: {
      name: "メンズ用高密着スティックコンシーラー",
      brand: "清潔感メイク",
      price: "1,650円〜",
      rating: 4.7,
      reviewCount: 280,
      imageUrl: "https://thumbnail.image.rakuten.co.jp/@0_mall/cosme-de-net/cabinet/item_img/2023_09/20000000.jpg?_ex=600x600",
      affiliateUrl: "https://hb.afl.rakuten.co.jp/ichiba/4f05786b.d33190cb.4f05786c.6b5e0ee3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcosme-de-net%2Fitem%2F",
      articleSlug: "mens-beard-cover-stick-concealer",
      recommendReason: "オレンジ味の補色効果で青髭や頑固なクマを塗った瞬間に無効化。バレない自然な仕上がり。"
    }
  },
  {
    id: "hair-flat",
    label: "軟毛・ペタ毛・髪型崩れ",
    icon: "✂️",
    targetCategory: "ヘアスタイリング",
    problem: "ワックスを付けても昼にはペタッと潰れる、テカリのない自然な束感が欲しい",
    bestItem: {
      name: "超強力ホールド マットクレイヘアワックス",
      brand: "プロ仕様スタイリング",
      price: "1,870円〜",
      rating: 4.9,
      reviewCount: 450,
      imageUrl: "https://thumbnail.image.rakuten.co.jp/@0_mall/goodyouth/cabinet/syouhingazou/matwax/mens_matwax_1.jpg?_ex=600x600",
      affiliateUrl: "https://hb.afl.rakuten.co.jp/ichiba/4f05786b.d33190cb.4f05786c.6b5e0ee3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fgoodyouth%2Fmatwax%2F",
      articleSlug: "mens-matte-clay-hair-wax-strong",
      recommendReason: "油分ゼロ設計で細毛・軟毛を根元から強力リフト。夜まで絶対にヘタらない殿堂入りクレイ。"
    }
  },
  {
    id: "body-odor",
    label: "汗臭・脇汗・服の生乾き臭",
    icon: "🚿",
    targetCategory: "ニオイ・体臭対策",
    problem: "すれ違いざまの汗臭やワキガ臭が不安、香水で誤魔化さず無臭化したい",
    bestItem: {
      name: "薬用デオドラント制汗スティック",
      brand: "密着24時間殺菌",
      price: "2,200円〜",
      rating: 4.8,
      reviewCount: 510,
      imageUrl: "https://thumbnail.image.rakuten.co.jp/@0_mall/menscosme-zigen/cabinet/product/6.jpg?_ex=600x600",
      affiliateUrl: "https://hb.afl.rakuten.co.jp/ichiba/4f05786b.d33190cb.4f05786c.6b5e0ee3/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmenscosme-zigen%2Fitem%2F",
      articleSlug: "mens-body-odor-deodorant-best",
      recommendReason: "汗腺にフタをして雑菌を分子レベルでシャットアウト。一日中完全に無臭をキープする守護神。"
    }
  }
];

export default function QuickDiagnostic() {
  const [selectedId, setSelectedId] = useState<string>(DIAGNOSTIC_OPTIONS[0].id);
  const current = DIAGNOSTIC_OPTIONS.find((o) => o.id === selectedId) || DIAGNOSTIC_OPTIONS[0];

  return (
    <section className="container my-8" aria-label="悩み別・最短垢抜けアイテム診断">
      <div className="bg-gradient-to-br from-[#18181b] via-[#121215] to-[#0c0c0e] border border-[#f97316]/30 rounded-2xl p-4 sm:p-7 shadow-[0_8px_32px_rgba(0,0,0,0.5)]">
        {/* ヘッダー */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-5 pb-4 border-b border-zinc-800">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-black bg-gradient-to-r from-orange-500 to-amber-500 text-black uppercase tracking-wider mb-1">
              ⚡ 30秒・即決ナビ
            </div>
            <h2 className="text-lg sm:text-2xl font-black text-white tracking-tight">
              迷ったらここから！お前の「最も深い悩み」を1つ選べ
            </h2>
          </div>
          <span className="text-xs text-zinc-400 font-medium">
            ※全235本の検証データから厳選された最短解
          </span>
        </div>

        {/* タブボタン */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 mb-6">
          {DIAGNOSTIC_OPTIONS.map((opt) => {
            const isSelected = opt.id === selectedId;
            return (
              <button
                key={opt.id}
                type="button"
                onClick={() => setSelectedId(opt.id)}
                className={`flex items-center gap-2 p-2.5 sm:p-3 rounded-xl border text-left transition-all cursor-pointer ${
                  isSelected
                    ? "bg-[#27272a] border-[#ccff00] text-white shadow-[0_0_15px_rgba(204,255,0,0.2)] scale-[1.02]"
                    : "bg-[#18181b]/70 border-zinc-800 text-zinc-400 hover:border-zinc-700 hover:text-zinc-200"
                }`}
              >
                <span className="text-xl sm:text-2xl shrink-0">{opt.icon}</span>
                <span className="text-xs sm:text-sm font-bold leading-tight">
                  {opt.label}
                </span>
              </button>
            );
          })}
        </div>

        {/* 診断結果表示カード */}
        <div className="bg-[#09090b]/80 border border-zinc-800 rounded-xl p-4 sm:p-6 transition-all animate-in fade-in">
          <div className="flex flex-col md:flex-row md:items-center gap-4 sm:gap-6">
            {/* サムネイル画像 */}
            <div className="relative w-full md:w-44 h-44 shrink-0 rounded-lg overflow-hidden bg-zinc-900 border border-zinc-700 mx-auto">
              <img
                src={current.bestItem.imageUrl}
                alt={current.bestItem.name}
                className="w-full h-full object-cover"
                loading="lazy"
                decoding="async"
              />
              <span className="absolute top-2 left-2 bg-[#ccff00] text-black font-black text-[10px] px-2 py-0.5 rounded shadow">
                殿堂入り1位
              </span>
            </div>

            {/* 詳細情報 */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap mb-1">
                <span className="text-[11px] font-bold text-orange-400 bg-orange-950/60 border border-orange-800/60 px-2 py-0.5 rounded">
                  {current.targetCategory}
                </span>
                <span className="text-xs text-amber-400 font-bold">
                  ★ {current.bestItem.rating}（口コミ {current.bestItem.reviewCount}件超）
                </span>
              </div>

              <h3 className="text-base sm:text-xl font-black text-white leading-snug mb-1">
                {current.bestItem.brand}｜{current.bestItem.name}
              </h3>

              <div className="text-xs text-zinc-300 font-bold mb-2">
                参考価格：<span className="text-sm sm:text-base text-[#ccff00] font-black">{current.bestItem.price}</span>
                <span className="text-zinc-500 font-normal ml-2">（送料無料・公式在庫保証）</span>
              </div>

              <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed mb-4 bg-zinc-900/60 p-2.5 rounded border border-zinc-800">
                💡 <strong>選ぶべき理由：</strong>{current.bestItem.recommendReason}
              </p>

              {/* アクションボタン */}
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
                <a
                  href={current.bestItem.affiliateUrl}
                  target="_blank"
                  rel="sponsored noopener noreferrer"
                  className="btn-rakuten py-3 px-6 text-sm font-black flex-1 text-center"
                >
                  楽天市場公式で最安値＆在庫を見る →
                </a>
                <Link
                  href={`/posts/${current.bestItem.articleSlug}`}
                  className="inline-flex items-center justify-center py-2.5 px-4 text-xs font-bold text-zinc-300 bg-zinc-800/80 hover:bg-zinc-700 hover:text-white rounded-lg border border-zinc-700 transition-colors"
                >
                  徹底検証記事を読む 📖
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
