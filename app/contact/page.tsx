"use client";

import { useState } from "react";

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <main className="subpage-container" style={{ maxWidth: "700px" }}>
      <div className="subpage-header">
        <span className="subpage-en">CONTACT US</span>
        <h1 className="subpage-title">お問い合わせ・レビュー要望</h1>
        <p className="subpage-lead">
          「このメンズコスメを検証してほしい」「肌荒れの相談をしたい」など、ご意見・ご要望がございましたら下記フォームよりご連絡ください。
        </p>
      </div>

      <div className="content-box">
        {submitted ? (
          <div className="callout-box" style={{ padding: "30px 20px" }}>
            <span style={{ fontSize: "2rem", display: "block", marginBottom: "10px" }}>✅</span>
            <span className="callout-title" style={{ fontSize: "1.1rem", marginBottom: "8px" }}>
              お問い合わせを受け付けました
            </span>
            <span className="callout-text">
              ご意見・レビューリクエストありがとうございます。内容を確認のうえ、今後の検証記事に反映させていただきます。
            </span>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">お名前 / ニックネーム</label>
              <input
                type="text"
                required
                placeholder="例: チー牛卒業生"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">メールアドレス</label>
              <input
                type="email"
                required
                placeholder="example@gmail.com"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label className="form-label">お問い合わせ種別</label>
              <select className="form-select">
                <option value="review">コスメ・アイテムの検証リクエスト</option>
                <option value="consultation">肌質・スキンケアのお悩み</option>
                <option value="business">お仕事・広告掲載のご相談</option>
                <option value="other">その他</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">お問い合わせ内容</label>
              <textarea
                rows={5}
                required
                placeholder="お問い合わせ内容を具体的にご記入ください。"
                className="form-textarea"
              ></textarea>
            </div>

            <button type="submit" className="btn-submit">
              送信する
            </button>
          </form>
        )}
      </div>
    </main>
  );
}
