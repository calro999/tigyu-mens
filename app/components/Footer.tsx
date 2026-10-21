import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-[#18181b] border-t border-[#27272a] pt-16 pb-8 mt-20">
      <div className="max-w-[1200px] mx-auto px-5">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-12">
          <div>
            <div className="text-lg font-black mb-3 text-[#f4f4f5]">
              もうチー牛とは呼ばせない！<br />
              ゼロから始める垢抜けコスメ塾
            </div>
            <p className="text-sm text-[#a1a1aa] leading-relaxed">
              本気で清潔感を手に入れ、陰キャ・チー牛から脱却したい男性のための垢抜け検証メディア。乾燥肌・脂性肌などタイプ別に徹底比較し、迷わず選べる最適解を届けます。
            </p>
          </div>
          <div>
            <h4 className="text-base font-bold mb-4 text-[#f4f4f5]">カリキュラム</h4>
            <ul className="space-y-2.5 text-sm text-[#a1a1aa]">
              <li>
                <Link href="/curriculum" className="hover:text-[#ccff00] transition-colors">
                  スキンケア基礎編
                </Link>
              </li>
              <li>
                <Link href="/curriculum" className="hover:text-[#ccff00] transition-colors">
                  ヘア＆眉毛セット編
                </Link>
              </li>
              <li>
                <Link href="/curriculum" className="hover:text-[#ccff00] transition-colors">
                  体型・姿勢改善編
                </Link>
              </li>
              <li>
                <Link href="/curriculum" className="hover:text-[#ccff00] transition-colors">
                  ニオイ・体臭対策編
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="text-base font-bold mb-4 text-[#f4f4f5]">サイトについて</h4>
            <ul className="space-y-2.5 text-sm text-[#a1a1aa]">
              <li>
                <Link href="/profile" className="hover:text-[#ccff00] transition-colors">
                  塾長プロフィール
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-[#ccff00] transition-colors">
                  お問い合わせ
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-[#ccff00] transition-colors">
                  プライバシーポリシー
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="text-center pt-8 border-t border-[#27272a] text-xs text-[#a1a1aa]">
          &copy; {new Date().getFullYear()} ZERO TO HERO GLOW-UP ACADEMY. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}
