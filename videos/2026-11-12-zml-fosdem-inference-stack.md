# ZML：为生产与多加速器而生的高性能 AI 推理栈（FOSDEM 2025）

- **视频直链**：https://video.fosdem.org/2025/ub2252a/fosdem-2025-5923-zml-a-high-performance-ai-inference-stack-built-for-production-and-multi-accelerator-deployment.mp4（镜像验证：ftp.fau.de，video/mp4，约 472 MB）
- **来源页面**：https://archive.fosdem.org/2025/schedule/event/fosdem-2025-5923-zml-a-high-performance-ai-inference-stack-built-for-production-and-multi-accelerator-deployment/
- **时长**：约 30 分钟（FOSDEM 2025-02-02，UB2.252A Lameere 会场，Low-level AI Engineering and Hacking devroom）
- **讲者**：Rene Schallner、Guillaume Wenzek（ZML 团队，自述 "AI flavored backend engineers"）

![FOSDEM 演讲海报](assets/2026-11-12/zml-talk-poster.svg)

## 📺 视频讲了什么

这场演讲介绍了 ZML——一个用 Zig 语言编写、经 MLIR/StableHLO 下沉到 OpenXLA、由 Bazel 构建的**纯推理** AI 框架（"白话解释"：不跑训练、只管把训练好的模型又快又稳地跑起来的软件底座）。全片用复古游戏/梗图风格串场：以街霸 "PLAYER SELECT"（1P=训练 vs 2P=推理）开场，用魂系 "YOU DIED" 黑屏嘲讽 `python3 model.py` 崩溃体验，主张推理场景应该彻底抛弃 Python、静态编译、一条命令跨五种加速器后端（CPU/CUDA/ROCm/Neuron/TPU）部署。结尾预告了 LLM 服务器 llmd。

## 🔑 关键内容

**画面里看到的**（bl vision 视频理解结果）：

- **训练 vs 推理的世界观对比页**：训练=研究、"越多越好"、快速迭代、Python=❤️；推理=生产、"越省越好"、可预测延迟、Python=🤭。这是全篇论证的出发点。
- **技术栈架构图**：ZIG → MLIR → OPENXLA → NVIDIA CUDA / AMD ROCm / 通用芯片，BAZEL 托底构建。
- **设计原则**：Inference only / Zig as the frontend / Zero Python / Modular code / Focus on maintainability；异步靠 zigcoro。
- **Axis tagging 代码示例**：`zml.Shape.init(.{.w=1920,.h=1080,.c=3})`、`a.withTags(.{.m,.k})` 后 `a2.dot(b2, .{.k})`——张量的每个维度带语义标签，写注意力（sdpa）时不用手工 transpose/reshape，配梗标语 "Look ma, no MATMUL! …and no transpose!"。
- **部署命令行**：`bazel run -c opt //mnist --@zml//runtimes:cuda=true`；同一 llama-3.2-1B 命令仅切换 `cuda/rocm/neuron/tpu` 标志即换后端；还支持 OCI 镜像推送、runtime 沙箱裁剪（只打包所需 CUDA/ROCm 组件，显著缩小产物）。
- **无现场 live demo**：主屏全程幻灯片，"演示"靠内嵌终端动画（Python 崩溃 → YOU DIED）与 llmd 启动日志截图；全场也没有定量 benchmark 数字。社区反响页引用了 Yann LeCun 2024-09-17 的推文（约 20 万浏览）。

**资料补充**（web_search，非画面内容）：

- 性能来源是 XLA 编译器三件套：kernel fusion、coalesced memory allocation、autotuning（画面点过名）。
- 项目后续发展很快：2026-03 发布 ZML/v2（显式化、可组合性重构，DMA 分配器 + O_DIRECT 实现类 GPUDirect 的加载）；2026-07 发布 llmd 正式版，支持连续批处理、paged attention、张量并行、prefix caching、tool calling，宣称 H100×2 上 gemma-4-26B-A4B 达 ~1318 tok/s（bs=16）。GitHub：github.com/zml/zml（Apache-2.0）。

## 🛠 值得学的点（给想转 AI Infra 的 Java 工程师）

1. **ZML 的气质非常"Java"**：静态类型、显式编译、无动态运行时、构建产物是可分发的自包含二进制——和 JVM 生态"编译一次到处运行"的心智模型同构。理解它比从 PyTorch 入门更贴近后端工程师直觉。
2. **Axis tagging 值得借鉴**：把张量维度打上 `.w/.h/.c` 这类语义标签，让矩阵乘的转置/规约轴由类型系统保证正确——相当于给数值计算加了泛型和编译期校验，很多 Python 框架里靠注释和经验的坑在这里被编译器拦住。
3. **"推理不需要 Python"的产业信号**：llmd 这类 ahead-of-time 编译、延迟平坦可预测的服务器，正是 LLM serving 从"研究脚手架"走向"生产基础设施"的方向；关注其 Prometheus /metrics、continuous batching、paged attention 等特性，与 vLLM/SGLang 是同一赛道的不同路线（编译派 vs 解释派）。

## ⚠️ 局限

- 视频理解基于抽帧画面，**音频内容（讲者口述）未纳入**，幻灯片之外的口头解释、Q&A 全部缺失。
- 部分梗图小字、GitHub 截图细节可能识别不全；性能数字以官方文档/博客补充为准，演讲本身未给出 benchmark。
- 演讲录制于 2025 年初，ZML v1 时代的 API（如 `//runtimes:` 路径）在 v2 中已改为 `//platforms:`，照搬旧命令会失败。

---
*生成：2026-11-12，bl vision describe（qwen3-vl-plus）+ web_search 补充*
