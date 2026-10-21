import Link from "next/link";
import { getAllPosts } from "@/data/posts";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "検証・レビュー一覧 | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "メンズコスメ・身だしなみギアの最新検証記事一覧。肌質別の比較テーブルとリアルなレビューを掲載中。",
};

interface Props {
  searchParams: Promise<{ cat?: string; tag?: string }>;
}

export default async function ReviewsPage({ searchParams }: Props) {
  const { cat, tag } = await searchParams;
  const allPosts = getAllPosts();

  const filteredPosts = allPosts.filter((post) => {
    if (cat && post.category !== cat) return false;
    if (tag && !post.tags.includes(tag)) return false;
    return true;
  });

  const categories = ["すべて", "スキンケア・洗顔", "ヘア・眉毛セット", "ボディ・姿勢改善", "ニオイ・体臭対策"];

  return (
    <main className="subpage-container">
      <div className="subpage-header">
        <span className="subpage-en">REVIEWS & BENCHMARKS</span>
        <h1 className="subpage-title">最新の検証・比較レポート</h1>
        <p className="subpage-lead">
          ドラッグストアから楽天で話題の本格コスメまで、実際に効果の出るアイテムだけを肌質別に徹底比較しています。
        </p>
      </div>

      {/* カテゴリフィルタ */}
      <div className="filter-bar">
        {categories.map((c) => {
          const isSelected = (!cat && c === "すべて") || cat === c;
          return (
            <Link
              key={c}
              href={c === "すべて" ? "/reviews" : `/reviews?cat=${encodeURIComponent(c)}`}
              className={`filter-btn ${isSelected ? "active" : ""}`}
            >
              {c}
            </Link>
          );
        })}
      </div>

      {/* 記事一覧 */}
      {filteredPosts.length === 0 ? (
        <div className="content-box" style={{ textAlign: "center", padding: "40px" }}>
          <p style={{ color: "var(--text-muted)" }}>該当する記事が見つかりませんでした。</p>
          <Link href="/reviews" className="curriculum-link" style={{ marginTop: "10px", display: "inline-block" }}>
            すべての記事を表示する →
          </Link>
        </div>
      ) : (
        <div className="post-list">
          {filteredPosts.map((post) => (
            <Link key={post.slug} href={`/posts/${post.slug}`} className="post-card">
              <div className="post-thumb">
                <img src={post.heroImage} alt={post.title} />
              </div>
              <div className="post-info">
                <div className="post-meta">
                  <span className="tag">{post.tags[0] || "#コスメ"}</span>
                  <span>{post.date}</span>
                  <span>⏱ {post.readTime}</span>
                </div>
                <h3 className="post-title">{post.title}</h3>
                <p className="post-excerpt">{post.excerpt}</p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
