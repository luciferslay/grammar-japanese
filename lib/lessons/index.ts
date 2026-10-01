import { afterLongHoliday } from './after-long-holiday';
import { backFromRyokan } from './back-from-ryokan';
import { cafePartTime } from './cafe-part-time';
import { catchingACold } from './catching-a-cold';
import { deadlineRumor } from './deadline-rumor';
import { drinkingPartyInvite } from './drinking-party-invite';
import { festivalInterpreter } from './festival-interpreter';
import { foodCultureSeminar } from './food-culture-seminar';
import { foundWallet } from './found-wallet';
import { interviewNerves } from './interview-nerves';
import { kyotoDayTrip } from './kyoto-day-trip';
import { midnightRadio } from './midnight-radio';
import { mysterySweets } from './mystery-sweets';
import { newBicycle } from './new-bicycle';
import { phoneDinner } from './phone-dinner';
import { rainySeasonIndoors } from './rainy-season-indoors';
import { ramenTrip } from './ramen-trip';
import { roomViewing } from './room-viewing';
import { spicyCurry } from './spicy-curry';
import { springBreakPlans } from './spring-break-plans';
import { stoppedTrain } from './stopped-train';
import { strongWindStation } from './strong-wind-station';
import { supermarketNoodles } from './supermarket-noodles';
import { sushiApprentice } from './sushi-apprentice';
import { walkAndPhone } from './walk-and-phone';
import { weekendTalk } from './weekend-talk';
import type { Lesson } from './types';
import { levelOf, type LevelSlug } from './levels';

export type { Lesson, Word } from './types';
export { LEVELS, DEFAULT_LEVEL, levelOf, levelBySlug, type Level, type LevelSlug } from './levels';

/**
 * 课程顺序 = 网站上的课号。按 JLPT N5 → N4 → N3 → N2 → N1 分块（网站上 初级＝N5～N4、中级＝N3～N2、高级＝N1）、块内从易到难排（顺序表见 ~/Developer/nihongo/grammar/LESSON_ORDER.md）。
 * 新课按等级插入对应位置，插入点之后的课号顺延。课程 id 用 gj-NN（与网站课号无关，只是文件标识）。
 */
export const lessons: Lesson[] = [
  // —— JLPT N4 ——（2026-09-30 Luna：插图、音频都齐了、人耳听过的先上首页）
  ramenTrip,
  roomViewing,
  cafePartTime,
  weekendTalk,
];

/**
 * 已写好但音频与插图还没做完的课。放在这里不会出现在首页与姊妹课链接里
 * （RelatedLessons 只渲染 getLesson 能取到的课），等资源齐了再挪进上面的 lessons。
 */
export const pendingLessons: Lesson[] = [
  // —— JLPT N4 ——
  walkAndPhone,
  spicyCurry,
  // —— JLPT N3 ——（N4 后面的课做好了往上面插，课号顺延）
  supermarketNoodles,
  phoneDinner,
  springBreakPlans,
  newBicycle,
  backFromRyokan,
  drinkingPartyInvite,
  deadlineRumor,
  foundWallet,
  interviewNerves,
  mysterySweets,
  catchingACold,
  rainySeasonIndoors,
  afterLongHoliday,
  stoppedTrain,
  strongWindStation,
  festivalInterpreter,
  foodCultureSeminar,
  kyotoDayTrip,
  sushiApprentice,
  midnightRadio,
];

/** 某一级里已上架的课（首页、上一课／下一课用）。 */
export function lessonsInLevel(slug: LevelSlug): Lesson[] {
  return lessons.filter((lesson) => levelOf(lesson).slug === slug);
}

/**
 * 课序号（第 X 课）：在**每一级里**从 1 数起（2026-09-30 照韩语站分级）。
 * 已上架的按 lessons 的顺序；未上架的接在同一级已上架的后面编号。
 */
export function lessonNumber(id: string): number {
  const lesson = findLesson(id);
  if (!lesson) return 0;
  const slug = levelOf(lesson).slug;
  const live = lessonsInLevel(slug);
  const index = live.findIndex((item) => item.id === id);
  if (index >= 0) return index + 1;
  const pending = pendingLessons.filter((item) => levelOf(item).slug === slug).findIndex((item) => item.id === id);
  return pending >= 0 ? live.length + pending + 1 : 0;
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
