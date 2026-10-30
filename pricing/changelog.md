# LLM API 价格变更日志

## 2026-10-31（每日核对）
- 重新核对 30 行基线模型现价，全部官方一手源：platform.openai.com/docs/pricing + openai.com/api/pricing、platform.claude.com/docs/en/about-claude/pricing、ai.google.dev/gemini-api/docs/pricing（页面 Last updated 2026-10-28 UTC）、api-docs.deepseek.com/quick_start/pricing（curl 直取 PRICING 表）、docs.mistral.ai/inference/pricing、OpenRouter /api/v1/models（curl JSON）、help.aliyun.com/zh/model-studio/model-pricing。**一手官方价与 10-30 基线完全一致，零变动。**
- ⚠️ **Qwen3-Max 从阿里百炼官方价目表消失**（10-31 核对发现）：help.aliyun.com 千问Max 分区现仅列 qwen3.8-max / qwen3.7-max（均 ¥12/¥36，1M ctx）与 qwen-max（¥2.4/¥9.6），qwen3-max 已无条目，疑似退役并由 qwen3.8-max 接替（第三方站 pricemon 仍挂 ¥2.5/¥10 旧快照，10-10 验证）。看板已标注，价格保留为移除前记录。
- ✅ 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（官方明示至少至 11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30，12-01 起 $4/$20）、Gemini 3.8 Flash $0.75/$3.75（至 12-31）。
- ⏰ **DeepSeek Search/Fetch 免费期今日（10-31）最后一天**：官方页确认 11-01 北京时间 00:00 起 $0.75/千次（Harness/Claude Code/Codex 内服务端调用同样开始计费）。
- 近 7 天新闻扫描（llmprices.net 每日变更页 10-30 快照、tensorust、tokencost.app、huggingface 讨论区价格数据集等）：无新的主流模型官方降价 ≥20%、无新免费层、无新限时折扣。llmprices 记录的 26 项变动几乎全为 OpenRouter 路由渠道价（Kimi K3 输出 $20→$10.8 -46%、Qwen3.8-27B 缓存 -44%、GLM 4.6 -9.1% 等，均为聚合器内最低价路由切换），Mistral Large 4 三行 -50% 即 10-29 官方永久降价的渠道端反映（已于当日收录）。tensorust 的 "OpenAI 80% price cut" 文章为对 GPT-6 系降价历史的回顾分析，非新事件。

# 价格变动日志

