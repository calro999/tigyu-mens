import Link from "next/link";
import Image from "next/image";
import { getAllPosts, getRankingPosts } from "@/data/posts";

export default function Home() {
  const posts = getAllPosts();
  const heroMain = posts[0] || null;
  const heroSub1 = posts[1] || null;
  const heroSub2 = posts[2] || null;
  const rankingPosts = getRankingPosts();

  return (
    <main>
      {/* Hero Section (マガジン風アシンメトリー) */}
      <section className="hero-section container">
        <div className="hero-grid">
          {/* メイン特集 */}
          {heroMain && (
            <Link href={`/posts/${heroMain.slug}`} className="hero-card hero-main">
              <img src={heroMain.heroImage} alt={heroMain.title} />
              <div className="hero-content">
                <div className="hero-meta">
                  <span className="cat-label">{heroMain.category}</span>
                  <span>⏱ {heroMain.readTime}</span>
                </div>
                <h2 className="hero-title">{heroMain.title}</h2>
              </div>
            </Link>
          )}

          {/* サブ特集1 */}
          {heroSub1 && (
            <Link href={`/posts/${heroSub1.slug}`} className="hero-card hero-sub">
              <img src={heroSub1.heroImage} alt={heroSub1.title} />
              <div className="hero-content">
                <div className="hero-meta">
                  <span className="cat-label" style={{ background: "#fff", color: "#000" }}>
                    {heroSub1.category}
                  </span>
                </div>
                <h2 className="hero-title">{heroSub1.title}</h2>
              </div>
            </Link>
          )}

          {/* サブ特集2 */}
          {heroSub2 && (
            <Link href={`/posts/${heroSub2.slug}`} className="hero-card hero-sub">
              <img src={heroSub2.heroImage} alt={heroSub2.title} />
              <div className="hero-content">
                <div className="hero-meta">
                  <span className="cat-label" style={{ background: "#fff", color: "#000" }}>
                    {heroSub2.category}
                  </span>
                </div>
                <h2 className="hero-title">{heroSub2.title}</h2>
              </div>
            </Link>
          )}
        </div>
      </section>

      {/* Categories (タグクラウド風デザイン) */}
      <section className="container">
        <div className="cat-grid">
          <Link href="/reviews?cat=スキンケア・洗顔" className="cat-box">
            <div className="cat-icon">🧴</div>
            <div className="cat-name">
              スキンケア<span>SKIN & FACE</span>
            </div>
          </Link>
          <Link href="/reviews?cat=ヘア・眉毛セット" className="cat-box">
            <div className="cat-icon">✂️</div>
            <div className="cat-name">
              ヘア＆眉毛<span>HAIR & EYEBROW</span>
            </div>
          </Link>
          <Link href="/reviews?cat=ボディ・姿勢改善" className="cat-box">
            <div className="cat-icon">💪</div>
            <div className="cat-name">
              ボディメイク<span>BODY & DIET</span>
            </div>
          </Link>
          <Link href="/reviews?cat=ニオイ・体臭対策" className="cat-box">
            <div className="cat-icon">🚿</div>
            <div className="cat-name">
              ニオイ対策<span>CLEANLINESS</span>
            </div>
          </Link>
        </div>
      </section>

      {/* メインコンテンツ ＆ サイドバー */}
      <section className="container" id="latest">
        <div className="content-wrapper">
          {/* 左カラム：記事一覧 */}
          <div className="main-content">
            <div className="section-header">
              <div className="sec-title-wrap">
                <span className="sec-en">Latest Reports</span>
                <h2 className="sec-ja">最新の検証・レビュー</h2>
              </div>
              <Link href="/reviews" className="sec-more">
                View All →
              </Link>
            </div>

            <div className="post-list">
              {posts.map((post) => (
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
          </div>

          {/* 右カラム：サイドバー */}
          <aside className="sidebar" id="ranking">
            {/* ウィジェット1: ランキング */}
            <div className="widget">
              <h3 className="widget-title">殿堂入りランキング</h3>
              <ul className="ranking-list">
                {rankingPosts.map((post, idx) => (
                  <li key={post.slug} className="ranking-item">
                    <div className="ranking-num">{idx + 1}</div>
                    <div className="ranking-thumb">
                      <img src={post.heroImage} alt={post.title} />
                    </div>
                    <div className="ranking-title">
                      <Link href={`/posts/${post.slug}`}>{post.title}</Link>
                    </div>
                  </li>
                ))}
              </ul>
            </div>

            {/* ウィジェット2: タグクラウド風 */}
            <div className="widget">
              <h3 className="widget-title">注目キーワード</h3>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                {[
                  "#オールインワン",
                  "#青髭",
                  "#コンシーラー",
                  "#眉毛カット",
                  "#ワックス",
                  "#体臭対策",
                  "#猫背矯正",
                  "#チー牛脱却",
                ].map((tag) => (
                  <Link
                    key={tag}
                    href={`/reviews?tag=${encodeURIComponent(tag)}`}
                    style={{
                      background: "var(--bg-base)",
                      border: "1px solid var(--border-color)",
                      padding: "5px 10px",
                      fontSize: "0.8rem",
                      borderRadius: "4px",
                      color: "var(--text-muted)",
                    }}
                  >
                    {tag}
                  </Link>
                ))}
              </div>
            </div>
          </aside>
        </div>
      </section>

      {/* カリキュラム（Roadmap）セクション */}
      <section className="container" id="roadmap">
        <div className="section-header">
          <div className="sec-title-wrap">
            <span className="sec-en">Roadmap / Step 1</span>
            <h2 className="sec-ja">【必修】基礎カリキュラム</h2>
          </div>
          <Link href="/curriculum" className="sec-more">
            全ステップを見る →
          </Link>
        </div>

        <div className="roadmap-container">
          <div className="roadmap-list">
            {/* Step 1 */}
            <div className="roadmap-item">
              <div className="step-marker">01</div>
              <div className="step-content">
                <span className="step-meta">STEP 01 : FACE & SKIN</span>
                <h3 className="step-title">
                  <Link href="/posts/post-1-skincare">洗顔と保湿の土台作り（肌荒れ・テカリ撲滅）</Link>
                </h3>
                <p className="step-desc">
                  すべての始まりは肌だ。水洗顔をやめてドラッグストアの洗顔料を選び、乾燥肌・脂性肌別に保湿を徹底しろ。
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="roadmap-item">
              <div className="step-marker">02</div>
              <div className="step-content">
                <span className="step-meta">STEP 02 : EYEBROW & HAIR</span>
                <h3 className="step-title">
                  <Link href="/posts/post-3-hair-&-brows">眉毛デザインと髪型セットの基礎</Link>
                </h3>
                <p className="step-desc">
                  顔の印象の8割は眉毛で決まる。ボサボサ眉毛を整えて目力を200%引き上げるセルフカット術と、朝5分のワックス技術を伝授。
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="roadmap-item">
              <div className="step-marker">03</div>
              <div className="step-content">
                <span className="step-meta">STEP 03 : BODY & CLEANLINESS</span>
                <h3 className="step-title">
                  <Link href="/posts/post-5-cleanliness">姿勢改善と「無臭」エチケット</Link>
                </h3>
                <p className="step-desc">
                  BBクリームを塗る前に姿勢を正せ。猫背・巻き肩を矯正する自宅ストレッチと、香水に頼らない薬用デオドラント習慣で清潔感を完成させろ。
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
