import { cafePartTime } from './cafe-part-time';
import { ramenTrip } from './ramen-trip';
import { roomViewing } from './room-viewing';
import { spicyCurry } from './spicy-curry';
import { walkAndPhone } from './walk-and-phone';
import { weekendTalk } from './weekend-talk';
import type { Lesson } from './types';

export type { Lesson, Word } from './types';

/**
 * 课程顺序 = 网站上的课号。按 JLPT N4 → N3 → N2 分块、块内从易到难排（顺序表见 ~/Developer/nihongo/grammar/LESSON_ORDER.md）。
 * 新课按等级插入对应位置，插入点之后的课号顺延。课程 id 用 gj-NN（与网站课号无关，只是文件标识）。
 */
export const lessons: Lesson[] = [];

/**
 * 已写好但音频与插图还没做完的课。放在这里不会出现在首页与姊妹课链接里
 * （RelatedLessons 只渲染 getLesson 能取到的课），等资源齐了再挪进上面的 lessons。
 */
export const pendingLessons: Lesson[] = [
  // —— JLPT N4 ——
  ramenTrip,
  roomViewing,
  cafePartTime,
  weekendTalk,
  walkAndPhone,
  spicyCurry,
  // —— JLPT N3 ——（N4 后面的课做好了往上面插，课号顺延）
];

/** 课序号（第 X 课）：按 lessons 的排列顺序，未注册的课接在后面编号。 */
export function lessonNumber(id: string): number {
  const index = lessons.findIndex((lesson) => lesson.id === id);
  if (index >= 0) return index + 1;
  const pending = pendingLessons.findIndex((lesson) => lesson.id === id);
  return pending >= 0 ? lessons.length + pending + 1 : 0;
}

export function getLesson(id: string): Lesson | undefined {
  return lessons.find((lesson) => lesson.id === id);
}

/**
 * 课程页用：已上架 + 未上架都能取到。未上架的课不出现在首页和姊妹课链接里（那两处用 getLesson），
 * 但直接输网址可以打开，方便 Luna 在插图、音频没齐时先本地预览。
 */
export function findLesson(id: string): Lesson | undefined {
  return getLesson(id) ?? pendingLessons.find((lesson) => lesson.id === id);
}
