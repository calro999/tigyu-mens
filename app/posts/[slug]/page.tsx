import { notFound } from "next/navigation";
import Image from "next/image";
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
  const post = getPostBySlug(slug);
  if (!post) return {};

  return {
    title: `${post.title} | 垢抜けコスメ塾`,
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
  const post = getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const allPosts = getAllPosts();
  const relatedPosts = allPosts.filter((p) => p.slug !== post.slug).slice(0, 3);

  return (
    <article className="max-w-[1000px] mx-auto px-5 py-10">
      {/* パンくずリスト */}
      <nav className="text-xs text-[#a1a1aa] mb-6 flex items-center gap-2">
        <Link href="/" className="hover:text-[#ccff00]">
          TOP
        </Link>
        <span>&gt;</span>
        <Link href={`/reviews?cat=${encodeURIComponent(post.category)}`} className="hover:text-[#ccff00]">
          {post.category}
        </Link>
        <span>&gt;</span>
        <span className="text-[#f4f4f5] line-clamp-1">{post.title}</span>
      </nav>

      {/* 記事ヘッダー */}
      <header className="mb-8">
        <div className="flex flex-wrap items-center gap-2 text-xs mb-4">
          <span className="bg-[#ccff00] text-black font-black px-3 py-1 rounded-full">
            {post.category}
          </span>
          <span className="text-[#a1a1aa] font-medium">{post.date}</span>
          <span className="text-[#a1a1aa] font-medium">⏱ {post.readTime}</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-[#f4f4f5] leading-snug mb-4">
          {post.title}
        </h1>
        <p className="text-sm sm:text-base text-[#a1a1aa] leading-relaxed bg-[#18181b] border-l-4 border-[#ccff00] p-4 rounded-r-lg">
          {post.excerpt}
        </p>
      </header>

      {/* アイキャッチ画像 */}
      <div className="relative w-full h-[320px] sm:h-[460px] rounded-xl overflow-hidden mb-10 border border-[#27272a]">
        <Image
          src={post.heroImage}
          alt={post.title}
          fill
          priority
          className="object-cover"
        />
      </div>

      {/* 記事メインコンテンツ */}
      <div className="space-y-10 leading-relaxed text-[#f4f4f5]">
        {/* 導入パート */}
        <section className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-8">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-xl">🔥</span>
            <h2 className="text-xl sm:text-2xl font-black text-[#f4f4f5]">
              なぜ放置すると「足切り」されるのか？
            </h2>
          </div>
          <p className="text-sm sm:text-base text-[#a1a1aa] leading-relaxed whitespace-pre-line mb-4">
            {post.intro}
          </p>
          <div className="bg-[#09090b] border border-[#3f3f46] p-4 rounded-lg">
            <h3 className="text-xs font-bold text-[#ccff00] mb-1">【塾長からのアドバイス】</h3>
            <p className="text-xs sm:text-sm text-[#f4f4f5]">
              {post.problemStatement}
            </p>
          </div>
        </section>

        {/* 比較テーブル＆商品ピックアップ */}
        <ComparisonTable products={post.comparisonTable} />

        {/* まとめ・背中を押すメッセージ */}
        <section className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-8">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-xl">🎯</span>
            <h2 className="text-xl sm:text-2xl font-black text-[#f4f4f5]">
              まとめ：今日から始めるアクションプラン
            </h2>
          </div>
          <p className="text-sm sm:text-base text-[#a1a1aa] leading-relaxed whitespace-pre-line mb-6">
            {post.conclusion}
          </p>
          <div className="p-4 bg-[#ccff00]/10 border border-[#ccff00]/30 rounded-lg text-center">
            <span className="text-sm font-extrabold text-[#ccff00] block mb-1">
              迷ったらまずは「乾燥肌」または「オイリー肌」の自分に合う方を1つだけ試すこと！
            </span>
            <span className="text-xs text-[#a1a1aa]">
              完璧を目指さず、1つルーティンに加えるだけで清潔感は5割増しになります。
            </span>
          </div>
        </section>

        {/* タグ一覧 */}
        <div className="flex flex-wrap gap-2 pt-4">
          {post.tags.map((tag) => (
            <Link
              key={tag}
              href={`/reviews?tag=${encodeURIComponent(tag)}`}
              className="bg-[#18181b] border border-[#27272a] text-[#a1a1aa] hover:text-[#f4f4f5] hover:border-[#ccff00] text-xs px-3 py-1.5 rounded"
            >
              {tag}
            </Link>
          ))}
        </div>
      </div>

      {/* 関連記事 */}
      {relatedPosts.length > 0 && (
        <section className="mt-16 pt-10 border-t border-[#27272a]">
          <h3 className="text-xl font-black text-[#f4f4f5] mb-6 flex items-center gap-2">
            <span className="w-1.5 h-4 bg-[#ccff00] inline-block"></span>
            あわせて読みたい検証記事
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
            {relatedPosts.map((rel) => (
              <Link
                key={rel.slug}
                href={`/posts/${rel.slug}`}
                className="bg-[#18181b] border border-[#27272a] hover:border-[#3f3f46] rounded-lg overflow-hidden group"
              >
                <div className="h-36 relative bg-[#222]">
                  <Image
                    src={rel.heroImage}
                    alt={rel.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform"
                  />
                </div>
                <div className="p-4">
                  <span className="text-[10px] text-[#ccff00] font-bold block mb-1">
                    {rel.category}
                  </span>
                  <h4 className="text-xs sm:text-sm font-bold text-[#f4f4f5] line-clamp-2 group-hover:text-[#ccff00] transition-colors leading-snug">
                    {rel.title}
                  </h4>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </article>
  );
}
