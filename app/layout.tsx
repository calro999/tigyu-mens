import type { Metadata } from "next";
import Header from "./components/Header";
import Footer from "./components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  title: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
  description: "【公式塾】本気で変わりたい男のための劇的垢抜けロードマップ。乾燥肌・脂性肌別の比較テーブル、青髭対策、眉毛・ヘアセットからニオイ対策まで徹底検証。",
  openGraph: {
    title: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
    description: "男の劇的垢抜け検証メディア。チー牛脱却のための肌質別比較＆最短ロードマップ。",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className="min-h-screen flex flex-col bg-[#09090b] text-[#f4f4f5]">
        <Header />
        <div className="flex-1">{children}</div>
        <Footer />
      </body>
    </html>
  );
}
