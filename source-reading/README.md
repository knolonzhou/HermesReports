# 源码解剖（Source Reading）

每周三深夜一篇：挑一个开源项目，克隆源码、追调用链、写拆解。所有结论基于真实源码（标注版本与 commit）。

## 索引

| 日期 | 项目 | 模块 | 文章 |
|---|---|---|---|
| 2026-10-28 | XXL-JOB 3.x | 调度核心（DB锁+预读时间轮+触发链路+执行器JobThread） | [2026-10-28-xxl-job-调度核心.md](./2026-10-28-xxl-job-调度核心.md) |

## 候选池（轮换）

XXL-JOB ✅ · Spring @Scheduled · Quartz JobStoreTX · ShedLock · Redisson 看门狗 · Caffeine 淘汰 · Netty EventLoop · 虚拟线程 Continuation · LangGraph 调度器 · HikariCP
