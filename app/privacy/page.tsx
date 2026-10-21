import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "プライバシーポリシー | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "当メディアの個人情報保護方針、広告配信（楽天アフィリエイト等）、免責事項について。",
};

export default function PrivacyPage() {
  return (
    <main className="max-w-[800px] mx-auto px-5 py-12">
      <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-10">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          LEGAL & PRIVACY
        </span>
        <h1 className="text-2xl sm:text-3xl font-black text-[#f4f4f5] mb-6">
          プライバシーポリシー・免責事項
        </h1>

        <div className="space-y-6 text-sm text-[#a1a1aa] leading-relaxed">
          <section>
            <h2 className="text-base font-bold text-[#f4f4f5] mb-2">1. 個人情報の利用目的</h2>
            <p>
              当サイト「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」（以下「当サイト」）では、お問い合わせなどの際に氏名・メールアドレス等の個人情報をご登録いただく場合がございます。これらの個人情報は、ご質問に対する回答や必要な情報を電子メールなどでご連絡する場合にのみ利用いたします。
            </p>
          </section>

          <section>
            <h2 className="text-base font-bold text-[#f4f4f5] mb-2">2. 広告配信について（アフィリエイトプログラム）</h2>
            <p>
              当サイトは、楽天グループ株式会社が提供する「楽天アフィリエイト」などの各種アフィリエイトプログラムに参加しています。第三者がコンテンツおよび宣伝を提供し、訪問者から直接情報を収集し、訪問者のブラウザにクッキー（Cookie）を設定または認識する場合があります。
            </p>
          </section>

          <section>
            <h2 className="text-base font-bold text-[#f4f4f5] mb-2">3. アクセス解析ツールについて</h2>
            <p>
              当サイトでは、アクセス解析ツールを利用してトラフィックデータを収集することがあります。このデータは匿名で収集されており、個人を特定するものではありません。
            </p>
          </section>

          <section>
            <h2 className="text-base font-bold text-[#f4f4f5] mb-2">4. 免責事項</h2>
            <p>
              当サイトに掲載されている情報については、可能な限り正確な情報を掲載するよう努めておりますが、誤情報が混入したり情報が古くなっていることもございます。当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。化粧品・スキンケア用品の使用に際しては、パッチテストを行うなどご自身の責任においてご判断ください。
            </p>
          </section>
        </div>
      </div>
    </main>
  );
}
