import type { Metadata } from "next";
import Header from "./components/Header";
import Footer from "./components/Footer";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://tigyu-mens.vercel.app"),
  title: {
    default: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
    template: "%s | もうチー牛とは呼ばせない！垢抜けコスメ塾",
  },
  description: "【公式塾】本気で変わりたい男のための劇的垢抜けロードマップ。乾燥肌・脂性肌別の比較テーブル、青髭対策、眉毛・ヘアセットからニオイ対策まで楽天高画質レビューで徹底検証。",
  keywords: [
    "メンズコスメ",
    "チー牛 垢抜け",
    "メンズスキンケア",
    "清潔感 男",
    "青髭 隠す コンシーラー",
    "メンズ 眉毛 整え方",
    "メンズ 体臭 デオドラント",
    "猫背 改善 グッズ",
    "男 垢抜け ロードマップ",
    "メンズ 美容 初心者"
  ],
  authors: [{ name: "ゼロから始める垢抜けコスメ塾 塾長", url: "https://tigyu-mens.vercel.app/profile" }],
  creator: "ZERO TO HERO GLOW-UP ACADEMY",
  publisher: "ZERO TO HERO GLOW-UP ACADEMY",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
    description: "男の劇的垢抜け検証メディア。チー牛脱却のための肌質別比較＆最短ロードマップ。",
    url: "https://tigyu-mens.vercel.app",
    siteName: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
    locale: "ja_JP",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
    description: "男の劇的垢抜け検証メディア。チー牛脱却のための肌質別比較＆最短ロードマップ。",
    creator: "@tigyu-cosme.bsky.social",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  alternates: {
    canonical: "https://tigyu-mens.vercel.app",
  },
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.png", type: "image/png", sizes: "512x512" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
  },
};

// AI-SEO / GEO / LLM検索エンジン向け構造化データ（Organization & WebSite）
const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://tigyu-mens.vercel.app/#organization",
      "name": "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
      "url": "https://tigyu-mens.vercel.app",
      "logo": "https://thumbnail.image.rakuten.co.jp/@0_mall/menscosme-zigen/cabinet/product/6.jpg?_ex=600x600",
      "description": "Z世代の男性に向けた、清潔感の獲得・メンズコスメ選び・身だしなみ改善のための検証メディアおよび教育講座。",
      "sameAs": [
        "https://bsky.app/profile/tigyu-cosme.bsky.social"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://tigyu-mens.vercel.app/#website",
      "url": "https://tigyu-mens.vercel.app",
      "name": "もうチー牛とは呼ばせない！ ゼロから始める垢抜けコスメ塾",
      "publisher": {
        "@id": "https://tigyu-mens.vercel.app/#organization"
      },
      "inLanguage": "ja",
      "description": "男の劇的垢抜け検証メディア。肌質別比較テーブルと楽天高解像度アイテムレビューを掲載。"
    }
  ]
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-screen flex flex-col bg-[#09090b] text-[#f4f4f5]">
        <Header />
        <div className="flex-1">{children}</div>
        <Footer />
      </body>
    </html>
  );
}
