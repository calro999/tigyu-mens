import Link from "next/link";

export default function Header() {
  return (
    <>
      <div className="bg-black text-[0.75rem] text-[#a1a1aa] py-1.5 border-b border-[#27272a]">
        <div className="max-w-[1200px] mx-auto px-5 flex justify-between items-center">
          <span className="font-medium tracking-wide">男の劇的垢抜け検証メディア【公式塾】</span>
          <span className="text-[#a1a1aa] hidden sm:inline">毎日自動更新中 / 最新メンズコスメ徹底比較</span>
        </div>
      </div>
      <header className="sticky top-0 z-50 bg-[#09090b]/90 backdrop-blur-md border-b border-[#27272a]">
        <div className="max-w-[1200px] mx-auto px-5 py-4 flex items-center justify-between">
          <div className="font-black tracking-tight leading-tight">
            <Link href="/" className="hover:opacity-90">
              <span className="text-xl sm:text-2xl text-[#f4f4f5] block">もうチー牛とは呼ばせない！</span>
              <span className="text-[0.75rem] text-[#ccff00] tracking-widest block font-bold">
                ZERO TO HERO GLOW-UP ACADEMY
              </span>
            </Link>
          </div>
          <nav className="hidden md:flex items-center gap-8">
            <Link
              href="/curriculum"
              className="text-sm font-bold text-[#a1a1aa] hover:text-[#f4f4f5] transition-colors relative py-1 hover:border-b-2 hover:border-[#ccff00]"
            >
              基礎カリキュラム
            </Link>
            <Link
              href="/reviews"
              className="text-sm font-bold text-[#a1a1aa] hover:text-[#f4f4f5] transition-colors relative py-1 hover:border-b-2 hover:border-[#ccff00]"
            >
              新着検証・比較
            </Link>
            <Link
              href="/ranking"
              className="text-sm font-bold text-[#a1a1aa] hover:text-[#f4f4f5] transition-colors relative py-1 hover:border-b-2 hover:border-[#ccff00]"
            >
              殿堂入りランキング
            </Link>
          </nav>
        </div>
      </header>
    </>
  );
}
