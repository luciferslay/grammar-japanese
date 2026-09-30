import type { Lesson } from './types';

/**
 * 等级（Luna 2026-09-30：照韩语站 하루한컷，首页标题左下角分 初级／中级／高级）。
 * 本站 JLPT N4 → 初级、N3 → 中级、N2 → 高级；按每课的 badge 归级。网址 /level/<slug>，课号在每一级里从 1 数起。
 */
export const LEVELS = [
  { slug: 'beginner', label: '初级', sub: 'JLPT N4', badge: 'JLPT N4' },
  { slug: 'intermediate', label: '中级', sub: 'JLPT N3', badge: 'JLPT N3' },
  { slug: 'advanced', label: '高级', sub: 'JLPT N2', badge: 'JLPT N2' },
] as const;

export type Level = (typeof LEVELS)[number];
export type LevelSlug = Level['slug'];

export const DEFAULT_LEVEL: LevelSlug = 'beginner';

export function levelOf(lesson: Lesson): Level {
  return LEVELS.find((level) => level.badge === lesson.badge) ?? LEVELS[0];
}

export function levelBySlug(slug: string): Level | undefined {
  return LEVELS.find((level) => level.slug === slug);
}
