# QA 自检日志

| 日期 | 检查项数 | 坏链数 | 坏图数 | 存疑条目 | 是否已修复 |
|---|---|---|---|---|---|
| 2026-10-22 | 22（14 外链 + 3 图片 + 2 Mermaid + 3 新闻抽查） | 1（glaforge.dev 404，URL 日期格式错误，已修正为有效路径；另 openai.com/baeldung 返回 403 为反爬，页面经搜索验证真实存在，保留） | 0 | 0（eMudhra CA 事故、OpenAI 模型上架 GCP、DeepSeek V4.1-Flash-1017 三条均验证属实，关键数字吻合） | 是 |
| 2026-10-23 | 37（30 外链 + 3 图片 + 1 Mermaid + 3 新闻抽查） | 0（28 条 200；aibriefs.news 429 为限流、technology.org 403 为反爬，两者经 web_extract 抓取正文验证页面真实且内容与报告吻合，保留） | 0（3 张图均存在且 file 验证为有效 JPEG/PNG） | 0（Claude Duet 主动式 agent/Opus 5.5/6000+ 连接器、微软+AI agent 证明 31 年 KLS 猜想、Recursive Flint 39.8B MoE/SWE-bench 74.2% 三条均验证属实，日期与关键数字吻合） | 无需修复 |
