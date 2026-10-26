# 价格变动日志

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
