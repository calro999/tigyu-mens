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
  bestFor?: string;
  deepReview?: string;
  dailyCost?: string;
}

export interface SelectionCriterion {
  title: string;
  body: string;
}

export interface UsageStep {
  step: string;
  title: string;
  description: string;
}

export interface ArticleFaq {
  q: string;
  a: string;
}

export interface BeforeAfterComparison {
  before: string[];
  after: string[];
}

export interface SynergyRecommendation {
  text: string;
  targetSlug: string;
  targetTitle: string;
}

export interface PostFeatureSection {
  title: string;
  body: string;
  imageUrl?: string;
  imageAlt?: string;
  imageGallery?: { url: string; alt: string }[];
  affiliateUrl?: string;
  affiliateButtonText?: string;
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
  beforeAfter?: BeforeAfterComparison;
  selectionCriteria?: SelectionCriterion[];
  usageSteps?: UsageStep[];
  faqs?: ArticleFaq[];
  synergyTip?: SynergyRecommendation;
  featureSections?: PostFeatureSection[];
}
