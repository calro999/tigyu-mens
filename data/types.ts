export interface ProductComparison {
  name: string;
  brand: string;
  category: string;
  targetSkin: "乾燥肌・敏感肌" | "脂性肌・オイリー" | "混合肌・初心者" | "全肌質・高機能";
  feature: string;
  price: string;
  pros: string[];
  cons: string[];
  imageUrl: string;
  affiliateUrl: string;
  rating: number;
  reviewCount: number;
}

export interface Post {
  slug: string;
  title: string;
  excerpt: string;
  category: string;
  categoryEn: string;
  date: string;
  readTime: string;
  heroImage: string;
  tags: string[];
  intro: string;
  targetAudience: string;
  problemStatement: string;
  comparisonTable: ProductComparison[];
  conclusion: string;
  views?: number;
}
