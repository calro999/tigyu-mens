"use client";

import Link from "next/link";
import { useState } from "react";

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <>
      {/* ヘッダー上部（マイクロコピー・メタ情報） */}
      <div className="header-top">
        <div className="container">
          <span className="header-top-left">男の劇的垢抜け検証メディア【公式塾】</span>
          <span className="header-top-right">最新アップデート・毎日更新中</span>
        </div>
      </div>

      {/* メインヘッダー */}
      <header className="site-header">
        <div className="container header-main">
          <div className="logo">
            <Link href="/" onClick={() => setMobileMenuOpen(false)}>
              もうチー牛とは呼ばせない！<br />
              <span>ZERO TO HERO GLOW-UP ACADEMY</span>
            </Link>
          </div>

          {/* デスクトップ用ナビゲーション */}
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

          {/* モバイル用ハンバーガーメニューボタン */}
          <button
            type="button"
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="メニューを開閉"
            aria-expanded={mobileMenuOpen}
          >
            <span className={`hamburger-line ${mobileMenuOpen ? "open" : ""}`}></span>
            <span className={`hamburger-line ${mobileMenuOpen ? "open" : ""}`}></span>
            <span className={`hamburger-line ${mobileMenuOpen ? "open" : ""}`}></span>
          </button>
        </div>

        {/* モバイル用スライドドロワーメニュー */}
        {mobileMenuOpen && (
          <div className="mobile-nav-drawer">
            <nav className="mobile-nav">
              <ul>
                <li>
                  <Link href="/curriculum" onClick={() => setMobileMenuOpen(false)}>
                    🎓 垢抜けカリキュラム
                  </Link>
                </li>
                <li>
                  <Link href="/reviews" onClick={() => setMobileMenuOpen(false)}>
                    🔍 新着レビュー検証
                  </Link>
                </li>
                <li>
                  <Link href="/ranking" onClick={() => setMobileMenuOpen(false)}>
                    🏆 部門別ランキング
                  </Link>
                </li>
                <li>
                  <Link href="/profile" onClick={() => setMobileMenuOpen(false)}>
                    👤 塾長プロフィール
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
        )}
      </header>
    </>
  );
}
