import Link from "next/link";
import { getRankingPosts } from "@/data/posts";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "殿堂入りランキング | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "当塾で読者から最もアクセス・高評価を集めた神コスメ＆垢抜けギアの殿堂入りランキング。",
};

export default function RankingPage() {
  const rankingPosts = getRankingPosts();

  return (
    <main className="subpage-container">
      <div className="subpage-header">
        <span className="subpage-en">HALL OF FAME RANKING</span>
        <h1 className="subpage-title">殿堂入り人気ランキング TOP 10</h1>
        <p className="subpage-lead">
          「まずは失敗しない王道から試したい」という塾生のために、全235本超の検証記事から読者支持率トップ10の人気記事＆神アイテムを厳選。
        </p>
      </div>

      <div className="flex flex-col gap-4">
        {rankingPosts.map((post, idx) => {
          const rankColorClass =
            idx === 0
              ? "rank-gold"
              : idx === 1
              ? "rank-silver"
              : idx === 2
              ? "rank-bronze"
              : "rank-default";

          const topProduct = post.comparisonTable && post.comparisonTable[0];

          return (
            <div key={post.slug} className="ranking-card flex flex-col md:flex-row items-stretch gap-4 p-4 rounded-xl border border-zinc-800 bg-zinc-900/40 hover:border-zinc-700 transition-all">
              <div className="flex items-start gap-3 flex-1 min-w-0">
                <div className="ranking-badge-col shrink-0">
                  <span className={`ranking-huge-num ${rankColorClass}`}>
                    #{idx + 1}
                  </span>
                </div>

                <div className="ranking-card-thumb shrink-0 w-24 h-24 md:w-32 md:h-32 rounded-lg overflow-hidden bg-zinc-800 border border-zinc-700">
                  <img
                    src={post.heroImage}
                    alt={post.title}
                    className="w-full h-full object-cover"
                    loading={idx < 3 ? "eager" : "lazy"}
                    decoding="async"
                  />
                </div>

                <div className="ranking-card-content flex-1 min-w-0">
                  <div className="ranking-card-meta flex items-center gap-2 mb-1 flex-wrap">
                    <span className="cat-label">{post.category}</span>
                    <span style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>
                      🔥 月間閲覧数: {post.views?.toLocaleString()} PV
                    </span>
                  </div>
                  <h2 className="ranking-card-title text-base md:text-lg font-bold leading-snug mb-1">
                    <Link href={`/posts/${post.slug}`} className="hover:text-[#ccff00] transition-colors">
                      {post.title}
                    </Link>
                  </h2>
                  <p className="ranking-card-excerpt text-xs text-zinc-400 line-clamp-2 mb-2">
                    {post.excerpt}
                  </p>

                  {/* 1位推奨アイテムのダイレクト表示 */}
                  {topProduct && (
                    <div className="p-2.5 rounded-lg bg-zinc-950/80 border border-zinc-800/80 mt-2">
                      <div className="flex items-center gap-2 flex-wrap text-xs">
                        <span className="bg-[#ccff00] text-black font-black text-[10px] px-1.5 py-0.5 rounded">
                          検証1位
                        </span>
                        <strong className="text-white truncate max-w-[200px] md:max-w-none">
                          {topProduct.brand} {topProduct.name}
                        </strong>
                        <span className="text-[#fbbf24] font-bold">
                          {topProduct.price}
                        </span>
                      </div>
                      <p className="text-[11px] text-zinc-400 mt-1 line-clamp-1">
                        🎯 {topProduct.feature || topProduct.bestFor}
                      </p>
                    </div>
                  )}
                </div>
              </div>

              {/* アクションボタン（ダブル導線） */}
              <div className="flex md:flex-col items-center justify-end gap-2 shrink-0 pt-2 md:pt-0 border-t md:border-t-0 md:border-l border-zinc-800 md:pl-4">
                {topProduct && (
                  <a
                    href={topProduct.affiliateUrl}
                    target="_blank"
                    rel="sponsored noopener noreferrer"
                    className="btn-rakuten text-xs font-black py-2.5 px-4 w-full text-center"
                  >
                    楽天で最安値を見る →
                  </a>
                )}
                <Link
                  href={`/posts/${post.slug}`}
                  className="inline-flex items-center justify-center py-2 px-3 text-xs font-bold text-zinc-300 bg-zinc-800/80 hover:bg-zinc-700 hover:text-white rounded-md border border-zinc-700 transition-colors w-full text-center"
                >
                  検証レビュー記事 →
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </main>
  );
}
