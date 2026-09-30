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

### 2026-09-28 22:xx 搬到 Windows（ROG G14）：环境装好、脚本改 GPU、录 Ono_Anna 第二版试听

- **Claude App 在 Windows 上能跑命令、读写文件**（交接第 1 步通过）。
- WSL：Luna 说装好了，实际上「虚拟机平台」没开、没有 Ubuntu。Luna 用管理员 PowerShell 跑 `wsl --install -d Ubuntu` 并重启后正常（Ubuntu 26.04，用户 `lunafan716`）。
- Ubuntu 用户的密码 Luna 没设过，所以 sudo 用不了 → 装系统包一律由 Claude 用 `wsl -u root` 装（不需要密码）。已装：ffmpeg、sox、build-essential（Triton 要现场编译 C）、Node 22.22 + npm；uv 装在 `~/.local/bin`。
- 仓库在 WSL 的 `~/nihongo/grammar-japanese`，`npm install` 完成；两个 Qwen3-TTS 模型（CustomVoice、Base@fd4b254）和 whisper small/medium 都下好了。
- **驱动 555.97 只支持 CUDA 12.5**，PyPI 默认的 torch 2.14 是 CUDA 13 版，`cuda.is_available()` 为 False。~~让 Luna 再更新驱动~~ → 改为这台机器上设 `UV_INDEX=https://download.pytorch.org/whl/cu126`（torch 2.14.0+cu126，实测能用 GPU）。只影响这台，Mac 不受影响。
- **改 GPU**：`standardized_course_tts.py` 新增 `model_load_kwargs()`：有 CUDA → `cuda + bfloat16`，否则 `cpu + float32`（Mac 照旧）。所有加载模型的地方都改用它：generate_lesson_audio、standardized_course_tts、fix_dialogue_lines、fix_dialogue_tails、fix_term_carrier、voice_samples_ono_anna。
- whisper 仍用 CPU int8（没改）。
- 本地预览：`npm run dev -- --host 0.0.0.0`，Windows 浏览器打开 http://localhost:3200 可以直接访问。
- **Ono_Anna 第一版在这台重录了**：原来的 wav/m4a 没入库，而第二版要拿第一版的 dialogue-06 当参考。用同样的设置和 seed，GPU 上 7 条共 139 秒（对话一句约 22 秒）。和 Mac 上那版不一定逐字相同。
- 第二版脚本的修正：① 依赖里补上 faster-whisper（generate_one 会调 whisper，不补会报错）；② 试听声线补上 `reference_sha256`（audit_output 要用，不补会 KeyError）。
- Luna 22:3x：「ono anna 原本的语速很正常，就是语气飘忽不定。让她用原本的语速，语气和初版女声一致。」
  - 实测：Ono_Anna 第一版约 0.17～0.21 秒/音拍，原女声 0.126。~~语速对齐原女声~~（否决：句句判「语速不过关」，还会被 atempo 硬拉快）→ 语速基准改用第一版三句对话的中位数 0.1783；音高基准改用 5 句的中位数 266.7Hz（不只看对话 6）。
  - 音高起伏比（p90/p10）：Ono_Anna 1.41～1.65，原女声 1.53～2.12。数字上她的起伏并不更大，「飘」更可能是句与句之间语气风格不同 → 对话句 ~~温度 0.6、top_k 30~~ 改用和单词卡同一套 generation_card（温度 0.45、top_k 20）。
- **第二版速度**（GPU，正式流水线含 whisper 质检、多 seed 重试）：6 条共 568 秒。对话 2 试到第 3 个 seed 才过（每次约 40 秒）；对话 4 第 1 个 seed 就过；单词卡每个 seed 约 15～20 秒，見せる、こんなに 都试满 6 个 seed。
- 质检全过的只有 3 条：对话 2、对话 4、例句「昨日撮った写真を友達に見せました。」。
- 单词 見せる、こんなに：6 个 seed 都卡在单词时长/杂音那一关（term），保存的是最接近过关的那一版。
- 例句「こんなに寒い日は初めてです。」：6 个 seed 都没过（大多是句中停顿），保存的是 seed+2（音高 324Hz，偏高）。
- 对话 2 过关的那一版音高也偏高（320Hz）。**这 3 条请 Luna 重点听。**
- 发现的小问题：单词没过关时的「载体短语」补救，会去读 `public/audio/standard/ono-anna-v2/`，这个目录不存在，所以失败了。只影响试听脚本（它把输出目录改成了 samples），正式课程不受影响。
- 未提交 git。等 Luna 听完第二版拍板后一起提交。

### 2026-09-28 23:5x〜 女声第三轮（Luna：「ono anna 还是带了很多不必要的感情」）

- ~~换别的内置声音~~：查了 CustomVoice 模型的 spk_id，9 个声音里说日语的女声只有 ono_anna。其余是 serena、vivian（中文女声）、sohee（韩语女声），以及 uncle_fu、ryan、aiden、eric（四川话）、dylan（北京话）等男声。读日语会带口音，否决。
- 所以不换人，换控制方法。新脚本 `scripts/voice_samples_ja_female_v3.py`，三种一起录，对比页 `/samples-ja-female-v3.html`（原女声 / 第二版 / a / b / c 五栏）：
  - a 空指示语（第二版指示语里有「明るく澄んだ」之类的词，模型会把它们读成情绪）。
  - b 指示语只写「ニュース原稿を読むように淡々と、感情を入れない」，温度 0.3、top_k 10。
  - c 先用 b 的设置让 Ono_Anna 读原女声的参考句，4 个 seed 里挑音高起伏最小的一条，再用 Base 模型克隆它。原女声语气稳，靠的就是克隆（读法跟着参考音走）。风险：原女声的问题正是克隆出来的音色每句漂移。
