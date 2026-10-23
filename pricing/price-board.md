# LLM API 价格看板

> 首次采集：2026-10-23；最近核对：2026-10-24（自动监控，每日更新）。单位：USD / 1M tokens（Qwen 为 CNY，已注明）。
> 来源：openai.com/api/pricing、platform.openai.com/docs/pricing、claude.com/pricing、ai.google.dev/gemini-api/docs/pricing、api-docs.deepseek.com、docs.mistral.ai/inference/pricing、openrouter.ai、help.aliyun.com（百炼，经 developer.aliyun.com 汇总核对）。
> 变动标记：🔺涨价 / 🔽降价 + 日期。

## 价格总表

| 模型 | 厂商 | 输入价/M | 输出价/M | 上下文 | 最后更新 | 备注 |
|---|---|---|---|---|---|---|
| GPT-6 Astra | OpenAI | $10.00 | $50.00 | 短ctx；长ctx $20/$75 | 2026-10-24 | 缓存输入 $1.00；旗舰 |
| GPT-6.1 Sol | OpenAI | $2.00 | $10.00 | 短ctx；长ctx $4/$15 | 2026-10-24 | 缓存输入 $0.10 |
| GPT-6 Luna | OpenAI | $0.10 | $0.50 | 短ctx；长ctx $0.20/$0.75 | 2026-10-24 | 缓存输入 $0.01；最低价大模型之一 |
| GPT-5.6 Sol | OpenAI | $4.00（促销） | $20.00（促销） | 270K | 2026-10-24 | 原价 $5/$30；促销至少至 2026-11-21 |
| GPT-5.6 Terra | OpenAI | $2.00 | $12.00 | 270K | 2026-10-24 | 缓存输入 $0.20 |
| GPT-5.6 Luna | OpenAI | $0.20 | $1.20 | 270K | 2026-10-24 | 缓存输入 $0.02 |
| GPT-5.3 Codex | OpenAI | $1.75 | $14.00 | — | 2026-10-24 | 代码专用 |
| Claude Fable 5.1 | Anthropic | $10.00 | $50.00 | 1M | 2026-10-24 | 缓存读 $0.25 / 写 $12.50；长程 agent 旗舰 |
| Claude Opus 5.5 | Anthropic | $4.00 | $20.00 | 1M | 2026-10-24 | 较 Opus 5 ($5/$25) 便宜 20%；Fast 模式 2x 价 |
| Claude Sonnet 5.5 | Anthropic | $2.00 | $10.00 | 1M | 2026-10-24 | 缓存读 $0.10；9/1 原定涨至 $3/$15 已取消 |
| Claude Haiku 5.5 | Anthropic | $0.10 | $0.50 | 1M | 2026-10-24 | >100K 提示词时 $0.50/$2.50 |
| Claude Sonnet 5（legacy） | Anthropic | $2.00 | $10.00 | 1M | 2026-10-24 | 旧代 |
| Claude Opus 5（legacy） | Anthropic | $5.00 | $25.00 | 1M | 2026-10-24 | 旧代 |
| Gemini 4 Argon | Google | $2.00 ⏳ | $10.00 ⏳ | 1M | 2026-10-24 | 限时首发价至 2026-11-30；12-01 起翻倍为 $4/$20 |
| Gemini 3.8 Flash | Google | $0.75 ⏳ | $3.75 ⏳ | 1M | 2026-10-24 | 限时价至 2026-12-31；2027-01-01 起 $1.50/$7.50 |
| Gemini 3.1 Pro Preview | Google | $2.00 | $12.00 | ≤200K；>200K $4/$18 | 2026-10-24 | Batch 半价 $1/$6 |
| Gemini 3.5 Flash-Lite | Google | $0.30 | $2.50 | 1M | 2026-10-24 | 有免费层；Batch $0.15/$1.25 |
| DeepSeek Flash (V4.1) | DeepSeek | $0.15（闲时） | $0.60（闲时） | 1M | 2026-10-24 | 忙时 $0.30/$1.20；缓存命中低至 $0.003 |
| DeepSeek V4 Pro | DeepSeek | $0.66（闲时） | $1.98（闲时） | 1M | 2026-10-24 | 忙时 $1.32/$3.96；缓存命中 $0.022 |
| Qwen3-Max | 阿里百炼 | ¥2.5 | ¥10 | 252K | 2026-10-23 | 32K 内价；32-128K ¥4/¥16；128-252K ¥7/¥28；Batch 5 折 |
| Qwen3.5-Plus | 阿里百炼 | ¥0.8 | ¥4.8 | 1M | 2026-10-23 | 128K 内价；128-256K ¥2/¥12；256K-1M ¥4/¥24 |
| Qwen-Long | 阿里百炼 | ¥0.5 | ¥2 | 10M | 2026-10-23 | Batch 5 折 |
| Mistral Large 4 | Mistral | 🔺 $1.36（2026-10-24，促销结束恢复原价） | 🔺 $4.18 | 256K | 2026-10-24 | 10-06 起限时 5 折（$0.68/$2.09）已结束，官方定价页恢复标准价；缓存输入 $0.14 |
| Mistral Medium 3.5 | Mistral | $1.50 | $7.50 | 256K | 2026-10-24 | 缓存输入 9 折省（$0.15）；Batch 半价 |
| Mistral Large 3 | Mistral | $0.50 | $1.50 | 256K | 2026-10-24 | 缓存输入 $0.05 |
| Mistral Small 4 | Mistral | $0.15 | $0.60 | 256K | 2026-10-24 | 缓存输入 $0.015 |
| Ministral 3 8B | Mistral | $0.15 | $0.15 | 262K | 2026-10-24 | 输入输出同价 |
| Z.ai GLM 5.3（Mistral 平台） | Z.ai/Mistral | $1.40 | $4.40 | — | 2026-10-24 | 🆕 新上架 La Plateforme；缓存输入 $0.14 |
| Z.ai GLM 5.3 Flash（Mistral 平台） | Z.ai/Mistral | $0.15 | $0.50 | — | 2026-10-24 | 🆕 新上架；缓存输入 $0.03 |
| Llama 3.3 70B Instruct | Meta (OpenRouter) | $0.10 | $0.32 | 131K | 2026-10-24 | OpenRouter 最低价路由（DeepInfra）；Meta 已无自助 Llama API |
| Llama 4 Scout | Meta (OpenRouter) | $0.10 | $0.30 | 1.31M | 2026-10-24 | 超长上下文 |
| Llama 4 Maverick | Meta (OpenRouter) | $0.1875 | $0.6525 | 524K | 2026-10-24 | 多模态输入 |

