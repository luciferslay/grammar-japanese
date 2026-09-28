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
