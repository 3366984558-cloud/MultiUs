# MultiUs 交接文档

> 给下一位接手的 AI / 开发者。读完这份文档你应该能不等任何人、直接继续干活。
> 最后更新：2026-08-07 18:0x（**线上已是最新**：bc4b7aa3.multius.pages.dev，curl 逐字节验证；新增——生日/星座输入 + **星座进模拟**（Oscar 拍板：MBTI 基座+星座微调写进 adv 控件，四象加权映射，压测 Δ婚 ≤11.5pp）+ 星座合盘 10 组合池/12 同星座专句 + 生日彩蛋 + 身份证星座印；**拆除乱点鸳鸯谱**（Oscar 拍板不好玩）；顺手修了 permalink boot TDZ——分享链接曾进不了落地页。**本地全部改动尚未 git commit**，备份链到 v24）

---

## 0. 当前最重要的一句话

**线上 https://multius.odin-lab.com 已部署到最新（2026-07-26 凌晨，d9944cee.multius.pages.dev），但本地 working tree 的新功能（MBTI 选择器、引擎平衡、3D 分身舞台、捏分身、跳跃 v3 重设计、墙/结局句/分歧点改版）全都还没 commit——第一件事是 `git add -A && git commit` 把这批落袋。** v10 之后的大件：三任务→MBTI 选择器、动效四件套、14 信物+2 Q 版分身、身份证（Q 版角砖+手写 QR）、分享落地信+角色行、原话复读、第 15 个宇宙「现实宇宙」、彩蛋化反事实、后劲层语料、moment 对话事件锚点、宇宙墙戏分排序、3D 分身对话舞台、捏分身系统（12 发型）、materialize 过渡、跳跃 v3（问句池+真蒙特卡洛蒙太奇+离屏收编，fps 14→56）、宇宙墙 10 真 2 恶搞、OUT_ENDLINE 四句池、worldFork 按宇宙分歧点。拿奖 backlog 在 `.qa/_backlog_win.md`，CLI loop 的进度账在 `.qa/_loop_progress.md`，方向咨询系列在 `.qa/consultN.md`。

---

## 1. 这是什么

**MultiUs** —— AdventureX 2026 黑客松作品，灵感来自《瞬息全宇宙》（Everything Everywhere All at Once）。
输入两个人的名字 + 三个人格参数（依恋类型/吵架风格/金钱观），浏览器端蒙特卡洛模拟 **10,000 个平行宇宙**里这段感情的下场（结婚/仍在交往/分手/冷战/异地五种结局），然后可以走进其中任意一个宇宙看它的完整时间线。

定位句（对外叙事用这个）：
> 「他们模拟是为了帮你找到那个人。我们模拟，是为了让你看懂你们俩。」

- **线上**：https://multius.odin-lab.com （Cloudflare Pages，备用 https://multius.pages.dev）
- **仓库**：https://github.com/3366984558-cloud/MultiUs （公开，main 分支）
- **本地**：`D:\km\MultiUs\MultiUs`（注意末尾没有点）
- **主文件**：`index.html` —— **零依赖单文件，双击 file:// 直接跑，无构建、无 npm、无后端**

## 2. 硬规矩（Oscar 会逐条查）

1. **改 index.html 前必须备份**：`cp index.html index-vN-cn.html`（N 递增，当前已到 v10）。备份不入 git（.gitignore 已排除）
2. **文案红线**：口语、短句、自嘲、冷幽默；禁止排比、禁止鸡汤说教、禁止「震撼/炸裂/惊艳」；每条文案只为它所在的宇宙/场景成立。无厘头≠低幼，梗要有智商
3. **绝不提交/上传**：`multius.local.js`（含 LLM key）、`.qa/`（含 Tripo key + 截图）、`vendor/`、`index-v*-cn.html`
4. **不引入外部依赖**：单文件原则，canvas + CSS 手写。像素角色全部 JS pixel map，不引图片库
5. **emoji 处理**：按码点切（`for..of` / `Array.from`），**绝不** `.split('')`（UTF-16 代理对会碎）
6. **hover 效果**必须包在 `@media (hover:hover)` 里；触控目标 ≥44px；手机端（360px+）零横向溢出是验收线
7. 非破坏性操作直接做，破坏性操作先问

## 3. 当前功能全景（v10）

