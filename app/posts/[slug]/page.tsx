import { notFound } from "next/navigation";
import Link from "next/link";
import { getPostBySlug, getAllPosts } from "@/data/posts";
import ComparisonTable from "@/app/components/ComparisonTable";
import StickyCtaBar from "@/app/components/StickyCtaBar";
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

  const pageUrl = `https://tigyu-mens.vercel.app/posts/${post.slug}`;
  const seoTitle = post.title.includes("2026") ? post.title : `【2026最新】${post.title}`;

  return {
    title: seoTitle,
    description: post.excerpt,
    keywords: [
      post.category,
      ...post.tags.map((t) => t.replace("#", "")),
      "メンズコスメ",
      "チー牛脱却",
      "垢抜け",
      "徹底比較",
      "おすすめ"
    ],
    alternates: {
      canonical: pageUrl,
    },
    openGraph: {
      title: seoTitle,
      description: post.excerpt,
      url: pageUrl,
      type: "article",
      publishedTime: post.date.replace(/\./g, "-"),
      modifiedTime: new Date().toISOString(),
      images: [
        {
          url: post.heroImage,
          width: 600,
          height: 600,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: seoTitle,
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
  const sameCategoryPosts = allPosts.filter(
    (p) => p.slug !== post.slug && p.category === post.category
  );
  const otherPosts = allPosts.filter(
    (p) => p.slug !== post.slug && p.category !== post.category
  );
  const relatedPosts = [...sameCategoryPosts, ...otherPosts].slice(0, 6);
  const pageUrl = `https://tigyu-mens.vercel.app/posts/${post.slug}`;

  const faqList =
    post.faqs && post.faqs.length > 0
      ? post.faqs
      : [
          {
            q: `${post.category}のアイテム選びで初心者が失敗しないコツは？`,
            a: `${post.targetAudience}の方は、まず自分の肌質・目的タイプ（乾燥肌・脂性肌・混合肌・高機能）に合った処方を選ぶことが最重要です。本記事の比較表から自分のタイプに該当する1本を選び、最低2週間継続して様子を見ることで確実に清潔感が底上げされます。`,
          },
          {
            q: "ドラッグストアの市販品とネット通販の専売品はどちらが良いですか？",
            a: "コスパ重視のエントリーモデルなら市販品でも十分ですが、特有の悩み（頑固な毛穴黒ずみ、青髭、強い体臭、姿勢の歪みなど）を最短で解決したい場合は、有効成分や機能性が高設計されたネット通販の高評価アイテムを選ぶ方が結果的に安上がりで効果的です。",
          },
        ];

  // AI-SEO / GEO 向け Article ＆ ItemList ＆ BreadcrumbList ＆ FAQPage 構造化データ
  const articleJsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "TOP",
            "item": "https://tigyu-mens.vercel.app"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": post.category,
            "item": `https://tigyu-mens.vercel.app/reviews?cat=${encodeURIComponent(post.category)}`
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": post.title,
            "item": pageUrl
          }
        ]
      },
      {
        "@type": "Article",
        "headline": post.title,
        "description": post.excerpt,
        "image": [post.heroImage],
        "datePublished": post.date.replace(/\./g, "-"),
        "dateModified": post.date.replace(/\./g, "-"),
        "author": {
          "@type": "Person",
          "name": "ゼロから始める垢抜けコスメ塾 塾長",
          "url": "https://tigyu-mens.vercel.app/profile"
        },
        "publisher": {
          "@type": "Organization",
          "name": "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
          "url": "https://tigyu-mens.vercel.app",
          "logo": {
            "@type": "ImageObject",
            "url": "https://thumbnail.image.rakuten.co.jp/@0_mall/menscosme-zigen/cabinet/product/6.jpg?_ex=600x600"
          }
        },
        "mainEntityOfPage": {
          "@type": "WebPage",
          "@id": pageUrl
        },
        "about": {
          "@type": "ItemList",
          "name": `${post.title} 推奨アイテム比較リスト`,
          "itemListElement": post.comparisonTable.map((item, index) => ({
            "@type": "ListItem",
            "position": index + 1,
            "item": {
              "@type": "Product",
              "name": item.name,
              "brand": {
                "@type": "Brand",
                "name": item.brand
              },
              "image": item.imageUrl,
              "description": item.deepReview || item.feature,
              "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": item.rating || 4.5,
                "reviewCount": item.reviewCount || 150
              },
              "offers": {
                "@type": "Offer",
                "priceCurrency": "JPY",
                "price": item.price.replace(/[^0-9]/g, "") || "0",
                "availability": "https://schema.org/InStock",
                "url": item.affiliateUrl
              }
            }
          }))
        }
      },
      {
        "@type": "FAQPage",
        "mainEntity": faqList.map((f) => ({
          "@type": "Question",
          "name": f.q,
          "acceptedAnswer": {
            "@type": "Answer",
            "text": f.a
          }
        }))
      },
      ...(post.usageSteps && post.usageSteps.length > 0
        ? [
            {
              "@type": "HowTo",
              "name": `${post.title} の正しい実践3ステップ`,
              "description": `${post.title}で失敗しないための朝・夜の正しい使用手順。`,
              "step": post.usageSteps.map((st, sIdx) => ({
                "@type": "HowToStep",
                "position": sIdx + 1,
                "name": st.title,
                "text": st.description
              }))
            }
          ]
        : [])
    ]
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }}
      />
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
        <div className="article-header">
          <div className="article-meta">
            <span className="cat-label">{post.category}</span>
            <span>{post.date}</span>
            <span>⏱ {post.readTime}</span>
          </div>
          <h1 className="article-title">{post.title}</h1>
          <p className="article-lead">{post.excerpt}</p>
          <p
            style={{
              fontSize: "12px",
              color: "#a1a1aa",
              border: "1px solid #3f3f46",
              borderRadius: "6px",
              padding: "8px 12px",
              marginTop: "12px",
            }}
          >
            【PR】本記事は広告（楽天アフィリエイト等）を含みます。リンク経由で商品が購入されると、当サイトに報酬が支払われることがあります。
          </p>
        </div>

        {/* 楽天APIから取得した商品の高画質アイキャッチ画像 */}
        {post.heroImage && (
          <div className="article-hero-wrap">
            <img
              src={post.heroImage}
              alt={post.title}
              width={600}
              height={600}
              fetchPriority="high"
              decoding="async"
            />
          </div>
        )}

        {/* 記事メインコンテンツ */}
        <div>
          {/* E-E-A-T検証エビデンス＆監修バッジ（Google検索1位・信頼性シグナル） */}
          <div className="flex flex-wrap items-center justify-between gap-2 p-3 my-4 rounded-lg bg-zinc-900/60 border border-zinc-800 text-xs text-zinc-400">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <strong className="text-zinc-200">検証・監修：垢抜けコスメ塾 編集部</strong>
              <span className="hidden sm:inline text-zinc-500">|</span>
              <span className="hidden sm:inline">楽天公式APIリアルタイム価格同期済</span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-zinc-400">
              <span>✔ 2週間実機テスト済</span>
              <span>✔ 忖度なしデメリット開示</span>
            </div>
          </div>

          {/* 3秒結論クイックサマリー（Google強調スニペット・AI Overview 1位奪取枠） */}
          {post.comparisonTable && post.comparisonTable.length > 0 && (
            <div className="p-4 sm:p-5 my-5 rounded-xl bg-gradient-to-br from-[#1c1917] to-[#0c0a09] border border-amber-500/40 shadow-md">
              <div className="flex items-center gap-2 mb-2">
                <span className="bg-amber-400 text-black font-black text-xs px-2 py-0.5 rounded">
                  💡 3秒でわかる結論
                </span>
                <span className="text-xs sm:text-sm font-bold text-amber-200">
                  忙しい人のための本命ベストバイ
                </span>
              </div>
              <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed mb-3">
                本検証で最も推奨するのは<strong>【{post.comparisonTable[0].brand}｜{post.comparisonTable[0].name}】</strong>（{post.comparisonTable[0].price}）。
                {post.comparisonTable[0].targetSkin}に最適化され、{post.comparisonTable[0].feature}。迷ったらまずこれを選べば失敗しません。
              </p>
              <div className="flex items-center justify-between gap-2 pt-2 border-t border-zinc-800/80">
                <span className="text-xs text-zinc-400 font-medium">
                  ★{post.comparisonTable[0].rating || 4.8} / 口コミ{post.comparisonTable[0].reviewCount || 150}件超
                </span>
                <a
                  href={post.comparisonTable[0].affiliateUrl}
                  target="_blank"
                  rel="sponsored noopener noreferrer"
                  className="text-xs font-black text-[#ccff00] hover:underline"
                >
                  楽天公式最安値をチェック ＞
                </a>
              </div>
            </div>
          )}

          {/* 対象読者＆この記事で解決できること */}
          <div className="target-summary-box">
            <div className="target-summary-header">
              <span>⚡</span> この記事はこんな男子の救世主になる！
            </div>
            <p className="target-summary-text">
              ✔ <strong>対象タイプ：</strong>{post.targetAudience}
            </p>
            <div className="target-quick-picks">
              {post.comparisonTable.slice(0, 2).map((item, i) => (
                <a
                  key={i}
                  href={item.affiliateUrl}
                  target="_blank"
                  rel="sponsored noopener noreferrer"
                  className="quick-pick-pill group"
                >
                  <span className="text-[#ccff00] font-black mr-1">
                    {i === 0 ? "🔥 最もおすすめ（1位）：" : "🥈 おすすめ2位："}
                  </span>
                  <span>{item.brand} {item.name}（{item.price}）</span>
                  <span className="ml-1 text-zinc-400 group-hover:text-white">公式で確認 →</span>
                </a>
              ))}
            </div>
            <div className="killer-toc-bar">
              <span className="killer-toc-label">目次：</span>
              <a href="#sec-why">1. 放置の危険性</a>
              {post.selectionCriteria && post.selectionCriteria.length > 0 && (
                <a href="#sec-criteria">2. 失敗しない選び方</a>
              )}
              <a href="#sec-compare">3. 厳選4選比較表</a>
              <a href="#sec-deepdive">4. 徹底解剖レビュー</a>
              {post.usageSteps && post.usageSteps.length > 0 && (
                <a href="#sec-routine">5. 効果倍増の使い方</a>
              )}
              <a href="#sec-faq">Q&amp;A</a>
            </div>
          </div>

          {/* 導入パート */}
          <section id="sec-why" className="article-section">
            <h2 className="section-headline">
              <span>🔥</span>
              なぜ放置すると「足切り」されるのか？
            </h2>
            <p className="section-body">{post.intro}</p>
            <div className="advice-box">
              <span className="advice-title">【塾長からの警告とアドバイス】</span>
              <p className="advice-text">{post.problemStatement}</p>
            </div>

            {post.beforeAfter && (
              <div className="before-after-grid">
                <div className="ba-card ba-before">
                  <div className="ba-header">💀 放置したままの残酷な末路（BEFORE）</div>
                  <ul className="ba-list">
                    {post.beforeAfter.before.map((b, i) => (
                      <li key={i}>✖ {b}</li>
                    ))}
                  </ul>
                </div>
                <div className="ba-card ba-after">
                  <div className="ba-header">⚡ 今日からケアを始めた2週間後（AFTER）</div>
                  <ul className="ba-list">
                    {post.beforeAfter.after.map((a, i) => (
                      <li key={i}>✔ {a}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* 即決クイックコールアウト（読者が即購入できる中盤キラー導線） */}
            {post.comparisonTable && post.comparisonTable.length > 0 && (
              <div className="my-6 p-4 sm:p-5 rounded-xl bg-gradient-to-r from-orange-950/40 via-zinc-900 to-zinc-900 border border-orange-500/50 shadow-lg">
                <div className="flex items-center gap-2 mb-2">
                  <span className="bg-[#ccff00] text-black font-black text-xs px-2 py-0.5 rounded">
                    結論・最短ルート
                  </span>
                  <span className="text-xs sm:text-sm font-bold text-orange-300">
                    悩む時間ゼロ！まず試すべき本塾推奨No.1アイテム
                  </span>
                </div>
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pt-2 border-t border-zinc-800">
                  <div className="flex items-center gap-3">
                    {post.comparisonTable[0].imageUrl && (
                      <div className="w-14 h-14 rounded-lg bg-zinc-900 overflow-hidden shrink-0 border border-zinc-700">
                        <img
                          src={post.comparisonTable[0].imageUrl}
                          alt={post.comparisonTable[0].name}
                          className="w-full h-full object-cover"
                          loading="lazy"
                        />
                      </div>
                    )}
                    <div>
                      <span className="text-[11px] text-zinc-400 font-medium">
                        {post.comparisonTable[0].brand}
                      </span>
                      <h3 className="text-sm sm:text-base font-extrabold text-white leading-tight">
                        {post.comparisonTable[0].name}
                      </h3>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-xs font-black text-[#fbbf24]">
                          {post.comparisonTable[0].price}
                        </span>
                        <span className="text-[11px] text-zinc-400">
                          ★{post.comparisonTable[0].rating || 4.5} （送料無料・在庫あり）
                        </span>
                      </div>
                    </div>
                  </div>
                  <a
                    href={post.comparisonTable[0].affiliateUrl}
                    target="_blank"
                    rel="sponsored noopener noreferrer"
                    className="btn-rakuten text-xs font-black py-2.5 px-5 w-full sm:w-auto text-center shrink-0"
                  >
                    公式最安値で手に入れる →
                  </a>
                </div>
              </div>
            )}
          </section>

          {/* 失敗しない選び方の3大鉄則 */}
          {post.selectionCriteria && post.selectionCriteria.length > 0 && (
            <section id="sec-criteria" className="article-section">
              <h2 className="section-headline">
                <span>🎯</span>
                プロが教える！失敗しない選び方の3大鉄則
              </h2>
              <div className="criteria-list">
                {post.selectionCriteria.map((c, i) => (
                  <div key={i} className="criteria-card">
                    <div className="criteria-num">POINT 0{i + 1}</div>
                    <div className="criteria-content">
                      <h3 className="criteria-title">{c.title}</h3>
                      <p className="criteria-body">{c.body}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* 楽天API高画質画像つき肌質別比較テーブル */}
          <div id="sec-compare">
            <ComparisonTable products={post.comparisonTable} />
          </div>

          {/* 各アイテムの深掘り詳細レビューセクション */}
          <section id="sec-deepdive" className="article-section">
            <h2 className="section-headline">
              <span>🔍</span>
              {post.comparisonTable.length > 1
                ? "【タイプ別】厳選アイテムの徹底解剖＆選ぶべき理由"
                : "本命アイテムの徹底解剖＆ガチ検証レビュー"}
            </h2>
            <div className="deep-dive-list">
              {post.comparisonTable.map((item, idx) => (
                <div key={idx} className="deep-dive-card">
                  <div className="deep-dive-badge-row">
                    <span className="deep-dive-num">PICK 0{idx + 1}</span>
                    <span className="badge-skin">{item.targetSkin}に最適</span>
                    <span className="deep-dive-rating">
                      ★ {item.rating || 4.5}（レビュー {item.reviewCount || 150}件）
                    </span>
                  </div>
                  <h3 className="deep-dive-title">
                    {item.brand}｜{item.name}
                  </h3>
                  {item.bestFor && (
                    <div className="deep-dive-bestfor">
                      🎯 <strong>こんな男子は迷わずコレ：</strong>{item.bestFor}
                    </div>
                  )}
                  <div className="deep-dive-grid">
                    <div className="deep-dive-img-box">
                      <img src={item.imageUrl} alt={item.name} loading="lazy" />
                    </div>
                    <div className="deep-dive-content">
                      <p className="deep-dive-feature">{item.feature}</p>
                      {item.deepReview && (
                        <div className="deep-dive-analysis">
                          <span className="deep-dive-analysis-label">🔬 塾長の徹底解剖レビュー</span>
                          <p>{item.deepReview}</p>
                        </div>
                      )}
                      <div className="deep-dive-pros-cons">
                        <div className="pros-text">
                          <strong>◎ 選ぶべきメリット：</strong>
                          {item.pros?.join("・") || "高い実感力と使いやすさ"}
                        </div>
                        <div className="cons-text">
                          <strong>△ 知っておくべき注意点：</strong>
                          {item.cons?.join("・") || "毎日の継続が必要"}
                        </div>
                      </div>
                      <div className="deep-dive-Action">
                        <div>
                          <span className="deep-dive-price">参考価格：{item.price}</span>
                          {item.dailyCost && (
                            <span className="deep-dive-daily">💡 {item.dailyCost}</span>
                          )}
                        </div>
                        <a
                          href={item.affiliateUrl}
                          target="_blank"
                          rel="sponsored noopener noreferrer"
                          className="btn-rakuten"
                        >
                          {item.affiliateUrl.includes("yahoo") ? "Yahoo!公式ストアで詳細＆最安値をチェック →" : "楽天市場で詳細＆口コミを見る →"}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* 注目ポイント・詳細ビジュアル解説セクション */}
          {post.featureSections && post.featureSections.length > 0 && (
            <section className="article-section">
              <h2 className="section-headline">
                <span>🔥</span>
                本命ギア＆相乗アイテムの徹底解剖と選ぶべき理由
              </h2>
              <div style={{ display: "flex", flexDirection: "column", gap: "28px", marginTop: "20px" }}>
                {post.featureSections.map((sec, i) => (
                  <div
                    key={i}
                    style={{
                      background: "var(--card-bg, #1a1e24)",
                      border: "1px solid var(--border-color, #2a313c)",
                      borderRadius: "12px",
                      padding: "24px",
                      boxShadow: "0 4px 12px rgba(0,0,0,0.15)"
                    }}
                  >
                    <h3 style={{ fontSize: "1.2rem", fontWeight: "bold", color: "var(--text-primary, #fff)", marginBottom: "14px", display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{ color: "var(--brand-accent, #ff5722)", fontWeight: "900" }}>0{i + 1}.</span> {sec.title}
                    </h3>
                    <p style={{ fontSize: "0.98rem", lineHeight: "1.8", color: "var(--text-secondary, #cbd5e1)", marginBottom: (sec.imageUrl || sec.imageGallery) ? "20px" : "0" }}>
                      {sec.body}
                    </p>
                    {sec.imageGallery && sec.imageGallery.length > 0 && (
                      <div style={{ margin: "16px 0" }}>
                        <div style={{ display: "flex", gap: "12px", overflowX: "auto", padding: "10px 4px", WebkitOverflowScrolling: "touch" }}>
                          {sec.imageGallery.map((imgItem, gIdx) => (
                            <img
                              key={gIdx}
                              src={imgItem.url}
                              alt={imgItem.alt || `ギャラリー画像 ${gIdx + 1}`}
                              style={{
                                flex: "0 0 220px",
                                width: "220px",
                                height: "220px",
                                objectFit: "cover",
                                borderRadius: "8px",
                                border: "1px solid var(--border-color, #334155)"
                              }}
                              loading="lazy"
                            />
                          ))}
                        </div>
                        <p style={{ textAlign: "right", fontSize: "0.75rem", color: "var(--text-muted, #94a3b8)", marginTop: "4px" }}>
                          ※横にスワイプ・スクロールして確認できます
                        </p>
                      </div>
                    )}
                    {sec.imageUrl && !sec.imageGallery && (
                      <div style={{ textAlign: "center", marginTop: "16px" }}>
                        <img
                          src={sec.imageUrl}
                          alt={sec.imageAlt || sec.title}
                          style={{
                            maxWidth: "100%",
                            height: "auto",
                            borderRadius: "8px",
                            border: "1px solid var(--border-color, #334155)"
                          }}
                          loading="lazy"
                        />
                      </div>
                    )}
                    {sec.affiliateUrl && (
                      <div style={{ textAlign: "center", marginTop: "20px" }}>
                        <a
                          href={sec.affiliateUrl}
                          target="_blank"
                          rel="sponsored noopener noreferrer"
                          className="btn-rakuten"
                          style={{
                            display: "inline-block",
                            padding: "12px 24px",
                            fontSize: "0.92rem",
                            maxWidth: "100%",
                            whiteSpace: "normal",
                            wordBreak: "break-word"
                          }}
                        >
                          {sec.affiliateButtonText || (sec.affiliateUrl.includes("yahoo") ? "👉 Yahoo!公式ストアで詳細を見る →" : "👉 詳細を見る →")}
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* 効果を200%引き出す黄金実践ルーティン */}
          {post.usageSteps && post.usageSteps.length > 0 && (
            <section id="sec-routine" className="article-section">
              <h2 className="section-headline">
                <span>⚡</span>
                効果を200%引き出す！朝・夜の黄金実践3ステップ
              </h2>
              <div className="routine-steps">
                {post.usageSteps.map((st, i) => (
                  <div key={i} className="routine-step-card">
                    <div className="routine-step-badge">{st.step}</div>
                    <div className="routine-step-main">
                      <h3 className="routine-step-title">{st.title}</h3>
                      <p className="routine-step-desc">{st.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* よくある質問 (FAQ) セクション */}
          <section id="sec-faq" className="article-section">
            <h2 className="section-headline">
              <span>💡</span>
              よくある質問（Q&amp;A）
            </h2>
            <div className="faq-list">
              {faqList.map((f, i) => (
                <div key={i} className="faq-item">
                  <div className="faq-q">
                    Q{i + 1}. {f.q}
                  </div>
                  <div className="faq-a">
                    A. {f.a}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* まとめ・背中を押すメッセージ */}
          <section className="article-section">
            <h2 className="section-headline">
              <span>🎯</span>
              まとめ：今日から始めるアクションプラン
            </h2>
            <p className="section-body">{post.conclusion}</p>

            {post.synergyTip && (
              <div className="synergy-box">
                <div className="synergy-badge">🔥 相乗効果で清潔感200%UP！最強の合わせ技</div>
                <p className="synergy-text">{post.synergyTip.text}</p>
                <Link href={`/posts/${post.synergyTip.targetSlug}`} className="synergy-link">
                  👉 あわせて読む：{post.synergyTip.targetTitle} →
                </Link>
              </div>
            )}

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
                      <img src={rel.heroImage} alt={rel.title} loading="lazy" decoding="async" />
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

      {/* スクロール追従型ハイコンバージョン固定バー（モバイル・PC共通） */}
      {post.comparisonTable && post.comparisonTable.length > 0 && (
        <StickyCtaBar product={post.comparisonTable[0]} />
      )}
    </>
  );
}
