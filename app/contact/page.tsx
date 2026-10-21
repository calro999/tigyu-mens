"use client";

import { useState } from "react";

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <main className="max-w-[700px] mx-auto px-5 py-12">
      <div className="bg-[#18181b] border border-[#27272a] rounded-xl p-6 sm:p-10">
        <span className="text-xs text-[#ccff00] font-black tracking-widest uppercase block mb-2">
          CONTACT US
        </span>
        <h1 className="text-2xl sm:text-3xl font-black text-[#f4f4f5] mb-4">
          お問い合わせ・レビュー要望
        </h1>
        <p className="text-sm text-[#a1a1aa] mb-8 leading-relaxed">
          「このメンズコスメを検証してほしい」「肌荒れの相談をしたい」など、ご意見・ご要望がございましたら下記フォームよりご連絡ください。
        </p>

        {submitted ? (
          <div className="bg-[#ccff00]/10 border border-[#ccff00]/30 rounded-lg p-6 text-center">
            <span className="text-2xl block mb-2">✅</span>
            <h3 className="text-base font-bold text-[#ccff00] mb-2">
              お問い合わせを受け付けました
            </h3>
            <p className="text-xs text-[#a1a1aa]">
              ご意見・レビューリクエストありがとうございます。内容を確認のうえ、今後の検証記事に反映させていただきます。
            </p>
          </div>
        ) : (
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-bold text-[#f4f4f5] mb-2">
                お名前 / ニックネーム
              </label>
              <input
                type="text"
                required
                placeholder="例: チー牛卒業生"
                className="w-full bg-[#09090b] border border-[#27272a] focus:border-[#ccff00] rounded-lg px-4 py-3 text-sm text-[#f4f4f5] outline-none transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#f4f4f5] mb-2">
                メールアドレス
              </label>
              <input
                type="email"
                required
                placeholder="example@gmail.com"
                className="w-full bg-[#09090b] border border-[#27272a] focus:border-[#ccff00] rounded-lg px-4 py-3 text-sm text-[#f4f4f5] outline-none transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-[#f4f4f5] mb-2">
                お問い合わせ種別
              </label>
              <select className="w-full bg-[#09090b] border border-[#27272a] focus:border-[#ccff00] rounded-lg px-4 py-3 text-sm text-[#f4f4f5] outline-none transition-colors">
                <option value="review">コスメ・アイテムの検証リクエスト</option>
                <option value="consultation">肌質・スキンケアのお悩み</option>
                <option value="business">お仕事・広告掲載のご相談</option>
                <option value="other">その他</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-[#f4f4f5] mb-2">
                お問い合わせ内容
              </label>
              <textarea
                rows={5}
                required
                placeholder="お問い合わせ内容を具体的にご記入ください。"
                className="w-full bg-[#09090b] border border-[#27272a] focus:border-[#ccff00] rounded-lg px-4 py-3 text-sm text-[#f4f4f5] outline-none transition-colors resize-none"
              ></textarea>
            </div>

            <button
              type="submit"
              className="w-full bg-[#ccff00] hover:bg-[#b8e600] text-black font-extrabold text-sm py-3.5 rounded-lg transition-transform hover:scale-[1.01] shadow-lg cursor-pointer"
            >
              送信する
            </button>
          </form>
        )}
      </div>
    </main>
  );
}
