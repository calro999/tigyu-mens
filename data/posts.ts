import { Post } from "./types";
import postsData from "./posts.json";

export function getAllPosts(): Post[] {
  return postsData as Post[];
}

export function getPostBySlug(slug: string): Post | undefined {
  const posts = getAllPosts();
  return posts.find((p) => p.slug === slug);
}

export function getFeaturedPosts(): Post[] {
  const posts = getAllPosts();
  return posts.slice(0, 3);
}

export function getRankingPosts(): Post[] {
  const posts = getAllPosts();
  return [...posts].sort((a, b) => (b.views || 0) - (a.views || 0)).slice(0, 5);
}
