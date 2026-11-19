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
            <h4 className="footer-title">カテゴリ別レビュー</h4>
            <ul className="footer-links">
              <li>
                <Link href="/reviews?cat=スキンケア・洗顔">スキンケア・洗顔</Link>
              </li>
              <li>
                <Link href="/reviews?cat=ヘア・眉毛セット">ヘア・眉毛セット</Link>
              </li>
              <li>
                <Link href="/reviews?cat=ボディ・姿勢改善">ボディ・姿勢改善</Link>
              </li>
              <li>
                <Link href="/reviews?cat=ニオイ・体臭対策">ニオイ・体臭対策</Link>
              </li>
              <li>
                <Link href="/reviews?cat=ファッション・身だしなみ">ファッション・身だしなみ</Link>
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
