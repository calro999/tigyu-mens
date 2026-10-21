import Link from "next/link";

export default function Footer() {
  return (
    <footer>
      <div className="container">
        <div className="footer-grid">
          <div>
            <div className="footer-logo">
              もうチー牛とは呼ばせない！<br />
              ゼロから始める垢抜けコスメ塾
            </div>
            <p className="footer-desc">
              本気で変わりたい男のための、劇的垢抜けロードマップとガチ検証レビューメディア。乾燥肌・脂性肌などタイプ別に徹底比較し、迷わず選べる最適解を届けます。
            </p>
          </div>
          <div>
            <h4 className="footer-title">カリキュラム</h4>
            <ul className="footer-links">
              <li>
                <Link href="/curriculum">スキンケア基礎</Link>
              </li>
              <li>
                <Link href="/curriculum">ヘア＆眉毛セット</Link>
              </li>
              <li>
                <Link href="/curriculum">ボディメイク・食事</Link>
              </li>
              <li>
                <Link href="/curriculum">ニオイ対策</Link>
              </li>
            </ul>
          </div>
          <div>
            <h4 className="footer-title">サイトについて</h4>
            <ul className="footer-links">
              <li>
                <Link href="/profile">塾長プロフィール</Link>
              </li>
              <li>
                <Link href="/contact">お問い合わせ</Link>
              </li>
              <li>
                <Link href="/privacy">プライバシーポリシー</Link>
              </li>
            </ul>
          </div>
        </div>
        <div className="copyright">
          &copy; {new Date().getFullYear()} ZERO TO HERO GLOW-UP ACADEMY. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}
