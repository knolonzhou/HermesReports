# 源码解剖（Source Reading）

每周三深夜一篇：挑一个开源项目，克隆源码、追调用链、写拆解。所有结论基于真实源码（标注版本与 commit）。

## 索引

| 日期 | 项目 | 模块 | 文章 |
|---|---|---|---|
| 2026-11-18 | LangGraph (master 02f2c2e, v1.2.22) | Pregel 调度器——通道/版本账本/超步循环/检查点/interrupt 重放恢复 | [2026-11-18-langgraph-Pregel调度器与中断恢复.md](./2026-11-18-langgraph-Pregel调度器与中断恢复.md) |
| 2026-11-11 | SGLang (master 9a1979b) | RadixAttention 前缀缓存（基数树/引用计数/淘汰）+ 调度器准入与 retract | [2026-11-11-sglang-RadixAttention前缀缓存与调度.md](./2026-11-11-sglang-RadixAttention前缀缓存与调度.md) |
| 2026-11-04 | vLLM (master c1d8fad) | V1 调度器 + PagedAttention 块管理（BlockPool/前缀缓存哈希链/抢占/懒淘汰） | [2026-11-04-vllm-调度器与PagedAttention.md](./2026-11-04-vllm-调度器与PagedAttention.md) |
| 2026-10-28 | XXL-JOB 3.x | 调度核心（DB锁+预读时间轮+触发链路+执行器JobThread） | [2026-10-28-xxl-job-调度核心.md](./2026-10-28-xxl-job-调度核心.md) |

## 候选池（轮换）

XXL-JOB ✅ · vLLM 调度器/PagedAttention ✅ · SGLang RadixAttention ✅ · LangGraph 调度器 ✅ · Spring @Scheduled · Quartz JobStoreTX · ShedLock · Redisson 看门狗 · Caffeine 淘汰 · Netty EventLoop · 虚拟线程 Continuation · HikariCP