## 2026-10-30（每日核对）⚡ 有重大变动
- 🔽 **Mistral Large 4 官方永久降价 ~50%（2026-10-29，触发快报）**：$1.36/$4.18 → **$0.70/$2.10**（缓存输入 $0.14→$0.07），一手源 docs.mistral.ai/inference/pricing 今日核实已生效。背景：10-29 Mistral 正式发布 Large 4 开源权重（"Le Chonk"，1T 总参 / 49B 激活 MoE，Mistral Ecosystem Open-Weight 许可 ≈ 修改版 MIT，MaaS 厂商需另购商业许可），同日官方将 API 定价腰斩为**新的永久标准价**（非限时促销）。Artificial Analysis 测得每 Intelligence Index 任务成本 $2.06，较 preview 的 $5.54 降 63%。注意时间线：10-06 发布 5 折促销（$0.68/$2.09）→ 10-20/24 促销结束恢复原价（+100%）→ 10-29 直接以约等于促销价的水平定为永久价。上下文窗口按 LiteLLM/HF 模型卡为 1M（此前板上记 256K，已更正）。
- ℹ️ **GPT-6.1 Terra 已列入 OpenAI 官方定价页**（10-28 时仅 OpenRouter 有）：$1/$5（短ctx ≤272K；长ctx $2/$7.50，缓存输入 $0.05），与 OpenRouter 价一致；板上厂商标注由 "OpenAI (OpenRouter)" 改为 "OpenAI"。
- 重新核对全部 33 行基线模型现价（platform.openai.com/docs/pricing.md、platform.claude.com/docs pricing、ai.google.dev/gemini-api/docs/pricing HTML 全解析、api-docs.deepseek.com pricing、docs.mistral.ai/inference/pricing、OpenRouter /api/v1/models、阿里百炼 help.aliyun.com + developer.aliyun.com 汇总）：除上述两项外**与 10-28 基线完全一致**。OpenAI 全系（Astra $10/$50、6.1 Sol $2/$10、Luna $0.10/$0.50、5.6 Sol 促销 $4/$20、5.6 Terra $2/$12、5.6 Luna $0.20/$1.20、5.3 Codex $1.75/$14）、Anthropic 全系（Fable 5.1 $10/$50、Opus 5.5 $4/$20、Sonnet 5.5 $2/$10、Haiku 5.5 $0.10/$0.50、legacy）、Google（Argon 首发 $2/$10 至 11-30、3.8 Flash $0.75/$3.75 至 12-31、3.1 Pro Preview $2/$12、3.5 Flash-Lite $0.30/$2.50）、DeepSeek（Flash 闲时 $0.15/$0.60、V4 Pro 闲时 $0.66/$1.98；Search/Fetch 免费⚠️仅剩 2 天，11-01 北京时间起 $0.75/千次）、Qwen（¥2.5/¥10、¥0.8/¥4.8、¥0.5/¥2）、Llama（3.3 70B $0.10/$0.32、4 Scout $0.10/$0.30、4 Maverick $0.1875/$0.6525）、Mistral 其余型号（Medium 3.5、Large 3、Small 4、Ministral 3、GLM 5.3 系）均无变化。
- 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（官方页明示至少至 2026-11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30，12-01 起 $4/$20）、Gemini 3.8 Flash $0.75/$3.75（至 12-31，2027 起翻倍）。
- 近 7 天新闻扫描（apicostcheck 价格变动日志、usagepricing、litellm、VentureBeat、web_search）：apicostcheck 官方页追踪 10-23 以来唯一新变动即 Mistral Large 4 三项 -48.5%/-49.8%/-50%（10-29）；无其他主流模型官方降价 ≥20%、无新免费层、无新限时折扣。渠道/非基线波动（DeepSeek V4 Flash 百度渠道等）此前已记录，不触发快报。

## 2026-10-28（每日核对）
- 重新核对 30 行基线模型现价，全部官方一手源：platform.openai.com/docs/pricing、docs.claude.com/en/docs/about-claude/pricing、ai.google.dev/gemini-api/docs/pricing、api-docs.deepseek.com/quick_start/pricing、docs.mistral.ai/inference/pricing、OpenRouter /api/v1/models、阿里百炼（help.aliyun.com qwen3-max 模型页 + developer.aliyun.com 汇总：qwen3-max ¥2.5/¥10、qwen3.5-plus ¥0.8/¥4.8、qwen-long ¥0.5/¥2）。**基线模型与 10-27 完全一致，零价格变动。**
- 🆕 **GPT-6.1 Terra / Terra Pro 上架 OpenRouter**（10-27，AIMap/OpenRouter API 双源确认）：$1/$5 per M（1.05M ctx），Batch 半价 $0.50/$2.50；已补入看板（OpenAI 官方定价页暂未单列，以 OpenRouter 价为准）。
- 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（官方页明示至少至 2026-11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30，12-01 起 $4/$20，官方页今日再确认）、Gemini 3.8 Flash $0.75/$3.75（至 12-31，2027 起 $1.50/$7.50）、DeepSeek Search/Fetch 免费（⚠️ 仅剩 4 天：11-01 北京时间 00:00 起 $0.75/千次，官方 pricing 页确认）。
- ℹ️ Anthropic Batch 表今日确认：Fable 5.1 $5/$25、Opus 5.5 $2/$10、Sonnet 5.5 $1/$5、Haiku 5.5 $0.05/$0.25（≤100K），均与基线一致；缓存写/读价格无变化。
- 近 7 天新闻扫描（SF·SIX 543 cuts/416 increases、LLM Cost Index、apipriceindex、AIMap、Yahoo/AWS 旧闻）：本周最大降幅集中在渠道/非基线模型——DeepSeek V4 Flash 0731 在百度渠道输出 $1.32→$0.133（-90%）、GLM 5.3 在 Reka 输出 -50%、腾讯云 Hy3 -37.5%、阿里云托管 DeepSeek V4.1 Flash -50%（10-27）等，均为聚合渠道价，非本板基线一手价，不触发快报。无新的主流模型官方降价 ≥20%、无新免费层、无新限时折扣。
- LLM Cost Index 新上架（非基线，仅记录）：Kimi K3.1 Pro $2/$10、MiniMax M3.1 Flash $0.15/$0.60、LFM2.5-2.6B $0.35/$0.50。

