import type { Lesson } from './types';

const AUDIO = '/audio/standard/gj-13';

/**
 * N3 第 7 课：普通形 + わけがない（根本不可能）。JLPT N3。
 * 大纲 notes/LESSON_DRAFT_gj-13-14.md（Luna 2026-10-01 批准）。
 * 人物：A＝拓也（男）；B＝リン（女，中国留学生）。朋友。
 * 语体：N3 → 朋友之间普通体，口语照写；练习第 1 题用丁寧語。
 */
export const deadlineRumor: Lesson = {
  id: 'gj-13',
  badge: 'JLPT N3',
  listTitle: '延びるわけがないよ',
  listSummary: '发表只剩五天，资料才做一半：截止日期「根本不可能」延后。',
  image: {
    src: '/deadline-rumor.png',
    alt: '傍晚的大学图书馆，男生对着满桌资料和笔记本电脑抱着头，戴圆眼镜的女生站在旁边抱着胳膊摇头，墙上日历圈着一个红圈',
  },
  grammar: {
    title: '〜わけがない',
    summary: '「根本不可能……」：说话人有理由，强烈断定。',
    example: '延びるわけがないよ。',
    note: '普通形加 わけがない，是「根本不可能……、哪有……的道理」，说话人有理由，强烈断定。口语常省掉 が 说 〜わけない（間に合うわけないじゃない）。接续同 わけだ：な形容词、名词要加 な（簡単なわけがない）。和 〜わけではない 分清：わけではない 是「并不是」（弱，留余地），わけがない 是「绝对不可能」（强）。和 〜はずがない 很接近，わけがない 口气更主观、更强，日常会话里更常听到。和单纯的否定分清：延びない 只是陈述，延びるわけがない 是带着理由的强烈否定。',
    points: [
      '**普通形 + わけがない**：「**根本不可能……**」，有理由的强烈断定',
      '口语常省掉 が：**〜わけない**（間に合うわけないじゃない）',
      '接续：**な形容词、名词 加 な**（簡単なわけがない）',
      '和 **〜わけではない**（第 12 课）分清：わけではない＝「并不是」；わけがない＝「绝对不可能」',
      '和 **〜はずがない** 很接近；わけがない 更主观、更强，会话里更常用',
    ],
  },
  dialogue: [
    {
      role: 'A',
      text: 'リン、来週の発表、締め切りが延びるって噂、聞いた？',
      zh: '小粼，你听说了吗？有传言说下周发表的截止日期要延后。',
      audio: `${AUDIO}/dialogue-01.m4a`,
    },
    {
      role: 'B',
      text: '延びるわけがないよ。あの教授、時間には厳しいんだから。',
      zh: '不可能延的啦。那个教授对时间可严了。',
      audio: `${AUDIO}/dialogue-02.m4a`,
    },
    {
      role: 'A',
      text: 'だよね……。あの教授が延ばしてくれるわけないか。でも、資料がまだ半分しかできてないんだ。',
      zh: '也是……那个教授怎么可能给延期。可我的资料才做了一半。',
      audio: `${AUDIO}/dialogue-03.m4a`,
    },
    {
      role: 'B',
      text: 'えっ、あと五日しかないのに？ 一人で間に合うわけないじゃない。',
      zh: '啊？只剩五天了啊？一个人根本来不及吧。',
      audio: `${AUDIO}/dialogue-04.m4a`,
    },
    {
      role: 'A',
      text: 'だから、リンに手伝ってもらえないかなって……。',
      zh: '所以想问问小粼能不能帮帮我……',
      audio: `${AUDIO}/dialogue-05.m4a`,
    },
    {
      role: 'B',
      text: '自分の担当は自分でやるの。でも、分からないところがあったら、相談に乗るよ。',
      zh: '自己负责的部分自己做。不过有不懂的地方，我可以帮你出主意。',
      audio: `${AUDIO}/dialogue-06.m4a`,
    },
  ],
  feeling: {
    eyebrow: '整体感觉',
    question: 'リンはどうして締め切りが延びないと思っていますか。',
    choices: [
      { value: 'done', label: '拓也の資料がもう完成しているから' },
      { value: 'today', label: '発表が今日だから' },
      { value: 'sick', label: '教授が病気だから' },
      { value: 'strict', label: '教授が時間に厳しい人だから' },
    ],
    correct: 'strict',
    success: '答对了。第 2 句：那个教授对时间很严 —— 所以 延びるわけがない。',
    hint: '看第 2 句，リン 说完「不可能」之后给了什么理由？',
  },
  meaning: {
    eyebrow: '语法原型',
    question: '「延びるわけがない」は何を表す？',
    choices: [
      { value: 'maybe', label: '延びるかもしれない' },
      { value: 'hope', label: '延びてほしい' },
      { value: 'done', label: 'もう延びた' },
      { value: 'strong', label: '延びないと強く思っている（理由がある）' },
    ],
    correct: 'strong',
    success: '答对了。わけがない＝有理由地、强烈地断定「绝对不会」。',
    hint: 'リン 说得有多肯定？她后面给了理由吗？',
  },
  grammarTests: [
    {
      question: '把括号里的形容词接上适合句子的形式。',
      full: 'あんなに難しい試験が簡単なわけがありません。',
      blank: 'あんなに難しい試験が (簡単だ) ______ わけがありません。',
      choices: ['簡単だ', '簡単な', '簡単に', '簡単で'],
      correct: '簡単な',
      explain: '答对了。な形容词接 わけがない 要加 な：簡単なわけがありません。跟不太熟的人说用丁寧語。',
      zh: '那么难的考试，不可能简单。',
    },
    {
      question: '「彼がそんなことを言うわけがない」に一番近い意味は？',
      full: '彼がそんなことを言うわけがない。',
      blank: '「…」 ______',
      choices: [
        '彼がそんなことを言ったのは当然だ',
        '彼はそんなことを言うかもしれない',
        '彼がそんなことを言うことは、絶対にない',
        '彼はそんなことを言ったことがない',
      ],
      correct: '彼がそんなことを言うことは、絶対にない',
      explain: '答对了。わけがない＝绝对不可能：他不可能说那种话。',
      zh: '他不可能说那种话。',
    },
    {
      question: '次の中で自然な文は？',
      full: '三分で十キロ走れるわけがない。',
      blank: '「…」 ______',
      choices: [
        '三分で十キロ走れるわけがない。',
        '明日は雨が降るわけがないかもしれない。',
        '私は昨日、学校に行ったわけがない。',
        'このケーキはおいしいわけがないので、たくさん食べた。',
      ],
      correct: '三分で十キロ走れるわけがない。',
      explain: '答对了。② わけがない 是强烈断定，和 かもしれない 矛盾；③ 自己做过的事直接说「行かなかった」；④ 前后矛盾。',
      zh: '三分钟不可能跑十公里。',
    },
  ],
  grammarTestHint: '不太对。わけがない 是有理由的「绝对不可能」；な形容词、名词要加 な 再接。',
  errorTests: [
    {
      wrong: 'あの教授が優しいわけがあります。',
      fixed: 'あの教授が優しいわけがない。',
      choices: [
        'わけがない は否定の形で使う。「わけがある」は「理由がある」という別の意味',
        '優しい は 優しく にする',
        '教授が は 教授を にする',
        'あの は この にしなければならない',
      ],
      correct: 'わけがない は否定の形で使う。「わけがある」は「理由がある」という別の意味',
      explain: '「不可能」这个意思只有否定形 わけがない。わけがある 是「有原因」，意思完全不同。',
      zh: '那个教授不可能温柔。',
    },
    {
      wrong: '一人で間に合うわけではない。（想说「一个人绝对来不及」）',
      fixed: '一人で間に合うわけがない。',
      choices: [
        '一人で は 一人に にする',
        '間に合う は 間に合った にしなければならない',
        '「絶対に無理だ」と強く言うときは わけがない。わけではない は「必ずしもそうではない」という弱い否定',
        'ない は ありません にしなければならない',
      ],
      correct: '「絶対に無理だ」と強く言うときは わけがない。わけではない は「必ずしもそうではない」という弱い否定',
      explain: 'わけではない 只是「并不是」；想说「根本来不及」要用 わけがない。',
      zh: '一个人根本来不及。',
    },
    {
      wrong: '彼は日本人だわけがない。',
      fixed: '彼は日本人なわけがない。',
      choices: [
        '彼は は 彼が にしなければならない',
        '名詞は な（または である）を付けてから わけがない に続ける',
        '日本人 は 日本の人 にする',
        'わけがない は わけない にしなければならない',
      ],
      correct: '名詞は な（または である）を付けてから わけがない に続ける',
      explain: '名词接 わけがない：日本人だ → 日本人な（日本人である）→ 日本人なわけがない。',
      zh: '他不可能是日本人。',
    },
  ],
  lessonWords: [
    { ja: '噂', zh: '传言；传闻', example: 'あの店が閉まるという噂を聞きました。', audio: `${AUDIO}/lesson-01-example.m4a`, termAudio: `${AUDIO}/lesson-01-term.m4a`, quiz: '本当かどうか分からないまま、人から人へ伝わる話を「___」と言う。' },
    { ja: '締め切り', zh: '截止日期', example: 'レポートの締め切りは金曜日です。', audio: `${AUDIO}/lesson-02-example.m4a`, termAudio: `${AUDIO}/lesson-02-term.m4a`, quiz: '「この日までに出してください」と決められた最後の日を「___」と言う。' },
    { ja: '延びる', zh: '延长；推迟', example: '雨で、試合が来週に延びました。', audio: `${AUDIO}/lesson-03-example.m4a`, termAudio: `${AUDIO}/lesson-03-term.m4a`, quiz: '決まっていた日や時間が、あとになることを「___」と言う。' },
    { ja: '発表', zh: '发表；报告', example: '授業で、日本の祭りについて発表しました。', audio: `${AUDIO}/lesson-04-example.m4a`, termAudio: `${AUDIO}/lesson-04-term.m4a`, quiz: '調べたことや考えを、みんなの前で話して知らせることを「___」と言う。' },
    { ja: '教授', zh: '教授', example: '田中教授の授業は、とても人気があります。', audio: `${AUDIO}/lesson-05-example.m4a`, termAudio: `${AUDIO}/lesson-05-term.m4a`, quiz: '大学で教えたり研究したりする、いちばん上の先生を「___」と言う。' },
    { ja: '資料', zh: '资料', example: '会議の資料を十部コピーしてください。', audio: `${AUDIO}/lesson-06-example.m4a`, termAudio: `${AUDIO}/lesson-06-term.m4a`, quiz: '会議や発表のときに使う、情報が書いてある紙などを「___」と言う。' },
    { ja: '担当', zh: '负责；负责人', example: 'この仕事の担当は、山田さんです。', audio: `${AUDIO}/lesson-07-example.m4a`, termAudio: `${AUDIO}/lesson-07-term.m4a`, quiz: 'ある仕事を受け持つこと、またはその人を「___」と言う。' },
    { ja: '相談に乗る', zh: '帮人出主意；听人商量', example: '先輩が、進路の相談に乗ってくれました。', audio: `${AUDIO}/lesson-08-example.m4a`, termAudio: `${AUDIO}/lesson-08-term.m4a`, quiz: '困っている人の話を聞いて、一緒に考えてあげることを「___」と言う。' },
  ],
  bonusWords: [
    { ja: '論文', zh: '论文', example: '卒業論文のテーマを決めました。', audio: `${AUDIO}/word-01-example.m4a`, termAudio: `${AUDIO}/word-01-term.m4a`, quiz: '研究したことを、決まった形でまとめて書いた文章を「___」と言う。' },
    { ja: '提出する', zh: '提交', example: '宿題は、明日までに提出してください。', audio: `${AUDIO}/word-02-example.m4a`, termAudio: `${AUDIO}/word-02-term.m4a`, quiz: 'レポートや書類を、先生や会社に出すことを「___」と言う。' },
    { ja: '課題', zh: '课题；作业', example: '今週は課題が多くて、とても忙しいです。', audio: `${AUDIO}/word-03-example.m4a`, termAudio: `${AUDIO}/word-03-term.m4a`, quiz: '先生から出された、やらなければならない勉強を「___」と言う。' },
    { ja: '単位', zh: '学分', example: 'この授業を休みすぎると、単位がもらえません。', audio: `${AUDIO}/word-04-example.m4a`, termAudio: `${AUDIO}/word-04-term.m4a`, quiz: '大学で授業を終えると、もらえる点数のようなものを「___」と言う。' },
    { ja: '欠席する', zh: '缺席', example: '熱があったので、授業を欠席しました。', audio: `${AUDIO}/word-05-example.m4a`, termAudio: `${AUDIO}/word-05-term.m4a`, quiz: '授業や会に出ないで休むことを「___」と言う。' },
    { ja: '参考', zh: '参考', example: '先輩のレポートを参考にしました。', audio: `${AUDIO}/word-06-example.m4a`, termAudio: `${AUDIO}/word-06-term.m4a`, quiz: '自分で考えたり作ったりするときに、ほかのものを見て助けにすることを「___」と言う。' },
    { ja: '引用する', zh: '引用', example: '本の文章を引用するときは、出典を書きます。', audio: `${AUDIO}/word-07-example.m4a`, termAudio: `${AUDIO}/word-07-term.m4a`, quiz: 'ほかの人の文章や言葉を、そのまま自分の文の中に使うことを「___」と言う。' },
    { ja: '分析する', zh: '分析', example: 'アンケートの結果を分析しました。', audio: `${AUDIO}/word-08-example.m4a`, termAudio: `${AUDIO}/word-08-term.m4a`, quiz: 'ものごとを細かく分けて、よく調べることを「___」と言う。' },
    { ja: '調査', zh: '调查', example: '学生の生活について調査を行いました。', audio: `${AUDIO}/word-09-example.m4a`, termAudio: `${AUDIO}/word-09-term.m4a`, quiz: '本当のことを知るために、くわしく調べることを「___」と言う。' },
    { ja: '結論', zh: '结论', example: '長い話し合いのあと、やっと結論が出ました。', audio: `${AUDIO}/word-10-example.m4a`, termAudio: `${AUDIO}/word-10-term.m4a`, quiz: 'よく考えたり話し合ったりして、最後に決まった考えを「___」と言う。' },
    { ja: '徹夜する', zh: '熬通宵', example: 'レポートのために、昨日は徹夜しました。', audio: `${AUDIO}/word-11-example.m4a`, termAudio: `${AUDIO}/word-11-term.m4a`, quiz: '夜、一度も寝ないで朝まで起きていることを「___」と言う。' },
  ],
  sentence: {
    marker: 'わけ(が)?(ない|ありません|なかった)',
    markerNoSpace: '訳(が)?(ない|あり)',
    spacingLabel: '写法：わけ 用假名，没有写成「訳」',
    displayName: '〜わけがない',
    meaningSide: 'before',
    meaningLabel: '句意完整：わけがない 前面写出了「不可能」的事',
    starters: ['あの人が', '三日で', 'こんなに難しい問題が'],
    placeholder: '例：三日でこの本を全部覚えられるわけがない。',
  },
  sentenceTitle: '用 〜わけがない 说说「不可能」',
  related: [
    { id: 'gj-12', note: '〜わけではない＝「并不是」（弱）；〜わけがない＝「绝对不可能」（强）' },
    { id: 'gj-11', note: '〜わけだ＝知道原因后「怪不得」；〜わけがない＝「根本不可能」' },
  ],
};
