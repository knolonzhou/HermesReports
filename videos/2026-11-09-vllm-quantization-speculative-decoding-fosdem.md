# 量化 + 投机解码：vLLM 推理加速实战蓝图（FOSDEM 2026）

- **视频直链**：https://video.fosdem.org/2026/aw1120/WJUJ3R-accelerating_vllm_inference_with_quantization_and_speculative_decoding.av1.webm （99 MB，AV1/WebM；另有 [605 MB MP4 版](https://video.fosdem.org/2026/aw1120/WJUJ3R-accelerating_vllm_inference_with_quantization_and_speculative_decoding.mp4)）
- **来源页面**：https://archive.fosdem.org/2026/schedule/event/WJUJ3R-accelerating_vllm_inference_with_quantization_and_speculative_decoding/
- **时长**：约 30 分钟（FOSDEM 2026-02-01，AW1.120，Open Research track）
- **演讲者**：Eldar Kurtić —— Red Hat 首席研究科学家 / IST Austria，vLLM 推理研究负责人（资料补充）

## 📺 视频讲了什么

这是 vLLM 核心研究者 Eldar Kurtić 在 FOSDEM 2026 的半小时演讲，主题是给 LLM 推理加速的两板斧：**量化**（把模型权重从高精度压成低精度）和**投机解码**（小模型先猜几个 token，大模型一次性验证）。演讲按"概念 → 在服务器架构中的位置 → 工具实操 → 精度/速度实测数据 → 投机解码的适用边界"推进，全程数据说话，最后给出 vLLM 项目族的行动清单。对想搞 AI Infra 的工程师来说，这是一份"部署就绪"的决策指南。

## 🔑 关键内容

以下**均来自视频画面**（bl 视频理解读取幻灯片），背景补充单独标注：

**1. 为什么要量化？—— 一张 H100 规格表讲透**
幻灯片用存储金字塔（CPU DRAM 大而慢 → GPU HBM 小而快 → SRAM/Tensor Core 最小最快）说明瓶颈：模型要从慢存储加载 N 次。再亮出 H100 SXM 算力表：BF16 Tensor Core 1,979 TFLOPS，FP8 翻倍到 3,958，INT4 到 7,916 —— **精度每减半，硬件吞吐理论翻倍**。加速加载用 weight-only 量化，加速计算则要 weight+activation 都量化。

**2. 实操只要 3 行代码（llm-compressor）**
`fp8_quantize.py` 示例：加载 DeepSeek-R1-Distill-Llama-8B → `QuantizationModifier(scheme="FP8_DYNAMIC")` → `oneshot()` + `save_pretrained()`。MXFP8 版本多了校准数据集（max_samples=512），因为激活量化需要看真实数据分布。

**3. 精度代价实测（画面柱状图读数）**
DeepSeek-R1-Distill 全系在 AIME24/MATH-500/GPQA 平均分上：BF16 vs FP8-W8A8 **几乎无损**（如 Qwen-32B 78.4 vs 78.4）；INT4 多数模型掉 1–2 分以内，**唯一翻车的是 Qwen-1.5B：50.8 → 40.8** —— 小模型经不起激进量化。

**4. 速度收益要看并发（画面延迟-吞吐曲线）**
Llama-3.1-8B 单卡 A6000：低并发（1–4 QPS）时 W4A16 延迟最低；高吞吐区 W8A8 反超，且 W4A16 的吞吐天花板最低（约 5 QPS），甚至不如 BF16。**结论：延迟敏感选 W4A16，吞吐优先选 W8A8。**

**5. 投机解码不是万能药（画面实证图）**
- Llama 3.3 70B：batch 1–4 收益≈0，batch 32 慢 20%，batch 64 慢 50% —— **高并发下反而拖累**；
- Qwen3-32B 数学推理：全程加速，最高 1.6–2×；Coding 场景超过 ~0.2 RPS 后进入减速区。收益取决于任务输出可预测性和负载水平。

**6. 工具链清单（收尾幻灯片）**：量化用 llm-compressor、基准测试用 GuideLLM、部署用 vLLM、训练投机模型用 speculators、现成量化模型在 huggingface.co/RedHatAI。

## 🛠 值得学的点（写给转 AI Infra 的 Java 工程师）

1. **这就是 JVM 调优思维的平移**：量化 ≈ 对象压缩/逃逸分析（省内存换吞吐），投机解码 ≈ JIT 的投机优化 + 分支预测（先猜后验，猜错回滚）。H100 那张算力表相当于你的"CPU 指令吞吐手册"，选型前先背下来：FP8 几乎无损是默认起点。
2. **基准测试姿势可以直接抄**：不要只看单点延迟，要用 GuideLLM 画延迟-QPS 曲线找拐点 —— 和压测 Java 服务画 RT-TPS 曲线一模一样，只是指标换成了 inter-token latency。
3. **决策树很清晰**：显存不够/延迟敏感 → W4A16 或 INT4（但 ≥7B 模型才安全）；吞吐优先 → W8A8-FP8/INT8；低并发 + 结构化输出 → 加投机解码；高并发 → 别加。

## ⚠️ 局限

- qwen3-vl-plus 只"看"了画面，**演讲音频内容未覆盖**——讲者的口头补充、现场 Q&A 无法获取；
- 柱状图/曲线读数为视觉估计，个别数值可能有 ±0.5 分误差；
- 幻灯片引用的两篇论文（Kurtić et al. 2025 量化 R1 模型、量化精度-性能权衡）未展开，需自行查阅。
- FOSDEM 归档页无可下载的高清封面图（讲者照片仅 32×25），本期不配图。

---
*笔记生成：2026-11-09 · bl vision (qwen3-vl-plus) 视频理解 + web_search 背景补充*
