import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  // AI/LLM特化クローラーおよび主要検索エンジンを明示的に全開放
  const aiAndSearchCrawlers = [
    "*",
    "DuckDuckBot",
    "Bingbot",
    "Googlebot",
    "Google-Extended",
    "GPTBot",
    "ChatGPT-User",
    "ClaudeBot",
    "Claude-Web",
    "PerplexityBot",
    "Applebot",
    "Applebot-Extended",
    "cohere-ai",
    "Bytespider",
    "CCBot",
    "Diffbot",
    "FacebookBot",
    "YouBot",
    "Amazonbot"
  ];

  return {
    rules: aiAndSearchCrawlers.map((agent) => ({
      userAgent: agent,
      allow: "/",
    })),
    sitemap: "https://tigyu-mens.vercel.app/sitemap.xml",
  };
}
