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
    <main className="max-w-[1200px] mx-auto px-5">
      {/* Hero Section (マガジン風アシンメトリー) */}
      <section className="py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {/* メイン特集 */}
          {heroMain && (
            <Link
              href={`/posts/${heroMain.slug}`}
              className="lg:col-span-2 relative rounded-lg overflow-hidden min-h-[340px] lg:min-h-[460px] bg-[#18181b] border border-[#27272a] flex flex-col justify-end p-6 sm:p-10 group"
            >
              <Image
                src={heroMain.heroImage}
                alt={heroMain.title}
                fill
                priority
                className="object-cover opacity-60 group-hover:scale-105 group-hover:opacity-40 transition-all duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-transparent pointer-events-none" />
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-3 text-xs font-bold">
                  <span className="bg-[#ccff00] text-black px-3 py-1 rounded-full font-black tracking-wide">
                    {heroMain.category}
                  </span>
                  <span className="text-[#a1a1aa] font-medium">⏱ {heroMain.readTime}</span>
                </div>
                <h2 className="text-xl sm:text-3xl font-black text-[#f4f4f5] leading-snug drop-shadow-md">
                  {heroMain.title}
                </h2>
                <p className="text-sm text-[#a1a1aa] mt-3 line-clamp-2 hidden sm:block">
                  {heroMain.excerpt}
                </p>
              </div>
            </Link>
          )}

          {/* サブ特集 2件 */}
          <div className="flex flex-col gap-5">
            {heroSub1 && (
              <Link
                href={`/posts/${heroSub1.slug}`}
                className="relative rounded-lg overflow-hidden min-h-[200px] flex-1 bg-[#18181b] border border-[#27272a] flex flex-col justify-end p-5 group"
              >
                <Image
                  src={heroSub1.heroImage}
                  alt={heroSub1.title}
                  fill
                  className="object-cover opacity-60 group-hover:scale-105 group-hover:opacity-40 transition-all duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-transparent pointer-events-none" />
                <div className="relative z-10">
                  <span className="inline-block bg-white text-black text-[11px] font-black px-2.5 py-0.5 rounded-full mb-2">
                    {heroSub1.category}
                  </span>
                  <h3 className="text-base sm:text-lg font-bold text-[#f4f4f5] leading-snug line-clamp-2">
                    {heroSub1.title}
                  </h3>
                </div>
              </Link>
            )}

            {heroSub2 && (
              <Link
                href={`/posts/${heroSub2.slug}`}
                className="relative rounded-lg overflow-hidden min-h-[200px] flex-1 bg-[#18181b] border border-[#27272a] flex flex-col justify-end p-5 group"
              >
                <Image
                  src={heroSub2.heroImage}
                  alt={heroSub2.title}
                  fill
                  className="object-cover opacity-60 group-hover:scale-105 group-hover:opacity-40 transition-all duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/40 to-transparent pointer-events-none" />
                <div className="relative z-10">
                  <span className="inline-block bg-white text-black text-[11px] font-black px-2.5 py-0.5 rounded-full mb-2">
                    {heroSub2.category}
                  </span>
                  <h3 className="text-base sm:text-lg font-bold text-[#f4f4f5] leading-snug line-clamp-2">
                    {heroSub2.title}
                  </h3>
                </div>
              </Link>
            )}
          </div>
        </div>
      </section>

      {/* Categories タグクラウド風 */}
      <section className="py-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Link
            href="/reviews?cat=スキンケア・洗顔"
            className="bg-[#18181b] border border-[#27272a] hover:border-[#ccff00] hover:bg-[#27272a] rounded-lg p-5 flex items-center gap-4 transition-all"
          >
            <div className="text-2xl bg-[#09090b] w-12 h-12 flex items-center justify-center rounded-full border border-[#3f3f46]">
              🧴
            </div>
            <div>
              <div className="font-extrabold text-sm sm:text-base text-[#f4f4f5]">スキンケア</div>
              <span className="text-[10px] text-[#a1a1aa] uppercase font-bold tracking-wider">SKIN & FACE</span>
            </div>
          </Link>
          <Link
            href="/reviews?cat=ヘア・眉毛セット"
            className="bg-[#18181b] border border-[#27272a] hover:border-[#ccff00] hover:bg-[#27272a] rounded-lg p-5 flex items-center gap-4 transition-all"
          >
            <div className="text-2xl bg-[#09090b] w-12 h-12 flex items-center justify-center rounded-full border border-[#3f3f46]">
              ✂️
            </div>
            <div>
              <div className="font-extrabold text-sm sm:text-base text-[#f4f4f5]">ヘア＆眉毛</div>
              <span className="text-[10px] text-[#a1a1aa] uppercase font-bold tracking-wider">HAIR & EYEBROW</span>
            </div>
          </Link>
          <Link
            href="/reviews?cat=ボディ・姿勢改善"
            className="bg-[#18181b] border border-[#27272a] hover:border-[#ccff00] hover:bg-[#27272a] rounded-lg p-5 flex items-center gap-4 transition-all"
          >
            <div className="text-2xl bg-[#09090b] w-12 h-12 flex items-center justify-center rounded-full border border-[#3f3f46]">
              💪
            </div>
            <div>
              <div className="font-extrabold text-sm sm:text-base text-[#f4f4f5]">ボディメイク</div>
              <span className="text-[10px] text-[#a1a1aa] uppercase font-bold tracking-wider">BODY & DIET</span>
            </div>
          </Link>
          <Link
            href="/reviews?cat=ニオイ・体臭対策"
            className="bg-[#18181b] border border-[#27272a] hover:border-[#ccff00] hover:bg-[#27272a] rounded-lg p-5 flex items-center gap-4 transition-all"
          >
            <div className="text-2xl bg-[#09090b] w-12 h-12 flex items-center justify-center rounded-full border border-[#3f3f46]">
              🚿
            </div>
            <div>
              <div className="font-extrabold text-sm sm:text-base text-[#f4f4f5]">ニオイ対策</div>
              <span className="text-[10px] text-[#a1a1aa] uppercase font-bold tracking-wider">CLEANLINESS</span>
            </div>
          </Link>
        </div>
      </section>

      {/* メインコンテンツ ＆ サイドバー */}
      <section className="py-12" id="latest">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* 左カラム：記事一覧 */}
          <div className="lg:col-span-2">
            <div className="flex items-end justify-between mb-8 pb-4 border-b-2 border-[#27272a]">
              <div>
                <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block">
                  Latest Reports
                </span>
                <h2 className="text-2xl sm:text-3xl font-black text-[#f4f4f5] mt-1">最新の検証・レビュー</h2>
              </div>
              <Link href="/reviews" className="text-xs text-[#a1a1aa] hover:text-[#ccff00] font-bold">
                View All →
              </Link>
            </div>

            <div className="space-y-6">
              {posts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/posts/${post.slug}`}
                  className="bg-[#18181b] border border-[#27272a] hover:border-[#3f3f46] hover:-translate-y-0.5 rounded-lg overflow-hidden flex flex-col sm:flex-row transition-all duration-300 group"
                >
                  <div className="w-full sm:w-[35%] h-48 sm:h-auto relative bg-[#222] flex-shrink-0">
                    <Image
                      src={post.heroImage}
                      alt={post.title}
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                  </div>
                  <div className="p-6 flex flex-col justify-center flex-grow">
                    <div className="flex flex-wrap items-center gap-2 text-xs text-[#a1a1aa] mb-2.5">
                      <span className="text-[#ccff00] bg-[#ccff00]/10 border border-[#ccff00]/20 px-2 py-0.5 rounded font-bold">
                        {post.tags[0] || "#コスメ"}
                      </span>
                      <span>{post.date}</span>
                      <span>⏱ {post.readTime}</span>
                    </div>
                    <h3 className="text-lg font-black text-[#f4f4f5] group-hover:text-[#ccff00] transition-colors mb-2 leading-snug">
                      {post.title}
                    </h3>
                    <p className="text-xs sm:text-sm text-[#a1a1aa] line-clamp-2 leading-relaxed">
                      {post.excerpt}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* 右カラム：サイドバー */}
          <aside className="space-y-8" id="ranking">
            {/* ウィジェット1: ランキング */}
            <div className="bg-[#18181b] border border-[#27272a] rounded-lg p-6">
              <h3 className="text-base font-black text-[#f4f4f5] mb-5 pb-3 border-b-2 border-[#27272a] flex items-center gap-2">
                <span className="w-1.5 h-4 bg-[#ccff00] inline-block"></span>
                殿堂入りランキング
              </h3>
              <ul className="space-y-4">
                {rankingPosts.map((post, index) => (
                  <li key={post.slug}>
                    <Link href={`/posts/${post.slug}`} className="flex gap-3 items-center group">
                      <div
                        className={`text-lg font-black italic w-6 text-center ${
                          index === 0 ? "text-[#ccff00]" : "text-[#71717a]"
                        }`}
                      >
                        {index + 1}
                      </div>
                      <div className="w-14 h-14 relative rounded overflow-hidden flex-shrink-0 bg-black/40 border border-[#3f3f46]">
                        <Image
                          src={post.heroImage}
                          alt={post.title}
                          fill
                          className="object-cover"
                        />
                      </div>
                      <div className="text-xs font-bold text-[#f4f4f5] group-hover:text-[#ccff00] transition-colors line-clamp-2 leading-snug">
                        {post.title}
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* ウィジェット2: 注目キーワード */}
            <div className="bg-[#18181b] border border-[#27272a] rounded-lg p-6">
              <h3 className="text-base font-black text-[#f4f4f5] mb-4 pb-3 border-b-2 border-[#27272a] flex items-center gap-2">
                <span className="w-1.5 h-4 bg-[#ccff00] inline-block"></span>
                注目キーワード
              </h3>
              <div className="flex flex-wrap gap-2 text-xs">
                {["#オールインワン", "#青髭", "#コンシーラー", "#眉毛カット", "#ワックス", "#体臭対策", "#猫背矯正", "#チー牛脱却"].map(
                  (tag) => (
                    <Link
                      key={tag}
                      href={`/reviews?tag=${encodeURIComponent(tag)}`}
                      className="bg-[#09090b] border border-[#27272a] hover:border-[#ccff00] text-[#a1a1aa] hover:text-[#f4f4f5] px-3 py-1.5 rounded transition-colors"
                    >
                      {tag}
                    </Link>
                  )
                )}
              </div>
            </div>
          </aside>
        </div>
      </section>

      {/* カリキュラム（Roadmap）セクション */}
      <section className="py-12" id="roadmap">
        <div className="flex items-end justify-between mb-8 pb-4 border-b-2 border-[#27272a]">
          <div>
            <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block">
              Roadmap / Curriculum
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-[#f4f4f5] mt-1">【必修】基礎カリキュラム</h2>
          </div>
          <Link href="/curriculum" className="text-xs text-[#a1a1aa] hover:text-[#ccff00] font-bold">
            全ステップを見る →
          </Link>
        </div>

        <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-10 relative">
          <div className="space-y-8 relative before:absolute before:top-4 before:bottom-4 before:left-[23px] before:w-0.5 before:bg-[#27272a]">
            {/* Step 1 */}
            <div className="flex gap-6 items-start relative z-10">
              <div className="w-12 h-12 bg-[#09090b] border-2 border-[#ccff00] text-[#ccff00] rounded-full flex items-center justify-center font-black text-sm flex-shrink-0">
                01
              </div>
              <div className="bg-[#09090b] border border-[#27272a] hover:border-[#ccff00] p-6 rounded-lg flex-grow transition-colors">
                <span className="text-xs text-[#a1a1aa] font-bold block mb-1">STEP 1: FACE & SKIN</span>
                <h3 className="text-lg font-bold text-[#f4f4f5] mb-2">
                  <Link href="/posts/post-1-skincare" className="hover:text-[#ccff00]">
                    洗顔と保湿の土台作り（肌荒れ・テカリ撲滅）
                  </Link>
                </h3>
                <p className="text-sm text-[#a1a1aa] leading-relaxed">
                  すべての始まりは肌。水洗顔をやめて適切な洗顔料を選び、乾燥肌かオイリー肌かに合わせて保湿を徹底するファーストステップ。
                </p>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex gap-6 items-start relative z-10">
              <div className="w-12 h-12 bg-[#09090b] border-2 border-[#ccff00] text-[#ccff00] rounded-full flex items-center justify-center font-black text-sm flex-shrink-0">
                02
              </div>
              <div className="bg-[#09090b] border border-[#27272a] hover:border-[#ccff00] p-6 rounded-lg flex-grow transition-colors">
                <span className="text-xs text-[#a1a1aa] font-bold block mb-1">STEP 2: EYEBROW & HAIR</span>
                <h3 className="text-lg font-bold text-[#f4f4f5] mb-2">
                  <Link href="/posts/post-3-hair-&-brows" className="hover:text-[#ccff00]">
                    眉毛デザインと髪型セットの基礎
                  </Link>
                </h3>
                <p className="text-sm text-[#a1a1aa] leading-relaxed">
                  顔の印象の8割を決める眉毛。ボサボサ眉毛を整えるセルフカット術と、美容室でのオーダー方法、朝5分のワックス技術を伝授。
                </p>
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex gap-6 items-start relative z-10">
              <div className="w-12 h-12 bg-[#09090b] border-2 border-[#ccff00] text-[#ccff00] rounded-full flex items-center justify-center font-black text-sm flex-shrink-0">
                03
              </div>
              <div className="bg-[#09090b] border border-[#27272a] hover:border-[#ccff00] p-6 rounded-lg flex-grow transition-colors">
                <span className="text-xs text-[#a1a1aa] font-bold block mb-1">STEP 3: BODY & CLEANLINESS</span>
                <h3 className="text-lg font-bold text-[#f4f4f5] mb-2">
                  <Link href="/posts/post-5-cleanliness" className="hover:text-[#ccff00]">
                    姿勢・体型改善と「無臭」のニオイマネジメント
                  </Link>
                </h3>
                <p className="text-sm text-[#a1a1aa] leading-relaxed">
                  猫背・巻き肩を解消して服を着こなす土台作りと、香水で誤魔化さない徹底的な体臭・口臭予防ルーティンを確立。
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
