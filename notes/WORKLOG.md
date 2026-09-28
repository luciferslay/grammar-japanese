# 日语语法互动学习网站 工作日志（第三个站）

> 规矩沿用韩语站与商务日语站：所有决定和被否决的方案都记在这里，否决的划掉保留。
> 项目文件夹：`~/Developer/nihongo/grammar-japanese`（拍板后从商务站复制）；文档在本目录 `~/Developer/nihongo/grammar/`。

## 项目目标（Luna 2026-09-27）

- 和商务日语站**分开**的第三个站：一课一语法（照韩语站的做法），JLPT **N4 → N2**，按难度从易到难分三块。
- 面向从零开始的日语学习者（不是 Luna 自己）；N4 从最基础的语法一课不落地排。Luna 负责拍板与人耳复核。
- 声线、配色、音频流水线、会员年卡制、预览链接、/review 等细节全部和商务站一样。
- 语体默认值：朋友、家人 → 普通体；店员、初次见面、前后辈 → 丁寧語；不碰商务敬語 —— **例外：语法点本身是尊敬語・謙譲語时单独开课**。
- 课程流程照韩语站的 6 步（不是商务站的 7 步、不做角色扮演）。
- 顺序表先排一版粗表，做的时候再调（附在大纲文件末尾）。

## 时间线

### 2026-09-27 起步

- Luna 提出需求、回答了四个问题（站名要和韩语站「하루한컷」差不多，Claude 给备选；从 N4 基础开始；语体默认值同意，敬语单独开课；顺序表先粗排）。
- 写了头两课大纲 `LESSON_DRAFT_gj-01-02.md`（第 1 课 〜たことがある，拉面店聊旅行，普通体；第 2 课 〜てもいい／〜てはいけない，看房问房东，丁寧語）+ N4→N2 顺序表初稿，答案位置已打散。等 Luna 在侧边栏批注、拍板。
- 22:20 Luna 批注：站名定为 **一日一コマ**；第 1 课的女生改成中国留学生 **リン**；N4 基础课课文**全部用です・ます**，「って言う」这类口语缩略写成正式的「と言う」；第 2 课第 6 句改成「それより長かったらちょっと困りますけどね」。已改（第 1 课词表因此从 5 个减到 4 个：いいなあ 没了）。
- 22:20 Luna 批注：站名定为 **一日一コマ**；第 1 课的女生改成中国留学生 **リン**；N4 基础课课文**全部用です・ます**，「って言う」这类口语缩略写成正式的「と言う」；第 2 课第 6 句改成「それより長かったらちょっと困りますけどね」。已改（第 1 课词表因此从 5 个减到 4 个：いいなあ 没了）。
- 22:25 批注：第 1 课第 6 句「東京の店」→「東京のお店」。

### 2026-09-27 22:2x～22:4x 拍板 → 建项目、写头两课、本地预览（Luna「开做吧」）

- 项目 `~/Developer/nihongo/grammar-japanese`：从商务站复制（node_modules 另外整份复制 —— 第一次 rsync 的 `--exclude dist` 把 node_modules 里所有叫 dist 的目录都排除了，tsc 报找不到 vinext/types，补拷后正常）。
- 改名与隔离：站名「一日一コマ」、口号「每天一个日语语法场景」、标记「一」；本地预览端口 **3200**（韩语 3000、商务 3100）；launchd 标签 `com.grammar-japanese.*`；邀请码前缀 **GJ-**；会话 cookie 改名 `gj_session / gj_otp / gj_preview` —— **不改的话三个站都在 localhost 上，cookie 不分端口，登录一个站会把另一个站踢下线**；`.dev.vars` 管理员邮箱沿用、AUTH_SECRET 新生成；`.openai/hosting.json` 的 project_id 清空，等 Luna 在 Codex 建新 Sites 项目。
- 课程页从商务站的 7 步改回韩语站的 **6 步**：删掉场景任务卡、场景拆解、角色扮演（连 `lib/roleplay-check.ts`、`Lesson.scene` 类型一起删），3/6 恢复完整对话列表，侧栏恢复「本课语法」。会员年卡制、预览链接、/review、门禁都保留，门禁文案改回「1/6 免费、2/6 起解锁」。
- 写好 `lib/lessons/ramen-trip.ts`（gj-01 〜たことがある）与 `room-viewing.ts`（gj-02 〜てもいい／てはいけない），先放 pendingLessons（插图、音频齐了再上首页）；`shuffle_answers.py`、`check_bonus_in_dialogue.py`、tsc 都过。
- 音频：新加 `scripts/generate_batch.py`（一个 job 顺序跑多课：`lessons=gj-01,gj-02`），`generate_lesson_audio.py` 支持环境变量 LESSON。job 已放进本站队列 `audio-jobs/gj-01-02.job`，**等 Luna 装好本站的 worker 就开跑**（四行命令，见 scripts/audio_worker_install.md）。
- 本地预览：经商务站 worker 起了本站的常驻预览服务，http://localhost:3200 ；/、/lesson/gj-01、/lesson/gj-02、/review、会员各页全 200。
- 新文件：本目录的 `LESSON_ORDER.md`（从大纲附录搬过来）、`WORD_RULES.md`（只写和商务站不同的地方）。