## 2026-10-27（每日核对）
- 重新核对 30 行模型现价，全部官方一手源：platform.openai.com/docs/pricing（.md 版）、docs.claude.com/en/docs/about-claude/pricing、ai.google.dev/gemini-api/docs/pricing（HTML 全文解析）、api-docs.deepseek.com/quick_start/pricing、docs.mistral.ai/inference/pricing、OpenRouter /api/v1/models、阿里百炼（经 pricemon/dayuyun 等汇总交叉核对 qwen3-max ¥2.5/¥10、qwen3.5-plus ¥0.8/¥4.8、qwen-long ¥0.5/¥2 无调价公告）。**与 10-26 基线完全一致，零变动。**
- 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（官方页明示至少至 2026-11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30，12-01 起 $4/$20）、Gemini 3.8 Flash $0.75/$3.75（至 12-31）、DeepSeek Search/Fetch 免费（⚠️ 仅剩 5 天：11-01 北京时间 00:00 起 $0.75/千次）。
- ℹ️ Anthropic 定价页观察到新条目（非基线模型，仅记录）：Claude Mythos 5.1 / Mythos 5（$10/$50，缓存读 0.025x）；新增 "Claude Managed Agents" 计费——会话运行时 $0.08/会话小时（按 running 状态毫秒级计量，idle 不计费），且 Managed Agents 会话不适用 Batch 折扣。
- ℹ️ OpenAI 定价页 gpt-5.6-cyber（$12.50/$75）与 gpt-rosalind（$5/$25）条目仍在，无变化。
- 近 7 天新闻扫描（tokenbarometer/sovyron/aitokenprice/stackspend 等追踪站 + 关键词检索）：无新的主流模型官方降价 ≥20%、无新免费层、无新限时折扣。检索到的 "OpenAI/Anthropic slash prices up to 80%" 类文章（lavx.hu 10-26、emergent.sh 10-26）均为对 6-10 月既有降价（GPT-5.6 Luna -80%、GPT-6 系 -50%、Opus 5.5 -20%）的回顾汇编，非新事件，已反映在本板基线中。追踪站近 7 天记录的变动（kimi-k3 wafer 输出 -14%、qwen3-6-27b chutes 输入 -17%、titan-text-lite bedrock -50% 等）均为渠道/非基线模型，不触发快报。

## 2026-10-26（每日核对）
- 重新核对 30 行模型现价，全部来自官方一手源：platform.openai.com/docs/pricing、claude.com/pricing、ai.google.dev/gemini-api/docs/pricing、api-docs.deepseek.com/quick_start/pricing、docs.mistral.ai/inference/pricing、OpenRouter /api/v1/models、help.aliyun.com（qwen3-max 输入 ≤32K ¥2.5/M 经官方模型页快照确认；qwen3.5-plus ¥0.8/¥4.8、qwen-long 无调价公告）。**与 10-25 基线完全一致，零变动。**
- 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（官方页明示至少至 2026-11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30，12-01 起 $4/$20）、Gemini 3.8 Flash $0.75/$3.75（至 12-31）、DeepSeek Search/Fetch 免费（至 11-01 北京时间 00:00 / 10-31 16:00 UTC 起 $0.75/千次）。
- 近 7 天新闻扫描（benchlm/thedecoded/aitokenprice/computeprices 等追踪站）：无新的主流模型官方降价 ≥20%、无新免费层、无新限时折扣。追踪站记录的近期变动（DeepSeek V4 Flash 0423 -68%、GLM 5.1 +37.7%，均 10-13）为渠道/旧快照价，非本板基线一手价，此前已收录或不适用。
- ℹ️ OpenAI 定价页观察到新条目（非基线模型，仅记录）：gpt-5.6-cyber（$12.50/$75，"Cyber models" 分类）与 gpt-rosalind-research/discovery（$5/$25，生命科学受限访问，10-05 起计费）。另 OpenAI 10-23 已在 API 关停 o1 与 gpt-4o 初版快照（不在板内）。
- ℹ️ Google Gemini API 免费层收缩已于 10-09 生效（免费用户仅 Flash Lite，Flash/Pro 需 Google AI Plus $4.99/月订阅）——超 7 天窗口且此前已反映，仅备忘。

