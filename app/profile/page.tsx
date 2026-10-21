import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "塾長プロフィール | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  description: "元・重度チー牛だった運営者が、メンズコスメと自己投資で人生を180度激変させた実体験と当メディアのビジョン。",
};

export default function ProfilePage() {
  return (
    <main className="max-w-[800px] mx-auto px-5 py-12">
      <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-10">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          FOUNDER PROFILE
        </span>
        <h1 className="text-2xl sm:text-3xl font-black text-[#f4f4f5] mb-6">
          塾長プロフィール：元「チー牛」が教える劇的垢抜け論
        </h1>

        <div className="space-y-6 text-sm sm:text-base text-[#a1a1aa] leading-relaxed">
          <p>
            はじめまして。「もうチー牛とは呼ばせない！ゼロから始める垢抜けコスメ塾」塾長です。
          </p>

          <p>
            かつての私は、黒髪ボサボサ・青髭くっきり・水洗顔で肌はギトギト＆毛穴黒ずみ、服は親が買ってきた謎のチェックシャツを着て下を向いて歩く、典型的な「チー牛」でした。
            自分に自信が持てず、女性はおろか人と目を合わせて会話することすら恐れていた時代がありました。
          </p>

          <div className="bg-[#09090b] border-l-4 border-[#ccff00] p-4 rounded-r-lg text-[#f4f4f5]">
            「顔の造形は整形しないと変わらないが、<span className="text-[#ccff00] font-bold">清潔感は1ヶ月あれば科学的に作れる</span>」
          </div>

          <p>
            転機となったのは、ドラッグストアで買った1本1,000円のメンズ洗顔料とコンシーラーでした。
            青髭を隠し、眉毛をハサミで整え、肌のテカリを抑えた瞬間、鏡に映った自分の顔つきが別人のように変わったのです。
            「身だしなみを整えること」は、単なる見栄えではなく、自分の自己肯定感を劇的に押し上げる最強の武器でした。
          </p>

          <h2 className="text-xl font-bold text-[#f4f4f5] pt-4 border-t border-[#27272a]">
            当メディア「垢抜けコスメ塾」の運営方針
          </h2>

          <ul className="space-y-3 text-sm">
            <li className="flex items-start gap-2">
              <span className="text-[#ccff00] font-bold">①</span>
              <span>
                <strong>抽象論・精神論はゼロ：</strong>「自分を磨け」といったフワッとした言葉ではなく、「この商品をこの順番で塗れ」という具体的アクションを提示します。
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#ccff00] font-bold">②</span>
              <span>
                <strong>肌質別の比較重視：</strong>人の肌は乾燥肌・脂性肌で全く異なります。万能を謳う適当な紹介はせず、常にタイプ別比較テーブルで自分に合うものを選べる構成を貫きます。
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-[#ccff00] font-bold">③</span>
              <span>
                <strong>Z世代に寄り添う親身なスタンス：</strong>上から目線で説教するのではなく、同じ悩みを乗り越えた先輩・講座の立ち位置として常に読者をバックアップします。
              </span>
            </li>
          </ul>
        </div>
      </div>
    </main>
  );
}
