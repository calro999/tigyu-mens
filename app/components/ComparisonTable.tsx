import Image from "next/image";
import { ProductComparison } from "@/data/types";

interface Props {
  products: ProductComparison[];
}

export default function ComparisonTable({ products }: Props) {
  if (!products || products.length === 0) return null;

  return (
    <div className="my-10 bg-[#18181b] border border-[#27272a] rounded-xl p-5 sm:p-8">
      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-[#27272a]">
        <span className="w-3 h-6 bg-[#ccff00] rounded-sm block"></span>
        <h3 className="text-xl sm:text-2xl font-black text-[#f4f4f5]">
          【肌質・タイプ別】徹底比較テーブル＆おすすめアイテム
        </h3>
      </div>

      <p className="text-sm text-[#a1a1aa] mb-6">
        「どれを買えばいいか分からない」を解消！自分の肌質（乾燥・オイリー・混合肌）に合わせて選べば失敗しません。楽天公認の高画質レビューリンク付きです。
      </p>

      {/* PC表示用テーブル */}
      <div className="hidden lg:block overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-[#3f3f46] text-[#a1a1aa] text-xs uppercase tracking-wider">
              <th className="py-3 px-4">商品 / ブランド</th>
              <th className="py-3 px-4">推奨タイプ</th>
              <th className="py-3 px-4">特徴・アピール点</th>
              <th className="py-3 px-4">メリット / デメリット</th>
              <th className="py-3 px-4 text-center">詳細・購入</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#27272a] text-sm">
            {products.map((p, idx) => (
              <tr key={idx} className="hover:bg-[#27272a]/50 transition-colors">
                <td className="py-4 px-4 flex items-center gap-4">
                  <div className="w-16 h-16 relative flex-shrink-0 bg-black/40 rounded-md overflow-hidden border border-[#3f3f46]">
                    {p.imageUrl ? (
                      <Image
                        src={p.imageUrl}
                        alt={p.name}
                        fill
                        className="object-contain p-1"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-xs text-[#a1a1aa]">
                        NO IMG
                      </div>
                    )}
                  </div>
                  <div>
                    <span className="text-[10px] text-[#ccff00] font-bold block">{p.brand}</span>
                    <span className="font-bold text-[#f4f4f5] text-sm line-clamp-2">{p.name}</span>
                    <span className="text-xs text-[#a1a1aa] font-semibold">{p.price}</span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <span className="inline-block bg-[#ccff00]/10 border border-[#ccff00]/30 text-[#ccff00] text-xs font-bold px-2.5 py-1 rounded-full whitespace-nowrap">
                    {p.targetSkin}
                  </span>
                </td>
                <td className="py-4 px-4 text-[#a1a1aa] text-xs leading-relaxed max-w-xs">
                  {p.feature}
                </td>
                <td className="py-4 px-4 text-xs space-y-1">
                  <div className="text-emerald-400">
                    <span className="font-bold">◎ </span>
                    {p.pros?.join(" / ") || "使用感が良い"}
                  </div>
                  <div className="text-rose-400">
                    <span className="font-bold">△ </span>
                    {p.cons?.join(" / ") || "やや高価"}
                  </div>
                </td>
                <td className="py-4 px-4 text-center">
                  <a
                    href={p.affiliateUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-block bg-[#ccff00] hover:bg-[#b8e600] text-black font-extrabold text-xs px-4 py-2 rounded-lg transition-transform hover:scale-105 shadow-md whitespace-nowrap"
                  >
                    楽天で見る →
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* スマホ・タブレット表示用カードグリッド */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 lg:hidden">
        {products.map((p, idx) => (
          <div
            key={idx}
            className="bg-[#09090b] border border-[#27272a] rounded-lg p-4 flex flex-col justify-between"
          >
            <div>
              <div className="flex gap-4 mb-3">
                <div className="w-20 h-20 relative flex-shrink-0 bg-[#18181b] rounded-md overflow-hidden border border-[#3f3f46]">
                  {p.imageUrl ? (
                    <Image
                      src={p.imageUrl}
                      alt={p.name}
                      fill
                      className="object-contain p-1"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-xs text-[#a1a1aa]">
                      NO IMG
                    </div>
                  )}
                </div>
                <div>
                  <span className="text-[10px] text-[#ccff00] font-bold block">{p.brand}</span>
                  <h4 className="text-sm font-bold text-[#f4f4f5] line-clamp-2">{p.name}</h4>
                  <span className="text-xs text-[#a1a1aa]">{p.price}</span>
                  <div className="mt-1">
                    <span className="inline-block bg-[#ccff00]/10 text-[#ccff00] text-[10px] font-bold px-2 py-0.5 rounded">
                      {p.targetSkin}
                    </span>
                  </div>
                </div>
              </div>
              <p className="text-xs text-[#a1a1aa] mb-3 leading-relaxed">{p.feature}</p>
              <div className="text-[11px] space-y-1 mb-4 bg-[#18181b] p-2.5 rounded border border-[#27272a]">
                <div className="text-emerald-400">
                  <span className="font-bold">◎ </span>
                  {p.pros?.join(" / ")}
                </div>
                <div className="text-rose-400">
                  <span className="font-bold">△ </span>
                  {p.cons?.join(" / ")}
                </div>
              </div>
            </div>
            <a
              href={p.affiliateUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full text-center block bg-[#ccff00] hover:bg-[#b8e600] text-black font-extrabold text-xs py-2.5 rounded-lg transition-transform shadow"
            >
              楽天市場で最安値を見る ↗
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