## 2026-10-25（每日核对）
- 重新核对 30 行模型现价（OpenAI 官方定价页+platform 定价表、docs.claude.com、ai.google.dev、api-docs.deepseek.com、docs.mistral.ai、OpenRouter API、阿里云百炼经 developer.aliyun.com 汇总）：**全部与 10-24 基线一致，零变动**。Qwen 三行今日已重新核对（Qwen3-Max ¥2.5/¥10、Qwen3.5-Plus ¥0.8/¥4.8、Qwen-Long ¥0.5/¥2 不变）。
- 在途优惠核实仍有效：GPT-5.6 Sol 促销 $4/$20（至少至 11-21）、Gemini 4 Argon 首发价 $2/$10（至 11-30）、Gemini 3.8 Flash $0.75/$3.75（至 12-31）、DeepSeek Search/Fetch 免费（至 11-01 北京时间）。
- 近 7 天新闻扫描（第三方追踪 SF·SIX/ModelBank/Sovyron/apipriceindex）：官方一手价无新变动；渠道/聚合价波动大——阿里云托管 DeepSeek V4 Flash 0731 回落 50%（$0.352/$1.06→$0.176/$0.528，10-24），百度渠道 DeepSeek V4 Pro/Flash、GLM 5.2 折扣低至 1-2 折（限时渠道价）。均非本板基线模型的一手官方价，不触发快报。
- 未发现主流模型官方降价 ≥20%、新免费层或新限时折扣。

## 2026-10-24（每日核对）
- 重新核对 29 个模型现价：OpenAI（gpt-6 全系/5.6 系/5.3 Codex）、Anthropic（Fable 5.1/Opus 5.5/Sonnet 5.5/Haiku 5.5 及 legacy）、Google（Argon/3.8 Flash/3.1 Pro/3.5 Flash-Lite）、DeepSeek（Flash/V4 Pro）、Mistral 全系、Llama（OpenRouter）——除下列变动外均与 10-23 基线一致。Qwen 百炼行今日未重新核对（沿用 10-23）。
- 🔺 **Mistral Large 4 促销结束**：$0.68/$2.09（发布 5 折）→ 恢复原价 $1.36/$4.18（对促销用户等效 +100%）。来源：docs.mistral.ai/inference/pricing。
- 🆕 Mistral La Plateforme 新上架 **Z.ai GLM 5.3**（$1.4/$4.4）与 **GLM 5.3 Flash**（$0.15/$0.5）。
- 在途优惠核实：GPT-5.6 Sol 促销（至少至 11-21）、Gemini 4 Argon 首发价（至 11-30）、Gemini 3.8 Flash 限时价（至 12-31）、DeepSeek Search/Fetch 免费（至 11-01 北京时间）均仍有效。
- 近 7 天新闻扫描：未发现主流模型新的降价 ≥20%、新免费层或新限时折扣（10-07 Claude Sonnet 5.5 缓存读 $0.20→$0.10、10-14 Google/Anthropic 缓存读降至 0.05x 均已超 7 天窗口，此前已收录或已反映在基线中）。

## 2026-10-23（首次建板）
- 建立价格看板，采集 29 个代表模型（OpenAI/Anthropic/Google/DeepSeek/Qwen/Mistral/Llama）。
- 记录在途限时优惠：Gemini 4 Argon 首发价（至 11-30）、Gemini 3.8 Flash（至 12-31）、GPT-5.6 Sol 促销（至 11-21）、Mistral Large 4 发布 5 折、DeepSeek Search/Fetch 免费（至 11-01）。
- 近 7 天变动（第三方追踪，非本板基线对比）：
  - 🔺 阿里云 DeepSeek V4 Flash 0731：输出 $0.40→$1.32/M（约 10-20，来源 Stork AI/Forbes 转述）。
  - 🔽 GLM-5-3（wafer）：输出 $7.00→$4.80/M（-31%，10-10，Token Barometer）。
