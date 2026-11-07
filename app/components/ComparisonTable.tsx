import { ProductComparison } from "@/data/types";

interface Props {
  products: ProductComparison[];
}

export default function ComparisonTable({ products }: Props) {
  if (!products || products.length === 0) return null;

  return (
    <div className="comparison-wrapper">
      <div className="comparison-header">
        <span className="comparison-bar"></span>
        <h3 className="comparison-heading">
          【肌質・タイプ別】徹底比較テーブル＆おすすめアイテム
        </h3>
      </div>

      <p className="comparison-desc">
        「どれを買えばいいか分からない」を解消！自分の肌質・目的タイプ（乾燥・オイリー・混合肌・高機能）に合わせて選べば失敗しません。楽天公式の高画質レビューリンク付きです。
      </p>

      {/* スマホ・タブレット向け高CVカードビュー */}
      <div className="comp-cards-mobile">
        {products.map((p, idx) => (
          <div
            key={idx}
            className={`comp-card-item relative ${
              idx === 0 ? "border-[#ccff00]/60 shadow-[0_0_20px_rgba(204,255,0,0.12)]" : ""
            }`}
          >
            {idx === 0 && (
              <div className="inline-block mb-2 bg-[#ccff00] text-black font-black text-[11px] px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                👑 おすすめNo.1・本命枠
              </div>
            )}
            <div className="comp-card-top">
              <span className="badge-skin">{p.targetSkin}</span>
              <span className="comp-card-rating">
                ★ {p.rating || 4.5} ({p.reviewCount || 120}件)
              </span>
            </div>
            <div className="comp-card-body">
              <div className="comp-card-img">
                {p.imageUrl ? (
                  <img src={p.imageUrl} alt={p.name} loading="lazy" decoding="async" />
                ) : (
                  <span>NO IMG</span>
                )}
              </div>
              <div className="comp-card-info">
                <span className="item-brand">{p.brand}</span>
                <h4 className="comp-card-name">{p.name}</h4>
                <span className="comp-card-price">{p.price}</span>
                {p.dailyCost && (
                  <span className="comp-card-daily">{p.dailyCost}</span>
                )}
              </div>
            </div>
            {p.bestFor && (
              <div className="comp-card-bestfor">
                🎯 <strong>おすすめな人：</strong>{p.bestFor}
              </div>
            )}
            <p className="comp-card-feature">{p.feature}</p>
            <div className="pros-cons-box" style={{ marginBottom: "14px" }}>
              <div className="pros-text">
                <span>◎ メリット：</span>
                {p.pros?.join(" / ") || "使用感が良い"}
              </div>
              <div className="cons-text">
                <span>△ 注意点：</span>
                {p.cons?.join(" / ") || "継続使用が前提"}
              </div>
            </div>
            <a
              href={p.affiliateUrl}
              target="_blank"
              rel="sponsored noopener noreferrer"
              className="btn-rakuten comp-card-btn"
            >
              {p.affiliateUrl.includes("yahoo")
                ? "Yahoo!公式で最安値・在庫を見る →"
                : "楽天市場で公式最安値・口コミを見る →"}
            </a>
          </div>
        ))}
      </div>

      {/* PC表示用テーブル */}
      <div className="table-responsive">
        <table className="comp-table">
          <colgroup>
            <col style={{ width: "27%" }} />
            <col style={{ width: "17%" }} />
            <col style={{ width: "23%" }} />
            <col style={{ width: "20%" }} />
            <col style={{ width: "13%" }} />
          </colgroup>
          <thead>
            <tr>
              <th>商品 / ブランド</th>
              <th>推奨タイプ</th>
              <th>特徴・アピール点</th>
              <th>メリット / デメリット</th>
              <th style={{ textAlign: "center" }}>詳細</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p, idx) => (
              <tr key={idx}>
                <td>
                  <div className="item-cell">
                    <div className="item-img-wrap">
                      {p.imageUrl ? (
                        <img src={p.imageUrl} alt={p.name} loading="lazy" decoding="async" />
                      ) : (
                        <div style={{ padding: "10px", fontSize: "0.7rem", color: "var(--text-muted)" }}>
                          NO IMG
                        </div>
                      )}
                    </div>
                    <div>
                      <span className="item-brand">{p.brand}</span>
                      <span className="item-name">{p.name}</span>
                      <span className="item-price">
                        {p.price}{" "}
                        <span style={{ fontSize: "0.72rem", color: "#facc15", marginLeft: "6px" }}>
                          ★{p.rating || 4.5} ({p.reviewCount || 120}件)
                        </span>
                      </span>
                    </div>
                  </div>
                </td>
                <td>
                  <span className="badge-skin">{p.targetSkin}</span>
                  {p.bestFor && (
                    <div style={{ fontSize: "0.72rem", color: "#e4e4e7", marginTop: "6px", lineHeight: "1.4" }}>
                      🎯 {p.bestFor}
                    </div>
                  )}
                </td>
                <td className="comp-table-feature-cell">
                  {p.feature}
                  {p.dailyCost && (
                    <div style={{ fontSize: "0.73rem", color: "var(--brand-accent)", marginTop: "6px", fontWeight: 700 }}>
                      💡 {p.dailyCost}
                    </div>
                  )}
                </td>
                <td>
                  <div className="pros-cons-box">
                    <div className="pros-text">
                      <span>◎ </span>
                      {p.pros?.join(" / ") || "使用感が良い"}
                    </div>
                    <div className="cons-text">
                      <span>△ </span>
                      {p.cons?.join(" / ") || "やや高価"}
                    </div>
                  </div>
                </td>
                <td style={{ textAlign: "center" }}>
                  <a
                    href={p.affiliateUrl}
                    target="_blank"
                    rel="sponsored noopener noreferrer"
                    className="btn-rakuten"
                  >
                    {p.affiliateUrl.includes("yahoo") ? "Yahoo!で見る →" : "楽天で見る →"}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
