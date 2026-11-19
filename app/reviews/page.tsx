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

  const categoryMeta = [
    { name: "すべて", icon: "🔥", count: allPosts.length },
    {
      name: "スキンケア・洗顔",
      icon: "🧴",
      count: allPosts.filter((p) => p.category === "スキンケア・洗顔").length,
    },
    {
      name: "ヘア・眉毛セット",
      icon: "✂️",
      count: allPosts.filter((p) => p.category === "ヘア・眉毛セット").length,
    },
    {
      name: "ボディ・姿勢改善",
      icon: "💪",
      count: allPosts.filter((p) => p.category === "ボディ・姿勢改善").length,
    },
    {
      name: "ニオイ・体臭対策",
      icon: "🚿",
      count: allPosts.filter((p) => p.category === "ニオイ・体臭対策").length,
    },
    {
      name: "ファッション・身だしなみ",
      icon: "👔",
      count: allPosts.filter((p) => p.category === "ファッション・身だしなみ").length,
    },
  ];

  return (
    <main className="subpage-container">
      <div className="subpage-header">
        <span className="subpage-en">REVIEWS & BENCHMARKS</span>
        <h1 className="subpage-title">最新の検証・比較レポート</h1>
        <p className="subpage-lead">
          ドラッグストアから楽天で話題の本格コスメ・身だしなみギアまで、実際に効果の出るアイテムだけを肌質・悩みタイプ別に徹底比較しています。
        </p>
      </div>

      {/* カテゴリフィルタ */}
      <div className="filter-bar">
        {categoryMeta.map((c) => {
          const isSelected = (!cat && c.name === "すべて") || cat === c.name;
          return (
            <Link
              key={c.name}
              href={c.name === "すべて" ? "/reviews" : `/reviews?cat=${encodeURIComponent(c.name)}`}
              className={`filter-btn ${isSelected ? "active" : ""}`}
            >
              <span style={{ marginRight: "6px" }}>{c.icon}</span>
              <span>{c.name}</span>
              <span
                style={{
                  marginLeft: "6px",
                  fontSize: "0.72rem",
                  opacity: isSelected ? 0.9 : 0.65,
                }}
              >
                ({c.count})
              </span>
            </Link>
          );
        })}
      </div>

      {/* タグ絞り込み中のステータス表示 */}
      {tag && (
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "12px",
            marginBottom: "24px",
            fontSize: "0.85rem",
          }}
        >
          <span style={{ color: "var(--text-muted)" }}>
            タグ絞り込み中: <strong style={{ color: "var(--brand-accent)" }}>{tag}</strong>（{filteredPosts.length}件）
          </span>
          <Link
            href={cat ? `/reviews?cat=${encodeURIComponent(cat)}` : "/reviews"}
            style={{
              padding: "3px 10px",
              borderRadius: "4px",
              background: "var(--bg-surface)",
              border: "1px solid var(--border-color)",
              fontSize: "0.75rem",
              color: "var(--text-main)",
            }}
          >
            ✕ タグ解除
          </Link>
        </div>
      )}

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
                <img
                  src={post.heroImage}
                  alt={post.title}
                  loading="lazy"
                  decoding="async"
                />
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
