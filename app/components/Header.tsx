import Link from "next/link";

export default function Header() {
  return (
    <>
      {/* ヘッダー上部（マイクロコピー・メタ情報） */}
      <div className="header-top">
        <div className="container">
          <span>男の劇的垢抜け検証メディア【公式塾】</span>
          <span>最新アップデート・毎日更新中</span>
        </div>
      </div>

      {/* メインヘッダー */}
      <header>
        <div className="container header-main">
          <div className="logo">
            <Link href="/">
              もうチー牛とは呼ばせない！<br />
              <span>ZERO TO HERO GLOW-UP ACADEMY</span>
            </Link>
          </div>
          <nav className="global-nav">
            <ul>
              <li>
                <Link href="/curriculum">カリキュラム</Link>
              </li>
              <li>
                <Link href="/reviews">新着検証</Link>
              </li>
              <li>
                <Link href="/ranking">ランキング</Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>
    </>
  );
}
