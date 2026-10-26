# QA 自检日志

| 日期 | 检查项数 | 坏链数 | 坏图数 | 存疑条目 | 是否已修复 |
|---|---|---|---|---|---|
| 2026-10-22 | 22（14 外链 + 3 图片 + 2 Mermaid + 3 新闻抽查） | 1（glaforge.dev 404，URL 日期格式错误，已修正为有效路径；另 openai.com/baeldung 返回 403 为反爬，页面经搜索验证真实存在，保留） | 0 | 0（eMudhra CA 事故、OpenAI 模型上架 GCP、DeepSeek V4.1-Flash-1017 三条均验证属实，关键数字吻合） | 是 |
| 2026-10-23 | 37（30 外链 + 3 图片 + 1 Mermaid + 3 新闻抽查） | 0（28 条 200；aibriefs.news 429 为限流、technology.org 403 为反爬，两者经 web_extract 抓取正文验证页面真实且内容与报告吻合，保留） | 0（3 张图均存在且 file 验证为有效 JPEG/PNG） | 0（Claude Duet 主动式 agent/Opus 5.5/6000+ 连接器、微软+AI agent 证明 31 年 KLS 猜想、Recursive Flint 39.8B MoE/SWE-bench 74.2% 三条均验证属实，日期与关键数字吻合） | 无需修复 |
| 2026-10-25 | 46（38链接+3图+1Mermaid+3新闻抽查+git同步） | 0 | 0 | 0 | 无需修复 |
| 2026-10-26 | 47（42 外链 + 3 图片 + 1 Mermaid + 3 新闻抽查） | 4 处坏链（2 个 TechCrunch URL 用了错误的 `2026-10-23` 短横线日期格式、2 个 Inside.java URL 应为 `2026/10/25` 路径格式且不带尾斜杠，均已修正并复测 200；openai.com 官方博文 403 为反爬，web_search 验证页面真实存在且内容吻合，保留） | 0（3 张图均存在且 file 验证为有效 JPEG/PNG） | 0（OpenAI 断网训练 10-23/DNS 事故 9-20/暂停 11 天 10-1 恢复、Grok 92% vs GPT 97% 政治偏好评测、MCP Tasks v2.1.304 10-23 公测/AGNTCon 10-22、Cerebras 59 片 WSE-3T 部署 Kimi K3 1000-2000+ tok/s、JEP 544 Integrated/Release 28/owner John Rose 五条抽查全部属实，日期与关键数字吻合） | 是 |
| 2026-10-27 | 49（45 外链 + 3 图片 + 1 Mermaid + 3 新闻抽查） | 3（micronaut.io、openliberty.io、CNBC 三条用了错误的 `2026-10-20/26` 短横线日期格式，均已修正为 `/2026/10/20`、`/2026/10/26` 路径格式并复测 200；marktechpost/reddit/sec.gov 三条 403 为反爬，web_search 验证页面真实存在且内容与报告吻合，保留） | 0（3 张图均存在且 file 验证为有效 JPEG/WebP） | 0（Anthropic S-1 10-26 公开递交/Nasdaq ANT/营收 $162.9 亿/净亏 $807 亿、OSS Scanner 650 申请 114 接纳/77 critical+803 high/97 盲评 88% 达标、AmiJa Java 周期精确 Amiga 模拟器三条抽查全部属实，日期与关键数字吻合） | 是 |
