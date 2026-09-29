import type { Lesson } from './types';

const AUDIO = '/audio/standard/gj-05';

/**
 * 网站第 5 课：動詞ます形 + ながら（同时做两件事）。JLPT N4。
 * 大纲 notes/LESSON_DRAFT_gj-05-06.md（Luna 2026-09-29「你刚给我的课文可以先做」）。
 * 人物：A＝拓也（男）；B＝リン（女，中国留学生）。大学同学。
 * 语体：N4 基础课一律丁寧語 → 练习第 1 题用普通体。
 */
export const walkAndPhone: Lesson = {
  id: 'gj-05',
  badge: 'JLPT N4',
  listTitle: '歩きながらスマホを見てはいけません',
  listSummary: '边走边看手机差点撞车，边看剧边写作业写了三小时。',
  image: {
    src: '/walk-and-phone.png',
    alt: '傍晚车站附近的商店街，戴圆眼镜的女生低头看手机，差点撞上停着的自行车，男生伸手拦住她',
  },
  grammar: {
    title: '動詞ます形 + ながら',
    summary: '同一个人同时做两件事：「一边……一边……」。',
    example: '地図を見ながら歩いていました。',
    note: '动词ます形去掉ます，接 ながら（見ます→見ながら、聞きます→聞きながら）。意思是同一个人同时做两件事。主要的动作放在后面：「音楽を聞きながら勉強します」主要在学习。两个人各做各的不能用 ながら。时态和礼貌体放在后面的动词上，ながら 本身不变。和前两课对比：〜たり〜たり 是举例子，〜て、〜て 是按顺序，〜ながら 是同时。',
    points: [
      '形：动词 **ます形去ます + ながら**（見ながら、聞きながら）',
      '意思：**同一个人同时做两件事**，一边……一边……',
      '**主要的动作放在后面**：音楽を聞きながら**勉強します**',
      '**前后必须是同一个人**，两个人各做各的不能用',
      '时态、礼貌体放在后面的动词上：〜ながら〜**しました**',
      '对比：**ながら**＝同时；**たり**＝举例；**〜て、〜て**＝按顺序',
    ],
  },
  dialogue: [
    {
      role: 'A',
      text: 'リンさん、危ないですよ。歩きながらスマホを見てはいけません。',
      zh: '小林，危险！不能边走边看手机。',
      audio: `${AUDIO}/dialogue-01.m4a`,
    },
    {
      role: 'B',
      text: 'すみません。地図を見ながら歩いていました。駅はこっちですよね。',
      zh: '对不起。我在边看地图边走。车站是这边吧？',
      audio: `${AUDIO}/dialogue-02.m4a`,
    },
    {
      role: 'A',
      text: 'はい。僕も時々、音楽を聞きながら歩きますけど、画面は見ません。',
      zh: '对。我有时也边听音乐边走，但不看屏幕。',
      audio: `${AUDIO}/dialogue-03.m4a`,
    },
    {
      role: 'B',
      text: '私は勉強するときも、いつも音楽を聞きながらします。',
      zh: '我学习的时候也总是边听音乐边学。',
      audio: `${AUDIO}/dialogue-04.m4a`,
    },
    {
      role: 'A',
      text: 'え、集中できますか。僕はテレビを見ながら宿題をすると、全然終わりません。',
      zh: '诶，能集中吗？我要是边看电视边写作业，怎么也写不完。',
      audio: `${AUDIO}/dialogue-05.m4a`,
    },
    {
      role: 'B',
      text: '実は私もです。昨日もドラマを見ながら宿題をして、三時間かかりました。',
      zh: '其实我也是。昨天也是边看剧边写作业，花了三个小时。',
      audio: `${AUDIO}/dialogue-06.m4a`,
    },
  ],
  feeling: {
    eyebrow: '整体感觉',
    question: 'リンさんは歩きながら何を見ていましたか。',
    choices: [
      { value: 'sign', label: '駅の看板' },
      { value: 'map', label: 'スマホの地図' },
      { value: 'tv', label: 'テレビ' },
      { value: 'photo', label: '友達の写真' },
    ],
    correct: 'map',
    success: '答对了。第 2 句：リン在边看地图边走，所以差点撞上。',
    hint: '看第 2 句。',
  },
  meaning: {
    eyebrow: '语法原型',
    question: '「〜ながら」は何を表す？',
    choices: [
      { value: 'same', label: '一人が二つのことを同時にする' },
      { value: 'order', label: '一つのことが終わってから次のことをする' },
      { value: 'examples', label: 'いくつかの例を挙げて言う' },
      { value: 'exp', label: '自分の経験を言う' },
    ],
    correct: 'same',
    success: '答对了。「地図を見ながら歩く」＝一边看地图一边走，两件事同时做，而且是同一个人。',
    hint: '第 2 句：リン是看完地图再走，还是边看边走？',
  },
  grammarTests: [
    {
      question: '把括号里的动词接上适合句子的形式。',
      full: 'コーヒーを飲みながら新聞を読んだ。',
      blank: 'コーヒーを (飲む) ______ 新聞を読んだ。',
      choices: ['飲むながら', '飲んでながら', '飲んだながら', '飲みながら'],
      correct: '飲みながら',
      explain: '答对了。飲む 的ます形是 飲みます，去掉ます 接 ながら：飲みながら。自言自语、跟朋友说话用普通体（読んだ）。',
      zh: '边喝咖啡边看报纸。',
    },
    {
      question: '「音楽を聞きながら勉強します」に一番近い意味は？',
      full: '音楽を聞きながら勉強します。',
      blank: '「…」 ______',
      choices: [
        '音楽を聞いてから勉強する',
        '勉強しているとき、同時に音楽を聞いている',
        '勉強が終わってから音楽を聞く',
        '音楽を聞くか、勉強するか、どちらかをする',
      ],
      correct: '勉強しているとき、同時に音楽を聞いている',
      explain: '答对了。ながら 是两件事同时做，主要在学习，音乐是陪衬。',
      zh: '边听音乐边学习。',
    },
    {
      question: '次の中で自然な文は？',
      full: '電話をしながら、メモを取りました。',
      blank: '「…」 ______',
      choices: [
        '歯を磨きながら、ご飯を食べました。',
        '寝ながら、公園を走りました。',
        '電話をしながら、メモを取りました。',
        '母が料理をしながら、私はテレビを見ました。',
      ],
      correct: '電話をしながら、メモを取りました。',
      explain: '答对了。①②两件事不可能同时做；④前后不是同一个人，要说「母が料理をしている間に」。',
      zh: '边打电话边记笔记。',
    },
  ],
  grammarTestHint: '不太对。动词先变成ます形、去掉ます，再接 ながら；主要的动作放在后面。',
  errorTests: [
    {
      wrong: '地図を見るながら歩いていました。',
      fixed: '地図を見ながら歩いていました。',
      choices: [
        '見る は ます形（見）にしてから ながら を付ける',
        '地図を は 地図が にする',
        '歩いていました は 歩きました にしなければならない',
        'ながら は 過去の文に使えない',
      ],
      correct: '見る は ます形（見）にしてから ながら を付ける',
      explain: 'ながら 接在ます形后面：見ます→見ながら。',
      zh: '我在边看地图边走。',
    },
    {
      wrong: '母が料理をしながら、私は宿題をしました。',
      fixed: '母が料理をしている間に、私は宿題をしました。',
      choices: [
        '料理 は 料理する にする',
        '宿題 の後ろは が にする',
        'しました は します にする',
        'ながら は同じ人が二つのことをするときに使う。人が違うときは使えない',
      ],
      correct: 'ながら は同じ人が二つのことをするときに使う。人が違うときは使えない',
      explain: '做饭的是妈妈，写作业的是我，两个人各做各的，不能用 ながら。',
      zh: '妈妈做饭的时候，我写了作业。',
    },
    {
      wrong: '宿題をしながらドラマを見ました。（想说「主要在写作业，顺便开着剧」）',
      fixed: 'ドラマを見ながら宿題をしました。',
      choices: [
        'ドラマ は テレビ にする',
        '宿題を は 宿題が にする',
        '主な動作は ながら の後ろに置く',
        '見ました は 見ていました にしなければならない',
      ],
      correct: '主な動作は ながら の後ろに置く',
      explain: '主要在写作业，所以「宿題をしました」放在后面，陪衬的「ドラマを見」放在 ながら 前面。',
      zh: '边看剧边写了作业。',
    },
  ],
  lessonWords: [
    {
      ja: '画面',
      zh: '屏幕；画面',
      example: 'スマホの画面が暗くて、よく見えません。',
      audio: `${AUDIO}/lesson-01-example.m4a`,
      termAudio: `${AUDIO}/lesson-01-term.m4a`,
      quiz: 'テレビやスマホで字や絵が映る所を「___」と言う。',
    },
    {
      ja: '集中する',
      zh: '集中（精神）',
      example: '静かな所だと勉強に集中できます。',
      audio: `${AUDIO}/lesson-02-example.m4a`,
      termAudio: `${AUDIO}/lesson-02-term.m4a`,
      quiz: 'ほかのことを考えないで、一つのことだけをすることを「___」と言う。',
    },
  ],
  bonusWords: [
    { ja: '充電する', zh: '充电', example: '寝る前にスマホを充電します。', audio: `${AUDIO}/word-01-example.m4a`, termAudio: `${AUDIO}/word-01-term.m4a`, quiz: '電池に電気をためることを「___」と言う。' },
    { ja: '電池', zh: '电池；电量', example: '電池がもうすぐなくなります。', audio: `${AUDIO}/word-02-example.m4a`, termAudio: `${AUDIO}/word-02-term.m4a`, quiz: '時計やリモコンなどに入れて電気を出す物を「___」と言う。' },
    { ja: 'アプリ', zh: '应用程序', example: '便利なアプリを友達に教えてもらいました。', audio: `${AUDIO}/word-03-example.m4a`, termAudio: `${AUDIO}/word-03-term.m4a`, quiz: 'スマホに入れて使うソフトを「___」と言う。' },
    { ja: '調べる', zh: '查', example: '分からない言葉を辞書で調べます。', audio: `${AUDIO}/word-04-example.m4a`, termAudio: `${AUDIO}/word-04-term.m4a`, quiz: '分からないことを本やネットで見て知ることを「___」と言う。' },
    { ja: '連絡する', zh: '联系', example: '遅れるときは連絡してください。', audio: `${AUDIO}/word-05-example.m4a`, termAudio: `${AUDIO}/word-05-term.m4a`, quiz: '電話やメールで相手に知らせることを「___」と言う。' },
    { ja: '返事', zh: '回复', example: '友達からまだ返事が来ません。', audio: `${AUDIO}/word-06-example.m4a`, termAudio: `${AUDIO}/word-06-term.m4a`, quiz: '聞かれたことやメールに答えることを「___」と言う。' },
    { ja: 'イヤホン', zh: '耳机', example: '電車ではイヤホンで音楽を聞きます。', audio: `${AUDIO}/word-07-example.m4a`, termAudio: `${AUDIO}/word-07-term.m4a`, quiz: '耳に入れて音を聞く小さい道具を「___」と言う。' },
    { ja: 'ぶつかる', zh: '撞上', example: '自転車が電柱にぶつかりました。', audio: `${AUDIO}/word-08-example.m4a`, termAudio: `${AUDIO}/word-08-term.m4a`, quiz: '人や物が強く当たることを「___」と言う。' },
    { ja: '気をつける', zh: '小心；注意', example: '車に気をつけて帰ってください。', audio: `${AUDIO}/word-09-example.m4a`, termAudio: `${AUDIO}/word-09-term.m4a`, quiz: '危なくないように注意することを「___」と言う。' },
    { ja: '信号', zh: '红绿灯', example: '信号が青になってから渡ります。', audio: `${AUDIO}/word-10-example.m4a`, termAudio: `${AUDIO}/word-10-term.m4a`, quiz: '道で赤・青・黄色に光って、渡るかどうかを知らせる物を「___」と言う。' },
    { ja: '道に迷う', zh: '迷路', example: '初めての町で道に迷いました。', audio: `${AUDIO}/word-11-example.m4a`, termAudio: `${AUDIO}/word-11-term.m4a`, quiz: 'どこへ行けばいいか分からなくなることを「___」と言う。' },
  ],
  sentence: {
    marker: 'ながら',
    markerNoSpace: '乍ら',
    spacingLabel: '写法：ながら 用假名，没有写成「乍ら」',
    displayName: '〜ながら',
    meaningSide: 'after',
    meaningLabel: '句意完整：ながら 后面写出了主要在做什么',
    starters: ['電車で', '朝ご飯を', '友達と'],
    placeholder: '例：朝ご飯を食べながらニュースを見ます。',
  },
  sentenceTitle: '用 〜ながら 说说看',
  related: [
    { id: 'gj-04', note: '〜たり〜たり 是举例子；〜ながら 是同一个人同时做两件事' },
  ],
};
