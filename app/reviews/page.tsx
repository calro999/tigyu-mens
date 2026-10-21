import Link from "next/link";
import Image from "next/image";
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
    <main className="max-w-[1200px] mx-auto px-5 py-12">
      <div className="mb-10 text-center">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          REVIEWS & BENCHMARKS
        </span>
        <h1 className="text-3xl sm:text-4xl font-black text-[#f4f4f5] mb-4">
          最新の検証・比較レポート
        </h1>
        <p className="text-sm text-[#a1a1aa] max-w-xl mx-auto">
          ドラッグストアから楽天で話題の本格コスメまで、実際に効果の出るアイテムだけを肌質別に徹底比較しています。
        </p>
      </div>

      {/* カテゴリフィルタ */}
      <div className="flex flex-wrap justify-center gap-2 mb-10">
        {categories.map((c) => {
          const isSelected = (!cat && c === "すべて") || cat === c;
          return (
            <Link
              key={c}
              href={c === "すべて" ? "/reviews" : `/reviews?cat=${encodeURIComponent(c)}`}
              className={`text-xs px-4 py-2 rounded-full font-bold transition-colors ${
                isSelected
                  ? "bg-[#ccff00] text-black"
                  : "bg-[#18181b] border border-[#27272a] text-[#a1a1aa] hover:text-[#f4f4f5]"
              }`}
            >
              {c}
            </Link>
          );
        })}
      </div>

      {/* 記事一覧 */}
      {filteredPosts.length === 0 ? (
        <div className="text-center py-20 bg-[#18181b] rounded-lg border border-[#27272a]">
          <p className="text-sm text-[#a1a1aa]">該当する記事が見つかりませんでした。</p>
          <Link href="/reviews" className="mt-4 inline-block text-xs font-bold text-[#ccff00]">
            すべての記事を表示する →
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPosts.map((post) => (
            <Link
              key={post.slug}
              href={`/posts/${post.slug}`}
              className="bg-[#18181b] border border-[#27272a] hover:border-[#3f3f46] hover:-translate-y-1 rounded-xl overflow-hidden flex flex-col justify-between transition-all duration-300 group"
            >
              <div>
                <div className="h-48 relative bg-[#222]">
                  <Image
                    src={post.heroImage}
                    alt={post.title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <span className="absolute top-3 left-3 bg-black/80 backdrop-blur-sm text-[#ccff00] text-[10px] font-bold px-2.5 py-1 rounded">
                    {post.category}
                  </span>
                </div>
                <div className="p-5">
                  <div className="flex items-center gap-2 text-[11px] text-[#a1a1aa] mb-2">
                    <span>{post.date}</span>
                    <span>•</span>
                    <span>⏱ {post.readTime}</span>
                  </div>
                  <h2 className="text-base font-black text-[#f4f4f5] group-hover:text-[#ccff00] transition-colors leading-snug mb-2 line-clamp-2">
                    {post.title}
                  </h2>
                  <p className="text-xs text-[#a1a1aa] line-clamp-2 leading-relaxed">
                    {post.excerpt}
                  </p>
                </div>
              </div>
              <div className="p-5 pt-0">
                <span className="text-xs font-bold text-[#ccff00] group-hover:underline">
                  比較テーブルを見る →
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </main>
  );
}
