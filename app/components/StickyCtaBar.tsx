"use client";

import { useState, useEffect } from "react";
import { ProductComparison } from "@/data/types";

interface Props {
  product: ProductComparison;
}

export default function StickyCtaBar({ product }: Props) {
  const [isVisible, setIsVisible] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      // 350px以上スクロールされたら表示
      if (window.scrollY > 350 && !isDismissed) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [isDismissed]);

  if (!product || isDismissed || !isVisible) return null;

  return (
    <aside
      aria-label="おすすめ商品の購入・申込み案内"
      className="fixed bottom-0 left-0 right-0 z-50 p-2 sm:p-3 bg-[#111318]/95 backdrop-blur-md border-t border-[#f97316]/40 shadow-[0_-8px_24px_rgba(0,0,0,0.7)] transition-all duration-300 animate-in fade-in slide-in-from-bottom"
    >
      <div className="max-w-4xl mx-auto flex items-center justify-between gap-2 sm:gap-4">
        {/* サムネイルと商品情報 */}
        <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
          {product.imageUrl && (
            <div className="relative w-11 h-11 sm:w-13 sm:h-13 shrink-0 rounded-md overflow-hidden bg-[#1f242d] border border-zinc-700">
              <img
                src={product.imageUrl}
                alt={product.name}
                className="w-full h-full object-cover"
                loading="lazy"
                decoding="async"
              />
            </div>
          )}
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="text-[10px] font-black uppercase tracking-wider px-1.5 py-0.5 rounded bg-gradient-to-r from-amber-500 to-orange-500 text-black">
                本命1位
              </span>
              <span className="text-[11px] text-zinc-400 font-medium truncate max-w-[140px] sm:max-w-none">
                {product.brand}
              </span>
            </div>
            <p className="text-xs sm:text-sm font-bold text-white truncate leading-tight mt-0.5">
              {product.name}
            </p>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-xs font-black text-[#fbbf24]">
                {product.price}
              </span>
              <span className="text-[10px] text-zinc-400 hidden sm:inline">
                ★{product.rating || 4.5} （送料無料・在庫確認）
              </span>
            </div>
          </div>
        </div>

        {/* CTAボタン & 閉じる */}
        <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <a
            href={product.affiliateUrl}
            target="_blank"
            rel="sponsored noopener noreferrer"
            className="group relative inline-flex items-center justify-center px-3.5 py-2 sm:px-5 sm:py-2.5 rounded-lg text-xs sm:text-sm font-extrabold text-white bg-gradient-to-r from-[#ea580c] via-[#f97316] to-[#fb923c] shadow-lg shadow-orange-950/50 hover:brightness-110 active:scale-95 transition-all overflow-hidden"
          >
            <span className="relative z-10 flex items-center gap-1">
              <span>{product.affiliateUrl.includes("yahoo") ? "公式で見る" : "楽天で詳細を見る"}</span>
              <span className="transition-transform group-hover:translate-x-0.5">→</span>
            </span>
            <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent transition-transform duration-700 ease-in-out" />
          </a>
          <button
            type="button"
            onClick={() => setIsDismissed(true)}
            aria-label="閉じる"
            className="p-1.5 text-zinc-400 hover:text-white rounded-md hover:bg-zinc-800/80 transition-colors"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </aside>
  );
}
