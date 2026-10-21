import { notFound } from "next/navigation";
import Link from "next/link";
import { getPostBySlug, getAllPosts } from "@/data/posts";
import ComparisonTable from "@/app/components/ComparisonTable";
import type { Metadata } from "next";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const posts = getAllPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const decodedSlug = decodeURIComponent(slug);
  const post = getPostBySlug(decodedSlug) || getPostBySlug(slug);
  if (!post) return {};

  return {
    title: `${post.title} | もうチー牛とは呼ばせない！垢抜けコスメ塾`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.heroImage],
    },
  };
}

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params;
  const decodedSlug = decodeURIComponent(slug);
  const post = getPostBySlug(decodedSlug) || getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const allPosts = getAllPosts();
  const relatedPosts = allPosts.filter((p) => p.slug !== post.slug).slice(0, 3);

  return (
    <article className="article-container">
      {/* パンくずリスト */}
      <nav className="article-breadcrumb">
        <Link href="/">TOP</Link>
        <span>&gt;</span>
        <Link href={`/reviews?cat=${encodeURIComponent(post.category)}`}>
          {post.category}
        </Link>
        <span>&gt;</span>
        <span className="current">{post.title}</span>
      </nav>

      {/* 記事ヘッダー */}
      <header className="article-header">
        <div className="article-meta">
          <span className="cat-label">{post.category}</span>
          <span>{post.date}</span>
          <span>⏱ {post.readTime}</span>
        </div>
        <h1 className="article-title">{post.title}</h1>
        <p className="article-lead">{post.excerpt}</p>
      </header>

      {/* 楽天APIから取得した商品の高画質アイキャッチ画像 */}
      {post.heroImage && (
        <div className="article-hero-wrap">
          <img src={post.heroImage} alt={post.title} />
        </div>
      )}

      {/* 記事メインコンテンツ */}
      <div>
        {/* 導入パート */}
        <section className="article-section">
          <h2 className="section-headline">
            <span>🔥</span>
            なぜ放置すると「足切り」されるのか？
          </h2>
          <p className="section-body">{post.intro}</p>
          <div className="advice-box">
            <span className="advice-title">【塾長からのアドバイス】</span>
            <p className="advice-text">{post.problemStatement}</p>
          </div>
        </section>

        {/* 楽天API高画質画像つき肌質別比較テーブル */}
        <ComparisonTable products={post.comparisonTable} />

        {/* まとめ・背中を押すメッセージ */}
        <section className="article-section">
          <h2 className="section-headline">
            <span>🎯</span>
            まとめ：今日から始めるアクションプラン
          </h2>
          <p className="section-body">{post.conclusion}</p>
          <div className="callout-box">
            <span className="callout-title">
              迷ったらまずは「乾燥肌」または「オイリー肌」の自分に合う方を1つだけ試すこと！
            </span>
            <span className="callout-text">
              完璧を目指さず、1つルーティンに加えるだけで清潔感は5割増しになります。
            </span>
          </div>
        </section>

        {/* タグ一覧 */}
        <div className="tag-cloud">
          {post.tags.map((tag) => (
            <Link
              key={tag}
              href={`/reviews?tag=${encodeURIComponent(tag)}`}
              className="tag-item"
            >
              {tag}
            </Link>
          ))}
        </div>
      </div>

      {/* 関連記事 */}
      {relatedPosts.length > 0 && (
        <section className="related-section">
          <h3 className="section-headline">
            <span style={{ width: "4px", height: "16px", background: "var(--brand-accent)", display: "inline-block" }}></span>
            あわせて読みたい検証記事
          </h3>
          <div className="related-grid">
            {relatedPosts.map((rel) => (
              <Link
                key={rel.slug}
                href={`/posts/${rel.slug}`}
                className="related-card"
              >
                <div className="related-thumb">
                  {rel.heroImage ? (
                    <img src={rel.heroImage} alt={rel.title} />
                  ) : (
                    <div style={{ color: "var(--text-muted)", fontSize: "0.75rem" }}>NO IMG</div>
                  )}
                </div>
                <div className="related-info">
                  <span className="related-cat">{rel.category}</span>
                  <h4 className="related-title">{rel.title}</h4>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