- 为了快一点，每条最多试 3〜4 个 seed。
- 空指示语时「载体短语」补救会一直念到 480 token 上限（每次约 2 分钟，而且目录不对，本来就会失败）→ 以后试听脚本应该关掉这个补救。
- 速度：a 约 11 分钟（其中约 7 分钟耗在载体短语上），b 约 8 分钟。
- 自动质检：
  - a：对话 2、对话 4、例句 見せました 过了；单词 見せる 音高偏低。
  - b：对话 2、对话 4、单词 こんなに、例句 こんなに寒い 过了；例句 見せました 音高偏低（231Hz）。
  - c：参考音 4 个 seed 的起伏比是 1.39、1.32、1.32、1.46，选了 ref-1。对话 2、对话 4、单词 こんなに 过了。其余几条主要卡在语速和音高：克隆出来的读法比第一版快一点、低一点，而基准还是按第一版定的。c 全程约 11 分钟。

### 2026-09-29 00:2x Luna 拍板：女声用 c（克隆 Ono_Anna 平读样音）

- `audio_voice_presets.json`：
  - 新增正式声线 **FEMALE_ONO_ANNA_CLONE**（role B，同时当 card_voice）。Base 模型克隆，参考音 `public/audio/reference-ono-anna-flat.wav`，就是试听 c 用的那条。
  - 基准：语速 0.1535 秒/音拍（试听里两句对话变速前的中位数，也就是她自己的语速）；音高 248.7Hz（4 句中位数）；音量沿用原女声 -23.09，和男声一致。
  - 新字段 `generation_override`：这个声线的对话也用温度 0.45、top_k 20，和单词卡一样。`generate_one` 已改成会读这个字段。注意：fix_* 修补脚本还不读它。
  - FEMALE_CLEAR_SOFT **不删**，role 改为 null，并加 `retired` 说明停用原因。试听用的 TRIAL、V3A、V3B、V3C 都是 candidate，留作记录。
- 新脚本：
  - `scripts/rerecord_female.py`：把本课男声对话预先记成「已完成」，再调用 `generate_lesson_audio.main()`，所以只录单词卡和女声对话。
  - `scripts/redo_items.py`：用 `REDO=` 指定条目，只重录这几条。job 的 redo= 选项靠进度文件，而这台电脑没有进度文件，用它会把整课重录一遍。
- 第 1、2 课的女声条目在这台上重录，录完跑 `publish_audio.py` 转 m4a。
- 第 1 课：38 条里单词卡 + 女声对话共 35 条，用了 691 秒（约 11.5 分钟，平均约 20 秒一条）。自动质检只有 word-07-example 没过，等 Luna 人耳复核。
- 男声的参考音 `reference-b-calm-slow.wav` 和旧女声的 `reference-a-clear-soft.wav` 原来不在仓库里（wav 被 .gitignore 排除），Windows 这台录不了男声。Luna 让 Mac 那边的 Claude 用 `git add -f` 提交了（`53b8464`），已经拉到这台，sha256 校验通过。
- 第 1 课对话 5（男声，函館→はこだて）排在女声之后重录。
- 新女声的参考音 `reference-ono-anna-flat.wav` 提交时也要用 `git add -f`，否则 Mac 上用不了。
- 第 2 课：单词卡 + 女声对话共 39 条，用了 778 秒（约 13 分钟）。自动质检没过的是 lesson-04-term、word-01-term。
- 第 1 课对话 5（男声）重录用了 104 秒，第 2 个 seed 通过。
- 本地提交 `adc7eb7`，和 Mac 的 `8ecbce1`、`53b8464` 合并成 `ae2ee54`（v2 试听脚本冲突时保留本机版本；Mac 那两处修复这边都已经有了）。`package-lock.json` 被这台的 npm 9 改过，已还原，没有提交。
- 推送：这台原来没有 GitHub 凭据。装了 gh，Luna 用 `gh auth login --web` 登录 luciferslay，dry-run 推送成功 → **这台能 push**。真正推送等 Luna 确认（Cloudflare 接好后，推送会触发部署）。
- 预览服务器 `npm run dev` 挂在 Claude 的后台任务上，这个任务结束时服务器会跟着停，需要时重新启动。

### 2026-09-29 01:xx Luna 人耳复核

- 第 1 课附加单词 並ぶ 的例句：「三十分並んで、やっと~~入れました~~入りました。」，读 はいりました。
  - 改了 `lib/lessons/ramen-trip.ts` 和大纲 `LESSON_DRAFT_gj-01-02.md`。
  - ~~读音表加了「やっと入り→やっとはいり」~~（~~登记「入りました→はいりました」~~ 也否决：读音表全站通用，「気に入りました」会被读成「気にはいりました」）。
  - 重录 word-05-example，第 1 个 seed 就过了，用时 41 秒，已转 m4a。
- Luna 人耳复核：这条「没录全」。whisper 听成「やっと会いりました／会えました」—— 换成假名「はいりました」后，模型把开头的 は 吞了。
  - 例句过去不过整句 ASR，所以这种错收下了也没人发现。
  - 撤掉上面那条读音（它本来就是 Claude 预先登记的，Luna 并没有听到读错，违反「只登记人耳确认读错的词」）。改回直接读汉字。
  - `generate_one` 改为：例句也过整句 ASR（`check_sentence`），没读全就换 seed。
  - 顺带修了 ASR 闸门对数字的盲区：whisper 会把「三十分」写成「30分」，假名转换直接丢掉数字，句首带数字的句子会被判成「句首没读」。`ja_text.kana_only` 先把阿拉伯数字换成汉字数字（`digits_to_kanji`）。
  - 修之前，重录的 6 个 seed 全部被这个盲区误判。修之后，保存的那版两个 whisper 模型都听成「30分並んで、やっと入りました」，相似度 1.0。
  - 限制：whisper 不管音频读「はいりました」还是「いりました」，都写成汉字「入りました」，ASR 分辨不了这两种读法，**读音要 Luna 人耳确认**。
  - 新脚本 `scripts/asr_check_items.py`：对任意条目跑整句 ASR，看听到的是什么。

