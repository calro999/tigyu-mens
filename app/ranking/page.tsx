import Link from "next/link";
import Image from "next/image";
import { getRankingPosts } from "@/data/posts";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "殿堂入りランキング | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "当塾で読者から最もアクセス・高評価を集めた神コスメ＆垢抜けギアの殿堂入りランキング。",
};

export default function RankingPage() {
  const rankingPosts = getRankingPosts();

  return (
    <main className="max-w-[1000px] mx-auto px-5 py-12">
      <div className="mb-10 text-center">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          HALL OF FAME RANKING
        </span>
        <h1 className="text-3xl sm:text-4xl font-black text-[#f4f4f5] mb-4">
          殿堂入り人気ランキング TOP 5
        </h1>
        <p className="text-sm text-[#a1a1aa] max-w-xl mx-auto">
          「まずは失敗しない王道から試したい」という塾生のために、読者支持率No.1の人気記事＆アイテムを厳選。
        </p>
      </div>

      <div className="space-y-6">
        {rankingPosts.map((post, idx) => (
          <Link
            key={post.slug}
            href={`/posts/${post.slug}`}
            className="bg-[#18181b] border border-[#27272a] hover:border-[#ccff00] rounded-xl overflow-hidden flex flex-col sm:flex-row items-center p-4 sm:p-6 gap-6 transition-all group"
          >
            {/* 順位バッジ */}
            <div className="flex sm:flex-col items-center justify-center w-full sm:w-16">
              <span
                className={`text-3xl sm:text-4xl font-black italic ${
                  idx === 0
                    ? "text-[#ccff00]"
                    : idx === 1
                    ? "text-slate-300"
                    : idx === 2
                    ? "text-amber-500"
                    : "text-[#71717a]"
                }`}
              >
                #{idx + 1}
              </span>
              <span className="text-[10px] text-[#a1a1aa] uppercase tracking-wider font-bold ml-2 sm:ml-0">
                RANK
              </span>
            </div>

            {/* サムネイル */}
            <div className="w-full sm:w-48 h-36 relative rounded-lg overflow-hidden flex-shrink-0 bg-[#222]">
              <Image
                src={post.heroImage}
                alt={post.title}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>

            {/* テキスト */}
            <div className="flex-1">
              <div className="flex items-center gap-2 text-xs text-[#a1a1aa] mb-2">
                <span className="bg-[#ccff00]/10 text-[#ccff00] px-2 py-0.5 rounded font-bold">
                  {post.category}
                </span>
                <span>🔥 月間閲覧数: {post.views?.toLocaleString()} PV</span>
              </div>
              <h2 className="text-lg sm:text-xl font-black text-[#f4f4f5] group-hover:text-[#ccff00] transition-colors mb-2 leading-snug">
                {post.title}
              </h2>
              <p className="text-xs sm:text-sm text-[#a1a1aa] line-clamp-2 leading-relaxed">
                {post.excerpt}
              </p>
            </div>

            {/* アクション */}
            <div className="hidden lg:block text-right">
              <span className="inline-block bg-[#ccff00] text-black font-extrabold text-xs px-4 py-2 rounded-lg group-hover:scale-105 transition-transform whitespace-nowrap">
                記事を読む →
              </span>
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
