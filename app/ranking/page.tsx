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
          「まずは失敗しない王道から試したい」という塾生のために、全160本超の検証記事から読者支持率トップ10の人気記事＆神アイテムを厳選。
        </p>
      </div>

      <div>
        {rankingPosts.map((post, idx) => {
          const rankColorClass =
            idx === 0
              ? "rank-gold"
              : idx === 1
              ? "rank-silver"
              : idx === 2
              ? "rank-bronze"
              : "rank-default";

          return (
            <Link key={post.slug} href={`/posts/${post.slug}`} className="ranking-card">
              <div className="ranking-badge-col">
                <span className={`ranking-huge-num ${rankColorClass}`}>
                  #{idx + 1}
                </span>
              </div>

              <div className="ranking-card-thumb">
                <img src={post.heroImage} alt={post.title} />
              </div>

              <div className="ranking-card-content">
                <div className="ranking-card-meta">
                  <span className="cat-label">{post.category}</span>
                  <span style={{ color: "var(--text-muted)" }}>
                    🔥 月間閲覧数: {post.views?.toLocaleString()} PV
                  </span>
                </div>
                <h2 className="ranking-card-title">{post.title}</h2>
                <p className="ranking-card-excerpt">{post.excerpt}</p>
              </div>

              <div style={{ flexShrink: 0 }}>
                <span className="btn-rakuten" style={{ padding: "8px 14px", fontSize: "0.75rem" }}>
                  記事を読む →
                </span>
              </div>
            </Link>
          );
        })}
      </div>
    </main>
  );
}
