import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "プライバシーポリシー | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "当メディアの個人情報保護方針、広告配信（楽天アフィリエイト等）、免責事項について。",
};

export default function PrivacyPage() {
  return (
    <main className="subpage-container" style={{ maxWidth: "800px" }}>
      <div className="subpage-header">
        <span className="subpage-en">LEGAL & PRIVACY</span>
        <h1 className="subpage-title">プライバシーポリシー・免責事項</h1>
        <p className="subpage-lead">当サイトの運営方針・法令遵守・個人情報保護に関する基本方針</p>
      </div>

      <div className="content-box">
        <div className="policy-section">
          <h3>1. 個人情報の利用目的</h3>
          <p>
            当サイト「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」（以下「当サイト」）では、お問い合わせなどの際に氏名・メールアドレス等の個人情報をご登録いただく場合がございます。これらの個人情報は、ご質問に対する回答や必要な情報を電子メールなどでご連絡する場合にのみ利用いたします。
          </p>
        </div>

        <div className="policy-section">
          <h3>2. 広告配信について（楽天アフィリエイト等の利用）</h3>
          <p>
            当サイトは、楽天グループ株式会社が提供する「楽天アフィリエイト」などの各種アフィリエイトプログラムに参加しています。第三者がコンテンツおよび宣伝を提供し、訪問者から直接情報を収集し、訪問者のブラウザにクッキー（Cookie）を設定または認識する場合があります。
          </p>
        </div>

        <div className="policy-section">
          <h3>3. アクセス解析ツールについて</h3>
          <p>
            当サイトでは、トラフィックデータの収集のためにアクセス解析ツールを利用することがあります。このデータは匿名で収集されており、個人を特定するものではありません。ブラウザの設定でCookieを無効にすることにより、収集を拒否することが可能です。
          </p>
        </div>

        <div className="policy-section">
          <h3>4. 免責事項</h3>
          <p>
            当サイトに掲載されている情報については、可能な限り正確な情報を掲載するよう努めておりますが、誤情報が混入したり情報が古くなっていることもございます。当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。化粧品・スキンケア用品の使用に際しては、パッチテストを行うなどご自身の責任においてご判断ください。
          </p>
        </div>
      </div>
    </main>
  );
}