| 模块 | 说明 |
|---|---|
| 首页 | 双名字输入 + 人格滑杆；WTF 跑马灯（26 条宇宙片段滚动）；「按 J 跳跃」 |
| 跳跃动画 | ~1200 条世界线 canvas 随机游走，五种结局色，收尾五条光带 + 计数 10,000，4.7s；小屏自动降 700 条 |
| 结局统计页 | 大字抽签标题（每结局 13-14 句池，`{pct}` 填真实占比）+ 五结局条 + 12 格宇宙墙（6 真 + 14 抽 6 恶搞） |
| 恶搞宇宙 ×14 | 石头/猫/拖鞋/多肉/贩卖机/路灯/冰箱(蛋+酒)/平行套娃/充电宝/蚊子/电梯广告屏/扫地机器人/耳机/螺蛳粉。每个：专属主题色+水波纹换肤、专属结局统计(合计 10000)、10 条专属时间线、pixel map 角色×2、hero 图、分桶语料（开场 24+中段 16 对+收尾 20，单宇宙 68,544 组合） |
| 开屏对话动画 | 点宇宙先播 640×360 像素场景（亮起三段→idle 微动→打字机对话→水波纹让位时间线），可跳过；规格书在 `.qa/motion_spec.md` + `.qa/motion_spec2.md` |
| 真宇宙时间线 | 90 事件/227 变体（含 16 条低概率离谱事件调味）；有 LLM key 时现场书写（逐条流式、缓存、可重写、坏返回静默回退） |
| 双人 moment | 点时间线任意天，两个分身以当下状态对话（LLM per-turn 或引擎 120 条模板） |
| 宇宙身份证 | 1080×1440 canvas 分享卡（最可能结局/最疯狂瞬间/命运分歧点/水印），toBlob 下载 PNG |
| 其他 | 手机全适配、中英文案（英文原版 `index-en.html`，已冻结不维护）、Web Audio 音效 |

**随机性体系**：种子 = 名字哈希 + Date.now() + 会话轮次（mulberry32），会话内组合签名去重。LLM 是加分项不是主路径——主办方网络下常连不上，语料库必须独立成立。

## 4. 密钥与外部服务（都在 git 之外）

| 服务 | 位置 | 说明 |
|---|---|---|
| LLM（主办方 openai-next） | `multius.local.js`（.gitignore） | endpoint `https://api.openai-next.com/v1`，首选模型 `qwen3-max`（1.8s）；备选 `deepseek-v4-flash`、`claude-sonnet-4-5-20250929`。653 模型但多半残的，**每次用新模型前必须实测**。文档 https://credits.openai-next.com/zh/guide/quickstart |
| Gemini（Oscar 备用） | key 在 `D:\claude\ONBOARDING.md` §14 | 本机直连 Google 不通（DNS 污染），需代理；`multius.local.js` 注释里有完整备用配置 |
| Tripo 3D | key 在 `.qa/tripo_key.txt` | base `https://api.tripo3d.com/v2/openapi`（**.com 不是 .ai**，.ai 不通）。余额 3000 分（2026-07-24 查）。**还没接进项目，见 §6 路线图** |
| Cloudflare | `C:\Users\Oscar\.cloudflare-config`（CF_TOKEN/CF_ACCOUNT/CF_ZONE，source 加载，绝不打印） | Pages 项目 `multius`，已绑 `multius.odin-lab.com` |

**claude-fable-5 在主办方 token 下 503**（计费组没渠道），动效/产品顾问用 `claude-sonnet-4-5-20250929` 代替，已有两轮咨询成果在 `.qa/motion_spec*.md` 和 `.qa/review.md`。

## 5. 工作流（都趟过坑，照抄）

### 部署（Cloudflare Pages）
```bash
DEST="/c/Users/Oscar/Documents/kimi/workspace/_deploy-staging/multius"
rm -rf "$DEST" && mkdir -p "$DEST" && cp -r ./* "$DEST/"
rm -rf "$DEST/multius.local.js" "$DEST/vendor" "$DEST/_gen" "$DEST/.qa" "$DEST/media"
rm -f "$DEST"/index-v*-cn.html "$DEST/.gitignore"
source /c/Users/Oscar/.cloudflare-config
export CLOUDFLARE_API_TOKEN="$CF_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT"
export NODE_OPTIONS="--dns-result-order=ipv4first"   # 关键！否则 node fetch 连不上 CF
cd "$DEST" && "/c/PROGRA~1/nodejs/npx.cmd" wrangler@latest pages deploy . \
  --project-name=multius --branch=main --commit-message="ASCII only" --commit-dirty=true
```
- 域名绑定已做好，不用重复绑；`--branch=main` 必须带
- **禁止** `--project-name=odin-lab`（主站封箱）
- curl 调 CF API 一律加 `--ssl-no-revoke`
- 缓存坑：重新部署后等 1-2 分钟或加 `?v=N` 验证
- **`media/`（Oscar 的 9GB 原始素材，2026-08 出现）必须 rm**，否则撞 CF Pages 单文件 25MiB 上限部署失败（2026-08-07 实测踩过）
- **npx 路径带空格会炸**（'C:\Program' 不是命令）：必须用 8.3 短路径 `/c/PROGRA~1/nodejs/npx.cmd`，别用 `$(dirname $(which node))`

### Git 推送（github.com 常被 DNS 污染）
先正常 push；不通就走 REST API 绕道：`printf "protocol=https\nhost=github.com\n\n" | git credential fill` 取 token → blob→tree→commit→ref 逐步 POST。注意 API 提交只存 UTC 时间戳，远端 sha 与本地不同但 tree 一致时，`git fetch && git reset --hard origin/main` 无损对齐。