## 通用折扣机制速查

| 厂商 | Batch | 缓存 | 其他 |
|---|---|---|---|
| OpenAI | -50% | 缓存输入约 1/10 价 | 数据驻留 +10% |
| Anthropic | -50% | 缓存读 ~1/10，写 1.25x | US-only 推理 1.1x；Opus 5.5 Fast 2x |
| Google | -50% | 隐式缓存 ~5% 价 | Flex 模式约 -50%；免费层仍在 |
| DeepSeek | — | 缓存命中约 1/50 价 | 闲时（UTC 非高峰+周末）半价 |
| 阿里百炼 | -50% | 缓存命中 ~10% | 新用户 7000 万免费 tokens（90 天） |
| Mistral | -50% | 缓存输入 -90% | EU 区域推理 +10% |

## 近期限时优惠 / 重要事件（2026-10）

- ⏳ **Gemini 4 Argon 首发价** $2/$10，2026-11-30 截止，12-01 起翻倍 $4/$20（相当于当前 5 折）。
- ⏳ **Gemini 3.8 Flash** $0.75/$3.75 至 2026-12-31，2027 年起翻倍。
- ⏳ **GPT-5.6 Sol 促销** $4/$20（原 $5/$30），官方称至少持续到 2026-11-21。
- ✅ **Mistral Large 4 发布 5 折已结束**（2026-10-24 核实）：官方定价页恢复 $1.36/$4.18，未延期。
- ⏳ **DeepSeek Search/Fetch API 免费**至 2026-11-01（北京时间），之后 $0.75/千次。
- 🔺 **阿里云上调 DeepSeek V4 Flash 0731 价格**（10-20 前后被 Stork AI 追踪到）：输出 $0.40 → $1.32/M（+230%），输入亦翻倍以上。
- 🔽 Zhipu GLM-5-3（wafer host）输出 $7.00 → $4.80（-31%，10-10，Token Barometer 记录）。
- ℹ️ Claude Sonnet 5.5 原定 9-01 涨至 $3/$15 的计划已取消，维持 $2/$10。