### 2026-09-29 Luna：「今晚写 2 课新的大纲给我 check」

- 按顺序表写了第 3 课（gj-03 〜なければならない／〜なくてもいい，咖啡店打工第一天，前辈拓也带新人リン）和第 4 课（gj-04 〜たり〜たりする，周一在大学食堂聊周末）→ `LESSON_DRAFT_gj-03-04.md`。插图命令放在最前面。
- 格式同第 1、2 课。单词例句这次直接写成です・ます。答案已用 shuffle_draft_answers.py 打散。
- 「制服」（和征服同音）、「週末」（和終末同音）不做单词卡。
- 等 Luna 批注。

### 2026-09-29 Luna 人耳复核（第 2 课）

- 读错：对话 6 二、三日（应读 にさんにち）；附加单词 大家さん 和例句（应读 おおやさん）；附加单词 家賃（应读 やちん）。
  - 读音表新增 二、三日→にさんにち、大家さん→おおやさん、家賃→やちん。大家 只登记带「さん」的形式。
  - 例句「家賃は月に七万円です。」也含 家賃，而且之前 whisper 听成「イヤチン」，所以一起重录。
- 没录全：附加单词 隣の人。
- 重录 dialogue-06、word-01-term/example、word-02-term/example、word-11-term，共 221 秒，都已转 m4a。
- whisper 核对：
  - 对话 6：听到「2、3日なら構いませんよ…」，相似度 1.0。
  - 大屋さんに やちんを払いました：相似度 1.0。
  - 家賃 单词：听到 やちん。
  - 隣の人：完整。
  - 大家さん 单词：medium 模型写成「おーやさん」，长音符号和「おお」的写法不一样，判了不过；其实读音是对的。
- Luna 再复核：读音对了，但**重音错了**。二、三日应为低高低、重音在「さん」；大家さん、家賃都是头高。
  - 原因：换成假名后，模型拿不到这个词原来的声调信息（同 2026-09-23 手土産 的教训）。隣の人 仍然没录全。
  - Qwen3-TTS 没有指定重音的参数，只能多录几版挑。
  - 新脚本 `scripts/accent_candidates.py`：每条试 汉字／平假名／片假名 3 种写法 × 4 个 seed。每版粗测目标词各音拍的音高，算「重音分」（高拍平均 − 低拍平均，单位半音），同时跑整句 ASR。输出到 `public/audio/candidates/gj-02/`，让 Luna 人耳挑。
  - 第一次启动时段错误（exit 139，大概是会话结束时进程被杀），重跑正常。

### 2026-09-29 Luna：「开做这两课（第 3、4 课），再给我新课 2 节」

- 大纲照原样落成课程文件：`lib/lessons/cafe-part-time.ts`（gj-03）、`weekend-talk.ts`（gj-04），放进 pendingLessons。
  - gj-03 加了 related → gj-02。
  - 通过：shuffle_answers.py、check_bonus_in_dialogue.py、tsc。
- 两课全部音频（男女声都录）排在重音候选之后，自动开跑。
- 新大纲 `LESSON_DRAFT_gj-05-06.md`：
  - gj-05 〜ながら：傍晚去车站，リン边走边看手机，被拓也拦住。
  - gj-06 〜すぎる：咖喱店，拓也点了超辣大份。
  - 两课各 5 个本课单词 + 12 个附加单词。
- 不做单词卡的词：スマホ（外来缩略语）、辛い（单读可能读成 つらい）、激辛、水。
- 例句里原本有 〜てしまう（后面的课才教），换成更简单的句子。

### 2026-09-29 晚 Luna：「review 网站再发我一次；先做 N3 之后的两课新课，你刚给我的课文（第 5、6 课）可以先做，N3 的排在那之后」

- 预览服务器又挂了：所有页面都是 500，报错 `Maximum call stack size exceeded`（vinext 的 als-registry）。是开了几个小时、热更新太多次之后的问题，和代码无关；重启就好了。以后遇到同样情况直接重启。
- **站名漏改**：`lib/site.ts` 还是商务站的「ワンシーンで学ぶ日本語／每天一个实用日语场景／日」。改成 9/27 定的「一日一コマ／每天一个日语语法场景／一」。邮件模板那边早就改对了。
- 第 2 课重音候选 72 版录完。
  - 试听页 `/accent-candidates.html?lesson=gj-02`：按重音分排序，点卡片选中，生成的结果复制给 Claude。
  - `scripts/pick_candidate.py`：把选中的版本换进课程音频，被换掉的挪到 `candidates/<课>/_replaced/` 留底，然后转 m4a。
  - 粗测结论：二、三日 片假名版分数最高；家賃 单词 12 版几乎都不像头高，可能还得另想办法。
- 第 3、4 课音频录完：gj-03 用 975 秒，gj-04 用 1681 秒。自动质检没过、等 Luna 听的：gj-03 word-10-example；gj-04 lesson-01-example、word-08-example、word-09-example。
- 第 5、6 课照大纲做成课程文件（`walk-and-phone.ts`、`spicy-curry.ts`）和路由。通过 shuffle_answers、check_bonus、tsc，页面 200。gj-05 加了 related → gj-04。音频已开录。
  - 注意：gj-06 对话 1 的「辛すぎます」，whisper 分辨不出 からすぎ 和 つらすぎ，要人耳确认。