### 2026-09-27 22:5x Codex 建好 Sites 项目 → 接上 + 定时报告

- Luna：Codex 已建好本站的 Sites 项目，ID `appgprj_6ab91dae36a88191ad7df86daefc71a4`。已写进 `grammar-japanese/.openai/hosting.json`（**发现里面原来还留着商务站的 project_id，没清掉 —— 如果就这样部署会覆盖商务站**，现已改正）。
- 照韩语站设了两个定时报告：每天 09:00（短报）、21:00（完整汇报 + 攒着的 Codex 作业清单、索电脑权限）。报告读本目录的 WORKLOG.md / LESSON_ORDER.md（有 CODEX_QUEUE.md 也读）和 grammar-japanese 仓库的 audio-jobs 日志、git 状态。
- 当时状态：gj-01/02 音频 job 在跑（本站 worker 已装好），日志 7 条 PASS、0 FAIL；`public/audio/` 未提交。

### 2026-09-28 13:3x /review 播不了音频 → 修好；上线准备（Luna「和韩语站一样推 Cloudflare」）

- **/review 没声音的原因有两层**：① 课程数据引用的是 `.m4a`，而 worker 只生成了 WAV 母带，没跑 `publish_audio.py` 转码 —— 已转（32 条，4.2 MB → 0.7 MB）；② `generate_lesson_audio.py` 抽附加单词的正则只认「一字段一行」的写法，而 bonusWords 是一行一个词，**每课 12 个附加词 × 2 条全被跳过**，所以 word-NN-*.m4a 根本不存在 —— 已改成允许任意空白，重新排队 `gj-01-02-bonus2.job` 只补缺的 48 条（已生成的自动跳过）。生成完还要再跑一次 `publish_audio.py`。
- 第一次排队写错格式（job 文件第一行必须是脚本名 `generate_batch.py`），失败的那份已删。
- 昨晚 job 里 `gj-01/lesson-04-term.wav` 自动检查没过（CHECK），今天 `word-01-example.wav` 也标了 low_pitch，都等 Luna 人耳复核。
- **上线准备**（照韩语站 2026-09-22 的 `4c00cf8`）：vite.config 只在构建变量 `D1_DATABASE_ID` 有值时绑定 D1（数据库名 `grammar-japanese-db`）；没数据库时会员功能自动关闭、全站开放；/outbox 线上要 `?key=OUTBOX_KEY`。tsc 过。
- 已提交 `59d6cc5`（代码 + 32 条 m4a + 两张插图）。Claude 这边推不了 GitHub（代理 403），**等 Luna 推**。
- Cloudflare 后台步骤见下面「上线步骤」；线上地址预计 `grammar-japanese.lunafan716.workers.dev`（Luna 建 Worker 时取的名字决定）。

#### 上线步骤（Luna 在 Cloudflare 后台操作，照韩语站）
1. 把仓库推到 GitHub（`git push`）。
2. Cloudflare 后台「Workers & Pages」→「Create」→「Import a repository」→ 选 `luciferslay/grammar-japanese`；Build command 填 `npm run build`，Deploy command 填 `npx wrangler deploy --config dist/server/wrangler.json`（和韩语站一样，如果韩语站填的不同就照韩语站的）。
3. 部署成功后先不用管数据库：全站开放、没有登录入口。
4. 要开会员功能时：D1 建 `grammar-japanese-db` → 构建变量加 `D1_DATABASE_ID` → 运行时密钥加 `ADMIN_EMAILS`、`AUTH_SECRET`、`OUTBOX_KEY` → 再推送一次。