### 验证（无 WebBridge，用 headless Chrome + Node CDP）
- 现成脚本参考 `.qa/_cdp_v10.mjs`（agent 自建的 CDP 驱动，截图+console 采集+设备模拟）
- `node --check` 检查三个 script 块；验收底线：console 零报错、手机 390×844 无横向溢出
- shell 里中文 prompt 必须用文件 `--data-binary @file.json` 发送（命令行内联中文会被 GBK 搞坏，返回答非所问）

## 6. 路线图（按优先级）

1. ~~**宇宙信物（Tripo 3D）**~~ ✅ 素材全齐（2026-07-25，CLI loop）：14 信物 + 2 Q 版主角（`assets/keepsakes/` + `render/`，216K–2.4M），model-viewer UMD 在 `assets/lib/`，全图鉴/双人原型页已验。**剩接入主站 + 印上身份证**（等验收窗口，方案 `.qa/_keepsake_integration.md`；关键坑：file:// 禁 fetch，GLB 只能外链+静态图降级；model-viewer 用 v3 UMD 不是 v4 ESM；Tripo 模型正面在 azimuth 270°）。
2. ~~**`.qa/review.md`（Fable 评审）剩余项**~~ ✅ 全部完成（爆炸开场/震屏/时间线图标/CRT/UNIVERSE #消散，已上线）。
3. **二轮评审（`.qa/review2.md`）落袋**：反事实已藏彩蛋 ✅、扎心后劲层 ✅、DEMO 改闪现+扫码 CTA ✅；剩「QR 上结果页/身份证」（生成器已验证 `qr-proto.html`，等窗口）。
4. **loop 定时任务**：Kimi Work 侧（`automation_69de7ef0…`，30 分钟）+ **Kimi Code CLI 侧（cron，5 分钟，领 `.qa/_backlog_win.md` 的活，北极星=拿奖）**。两边都可能动 index.html——动手前先 `git status` + 看 mtime，别人在改就等窗口；半成品不许碰。

## 7. 文件地图

```
index.html            主文件（中文版，全部功能）
index-en.html         英文原版（冻结）
index-vN-cn.html      备份链（N≤15，gitignored）
multius.local.js      本地 LLM 默认配置（gitignored，含 key）
assets/worlds/        22 张 hero 图（结局场景 10 + 恶搞宇宙 14，1536×864 jpg）
assets/chars/         LPC 像素小人（oscar/mira + 头像）
assets/keepsakes/     14 信物 + 2 Q 版主角的 web GLB（216K–2.4M）；render/ 静态渲染图 ×16
assets/lib/           model-viewer UMD（v3，910K，file:// 可用；v4 ESM 不行）
tools/lpc_build.py    LPC 捏人管线（vendor/lpc 是素材源，不入 git）
keepsakes-gallery.html 全图鉴（16 模型内联，18MB 单文件）
avatars-proto.html    双人 3D 分身原型页
keepsake-proto.html   单信物原型页（石头）
qr-proto.html         手写零依赖 QR 生成器（已 OpenCV 实证）
watch-proto*.html     8bit 对话原型页（已并入主站，仅存档）
char-preview.html     角色预览页
adventurex-2026-*.md  黑客松指南全文 + 赛道分析（主题选 D 万花筒，赛道 03+21）
CHANGELOG.md          版本记录
DEMO.md               3 分钟演示逐秒脚本（2026-07-25 版）
VISION.md             产品为什么（Oscar 原话+共识），改文案前先读
requirements-review.md Oscar 新需求背景（Kimi Work 整理）
.qa/                  QA 截图/CDP 脚本/LLM 咨询文档/Tripo key（gitignored）
  _backlog_win.md       拿奖 backlog（loop 领活队列，<3 项必须补）
  _loop_progress.md     CLI loop 进度账（含所有坑：Tripo 参数/CDP/编码等）
  _keepsake_integration.md 信物+身份证接入方案（验收窗口照做）
  review.md / review2.md 两轮 LLM 评审（Fable 视角 + sonnet 毒舌）
_gen/                 生图工作目录 + keepsakes-raw/（176MB 原始 GLB）+ gltf/（压缩工具链）
```

## 8. 给接手者的第一句话

先 `cp index.html index-v16-cn.html`，然后跑一遍线上 https://multius.odin-lab.com 感受当前状态——世界线跳跃、点开石头宇宙看开屏对话、最后生成一张宇宙身份证。注意**线上落后本地 13 个 commit**：本地的新鲜玩意看这三个页面就够了——`keepsakes-gallery.html`（人+信物全图鉴）、`qr-proto.html`（扫码玩第二遍）、DEMO.md（3 分钟怎么演）。你要改的所有东西，最终都要过这三关：文案不像 AI 写的、手机上是顺的、file:// 双击能跑。