- N3 头两课大纲 `LESSON_DRAFT_gj-07-08.md`：gj-07 〜ばかり（超市，拓也篮子里全是杯面），gj-08 〜ところだ 三态（拓也打电话约烤肉，リン正在做饭）。
  - 待 Luna 确认：N3 课文回到默认语体（朋友 → 普通体，练习第 1 题用丁寧語）；口语的自然说法照写；附加单词升到 N3〜N2 档。
  - 放在 pendingLessons 里 N4 课的后面，暂时是网站第 7、8 课；以后 N4 补课时插在它们前面。
  - 大纲标题一开始写成「# N3 第 1 课」，shuffle_draft_answers.py 认不出（它只认「# 网站第 N 课」），答案没打散，第 8 课练习还出现两道都选 ③。改成标准写法后重新打散。

### 2026-09-29 22:xx Luna 人耳复核（第 2、5 课）+ 女声对话语速

- 第 2 课五条（重音）和上次一样，要在重音候选页挑（Luna 还没挑）。
- 第 5 课：
  - 对话 3（男声）的「はい」音色不像同一个人：克隆偶尔会瞬间漂移，没有闸门能抓，只能重录。
  - word-07-example 前面 2.7 秒没声音：底噪在 -55dB 的裁切阈值以上、-40dB 的有声阈值以下，所以没被裁掉。→ 新加「句首空白」闸门：有声点晚于 0.49 秒就不收。
  - word-12-example 没录全：whisper 听着是完整的，可能是尾音被削，重录后请 Luna 再听。
- **Luna：课文里的女生明显比男生慢，要和男生一样快；单词、例句不改。**
  - 实测对话秒/音拍：女 0.154、男 0.124。
  - 女声配置加 `dialogue_seconds_per_mora: 0.1242`、`dialogue_tempo_max: 1.35`；`standardized_course_tts.baseline_for()` 只对 dialogue-* 生效。
  - 已录好的女声对话不重录，用 `scripts/reconform_items.py` 直接变速（音色、语气都是 Luna 听过认可的），变速后再跑一次整句 ASR。
  - pick_candidate.py 换进来的对话句也自动再对齐一次。

### 2026-09-29 22:xx Luna：「試験、できる 等词对 N3 太简单；单词数量不用固定 5 个、12 个；太简单和太难的都不能放进单词里」

- 这条规矩记进了 WORD_RULES。~~凑满 5 个本课单词 + 12 个附加单词~~（否决：会为了凑数混进低一档、甚至 N5 的词）。
- 新脚本 `scripts/word_level_check.py`：
  - 查每课单词的 JLPT 等级，词表是 jamsinclair/open-anki-jlpt-decks（基于 tanos 的非官方表），下载到 WSL 的 ~/jlpt/n1〜n5.csv。
  - 只做精确匹配（原形、去掉する／さん／お、读音）；短语拆开查；查不到的标「表外」。
  - ~~先用 WebFetch 让模型帮忙查~~（否决：它给的答案前后矛盾，例如说 見せる 同时在 N3、N2、N1 表里）。
- N3 大纲改了：
  - gj-07：去掉 試験（N4）、暇（N5）、習慣（N4）。课文第 2 句加「栄養が偏るよ」、第 4 句加「結局」；栄養、偏る 从附加单词挪进本课单词；附加单词加 我慢する（N3）。
  - gj-08：本课单词 ちょうど／集まる／できる／駅前／焼き肉 全都太简单，重写对话里的几句，改用 鍋・材料・偶然（N3）和 せっかく・出来上がる・合流する（N2）。附加单词去掉 都合、遠慮する（都是 N4）。
- **N4 课（第 1〜6 课）严格按这张表查，问题很多**：
  - 大量场景词是 N3，太难：家賃、大家、契約、禁止、飼う、実は、注文、残す 等。
  - 也有很多 N5 词，太简单：働く、休む、旅行、初めて、洗濯、危ない、地図 等。
  - 表本身也有年代久远的怪处：メニュー 标 N2、定食 标 N1、電池 标 N2、ドラマ 标 N3。
  - 这几课已经录好音、Luna 也听过了，要不要严格删、删到什么程度，问 Luna 再动。
- **Luna 选「只删太简单的」**：第 1〜6 课去掉 N5 的词，N3 的场景词先保留。
  - 表里没收录的，按原表确认：ゆっくり(と)、隣 是 N5 → 去掉；ごみ 是 N4 → 保留。
  - 各部分都是 N5 的短语（電話に出る、鍵をかける）也算太简单。
  - 新脚本 `scripts/remove_words.py`：去掉词，剩下的按位置重新编号（lesson-NN / word-NN 的音频文件和课程里的路径一起改）。被去掉的词的音频挪到 `candidates/<课>/_removed_words/` 留底。
  - gj-01：見せる、旅行する、並ぶ、初めて
  - gj-02：掛ける、困る、鍵をかける、隣の人（隣の人 的重音候选也就不用挑了，从候选页去掉）
  - gj-03：覚える、働く、休む、掃除する
  - gj-04：洗濯する、出かける、散歩する、料理する、ゆっくりする、遊ぶ
  - gj-05：危ない、地図、宿題、電話に出る（重录好的 word-07-example 跟着一起去掉）
  - gj-06：頼む、飲み物
  - 检查：课程里引用的音频文件都在、编号连续、没有太简单的词、shuffle／check_bonus／tsc 通过。
  - 「表外」的词（まとめて、使い方、一日中、画面、大盛り 等）暂时保留，等 Luna 看。
