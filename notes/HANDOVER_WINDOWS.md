# 交接：日语语法站「一日一コマ」搬到 Windows 电脑跑音频（2026-09-28）

> 给在 **ROG Zephyrus G14（Windows，RTX 4070 8GB，32GB）** 上新开的 Claude 对话看。先读完这份，再读同目录的
> `WORKLOG.md`（完整工作日志）、`LESSON_ORDER.md`（课程顺序表）、`WORD_RULES.md`、`LESSON_DRAFT_gj-01-02.md`。
> 这些文件原件在 Mac 的 `~/Developer/nihongo/grammar/`，这里是 2026-09-28 17:2x 的副本。以后**以仓库里的 notes/ 为准**，两台电脑都通过 git 同步。

## 为什么搬
- Mac 上韩语站和日语站共用一个音频队列（共用锁），模型只能跑 CPU，一条几分钟、两站互相排队。
- 这台有 RTX 4070：Qwen3-TTS 1.7B 用 GPU 跑应该快好几倍。**日语音频以后在这台跑，韩语站继续留在 Mac。**

## Luna 已经做好的
1. 装了 Claude 桌面 App（同一账号，项目「日语」）
2. `wsl --install` 装好 WSL2 并重启
3. 更新了 NVIDIA 驱动

## 新电脑上要做的（Claude 负责，Luna 只在需要时点确认）
1. **先确认 Claude App 在 Windows 上能不能操作文件夹 / 跑命令**（这是最大的未知数，不行就马上告诉 Luna）。
2. WSL2（Ubuntu）里：`nvidia-smi` 确认能看到 4070；装 `git`、`ffmpeg`、`uv`、Node 22+。
3. `git clone https://github.com/luciferslay/grammar-japanese.git`（建议放 WSL 里的 `~/nihongo/grammar-japanese`，别放 /mnt/c，速度差很多）；`npm install`。
4. 下载模型到 HuggingFace 缓存：`Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`（Ono_Anna 用）、`Qwen/Qwen3-TTS-12Hz-1.7B-Base`（男声克隆用，revision 见 `audio_voice_presets.json`）、以及脚本用到的 whisper（ASR 闸门）。脚本都是 `local_files_only=True`，必须先下好。
5. 改脚本用 GPU：`scripts/generate_lesson_audio.py` 的 `load_model` 和 `scripts/standardized_course_tts.py` 的 `generate` 里 `device_map="cpu", dtype=torch.float32` → 有 CUDA 时用 `"cuda"` + `torch.bfloat16`（保留 CPU 回退，Mac 上还要能跑）。先录一课测速度，报告给 Luna。
6. 音频队列：Mac 上是 `scripts/audio_worker.sh`（zsh + launchd + caffeinate + 两站共用锁）。WSL 里改成一个常驻循环（systemd 用户服务或开机脚本），**不用共用锁**（这台只跑日语）。防睡眠：请 Luna 在 Windows 电源设置里设「插电时不睡眠」。
7. 本地预览：`npm run dev`（端口 3200）；手机同 Wi-Fi 看要用 Windows 的局域网 IP（WSL2 需要端口转发或开 mirrored 网络）。
8. GitHub 推送：确认这台能不能 push（Mac 那边的 Claude 推不了，一直是 Luna 手动推）。

## 当前状态（2026-09-28 17:2x）
- 第 1、2 课（gj-01 〜たことがある、gj-02 〜てもいい／てはいけない）课程文件、插图已入库；还在 pendingLessons，没上首页。
- 音频：对话 + 本课单词已生成并入库（m4a）。**附加单词**原来因为脚本正则 bug 被跳过，已修；第 1 课用旧女声补录了 24 条（未入库），第 2 课没录 —— **女声可能要换，所以暂停**（Mac 上 `audio-jobs/STOP` 急停文件存在）。
- **女声问题**：原女声 FEMALE_CLEAR_SOFT 是「声线设计生成的样音再克隆」，每句音色漂移，Luna 人耳听出第 1 课 見せる、こんなに、对话 4 声音不一样。
  - 候选：Qwen3-TTS 内置日语女声 **Ono_Anna**（CustomVoice，和韩语站 Sohee 同类，稳定）。
  - 第一版试听：Luna 说「稳定，但语气过于夸张、前后有杂音/气声」。
  - 第二版（`scripts/voice_samples_ono_anna_v2.py`）：指示语改成原女声的平稳读法、对话温度 0.9→0.6、走正式流水线切气声。**正在 Mac 上排队**（排在韩语第 41 课后面；韩语第 42 课的 job 暂时改名为 `custom-42.job.hold-for-ja-samples`，Mac 那边的 Claude 录完会改回来）。对比页 `public/samples-ono-anna.html`。
  - **等 Luna 听完第二版拍板**。拍板用 Ono_Anna 的话：写进 `audio_voice_presets.json` 的正式 voices（替换 FEMALE_CLEAR_SOFT 的 role B + card_voice），第 1、2 课所有女声条目（对话 B + 全部单词卡）重录。
- 读音表 `tts_readings.json` 新增 函館→はこだて；对话 4、5 要重录。
- Cloudflare：代码已准备好（没配数据库时会员功能自动关闭）；等 Luna 在 Cloudflare 后台 Import repository（步骤见 WORKLOG 末尾）。
- 定时报告：每天 09:00 / 21:00 JST；Luna 打算开两个固定对话接收（prompt 已给她）。报告读的是 Mac 上的文件夹，**搬家后要把报告改成读这台 Windows / 或读 GitHub 仓库**。

## 规矩（沿用韩语站，别破）
- Claude 自己写的标题、栏名、说明一律中文；日文只用于课文、语法点。
- 所有决定和被否决的方案都记 WORKLOG，否决的划掉保留、不删。
- 音频只用固定声线，不用浏览器 TTS；每条都要过自动质检，Luna 人耳复核（/review 页）。
- N4 课文全部用です・ます，口语缩略写成正式形。
