import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    agentUpgrade: "security",
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "thumbnail.image.rakuten.co.jp",
      },
      {
        protocol: "https",
        hostname: "**.rakuten.co.jp",
      },
    ],
  },
};

export default nextConfig;