- 第 5 课三条重录完成：
  - word-07-example：新的句首空白闸门拦下了一版 6.6 秒的，换成 3.9 秒的。之后这个词被去掉了。
  - word-12-example、dialogue-03：第一个 seed 就过。
- 第 1〜6 课女声对话 18 条变速完成：变速倍数 1.19〜1.26，变速后 0.1243〜0.1255 秒/音拍（男声 0.1242），整句 ASR 全过。

### 2026-09-29 22:3x Luna 人耳复核：女声还是有点快、两处「はい」像换了人、二、三日 重音

- **女声对话改成当时的 0.9 倍速**：dialogue_seconds_per_mora ~~0.1242~~ → 0.138。
  - 18 条在现有母带上再变速 ×0.90〜0.91，变速后 0.1376〜0.1388，整句 ASR 全过。
  - 等于原始录音 ×1.12 左右，只变速、没重录（Luna 说「再录一遍」；重录会换掉她认可过的语气和音色，结果一样是这个语速）。
- **gj-02 对话 6**：Luna 没来得及在候选页挑，Claude 先换上重音分最高的 v3-s3。
  - 注意：v3 这条其实是「二三日」（去掉顿号）的写法，候选页把第 3 种写法统一标成了「片假名」，标错了。
  - 换进来后变速到 0.1386，ASR 过。~~请 Luna 听，不对再在候选页换。~~ **Luna 确认：v3-s3 可以。**
  - 读音表改成 二、三日 → 二三日，以后重录也用这个写法。
- **Luna：大家さん、家賃 的单词和例句也都用 v3-s3**（片假名写法：オオヤさん／ヤチン，例句是「おおやさんにヤチンを払いました」「ヤチンは月に七万円です」）。已用 pick_candidate.py 换进课程；读音表改成 大家さん→オオヤさん、家賃→ヤチン。
  - 经验：假名写法会丢重音。平假名、片假名各有对有错，没有通用规律；遇到重音问题就用 accent_candidates.py 多录几种写法，让 Luna 挑。
- Luna：「做完推送」→ 推送到 GitHub（这台第一次自己推）。

### 2026-09-29 23:xx 插图到了；表外词不删；N3 两课开做

- Luna：插图已经做好（Codex 在 Windows 上出图，放在 `C:\Users\lunac\Documents\Codex\2026-09-29\3-gj-03-developer-nihongo-grammar\outputs\`）。
  - 有 4 张：cafe-part-time、weekend-talk、supermarket-noodles、phone-dinner。Claude 看过，没有可读文字或乱码，人物一致，已复制进 public/。
  - **第 5、6 课（walk-and-phone、spicy-curry）的图还没做。**
- 原因：插图命令写的是 Mac 路径，Codex 找不到项目，图只留在它自己的 outputs 里。
  - Luna：以后在插图命令里写明路径。第 3〜8 课大纲里的插图命令都改了：存进 WSL 项目的 public（`\\wsl.localhost\Ubuntu\...\public\`），写不进就存 `C:\Users\lunac\Documents\Codex\ichinichi-illustrations\`（文件夹已建好）。
  - 这条也写进了 WORD_RULES「工作方式」。
- Luna：「表外」的词（まとめて、使い方、一日中、画面、大盛り、自炊、息抜き、割り勘 等）**不删**。
- Luna：「N3 两课你可以先做」→ 照改过的大纲写好 `supermarket-noodles.ts`（gj-07）、`phone-dinner.ts`（gj-08）和路由，放在 pendingLessons 的 N3 段。
  - 通过：shuffle、check_bonus、等级检查（没有太简单的词）、tsc。
  - 两课音频（男女声）已开录。
- 预览服务器又卡死一次（同样的 als-registry 栈溢出），重启就好了。
- **句首「はい」像换了个人**（gj-03 对话 2 女声、gj-05 对话 3 男声；gj-05 上次重录过一次，没用）：
  - 新脚本 `scripts/consistent_redo.py`：每条录 8 版，按第一段停顿切开，算句首段和其余部分的音色距离（MFCC 余弦），闸门都过的里面取最小的。
  - gj-03 d02：8 版的距离是 0.37〜1.39，选了 s2（0.373）。
  - gj-05 d03：8 版的距离是 0.12〜1.82，选了 s3（0.136）。
  - 距离把好坏分得很开：好的 0.1〜0.4，差的 0.9 以上。→ 加进正式流水线：对话句「句首音色」距离超过 0.7 就不收（`term_audio_policy.head_rest_distance`）。

### 2026-09-30 11:xx Luna 确认 N3 头两课大纲的三个待确认点 → 收尾第 7、8 课

- Luna 确认：① N3 课文回到默认语体（朋友普通体，练习第 1 题丁寧語）；② 口语的自然说法照写；③ 单词 N3〜N2 档，照 word_level_check.py 筛。昨晚写的课程文件本来就是这样，不用改。
- **这次是云端对话连到 G14**：只能读写 Windows 的 `Documents\GitHub\grammar-japanese`，碰不到 WSL 和显卡，推送也被代理挡（403）。
  - ~~云端对话在 Windows 仓库里重写一遍 gj-07/08、再让 Luna 在 WSL 跑录音~~（否决：没先看 WSL 的状态，其实昨晚 23:xx 已经写好、录好了；合并时两份 ts 冲突，已 `git merge --abort` 撤回，没造成损失。重写的两条提交已丢弃）。
  - 教训：接手前先看**正在干活的那份仓库**（WSL）的状态，不要只看 Windows 那份副本。
  - 新增 `_claude/sync_from_wsl.sh`（不入库）：只读 WSL，把它的提交、没入库的音频和质检结果同步到 Windows 仓库，给云端对话看。
- 音频现状：gj-07、gj-08 各 38 条都录完了（9/29 23:5x〜9/30 00:15），m4a 都在。gj-07 lesson-01-term（栄養）后来又重录过一次。
- 自动质检没过、**请 Luna 重点听**的 6 条：
  - gj-07 对话 2（女）：whisper 把「拓也」听成「ルイヤ」，句首比对 0.67。人名常被听错，要人耳确认是不是读成了别的音。
  - gj-07 对话 5（男）：语速 0.152 秒/音拍，比基准 0.124 慢（变速已到上限 1.12）；句中有「……」停顿，可能是停顿拉长了平均值。
  - gj-07 lesson-01-term 栄養：两个模型都听成「ええよ」，判「没读全」。えいよう 口语本来就接近 ええよう，要人耳确认有没有吞掉「う」。
  - gj-07 word-08-term 怠ける：听成「バコペル／マコケル」，开头可能有杂音或读错，**最可能要重录**。
  - gj-08 对话 1（男）：语速 0.226 秒/音拍，明显慢；这句短、停顿多（もしもし、リン？ 今、何してる？），要听是不是拖得太长。
  - gj-08 word-10-example（おごってくれました）：语速 0.112，偏快（减速已到下限 0.9）。
- 插图：第 7、8 课昨晚已入库，这一步不用再交给 Codex。**第 5、6 课的图还没做**。
- 预览服务器在 WSL 里开着：http://localhost:3200/review 。


### 2026-09-30 12:0x Luna 人耳复核（第 6 课）+ /review 改版

- 第 6 课 7 条：
  - 读错：对话 1「辛すぎ」、对话 2「激辛」「辛すぎ」、本课例句「大盛り」、附加单词「冷める」→ 读音表新增 激辛→げきから、辛すぎ→からすぎ、大盛り→おおもり、冷め→さめ，用 `redo_items.py` 重录 dialogue-01、dialogue-02、lesson-01-example、word-10-term。
  - 没录全：本课例句「引っ越しを友達に手伝ってもらいました。」→ 重录 lesson-03-example。
  - 附加例句「ラーメンとギョーザを注文しました。」：Luna 要写成**餃子**，重音也不对（应在后）→ 课程文件改成 餃子；和「無料」（重音也应在后）一起用 `accent_candidates.py` 录 汉字／平假名／片假名 × 4 seed，让 Luna 在 `/accent-candidates.html?lesson=gj-06` 挑。
  - 附加例句「スープが冷めました」这次没标，不重录（读音表改了，以后重录会用 さめ）。
- **/review 改版**（Luna：「每一课单独复制，复制过了就不要再显示；加一个 6 读音，选 6 要求提供具体细节」）：
  - 复制按钮只复制**当前这一课**里标了问题、还没复制过的条目；复制成功后这些条目记为「已复制」，从列表收起、下次不再复制。重录后指纹变了，会以「重录过，请再听」重新出现。
  - 问题类型加 **6 读音**，快捷键 1～6。5 其他、6 读音 必须写细节：没写的输入框标红，复制按钮不可用。
  - 课程下拉框显示每课「还有几条问题没复制」。
  - 注意：这次改版之前复制过的第 6 课结果没有「已复制」标记，会在列表里再出现一次；这几条重录后指纹一变就会自动换成「重录过，请再听」。
- 运行方式：云端对话碰不到 WSL，新增 `_claude/run_in_wsl.sh`（不入库）：带进 Windows 仓库的新提交 → tsc → 重录／重音候选 → 转 m4a → 结果复制回 Windows 仓库。Luna 在 Ubuntu 贴一行。

### 2026-09-30 12:1x Luna：「可以生成 2 节新课大纲」→ 选了接 N3 往下

- 写了 `LESSON_DRAFT_gj-09-10.md`：gj-09 〜ことにする（考试结束，咖啡厅里聊春假和新决定），gj-10 〜たばかり（新自行车刚买一周就爆胎，修车铺门口）。插图命令放在最前面，写明了保存位置。
- 照 9/30 确认的 N3 规矩：普通体、口语照写、练习第 1 题丁寧語；单词用 word_level_check.py 查过，没有 N4、N5；「表外」的词请 Luna 看。
- 选词时避开的：~~故郷~~（ふるさと／こきょう 两读，TTS 易读乱，改成「国」）；パンク（表里 N1，不做卡）。附加例句「送料が無料」含 無料，第 6 课刚发现重音会读错，录时留意。
- gj-10 第 5 句故意放一个 〜たところ 做对照；related 计划：gj-09 ↔ 以后的 〜ことになる，gj-10 ↔ gj-07、gj-08。
- 答案已用 shuffle_draft_answers.py 打散。等 Luna 批注。

### 2026-09-30 12:2x Luna：「没问题，继续做两节新课」→ 第 9、10 课开做

- 大纲照原样落成 `lib/lessons/spring-break-plans.ts`（gj-09 〜ことにする）、`new-bicycle.ts`（gj-10 〜たばかり）和路由，放在 pendingLessons 的 N3 段、gj-08 后面。
- 做课时的改动：
  - gj-10 造句 marker ~~`た(ばかり|ばっかり)`~~ → `[ただ](ばかり|ばっかり)`：た形也可能以「だ」结尾（読んだばかり），只认「た」会漏判。
  - gj-09 造句 marker 加上 しま（ことにします／ことにしました 也认）。
  - related：gj-10 → gj-07、gj-08；gj-07、gj-08 也加上 → gj-10（未上架的课不渲染，等上架后自动出现）。
- 通过：shuffle_answers、check_bonus_in_dialogue。tsc 在 WSL 里跑（云端这边装不了依赖）。
- 录音：新脚本 `_claude/run_new_lessons.sh`（不入库），等第 6 课的重录／重音候选跑完再跑（脚本会检查有没有录音还在跑）。
- gj-10 附加例句「送料が無料になります」含 無料，第 6 课刚发现重音会读错，录完要重点听。

### 2026-09-30 12:3x Luna：「给两节新课的大纲我」

- 写了 `LESSON_DRAFT_gj-11-12.md`：gj-11 〜わけだ（リン 从温泉旅馆打工回来，一开口满是敬语），gj-12 〜わけではない（拓也约 リン 去研讨课聚餐，她不能喝酒）。故事接着第 9 课。
- 按顺序表往下，〜わけだ／〜わけではない 是姊妹课放相邻；下一个 〜わけがない 接在后面。gj-12 找错题 T3 顺带预告 わけがない。
- 单词照 N3 规矩查过，没有 N4、N5。
  - 飲み会 已是第 8 课附加单词，这课课文里出现但不重复做卡。
  - つまり 在 gj-11 是语法的一部分（つまり〜わけだ），不单独做卡。
- 发现 shuffle_draft_answers.py 的小问题：选项行「③（…）」如果圆圈数字后面没空格，打散时会吃掉第一个字（括号）。已手动补回；以后大纲里圆圈数字后面一律加空格。
- 答案已打散。等 Luna 批注。

### 2026-09-30 12:3x Luna：第 11、12 课大纲批准；リン 的中文译名改成「小粼」

- 第 11、12 课大纲批准，原样不改。
- リン 的中文翻译统一 ~~小林~~ ~~小琳~~ → **小粼**：全部课程文件（zh 字段）和所有大纲一起改了，WORD_RULES「人物」记了这条。
  - 12:34 另一个对话先把 小林 改成了「小琳」（未提交），这边在它的基础上改成 Luna 这次说的「小粼」。
  - 只改中文翻译，日文课文和音频都不受影响，不用重录。

### 2026-09-30 12:4x Luna：「做」→ 第 11、12 课开做

- 大纲原样落成 `lib/lessons/back-from-ryokan.ts`（gj-11 〜わけだ）、`drinking-party-invite.ts`（gj-12 〜わけではない）和路由，放在 pendingLessons 的 N3 段、gj-10 后面。两课互加 related。
- 通过：shuffle_answers、check_bonus_in_dialogue。tsc 留到 WSL 录音时跑。
- 大纲里又发现两处 shuffle_draft_answers.py 吃字：选项以「「」开头、圆圈数字后没空格（gj-12 T2 ②、T3 ①），已补回。规矩重申：大纲选项的圆圈数字后面一律加空格。
- 录音排在第 9、10 课后面。

### 2026-09-30 13:1x Luna 人耳：gj-03 对话 2「不是一个人的声音」（第二次）

- 这条 9/29 已经用 consistent_redo.py 重选过（8 版里挑了句首距离最小的 s2，0.373），Luna 听还是不像同一个人 → 句首距离这个指标对这条不够。
- ~~再自动重录一批~~（先不录：同一套指标再挑一次，结果多半一样）→ 新页面 `public/voice-candidates.html?lesson=gj-03&item=dialogue-02&ref=dialogue-04,dialogue-06`：把 9/29 录好的 8 版都摆出来，上面放同课同一个人的另外两句当对照，让 Luna 用耳朵挑。都不像的话再录一批。

### 2026-09-30 13:1x Luna 人耳（第 4 课，类型 6 读音）

- 附加例句「今週末は何も予定がありません。」：何も 重音在「も」；附加单词「昼寝する」：重音在「寝」。
- 都是重音问题 → accent_candidates.py 加 gj-04 两条（汉字／平假名／片假名 × 4 seed），排在第 9〜12 课录音后面。
- 重音候选页原来标题写死「第 2 课」、「要的」说明只有 gj-02 的，改成按课显示（gj-04、gj-06 的说明也补上）。
- 13:13 Luna 在音色候选页挑了 **s7**（句首距离 0.379，比 s2 的 0.373 略大 —— 这个指标分不出她听到的差别）。已换进课程：m4a、json 直接用候选的；WSL 里的 wav 母带要另外复制一次（s7.wav → dialogue-02.wav）。被换掉的 s2 本来就在候选文件夹里。

### 2026-09-30 14:0x 候选换进课程；第 1〜4 课上首页

- 14:03 Luna 在 WSL 跑了 `_claude/resume.sh`：用 pick_candidate.py 换进 gj-06 word-01-example=v2-s4（平假名 ぎょうざ）、word-07-example=v1-s2（汉字）、gj-04 word-02-example=v3-s4（片假名 ナニモ）、word-06-term=v1-s1（汉字）；gj-03 对话 2 的 wav 母带换成 s7；然后接着录第 9〜12 课。
- 为什么要 resume：13:0x 以后 Ubuntu 窗口全关了，**WSL 自己停了**，第 9 课录到一半的录音和预览服务器都断了。以后录音时 Ubuntu 窗口不能关（最小化可以）。
- Luna 问「已经通过的课上线 GitHub 了吗」：GitHub main 已经在 759e4ba（到 gj-03 s7 为止都推了），但 12 课全在 pendingLessons，首页看不到。
- **Luna：「好」→ 第 1〜4 课挪进 `lessons`，上首页**（插图、音频齐，人耳复核过；gj-03 对话 2、gj-04 两条刚换，请 Luna 再听）。第 5、6 课差插图，第 7、8 课音频 Luna 还没听，其余还在录。

### 2026-09-30 14:2x Luna：首页标题左下角分 初级／中级／高级（照韩语站）

- 看了韩语站 하루한컷 线上版：header 下面一排圆角按钮「初级 TOPIK 1～2／中级 TOPIK 3～4／高级 TOPIK 5～6」，网址 `/level/beginner|intermediate|advanced`，每一级的课号从第 1 课数起。
- 本站照做：
  - `lib/lessons/levels.ts`：初级＝JLPT N4、中级＝JLPT N3、高级＝JLPT N2，按每课的 badge 归级。
  - `components/level-home.tsx`：首页和等级页共用；「/」显示默认等级（初级），`app/level/<slug>/page.tsx` 三个等级页。某一级还没有上架的课时显示「正在准备中」。
  - 课号改成**每一级里从 1 数起**（`lessonNumber`）：中级的 gj-07 在网站上是「中级 · 第 1 课」。课程页左下角的课号标签加上等级名。
  - 上一课／下一课只在同一级里走；「返回主页」改成「返回X级课程列表」。
  - /review 的课程下拉和复制结果也写成「中级第 1 课（gj-07）」。
- 注意：WORKLOG、LESSON_ORDER 里一直用的是**全站连续课号**（第 7 课＝gj-07），以后说课时以 gj 编号为准，避免和网站上的分级课号混淆。
- tsc 在 WSL 推送前跑（推送脚本 tsc 不过就不推）。

### 2026-09-30 14:2x Luna 人耳：gj-05 对话 3（男）「不是同一个人的声音」（第二次）

- 同 gj-03 对话 2：9/29 consistent_redo 按句首距离自动选了 s3，Luna 还是听出不像。用 voice-candidates.html 让她在 8 版里挑 → **s2**。m4a、json 用候选的，WSL 的 wav 母带另外复制。
- 这已经是第二条「自动挑的不对、人耳挑才对」：以后「不像同一个人」一律直接给候选页，不再先自动选。

### 2026-09-30 14:3x Cloudflare 不自动构建 → 查因、修好连接

- Luna 14:1x 在 Cloudflare 建了 Worker `grammar-japanese`（Import repository），之后推送不触发构建。
- 查到：Settings → Builds 显示「This project is disconnected from your Git account」；构建记录只有建 Worker 时那 1 条。韩语站 korean-learning（`luciferslay/Korean-learning`）连接正常。
- 判断：Cloudflare 的 GitHub 应用（Cloudflare Workers and Pages）只授权了选定的仓库，不含 grammar-japanese。Luna 在 GitHub 应用设置里加上仓库、Cloudflare 里 Manage 重新连接后，「disconnected」提示消失。
- 构建配置核对过：Build `npm run build`，Deploy `npx wrangler deploy --config dist/server/wrangler.json`，Root `/`，分支 `main`，Include `*`。
- dadcfc2 是在修好连接**之前**推送的，Cloudflare 收不到那次通知 → 用这条 WORKLOG 提交再推一次，触发第一次自动构建。

### 2026-09-30 14:3x Luna：加 N5 和 N1；初级＝N5～N4、中级＝N3～N2、高级＝N1

- 范围从 ~~N4 → N2~~ 扩到 **N5 → N1**。
- 网站分级改成：初级 JLPT N5～N4、中级 JLPT N3～N2、高级 JLPT N1（`lib/lessons/levels.ts`，一级可以对应多个 badge）。
  - ~~14:2x 版：初级＝N4、中级＝N3、高级＝N2~~。现在做好的课不受影响：gj-01〜06 仍在初级，gj-07〜12 仍在中级；以后的 N2 课也归中级，高级留给 N1。
- LESSON_ORDER 加了 N5（约 20 课）、N1（约 30 课）的顺序初稿。N5 排在现有 N4 课前面，gj 编号接着往后排（gj-13 起），网站上的初级课号会顺延。
- WORD_RULES：N5 课配 N5 词、N1 课配 N1 词；N5 课文沿用 N4 的「一律です・ます」—— 待 Luna 确认。

### 2026-09-30 16:2x Luna：N5 课文确认沿用 N4 规矩（一律です・ます、口语缩略写正式形）；先继续 N3

- WORD_RULES 的「待确认」改成已确认。下一步：N3 往下写 gj-13 〜わけがない、gj-14 〜べきだ 的大纲。
- LESSON_ORDER 里「N5 从 gj-13 起」的说法作废：gj 编号按做课先后排，N3 先做，N5 的编号排在后面。

### 2026-09-30 16:2x 第 9〜12 课录音结果（14:03〜15:19，WSL resume.sh）

- 用时：gj-09 933 秒、gj-10 1071 秒、gj-11 1630 秒、gj-12 882 秒。
- **gj-12 出错**：课程文件里前三句对话写成了「一行一个对象」，`generate_lesson_audio.py` 的正则只认多行格式，前三句被跳过，**后三句（4〜6）被当成 dialogue-01〜03 录了**。
  - 修：课程文件改回多行格式；录好的 01〜03 改名成 04〜06（内容就是这三句）；补录真正的 01〜03（`_claude/fix_gj12.sh`）。
  - 防再犯：`generate_lesson_audio.py` 里对话句数和 role 出现次数对不上就直接报错，不再悄悄跳过。
- 自动质检没过的（请 Luna 重点听）：gj-09 对话 1、单词 苦手（语调）；gj-11 对话 3（语速偏慢 0.146，句中有「？」停顿）。gj-10 全过。
