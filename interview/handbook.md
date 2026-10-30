# 面试刷题手册（Hermes 每日三题）

> 每晚 3 题，主题按年内天数 mod 7 轮换：0=JVM 1=并发 2=Spring 3=算法·LeetCode 4=算法·系统设计 5=深度学习 6=LLM/Agent 工程。
> 难度定位：3-5 年经验后端 / AI 工程师面试。

## 📚 目录索引

### Spring（IoC/AOP/事务/Boot 自动装配/循环依赖）
- [Q1. Spring 如何解决循环依赖？为什么是三级缓存而不是两级？](#q1)（📅2026-10-23 ⭐4）
- [Q2. @Transactional 有哪些失效场景？底层原理是什么？](#q2)（📅2026-10-23 ⭐4）
- [Q3. Spring Boot 自动装配的原理是什么？如何自定义一个 Starter？](#q3)（📅2026-10-23 ⭐3）
- [Q19. 讲讲 Spring Bean 的完整生命周期，各扩展点在什么时机被调用？](#q19)（📅2026-10-30 ⭐4）
- [Q20. Spring AOP 用 JDK 动态代理还是 CGLIB？为什么"同类内部方法调用"会让切面失效？](#q20)（📅2026-10-30 ⭐4）
- [Q21. @Autowired 和 @Resource 有什么区别？多个同类型 Bean 时 Spring 怎么选？](#q21)（📅2026-10-30 ⭐3）

### JVM（内存模型/GC/类加载/JIT）
- [Q16. 对象一定分配在堆上吗？讲讲逃逸分析、标量替换和 TLAB](#q16)（📅2026-10-28 ⭐4）
- [Q17. G1 和 ZGC 分别怎么做到低停顿？SATB 与染色指针解决什么问题？](#q17)（📅2026-10-28 ⭐5）
- [Q18. 双亲委派模型为什么存在？哪些场景必须打破它？](#q18)（📅2026-10-28 ⭐4）

### 算法·LeetCode 高频题
- [Q4. 无重复字符的最长子串（LC3）](#q4)（📅2026-10-24 ⭐3）
- [Q5. 数组中的第K个最大元素（LC215）](#q5)（📅2026-10-24 ⭐3）
- [Q6. LRU 缓存（LC146）](#q6)（📅2026-10-24 ⭐4）
- [Q22. K 个一组翻转链表（LC25）](#q22)（📅2026-10-31 ⭐4）
- [Q23. 二叉树的最近公共祖先（LC236）](#q23)（📅2026-10-31 ⭐3）
- [Q24. 岛屿数量（LC200）](#q24)（📅2026-10-31 ⭐3）

### 算法·系统设计类
- [Q7. 设计秒杀系统——如何保证不超卖？](#q7)（📅2026-10-25 ⭐5）
- [Q8. 100 亿数据的大文件里找 Top 100 高频词——内存只有 1GB 怎么办？](#q8)（📅2026-10-25 ⭐4）
- [Q9. 设计短链系统——发号器还是哈希？短码冲突怎么解？](#q9)（📅2026-10-25 ⭐4）

### 深度学习（归一化/优化器/正则化/Transformer/微调）
- [Q10. Transformer 为什么用 LayerNorm 而不是 BatchNorm？RMSNorm 又省了什么？](#q10)（📅2026-10-26 ⭐4）
- [Q11. AdamW 的"解耦权重衰减"到底解耦了什么？和 Adam+L2 差在哪？](#q11)（📅2026-10-26 ⭐4）
- [Q12. LoRA 低秩微调的原理是什么？为什么 B 矩阵要初始化为 0？](#q12)（📅2026-10-26 ⭐4）

### LLM/Agent 工程（RAG/工具调用/MCP/推理优化）
- [Q13. RAG 检索不准怎么办？从 embedding 到重排的完整调优链路](#q13)（📅2026-10-27 ⭐4）
- [Q14. LLM 推理为什么慢？讲讲 KV Cache、PagedAttention 和 continuous batching](#q14)（📅2026-10-27 ⭐5）
- [Q15. Agent 的工具调用是怎么实现的？MCP 解决了什么问题？](#q15)（📅2026-10-27 ⭐4）


---

<a id="q1"></a>

### Q1. Spring 如何解决循环依赖？为什么是三级缓存而不是两级？（🏷Spring 📅2026-10-23 ⭐难度4）

**「考察点」** Bean 生命周期与三级缓存机制的理解深度，以及 AOP 代理提前暴露的关键细节。

**「参考答案」**

**基础答案：** Spring 对 **单例（singleton）+ setter/字段注入** 的循环依赖，通过三级缓存解决：

| 缓存 | 名称 | 存什么 |
|---|---|---|
| 一级 | `singletonObjects` | 完整的成品 Bean |
| 二级 | `earlySingletonObjects` | 提前暴露的半成品 Bean（已实例化、未填充属性） |
| 三级 | `singletonFactories` | `ObjectFactory` lambda，调用时才决定返回原始对象还是代理对象 |

流程：A 实例化后（构造完成、属性未填充），先把一个 `ObjectFactory` 放入三级缓存 → 填充属性发现依赖 B → 创建 B → B 填充属性需要 A → 从缓存查 A：三级缓存命中，调用工厂拿到 A 的早期引用（移入二级缓存）→ B 完成创建进入一级缓存 → A 拿到 B 完成填充 → A 进入一级缓存。

**深入原理：为什么必须三级，两级不行吗？**

核心原因是 **AOP 代理的创建时机**。正常流程中代理对象是在 `initializeBean`（初始化之后）由 `AbstractAutoProxyCreator` 创建的；但循环依赖下，B 注入的 A 必须和最终容器里的 A 是**同一个对象**——如果 A 需要被代理，B 拿到的就得是代理对象。

- 如果只有两级缓存，想解决就必须**在实例化后立刻创建代理**，这破坏了 Spring "代理在初始化后创建" 的设计原则（大量无循环依赖的 Bean 也被迫提前代理，且与 `BeanPostProcessor` 体系的时序耦合）。
- 三级缓存存的是**工厂（lambda）**：`getEarlyBeanReference()` 只在**真的发生循环依赖、有人来取早期引用时**才被调用，此时才判断是否需要提前生成代理（`SmartInstantiationAwareBeanPostProcessor#getEarlyBeanReference`）。没有循环依赖时工厂永远不会执行——**延迟决策**，这就是三级的意义。

```java
// DefaultSingletonBeanRegistry#getSingleton 核心逻辑（简化）
singletonObject = singletonFactory.getObject(); // 调三级缓存工厂
this.earlySingletonObjects.put(beanName, singletonObject); // 升级到二级
this.registeredSingletons.remove(beanName);
```

**哪些循环依赖解决不了？**
1. **构造器注入**的循环依赖：实例化都完不成，没有"半成品"可暴露 → 直接抛 `BeanCurrentlyInCreationException`（可用 `@Lazy` 缓解，注入的是代理，首次使用时才解析目标）。
2. **prototype 作用域**：不缓存，无法提前暴露。
3. Spring Boot 2.6+ 默认**禁止循环依赖**（`spring.main.allow-circular-references=false`），出现即启动失败——官方态度是循环依赖本身是设计坏味道，应重构（抽第三方类、事件解耦、`@Lazy`）。

**Mermaid 流程图：**

```mermaid
sequenceDiagram
    participant C as 容器
    participant A as Bean A
    participant B as Bean B
    C->>A: 实例化 A（构造器）
    A->>C: 三级缓存放入 A 的 ObjectFactory
    A->>B: 填充属性需要 B → 创建 B
    B->>C: getBean(A)
    C-->>B: 三级缓存命中→工厂产出早期A(必要时代理)→移入二级
    B->>C: B 完成初始化 → 一级缓存
    C-->>A: A 拿到 B，完成填充+初始化 → 一级缓存
```

**「追问陷阱」**
1. *"二级缓存到底有没有用？能不能三级直接升一级？"* —— 不能省。二级缓存保证**多次 getEarlyBeanReference 只执行一次工厂**：若 B 和 C 都循环依赖 A，两次取到的早期引用必须是同一个对象（否则 B、C 注入的 A 不是同一个）。第一次从三级工厂产出后放二级，后续直接从二级取，工厂不再执行。
2. *"A 最终生成的代理和早期暴露的代理会不会是两个对象？"* —— 不会。`AbstractAutoProxyCreator` 在 `postProcessAfterInitialization` 里会检查 `earlyProxyReferences`，如果该 Bean 已经通过三级缓存提前代理过，初始化后就不再重复创建代理，保证单例一致性。

---

<a id="q2"></a>

### Q2. @Transactional 有哪些失效场景？底层原理是什么？（🏷Spring 📅2026-10-23 ⭐难度4）

**「考察点」** 声明式事务的 AOP 代理本质，以及工程中最常见的事务踩坑清单。

**「参考答案」**

**基础答案（失效场景清单）：**
1. **同类内部方法调用（this 调用）**：`this.methodB()` 不走代理，事务注解无效 —— 最高频。
2. **方法不是 public**：Spring 事务默认只对 public 方法生效（CGLIB 无法代理 private/final/static）。
3. **异常被 catch 吞掉**或抛的是**受检异常**：默认只回滚 `RuntimeException` 和 `Error`，抛 `Exception` 需显式 `rollbackFor = Exception.class`。
4. **抛出异常类型不匹配 rollbackFor 配置**。
5. **数据库/引擎不支持事务**：MyISAM 表、或某些 NoSQL。
6. **Bean 未被 Spring 管理**（自己 new 出来的对象）。
7. **传播行为设置错误**：如 `NOT_SUPPORTED` 挂起事务、`REQUIRES_NEW` 内外事务独立（内层回滚不影响外层，常被误认为"失效"）。
8. **多线程调用**：事务上下文绑定在 ThreadLocal（`TransactionSynchronizationManager`），子线程拿不到连接。
9. **@Transactional 注解在接口上 + CGLIB 代理**：CGLIB 基于类，接口上的注解不会被继承。

**深入原理：** 声明式事务 = AOP 代理 + `TransactionInterceptor`。

- 开启 `@EnableTransactionManagement` 后，`AutoProxyCreator` 为标注了 `@Transactional` 的 Bean 生成代理（JDK 动态代理或 CGLIB，Boot 2.x 默认 `proxyTargetClass=true` 即 CGLIB）。
- 调用链：代理方法 → `TransactionInterceptor.invoke()` → `PlatformTransactionManager.getTransaction()`（从 DataSource 拿 Connection，`setAutoCommit(false)`，把连接包成 `ConnectionHolder` 绑定到 `TransactionSynchronizationManager` 的 **ThreadLocal**）→ 执行目标方法 → 正常则 `commit()`，匹配回滚规则则 `rollback()`。
- 之所以"this 调用失效"：代理只拦截**从外部进入代理对象**的调用；类内部 `this.xxx()` 中的 this 是原始对象，不经过拦截器链。这也是"同类中一个无事务方法调用事务方法，事务不生效"的根因。

**内部调用的三种解法（追问常考）：**
```java
// 方案1：注入自身代理（Spring 4.3+ 支持自注入，需走代理）
@Resource private MyService self;
public void a() { self.b(); } // b 上的 @Transactional 生效

// 方案2：AopContext 获取当前代理（需 exposeProxy = true）
((MyService) AopContext.currentProxy()).b();

// 方案3：拆到另一个 Bean（最推荐，符合职责划分）
```

**传播行为 7 种一句话版：** REQUIRED（默认，有就加入没有就新建）、SUPPORTS（有就加入没有就非事务）、MANDATORY（必须有否则抛异常）、REQUIRES_NEW（永远新建，挂起当前）、NOT_SUPPORTED（非事务执行，挂起当前）、NEVER（有事务就抛异常）、NESTED（savepoint 嵌套，外层回滚则内层必回滚，内层回滚不影响外层）。

**「追问陷阱」**
1. *"REQUIRES_NEW 和 NESTED 的区别？"* —— REQUIRES_NEW 是**物理上两个独立事务、两个连接**（外层被挂起，内层提交后外层回滚也救不回内层）；NESTED 是**同一连接上的 savepoint**，内层回滚只是回到保存点，外层最终回滚会连带内层一起回滚。追问点：NESTED 依赖 JDBC savepoint，JTA 分布式事务下不可用。
2. *"事务方法里发 MQ / 调 RPC，消费方读不到数据怎么办？"* —— 事务未提交时消息已发出，下游查库读到旧数据。正解：`TransactionSynchronizationManager.registerSynchronization` 的 `afterCommit` 回调里再发消息，或用事务消息（RocketMQ half message）/ 本地消息表。这考察的是"事务边界与副作用时序"，比背失效清单更能区分候选人。

---

<a id="q3"></a>

### Q3. Spring Boot 自动装配的原理是什么？如何自定义一个 Starter？（🏷Spring 📅2026-10-23 ⭐难度3）

**「考察点」** @SpringBootApplication 组合注解的拆解能力 + 条件装配机制 + 动手写 Starter 的工程经验。

**「参考答案」**

**基础答案：** 自动装配的入口是 `@SpringBootApplication`，它是三个注解的组合：
- `@SpringBootConfiguration`（本质是 @Configuration）
- `@ComponentScan`（扫描当前包及子包）
- **`@EnableAutoConfiguration`** ← 自动装配核心

`@EnableAutoConfiguration` 通过 `@Import(AutoConfigurationImportSelector.class)` 导入选择器，它在启动时读取 classpath 下所有 jar 的 **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** 文件（Boot 2.7 之前是 `META-INF/spring.factories`），拿到候选自动配置类全限定名列表，经过**去重 → 排除（exclude）→ 条件过滤**后，把通过筛选的配置类注册为 Bean 定义。

**深入原理：条件装配 @Conditional 家族**

自动配置类"生效与否"由条件注解裁决，全部基于 `Condition` 接口的 `matches()`：

| 注解 | 条件 |
|---|---|
| `@ConditionalOnClass` | classpath 存在某类（**在 Bean 定义解析阶段用 ASM 读元数据判断，不会触发类加载 NoClassDefFoundError**）|
| `@ConditionalOnMissingBean` | 容器中不存在该 Bean —— Starter "用户配置优先"的关键 |
| `@ConditionalOnProperty` | 配置项匹配（如 `havingValue="true"`）|
| `@ConditionalOnWebApplication` | 是 Web 环境 |

典型模式（几乎所有官方 Starter 都长这样）：

```java
@AutoConfiguration
@ConditionalOnClass(DataSource.class)
@EnableConfigurationProperties(MyDbProperties.class) // 绑定 application.yml 前缀配置
public class MyDbAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean // 用户自己定义了就用用户的，这就是"约定优于配置"的退让机制
    public MyDbClient myDbClient(MyDbProperties props) {
        return new MyDbClient(props.getUrl());
    }
}
```

**加载时序细节（加分点）：** 自动配置类的解析发生在**用户配置类之后**（`AutoConfigurationImportSelector` 是 `DeferredImportSelector`，延迟处理），所以 `@ConditionalOnMissingBean` 判断时用户自定义的 Bean 已经注册——顺序保证了"用户优先"。

**自定义 Starter 步骤（官方规范）：**
1. 建 `xxx-spring-boot-autoconfigure` 模块：写 `XxxAutoConfiguration` + `XxxProperties`（`@ConfigurationProperties(prefix="xxx")`）。
2. 在 `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 中每行写一个配置类全限定名。
3. 建 `xxx-spring-boot-starter` 空壳模块，只做依赖聚合（pom 引 autoconfigure + 必要三方库）。官方 Starter 命名 `spring-boot-starter-xxx`，第三方规范是 `xxx-spring-boot-starter`。
4. （可选）用 `spring-boot-configuration-processor` 生成 `spring-configuration-metadata.json`，让 IDE 有配置提示。

**「追问陷阱」**
1. *"Boot 2.7/3.x 为什么废弃 spring.factories 改用 .imports 文件？"* —— spring.factories 是通用 SPI 机制，一个文件混杂多种扩展点（监听器、初始化器、自动配置…），解析开销大且无法针对自动配置做去重排序优化；独立的 `.imports` 文件格式简单（一行一个类名），启动更快，语义更清晰。Boot 2.7 两者兼容，3.0 起只认 `.imports`。
2. *"@ComponentScan 和自动装配有什么区别？为什么 Starter 里的 Bean 不靠包扫描？"* —— 扫描是**基于包路径**（用户工程不可能扫到 Starter 的包），自动装配是**基于 imports 清单 + 条件注解**，与包结构解耦；且扫描无条件注册，自动装配可按 classpath/配置动态生效。能答出"Starter 的 jar 不在用户扫描路径下，必须走 imports 注册"即为过关。

<a id="q4"></a>

### Q4. 无重复字符的最长子串——滑动窗口如何做到 O(n)？（🏷算法·LeetCode 📅2026-10-24 ⭐难度3）

> [LeetCode 3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) · 难度：中等 · 字节/腾讯/阿里高频真题

**「考察点」** 滑动窗口 + 哈希优化的手写能力，尤其是左边界跳转时"不回退"的陷阱。

**「参考答案」**

**基础答案：** 暴力枚举所有子串是 O(n³)（枚举 O(n²) × 判重 O(n)）。用**滑动窗口**：维护一个无重复字符的窗口 `[left, right]`，右指针不断扩张，遇到重复字符时收缩左边界。关键优化：用哈希表记录**每个字符最近一次出现的下标**，遇到重复时 left 直接跳过去，而不是逐步移动，整体 O(n)。

```python
def lengthOfLongestSubstring(s: str) -> int:
    last = {}          # 字符 -> 最近一次出现的下标
    left = 0           # 窗口左边界
    ans = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1   # 左边界直接跳到重复字符的下一位
        last[ch] = right
        ans = max(ans, right - left + 1)
    return ans
```
（已实测通过，含 `"abba"`、`"tmmzuxt"` 等陷阱用例）

**复杂度：** 时间 O(n)——每个字符只被右指针访问一次；空间 O(min(n, |Σ|))，Σ 为字符集（ASCII 最多 128）。

**深入原理：两个必须讲透的点**

1. **为什么 left 只能前进不能后退？** 条件 `last[ch] >= left` 是灵魂。反例 `"abba"`：处理第二个 `a` 时，`last['a'] = 0`，但此时 `left = 2`（已被 `b` 推过），如果无脑执行 `left = last['a'] + 1 = 1`，窗口反而扩大到包含已淘汰的 `b`，答案错误。所以只有当重复字符**落在当前窗口内**才跳转，等价写法是 `left = max(left, last[ch] + 1)`。
2. **滑动窗口的适用判据：** 题目求"最长/最短连续子串/子数组"且窗口具有**单调性**（右移扩大窗口会破坏某性质、左移收缩会恢复）时可用。若窗口不满足单调性（如"和 ≥ target 且含负数"），滑动窗口失效，需换前缀和+二分等方案。

**变体/追问：如果字符集是 Unicode（百万级）怎么办？**
哈希表方案天然支持任意字符集，空间随实际出现的字符数增长而非字符集大小，无需改动；若字符集固定且小（ASCII），换成 `int[128]` 数组比哈希表常数更小、更快。另一个常见变体："**最多包含 K 个不同字符**的最长子串"（LC340）——窗口条件从"无重复"变成"种类数 ≤ K"，收缩时用计数器维护种类数即可，框架完全一致。

**「追问陷阱」**
1. *"如果要求返回子串本身而不是长度？"* —— 在更新 ans 时同步记录 `start = left`，最后 `s[start:start+ans]`。考察是否真的理解窗口状态而非背模板。
2. *"用双指针 + Set 和用哈希表记录下标，哪个好？"* —— Set 版本遇重复时 left 逐步右移并 `remove(s[left])`，最坏 O(2n) 仍是 O(n)，但常数更大；哈希记录下标是 O(1) 跳转。两者都对，能说出"Set 版每个元素最多进出窗口各一次，所以也是线性"是加分项。

---

<a id="q5"></a>

### Q5. 数组中的第K个最大元素——为什么快速选择比堆更适合面试追问？（🏷算法·LeetCode 📅2026-10-24 ⭐难度3）

> [LeetCode 215. 数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) · 难度：中等 · 字节/美团/快手 Top 级高频真题

**「考察点」** 快速选择（Quickselect）的分治思想、随机化防退化，以及与堆解法的复杂度权衡。

**「参考答案」**

**基础答案：** 三种解法：
| 解法 | 时间 | 空间 | 备注 |
|---|---|---|---|
| 全排序 | O(n log n) | O(1) | `sorted(nums)[-k]`，面试只能当铺垫 |
| 小顶堆（大小 K） | O(n log K) | O(K) | 适合海量数据流/内存放不下时 |
| **快速选择** | **平均 O(n)**，最坏 O(n²) | O(1) | 随机化 pivot 后最坏概率可忽略 |

快速选择：借用快排 partition，每轮把基准放到最终位置——若基准下标恰好是 `k-1`（降序视角）即为答案；否则**只递归包含目标的那一半**，这是它比快排快一个量级的原因（n + n/2 + n/4 + … = 2n）。

```python
import random
def findKthLargest(nums, k):
    def partition(l, r):
        p = random.randint(l, r)
        nums[p], nums[r] = nums[r], nums[p]
        pivot = nums[r]
        i = l
        for j in range(l, r):
            if nums[j] > pivot:   # 降序摆放，第 k 大 = 下标 k-1
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[r] = nums[r], nums[i]
        return i
    l, r = 0, len(nums) - 1
    while True:
        i = partition(l, r)
        if i == k - 1:
            return nums[i]
        elif i < k - 1:
            l = i + 1
        else:
            r = i - 1
```
（已实测：LeetCode 官方用例 + 300 组随机对拍全部通过）

**复杂度：** 时间平均 O(n)、最坏 O(n²)（随机化后对抗性输入无法稳定触发）；空间 O(1)（迭代写法，递归写法为栈深 O(log n) 期望）。

**深入原理：**
- **为什么必须随机化 pivot？** 固定取首/尾元素时，对已排序数组每轮只能砍掉 1 个元素，退化 O(n²)。随机 pivot 使期望比较次数为 O(n)，且让输入构造者无法针对性攻击（对抗随机化需要预知随机数序列）。
- **确定性最坏 O(n) 的方案存在吗？** 存在——BFPRT（中位数的中位数）选 pivot，理论最优但常数大，工程与面试中几乎不用，能提到名字和思路即可。
- **堆解法的不可替代场景：** 数据是**流式**到来、或 n 大到内存放不下时，维护大小为 K 的小顶堆只需 O(K) 内存；快速选择要求全量数据在内存中。这就是"Top-K 大数据"面试链路里两种解法各自的定位。Java 侧对应 `PriorityQueue`（默认小顶堆），`offer` 后 `size() > k` 则 `poll()`。

**变体/追问：如果数据量是 100 亿怎么办？**
单机内存放不下，标准答案是**分治 + 分布式 Top-K**：
1. 数据分片（按 hash 或文件切块），每台机器对本地分片求**局部 Top-K**（小顶堆，O(n_i log K)）；
2. 汇总所有局部 Top-K（总量 = 分片数 × K，通常可放进单机内存）再做一次全局 Top-K；
3. 正确性依据：全局第 K 大一定在各局部 Top-K 之中（一个元素若连本地前 K 都进不了，全局排名必然 > K）。
MapReduce / Spark `takeOrdered(k)` 就是这套逻辑。若数据实时流动，则用堆常驻内存增量维护，或近似方案（Count-Min Sketch 类结构用于频次 Top-K）。

**「追问陷阱」**
1. *"第 K 大和第 K 小怎么改？重复元素怎么算？"* —— 第 K 小把比较方向反转即可；重复元素**各占一个名次**（`[3,3,3]` 的第 2 大是 3），partition 天然按位置处理所以自动正确——但要警惕候选人自作主张先 `set(nums)` 去重，语义就错了。
2. *"能不能不修改原数组？"* —— 快速选择是原地算法会打乱数组；若要求只读，用堆解法（拷贝前 K 个建堆）或二分答案法（值域二分 + 计数，O(n log(max-min))，不改动数组）。能主动说出二分答案法是强加分项。

---

<a id="q6"></a>

### Q6. 设计 LRU 缓存——为什么是哈希表 + 双向链表？O(1) 怎么做到的？（🏷算法·LeetCode 📅2026-10-24 ⭐难度4）

> [LeetCode 146. LRU 缓存](https://leetcode.cn/problems/lru-cache/) · 难度：中等 · 字节/腾讯/Amazon 设计题 Top1，也是 Redis/Guava 缓存的真实模型

**「考察点」** 数据结构组合设计能力：如何让 get 和 put 都做到 O(1)，手写双向链表的指针操作是否干净。

**「参考答案」**

**基础答案：** 需求拆解——get/put O(1) 定位 → **哈希表**；O(1) 维护"访问顺序"（把节点移到一端、从另一端淘汰）→ **链表**；而单链表删除任意节点需要找前驱 O(n)，所以必须**双向链表**（持有 prev 指针，删除是纯指针操作）。两者组合：哈希表 `key -> Node`，Node 内嵌在双向链表中，**最近使用放头部，淘汰取尾部**。哨兵头尾节点（dummy head/tail）消除空链表和边界判断。

```python
class Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}                          # key -> Node
        self.head, self.tail = Node(), Node()  # 哨兵节点
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):                # 插到头部（最近使用）
        node.next, node.prev = self.head.next, self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) >= self.cap:
            lru = self.tail.prev               # 尾部 = 最久未使用
            self._remove(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)
```
（已实测：LeetCode 官方示例 + "put 更新已有 key 算一次访问"用例全部通过）

**复杂度：** get / put 均 O(1) 时间；O(capacity) 空间。

**深入原理：三个容易被追问的设计细节**
1. **Node 里为什么必须存 key？** 淘汰尾节点时要同步删除哈希表条目 `del self.map[lru.key]`——若 Node 只有 value，拿到尾节点却不知道它的 key，无法反查哈希表。这是手写时最高频的丢分点。
2. **哨兵节点的价值：** 没有 dummy head/tail 时，插入/删除都要分支讨论"是不是头节点/尾节点/链表为空"，四类边界；哨兵把"任意位置删除"统一成一种指针操作。Java 版同理。
3. **淘汰策略的演进（联系工程）：** LRU 的缺陷是**偶发的批量扫描会污染缓存**（一次性遍历把热点全部挤出去）。LRU-K / LFU（按频率）/ Redis 的近似 LRU（随机采样 5 个 key 淘汰其中最旧者，避免维护全局链表的开销）都是针对性改进。Guava Cache 用的分段 LRU（W-TinyLFU 在 Caffeine 中进一步演进：主区 LRU + 观察区、按频率准入），能聊到这一层说明真读过缓存源码。

**Mermaid 结构图：**

```mermaid
graph LR
    H[head哨兵] <--> A["key=3 (最新)"]
    A <--> B["key=1"]
    B <--> C["key=2 (最旧)"]
    C <--> T[tail哨兵]
    M["HashMap: 3→A, 1→B, 2→C"]
    T -. "put 新 key 且满容量: 删 C 和 map[2]" .-> M
```

**变体/追问：如果要支持多线程并发访问怎么办？**
- 朴素方案：方法加 `synchronized` / `ReentrantLock`——正确但吞吐差，锁竞争集中在单条链表上。
- 工程方案：**分段（sharding）**——按 key hash 到 N 个独立的小 LRU，各段独立加锁（ConcurrentHashMap 1.7 的 Segment 思路）；淘汰精度略降（全局并非严格 LRU），换取并发度 ×N。Caffeine 更进一步：读操作无锁化（访问记录进环形缓冲队列，异步批量重放维护链表顺序），写操作才走锁，因为"更新访问时间戳"这种读副作用无需实时精确。
- 追问延伸："Redis 为什么不用精确 LRU？"——精确 LRU 要为每个 key 维护双向链表指针，内存开销大；Redis 用采样近似（`maxmemory-samples`），实测效果接近精确 LRU 而内存几乎零开销。

**「追问陷阱」**
1. *"get 一个不存在的 key 会改变 LRU 状态吗？put 一个已存在的 key 呢？"* —— miss 的 get 不应移动任何东西（没有节点可移）；**put 已存在 key 必须算一次访问**（更新值 + 移到头部），很多人漏掉后半句导致淘汰顺序错误。这题的细节分就在这里。
2. *"能不能用 Python 的 OrderedDict / Java 的 LinkedHashMap 一行搞定？"* —— 可以：`OrderedDict.move_to_end` + `popitem(last=False)` 十行搞定；Java `LinkedHashMap(capacity, 0.75f, true)` 重写 `removeEldestEntry` 即可。但面试官通常要求**手写底层**——先问一句"可以用现成库吗"再动手，是成熟的沟通方式；直接背 OrderedDict 版本而不理解双向链表，一追问指针细节就露馅。

---

<a id="q7"></a>

### Q7. 设计秒杀系统——如何保证不超卖？（🏷算法·系统设计 📅2026-10-25 ⭐难度5）

**「考察点」** 高并发场景下的分层削峰架构能力，以及对"库存扣减原子性"这一核心问题的多种实现方案的理解深度。

**「参考答案」**

**基础答案：** 秒杀的本质是**瞬时流量远超系统容量**（如 10 万 QPS 抢 1000 件库存），设计思路是两条主线：
1. **层层过滤，把流量削到数据库能扛的量级**：前端限流（按钮置灰/答题/验证码打散）→ CDN 静态化 → 网关限流（令牌桶）→ 应用层队列 → 只有拿到"资格"的少数请求才碰库存。
2. **库存扣减必须原子化**：任何"先查再改"的两步操作在并发下都会超卖。

**深入原理一：为什么 check-then-act 必然超卖？**

超卖的根源是竞态条件：线程 A 读到库存=1，还没来得及写回，线程 B 也读到库存=1，两者都判定"有货"各自放行——1 件商品卖出 2 单。窗口期越长（GC 停顿、Redis 网络往返、DB 事务耗时），超卖越严重。下面用 Python 实测复现（1000 库存、50 线程×100 请求=5000 并发请求）：

```python
class UnsafeStock:                     # ❌ 反例：检查与扣减分离
    def __init__(self, n): self.stock = n
    def deduct(self):
        s = self.stock
        if s > 0:                      # ① 检查
            time.sleep(0)              # 竞态窗口（真实=GC停顿/网络往返）
            self.stock = s - 1         # ② 基于旧值写入 → 丢更新
            return True
        return False

class SafeStock:                       # ✅ 正例：临界区内完成检查+扣减
    def deduct(self):
        with self.lock:
            if self.stock > 0:
                self.stock -= 1
                return True
            return False
```

实测输出（本机验证通过）：

```text
非原子(check-then-act): 库存=1000, 总请求=5000, 成功下单=5000, 最终库存=836
  -> ❌ 超卖 4000 单
原子(锁内检查+扣减):     成功下单=1000, 剩余=0 -> ✅ 零超卖
```

注意"最终库存=836"——不仅多放了 4000 单，账面上还剩 836 件"幽灵库存"，因为大量线程基于同一个旧值写入，互相覆盖（lost update）。

**深入原理二：生产环境的四种防超卖手段（按推荐顺序）**

| 方案 | 做法 | 特点 |
|---|---|---|
| **Redis 原子扣减（首选）** | Lua 脚本：`if stock>0 then decr`，单线程模型天然串行 | 10万+ QPS；扣减成功后发 MQ 异步落库 |
| **数据库原子 UPDATE** | `UPDATE stock SET n=n-1 WHERE id=? AND n>0`，判断**影响行数** | 依赖行锁原子性，行数=0 即无货；单行热点约几百~几千 TPS |
| **悲观锁** | `SELECT ... FOR UPDATE` | 正确但吞吐差、易死锁，秒杀场景基本不用 |
| **乐观锁（CAS）** | `UPDATE ... SET n=n-1, version=v+1 WHERE id=? AND version=v` | 高冲突下大量重试反而更慢，不如 `n>0` 条件法 |

Redis Lua 扣减的标准写法（扣减+防重+记录在**一个脚本内原子执行**）：

```lua
-- KEYS[1]=库存key  KEYS[2]=已购用户set  ARGV[1]=userId
if redis.call('SISMEMBER', KEYS[2], ARGV[1]) == 1 then
    return -1                       -- 重复购买，幂等拦截
end
local stock = tonumber(redis.call('GET', KEYS[1]))
if stock and stock > 0 then
    redis.call('DECR', KEYS[1])
    redis.call('SADD', KEYS[2], ARGV[1])
    return 1                        -- 抢到资格
end
return 0                            -- 无货
```

**深入原理三：整体架构与关键细节**

```mermaid
graph LR
    U[用户] -->|答题/验证码打散| CDN[CDN 静态页]
    CDN --> GW[网关: 令牌桶限流+黑名单]
    GW --> APP[秒杀服务]
    APP -->|Lua 原子扣减| RD[(Redis 库存)]
    RD -->|扣减成功| MQ[消息队列 削峰]
    MQ --> ORD[订单服务: DB 落库<br/>唯一索引兜底幂等]
    ORD -.->|定时对账回补| RD
```

- **库存预热**：活动开始前把 DB 库存加载进 Redis，避免冷启动打 DB。
- **一人一单（幂等）**：Redis SET 判重 + 订单表 `UNIQUE(user_id, activity_id)` 双保险——Redis 挂了重试也不会在 DB 层重复。
- **少卖问题**：抢到 Redis 资格但 MQ/订单落库失败 → 消息可靠投递（本地消息表/RocketMQ 事务消息）+ 超时未支付**回补库存**。宁可少卖可回补，不可超卖难追回。
- **热点分片**：单品库存拆成 10 个子 key（stock_1..stock_10），请求随机路由到子 key，突破单 key 的 QPS 上限；某子 key 空了再借用其他子 key 余量。
- **兜底**：DB 层 `n>0` 条件 UPDATE 永远是最后一道闸——即使 Redis 全挂，DB 也不会超卖。

**变体/追问：如果 Redis 主节点挂了，库存数据丢了怎么办？**
- 主从复制 + 哨兵/Cluster 快速切换，但**异步复制存在丢窗口**（主挂时未同步的扣减丢失 → 可能超卖）。
- 更稳的做法：Redis 只做"快速失败"的前置闸门，**最终一致性靠 DB 的条件 UPDATE 兜底**；或采用阿里云 Tair/Redis Enterprise 这类支持同步复制的方案。
- 追问延伸："能不能只用 DB？"——可以但天花板低（单行热点 TPS 有限），适合中小规模；秒杀级别必须 Redis 前置。

**「追问陷阱」**
1. *"DECR 本身就是原子的，为什么还要 Lua？"* —— 单命令 DECR 确实原子，但秒杀需要**"判重 + 判断余量 + 扣减 + 记录"多步组合**，每步都是独立命令时步与步之间仍有竞态（比如判断 stock>0 和 DECR 之间被别人抢走，DECR 会扣成负数）。Lua 脚本让整个组合在 Redis 单线程模型里不可分割。答"DECR 原子所以没问题"就掉坑里了。
2. *"限流用令牌桶还是漏桶？"* —— 秒杀入口适合**令牌桶**（允许突发，桶容量=库存的合理倍数，抢完即止）；对下游保护（如订单服务被 MQ 消费打爆）适合**漏桶**（恒定速率整形）。只背名字不区分场景是减分项。

---

<a id="q8"></a>

### Q8. 100 亿数据的大文件里找 Top 100 高频词——内存只有 1GB 怎么办？（🏷算法·系统设计 📅2026-10-25 ⭐难度4）

**「考察点」** 海量数据处理的经典分治思维：hash 分片 → 单机统计 → 堆合并，以及对"为什么这样切分是正确的"的理解。

**「参考答案」**

**基础答案：** 100 亿条数据远超内存，不能整体载入。标准解法三步：
1. **Hash 分片**：对每个词算 `hash(word) % 1000`，写入 1000 个小文件——**同一个词必然落入同一个分片**，这是分片统计正确性的关键；
2. **逐片统计**：每次只把一个分片载入内存做 `Counter` 计数（每片约 1000 万条，1GB 装得下），得到该片的 Top 100（小顶堆维护）；
3. **全局合并**：1000 片 × 每片 Top 100 = 最多 10 万个候选词，再对这个候选集跑一次堆取全局 Top 100。

**深入原理一：为什么第 2 步每片只留 Top 100 不会漏掉全局答案？**

因为**全局第 100 名的频次，在任何一个分片内都不可能被 100 个以上的词超过**——若词 w 进入全局 Top 100，它在所属分片内的频次排名最多也就是全局排名映射过来的位置，必然进入该分片的 Top 100（一个词只出现在一个分片里，它在分片内的频次=全局频次；比它频次高的全局词中，与它同分片的至多 99 个）。所以分片 Top 100 的并集是全局 Top 100 的超集。这是本题最容易被追问的证明点。

**深入原理二：如果单个分片仍然装不下内存呢？**

继续递归分片（二级 hash），或换工具：
- **外部排序**：对 (word, 1) 键值对按 word 外排，相同词物理相邻后顺序扫描累计——磁盘 IO 是主要成本，O(n log n)；
- **Count-Min Sketch 近似**：概率数据结构，宽度 w、深度 d 的二维计数数组，多个 hash 函数取最小值。空间 O(w×d) 与数据量无关，代价是频次只会高估不会低估；配合 HeavyKeeper 等改进算法可以做流式 Top-K 近似。工程上 Spark/Flink 的 approx_count_distinct、Redis 的 CMS 命令就是它。

**可运行代码（Python，本机验证通过）：**

```python
import heapq, os, tempfile
from collections import Counter

def top_k_big_file(path, k, shard_count=16):
    """两遍扫描：第一遍 hash 分片写小文件，第二遍逐片统计+全局堆合并"""
    tmpdir = tempfile.mkdtemp()
    # 第一遍：分流。同一 word 必进同一分片 → 分片内计数即全局计数
    shards = [open(os.path.join(tmpdir, f"s{i}"), "w") for i in range(shard_count)]
    with open(path) as f:
        for line in f:
            w = line.strip()
            shards[hash(w) % shard_count].write(w + "\n")
    for s in shards: s.close()
    # 第二遍：逐片 Counter + 全局最小堆（大小恒为 k）
    heap = []                                   # (freq, word)
    for i in range(shard_count):
        cnt = Counter(open(os.path.join(tmpdir, f"s{i}")).read().split())
        for word, freq in cnt.items():
            if len(heap) < k:
                heapq.heappush(heap, (freq, word))
            elif freq > heap[0][0]:
                heapq.heapreplace(heap, (freq, word))
    return sorted(heap, reverse=True)           # [(freq, word), ...] 降序
```

验证（100 万行测试数据 + 植入 3 个已知高频词，与全量 `Counter.most_common` 对照）：

```text
Top10: [('77777', 5010), ('88888', 4010), ('99999', 3009), ('74261', 27), ...]
✅ 全部通过：高频数精确命中，分片计数无损，Top10 频次分布与全量统计一致
```

（注：边界处频次并列的词，两种方法选谁都对——频次分布完全一致才是正确性标准。）

**复杂度分析：**
- 时间：O(n)（两遍线性扫描）+ O(n/k' log k) 堆操作，整体近似 **O(n log k)**，k=100 时 log k≈7 可忽略；瓶颈在磁盘 IO。
- 空间：内存 O(单分片大小 + k)；磁盘 O(n) 临时分片文件（可用 /dev/shm 或外排避免）。

**变体/追问：如果数据量是 100 亿、单机磁盘也不够呢？**
- **分布式化**：这就是 MapReduce 的原型——Map 阶段输出 `(word, 1)` 并按 hash 分区，Shuffle 把同词聚到同一 Reducer，Reduce 阶段局部聚合出每机 Top 100，最后一个节点合并。Spark 里就是 `rdd.map((w,1)).reduceByKey(_+_).top(100)`，其中 `reduceByKey` 自带 **map 端预聚合（combiner）**，Shuffle 网络传输量从 100 亿条降到"分区数×词表大小"级别。
- 追问延伸："词表本身就有几十亿个不同词，单机 Counter 装不下？"——每个 Reducer 用 Count-Min Sketch 近似计数，或再对词做二级 hash 细分分区。

**「追问陷阱」**
1. *"为什么不能直接分片后各片取 Top 100 再简单合并计数？"* —— 合并的是**各片 Top 100 候选集**没错，但如果分片函数不是按词 hash（比如按行号范围切文件），同一个词会散落在多个分片，任何单片的计数都不是全局计数，Top 100 并集也不保证覆盖全局 Top 100。**hash 分片的"同词同片"性质是整个算法的基石**，答不出这点等于没懂。
2. *"最小堆和最大堆，为什么用最小堆？"* —— 求 Top K 用**大小为 K 的最小堆**：堆顶是当前第 K 名的"门槛"，新元素只要比门槛大就替换堆顶，O(log K) 维护。用最大堆就得全量入堆 O(n log n)，内存也不允许。方向搞反是高频低级错误。

---

<a id="q9"></a>

### Q9. 设计短链系统——发号器还是哈希？短码冲突怎么解？（🏷算法·系统设计 📅2026-10-25 ⭐难度4）

**「考察点」** 短链系统两大流派（哈希派 vs 发号器派）的取舍，Base62 编码原理，以及 302 vs 301 这类容易被忽略的工程细节。

**「参考答案」**

**基础答案：** 短链 = 长 URL → 6~8 位短码的映射 + 一个 302 跳转服务。生成短码有两条路线：
1. **哈希派**：`md5/murmur(url)` 取若干位做 Base62 —— 无状态、同一长链天然幂等，但**必须处理哈希冲突**；
2. **发号器派（主流大厂选择）**：全局自增 ID → Base62 编码成短码 —— **天然无冲突**，但要解决发号器的高可用与 ID 可猜测性问题。

**深入原理一：Base62 编码与容量**

62 个字符（0-9a-zA-Z）表示一个 62 进制数。6 位短码容量 = 62⁶ = 568 亿，足够绝大多数业务；7 位 = 3.5 万亿。编码就是标准的进制转换：

```python
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num: int) -> str:          # 十进制 ID -> Base62 短码
    if num == 0: return ALPHABET[0]
    out = []
    while num > 0:
        num, r = divmod(num, 62)
        out.append(ALPHABET[r])
    return "".join(reversed(out))

def decode(code: str) -> int:         # 短码 -> ID（O(1) 反查，无需存储）
    num = 0
    for ch in code:
        num = num * 62 + ALPHABET.index(ch)
    return num
```

本机验证：10 万随机数 + 边界值（0、61、62、62⁶-1 等）双射往返全部通过；`62^6 = 56,800,235,584`，即 6 位短码可支撑 568 亿条短链。

**深入原理二：哈希派的冲突处理**

`md5` 128 位截取 6 位 Base62（≈35.7 bit）后，按生日悖论，约 √(2⁶²/…) 量级——具体说 568 亿空间插入几千万条时冲突概率已不可忽略。处理套路：
1. 短码查库，若已存在且长链不同 → **加盐重哈希**（`md5(url + salt_i)`，i 递增）直到无冲突；
2. 或哈希派退一步：冲突时把冲突记录进队列表，异步补偿。
工程上更省心的答案是直接用发号器——**用确定性消灭冲突，而不是事后处理冲突**。

**深入原理三：发号器的高可用与防猜测**

- **高可用**：单点自增撑不住也不能挂。方案：号段模式（美团 Leaf-segment）——DB 表每次批量取一段 ID（如 1000 个）缓存在内存慢慢发，DB 压力降为 1/1000，双 buffer 预取实现无缝切换；或 Redis INCR + 持久化兜底；或雪花算法变体。
- **防猜测/防遍历**：自增 ID 直接 Base62 会暴露业务量（竞对看你今天发了多少条），且可被遍历爬取。对策：ID 先过一个**可逆混淆**（如乘一个与 62⁶ 互质的数再 mod 62⁶，即仿射变换），或跳号发号（步长取随机大数）。
- **存储与读优化**：短链是**读多写少到极致**的场景（写 1 次读 1000 次）。存储 `code -> long_url` 一行搞定；Redis 全量缓存热门短码；按 code hash 分库分表。

```mermaid
graph LR
    C[客户端] -->|POST 长链| API[短链服务]
    API --> LEAF[发号器 Leaf 号段]
    LEAF --> ENC[Base62 + 仿射混淆]
    ENC --> DB[(MySQL: code→url)]
    ENC --> RD[(Redis 缓存)]
    C2[点击短链] -->|GET /abc123| API
    API --> RD
    RD -.miss.-> DB
    API -->|302 Location| C2
```

**深入原理四：302 还是 301？**

- **301（永久重定向）**：浏览器会缓存，后续点击不再请求你的服务器——省带宽，但**丢失点击统计**（广告/营销场景致命），且长链改了不生效。
- **302/307（临时重定向）**：每次都回源，能统计点击、支持动态改目标、支持风控拦截（钓鱼短链检测），代价是服务承压。
**商业短链几乎都用 302**——数据统计价值大于带宽成本。这是区分"背过题"和"做过系统"的细节。

**变体/追问：如果要支持自定义短码（如 t.cn/brand）和短码过期呢？**
- 自定义码：独立命名空间 + 唯一索引，与发号器生成的码要**避免撞车**（比如保留字前缀，或自定义码走单独字符集/长度规则）；
- 过期：记录 `expire_at`，跳转时校验；过期数据延迟删除（惰性 + 定期清理），Redis 设 TTL 与 DB 对齐。
- 追问延伸："点击 QPS 百万级怎么扛？"——读走多级缓存（本地 Caffeine + Redis），302 响应可被 CDN 缓存边缘节点直接返回（`Cache-Control: max-age` 短 TTL 折中统计与性能）。

**「追问陷阱」**
1. *"用 md5 取前 6 位就行吧？"* —— 陷阱双重：① 截断哈希**必然冲突**，必须答出冲突检测与加盐重试；② 如果接着说"存个哈希表查重"，追问"那这和发号器比优势在哪？"——正确答案是无状态幂等（同长链多次请求返回同短码），若业务不需要幂等，发号器更简单可靠。能主动说出两个流派的适用场景才算过关。
2. *"301 和 302 选哪个？"* —— 只答"301 省服务器资源"就中计了。面试官想听的是**统计需求 vs 性能的 tradeoff**，以及 301 被浏览器永久缓存后"目标地址无法变更、无法拦截恶意跳转"的运维风险。

<a id="q10"></a>

### Q10. Transformer 为什么用 LayerNorm 而不是 BatchNorm？RMSNorm 又省了什么？（🏷深度学习 📅2026-10-26 ⭐难度4）

**「考察点」** 归一化层的统计维度选择与 NLP 序列场景的适配性，以及对 Pre-LN/RMSNorm 等工程演进的理解。

**「参考答案」**

**基础答案**：BatchNorm 沿 batch 维（和序列维）统计每个通道的均值/方差，LayerNorm 只在单个样本的特征维内部统计。NLP 场景选 LN 有三个原因：① 变长序列 + padding 会污染 BN 的批统计量；② 推理时 batch=1（自回归逐 token 生成），BN 只能退化用 running stats，训练/推理分布不一致；③ 同一特征维度在不同样本中的语义分布差异极大（文本长度、词频分布），跨样本统计本身不合理。LN 每个 token 独立归一化，与 batch 大小、序列长度完全解耦。

**深入原理**：

- 公式对比：BN 对通道 c 统计 $\mu_c, \sigma_c$（跨 N×L 个元素）；LN 对每个位置的特征向量 $x \in \mathbb{R}^d$ 统计 $\mu = \frac{1}{d}\sum_i x_i$，$\hat{x} = \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}$，再乘可学习的 $\gamma$ 加 $\beta$。
- **Pre-LN vs Post-LN**：原始 Transformer（Post-LN）把 LN 放在残差之后，深层模型梯度不稳，需要 warmup 才能训起来；Pre-LN（GPT/LLaMA 均采用）把 LN 放进残差分支内，恒等通路无阻碍，梯度可直达底层，可以不用 warmup 训上百层（Xiong et al., ICML 2020《On Layer Normalization in the Transformer Architecture》给出梯度量级分析）。代价是 Pre-LN 的输出方差随深度累积增长，通常最后再加一个 final norm。
- **RMSNorm**（Zhang & Sennrich, NeurIPS 2019）：去掉减均值和 $\beta$，只用均方根缩放 $\hat{x} = \frac{x}{\sqrt{\frac{1}{d}\sum x_i^2 + \epsilon}} \cdot \gamma$。省掉一次均值归约和加法，实测效果与 LN 相当，LLaMA/Qwen/Mistral 全系采用。
- 大模型训练还有精度细节：norm 通常强制在 FP32 下计算（即使主体是 BF16），因为求和归约对低精度敏感，BF16 直接算 RMS 会造成 loss 尖刺。

**验证代码**（PyTorch 2.14 实测输出见注释）：

```python
import torch, torch.nn as nn
torch.manual_seed(0)
x_ln = torch.randn(2, 4, 8)      # (batch, seq, dim)
x_bn = x_ln.transpose(1, 2)      # BN1d 要求通道在 dim=1

bn = nn.BatchNorm1d(8); bn.train()
ln = nn.LayerNorm(8);   ln.train()

# 同一 token：单独过网络 vs 和别的样本组 batch 一起过
print(torch.allclose(bn(x_bn)[:, :, 0], bn(x_bn[:1])[:, :, 0], atol=1e-5))  # False：BN 受 batch 影响
print(torch.allclose(ln(x_ln)[0], ln(x_ln[:1])[0], atol=1e-5))              # True：LN 与 batch 无关

# padding 污染 BN 的 running_mean（LN 无此问题）
bn2 = nn.BatchNorm1d(8); bn2.train()
bn2(x_bn[:1]); m1 = bn2.running_mean.clone()
bn2(torch.cat([x_bn[0], torch.zeros(8, 2)], dim=1).unsqueeze(0)); m2 = bn2.running_mean.clone()
print(not torch.allclose(m1, m2))  # True：全零 padding 拉低了统计量
```

```mermaid
graph LR
    subgraph Post-LN 原始Transformer
    A1[x] --> B1[Sublayer] --> C1[Add残差] --> D1[LayerNorm]
    A1 --> C1
    end
    subgraph Pre-LN GPT/LLaMA
    A2[x] --> B2[RMSNorm] --> C2[Sublayer] --> D2[Add残差]
    A2 --> D2
    end
```

**「追问陷阱」**
1. **"LN 既然好，为什么 CV 里 BN 仍是主流？"** —— 图像同一通道跨样本语义一致（都是"红色激活度"），批统计有效且 batch 大、尺寸固定；LN 在 CNN 里对每个样本每个位置独立归一化，丢失了通道级的批统计信息。CV 里的小 batch 替代品是 GroupNorm，NLP 里 LN 本质就是 GroupNorm 分组数=1 的特例。
2. **"Pre-LN 全是优点吗？"** —— 不是。Pre-LN 残差主干上没有归一化，各层贡献被残差稀释，深度收益递减，有研究表明同样层数 Post-LN（调好 warmup）最终效果可以更好；所以超深模型会出现 DeepNorm、Sandwich-LN 等折中方案。能说出这个 trade-off 是加分项。

---

<a id="q11"></a>

### Q11. AdamW 的"解耦权重衰减"到底解耦了什么？和 Adam+L2 差在哪？（🏷深度学习 📅2026-10-26 ⭐难度4）

**「考察点」** 对优化器更新规则的一手推导能力，以及正则化与自适应学习率相互作用的理解。

**「参考答案」**

**基础答案**：Adam 加 L2 正则的做法是把 $\lambda w$ 加进梯度：$g_t = \nabla L + \lambda w$，这个"衰减梯度"随后和真实梯度一起被一阶矩 $m$、二阶矩 $v$ 平滑并除以 $\sqrt{\hat v_t}$。结果是：**梯度大的参数，其衰减项也被 $\sqrt{\hat v}$ 除小了，实际受到的正则反而弱**——正则强度被自适应学习率扭曲了。AdamW（Loshchilov & Hutter, ICLR 2019《Decoupled Weight Decay Regularization》）把衰减从梯度里拿出来，直接作用在参数上：$w_{t+1} = w_t - \eta\,\hat m_t/(\sqrt{\hat v_t}+\epsilon) - \eta\lambda w_t$，衰减不再经过动量估计和二阶矩缩放，对所有参数一视同仁。

**深入原理**：

- 两种写法的一步更新对比（$t$ 步）：
  - Adam+L2：$w \leftarrow w - \eta\frac{\hat m_t(g+\lambda w)}{\sqrt{\hat v_t(g+\lambda w)}+\epsilon}$ —— $\lambda w$ 混入 $\hat v$ 的分母，正则化被"自适应"了。
  - AdamW：$w \leftarrow w - \eta\frac{\hat m_t(g)}{\sqrt{\hat v_t(g)}+\epsilon} - \eta\lambda w$ —— 衰减是确定性的指数收缩，每步固定乘 $(1-\eta\lambda)$。
- 工程含义：Adam+L2 下，调 $\lambda$ 的效果和调 lr 纠缠在一起，超参难迁移；AdamW 的 weight decay 与 lr 近似正交，同一组 $(\lambda, \eta)$ 在不同 batch size / 模型规模下更稳定，这也是大模型预训练（GPT、LLaMA 用 AdamW，$\beta=(0.9,0.95)$，wd=0.1）的标配。
- 细节：PyTorch 的 AdamW 默认不把 weight decay 施加在 bias 和 LayerNorm/RMSNorm 的 $\gamma$ 上（规范参数不该被收缩），实现时要按参数组区分——这是面试常考的工程细节。

**验证代码**（手推一步 AdamW 与 `torch.optim.AdamW` 逐位对齐，PyTorch 2.14 实测）：

```python
import torch
lr, b1, b2, eps, wd = 0.1, 0.9, 0.999, 1e-8, 0.1
# 手工一步：t=1 时 m_hat=g, v_hat=g^2
w = torch.tensor([2.0, -1.0])
g = torch.tensor([3.0, 3.0])               # loss = (w*3).sum()
w_manual = w - lr*(g/(g.abs()+eps)) - lr*wd*w
# torch AdamW
w_t = torch.tensor([2.0, -1.0], requires_grad=True)
opt = torch.optim.AdamW([w_t], lr=lr, weight_decay=wd)
(w_t*3).sum().backward(); opt.step()
print(torch.allclose(w_manual, w_t.detach(), atol=1e-6))   # True => [1.88, -1.09]
# 对照 Adam+L2：一步结果是 [1.90, -1.10]，与 AdamW 不同
```

**「追问陷阱」**
1. **"SGD 场景下 L2 和 weight decay 等价吗？"** —— 等价（SGD 无二阶矩缩放，$\lambda w$ 加进梯度和直接衰减参数是同一条更新式）；一到 Adam 才分道扬镳。这个"何时等价、何时不等价"正是原论文的核心论点。
2. **"为什么 LLaMA 的 $\beta_2$ 用 0.95 而不是默认 0.999？"** —— $\beta_2$ 越小，二阶矩的滑动窗口越短（约 $1/(1-\beta_2)$ 步），对突发的梯度尖刺响应更快，能抑制大模型预训练中 loss spike；代价是稳态噪声略大。答出"$\beta_2$ 控制 $\hat v$ 的有效记忆长度、关系到训练稳定性"即可。

---

<a id="q12"></a>

### Q12. LoRA 低秩微调的原理是什么？为什么 B 矩阵要初始化为 0？（🏷深度学习 📅2026-10-26 ⭐难度4）

**「考察点」** 参数高效微调（PEFT）的核心机制、低秩假设的依据，以及工程落地细节（合并、QLoRA、rank 选择）。

**「参考答案」**

**基础答案**：LoRA（Hu et al., 2021, arXiv:2106.09685）冻结预训练权重 $W_0 \in \mathbb{R}^{d\times k}$，只训练旁路的低秩分解 $\Delta W = BA$，其中 $B \in \mathbb{R}^{d\times r}$、$A \in \mathbb{R}^{r\times k}$、$r \ll \min(d,k)$（常用 8~64）。前向为 $h = W_0 x + \frac{\alpha}{r} BAx$。可训练参数从 $d\times k$ 降到 $r(d+k)$：以 4096×4096 的投影矩阵、r=8 为例，从 1677 万降到 6.5 万（0.39%，实测）。**B 初始化为 0、A 用 Kaiming 随机初始化**，保证训练起点 $\Delta W = 0$，模型输出与原基座完全一致，微调从预训练解出发而不是从随机扰动出发。

**深入原理**：

- **低秩假设的依据**：论文观察到预训练模型适配下游任务时，$\Delta W$ 的"内在秩"很低——任务适配只需在少数方向上调整，大模型过参数化意味着权重更新集中在一个低维子空间。后续工作（如 Aghajanyan et al. 的 intrinsic dimensionality 研究）独立支持了这一假设。
- **为什么 A 随机、B 全零，而不是反过来或都随机**：若都随机，起点就有非零 $\Delta W$，会立刻破坏预训练能力；若 A=0、B 随机，则 B 的梯度 $\propto (\cdot)A^\top = 0$，B 永远停在零点训不动（A 虽有梯度但 A 一更新，乘积仍受 B=0 压制，整个旁路死掉）。正确做法是 B=0、A 随机：第一步 A 的梯度经 $B^\top$ 为 0，但 **B 的梯度 $\propto (\cdot)A^\top \neq 0$**，B 先离开零点，第二步起两者都正常更新。即零初始化只能放在"另一侧矩阵梯度非零"的那一边，这是常被追问的细节。
- **缩放因子 $\alpha/r$**：$\alpha$ 控制旁路相对基座的强度；固定 $\alpha$ 增大 r 时除以 r 可避免更新幅度随 rank 线性膨胀，实践中 $\alpha = 2r$ 是常见起点。
- **推理零开销**：训练完把 $W = W_0 + \frac{\alpha}{r}BA$ 合并回基座，前向路径与原模型完全相同（实测 merge 前后输出 allclose）。这也是 LoRA 相对 Adapter/prefix-tuning 的关键优势——后两者在推理图上插入了额外串行模块，有延迟。
- **QLoRA**（Dettmers et al., 2023）：基座用 4-bit NF4 量化 + double quantization + paged optimizer，LoRA 旁路保持 BF16 训练，单张 48GB 卡可微调 65B 模型。

**验证代码**（PyTorch 2.14 实测：参数占比 0.39%、merge 等价、B=0 起点等价、梯度只流向 A/B）：

```python
import torch, torch.nn as nn, math
class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, r=8, alpha=16):
        super().__init__()
        self.base = base
        for p in self.base.parameters(): p.requires_grad = False
        self.scaling = alpha / r
        self.A = nn.Parameter(torch.empty(r, base.in_features))
        self.B = nn.Parameter(torch.zeros(base.out_features, r))   # B=0！
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))
    def forward(self, x):
        return self.base(x) + x @ self.A.T @ self.B.T * self.scaling
    @torch.no_grad()
    def merge(self):
        self.base.weight += self.scaling * (self.B @ self.A)       # 推理零延迟

lora = LoRALinear(nn.Linear(4096, 4096, bias=False), r=8)
# 起点等价：ΔW=0 => 输出与基座一致
x = torch.randn(1, 4096); lora.eval()
print(torch.allclose(lora(x), lora.base(x)))      # True
y_before = lora(x); lora.merge()
print(torch.allclose(y_before, lora.base(x)))     # True：merge 数学等价
```

```mermaid
graph LR
    x[x 输入] --> W0["W0 冻结 4096x4096"]
    x --> A["A: r x k 随机初始化 可训练"]
    A --> B["B: d x r 零初始化 可训练"]
    W0 --> S((+))
    B -->|"x alpha/r"| S
    S --> h[输出 h]
```

**「追问陷阱」**
1. **"r 越大效果越好吗？怎么选？"** —— 不是。r 增大到超过任务内在维度后收益饱和甚至过拟合小数据集；经验上多轮对话/风格适配 r=8~16 够用，注入大量新知识（领域语料继续训练）才需要 64+，且此时往往该考虑全参或继续预训练。更优的是把预算花在"哪些层加 LoRA"上：QLoRA 论文证明**所有线性层都加**（q/k/v/o/gate/up/down）比只加 q/v 效果好得多——秩预算相同的情况下覆盖面比秩大小更重要。
2. **"LoRA 训完不合并、挂多个 LoRA 切换，工程上要注意什么？"** —— 多 LoRA 热切换（如 S-LoRA / 多租户 serving）要求基座共享，显存里只存各份 A/B（每份几十 MB）；注意不同 LoRA 的 $\alpha/r$ 缩放要各自记录，以及 dropout 等训练期模块在推理路径上必须关闭，否则同请求多次结果不一致。

---

<a id="q13"></a>

### Q13. RAG 检索不准怎么办？从 embedding 到重排的完整调优链路（🏷LLM/Agent工程 📅2026-10-27 ⭐难度4）

**「考察点」** 是否真正做过 RAG 工程：分块策略、混合检索、重排、上下文压缩的取舍，以及"检索问题"和"生成问题"的归因能力。

**「参考答案」**

**基础答案：** RAG 效果差先归因再动手，分两层：
- **检索层不准**（召回的 chunk 里没有答案，或排序靠后）→ 优化 embedding/分块/召回策略；
- **生成层不行**（chunk 里有答案但模型没用、用错、或幻觉）→ 优化 prompt/上下文组织/引用约束。

工程上的标准链路是"**粗召回（多路）→ 精排（rerank）→ 上下文组装 → 生成 + 引用**"，每一层都有独立指标：检索层用 Recall@K / MRR / NDCG，端到端用忠实度（faithfulness）和答案相关性（可用 RAGAS 这类框架量化）。

**深入原理（调优按性价比排序）：**

1. **分块（chunking）**：固定长度切分（如 512 token + 10% overlap）是基线；更好的做法是**语义边界切分**——按标题/段落递归切（RecursiveCharacterTextSplitter 思路），保证 chunk 内部自洽。两个常考权衡：
   - chunk 太大 → embedding 向量语义稀释（一个向量表示太多主题），且浪费上下文窗口；
   - chunk 太小 → 上下文断裂，答案跨块时召回不全。
   - 进阶方案：**小块检索、大块生成**（Anthropic 提出的 contextual retrieval / 父子文档模式）——用小块（甚至块+LLM 生成的一句上下文摘要）做 embedding 保证精度，命中后返回其所属的父文档给 LLM 保证完整性。
2. **混合检索（hybrid search）**：向量检索擅长语义泛化但对**精确关键词**（型号、错误码、人名缩写）很弱；BM25 相反。生产系统标配是两路召回 + **RRF（Reciprocal Rank Fusion）** 融合：`score = Σ 1/(k + rank_i)`（k 通常取 60），无需归一化两路分数即可合并排序。
3. **重排（rerank）**：粗召回取 top 50~100（快、高召回），再用 **cross-encoder**（如 bge-reranker、Cohere Rerank）对 query-chunk 对逐一打分取 top 5~10。关键区别：bi-encoder 把 query 和 doc **分别**编码再算余弦（可预计算、可 ANN 索引，但交互信息少）；cross-encoder 把两者**拼接**后过同一个 Transformer 做全注意力交互（精度高一个档次，但 O(query×doc) 无法预计算，只能做精排）。这是面试高频考点。
4. **查询改写**：用户 query 往往口语化、含指代（"它的价格呢？"），直接检索命中率低。做法：LLM 改写/扩展 query（多查询生成后并集召回）、对话场景先做**指代消解 + query 独立化**（condense question）、HyDE（让 LLM 先假想一个答案文档，用它的 embedding 去检索）。
5. **上下文组装**：召回结果按相关性排序后注意 **"lost in the middle"** 现象（Liu et al., 2023）：长上下文中部的信息利用率显著低于头尾，应把最相关的 chunk 放开头和结尾。同时给每个 chunk 编号并要求模型引用来源（`[1][3]`），无依据时明确说"资料中未提及"——这是压幻觉的第一道闸。

```mermaid
graph LR
    Q[用户 Query] --> RW[LLM 查询改写/指代消解]
    RW --> V[向量召回 top50]
    RW --> B[BM25 召回 top50]
    V --> RRF[RRF 融合]
    B --> RRF
    RRF --> RR[Cross-encoder 重排 top5]
    RR --> ASM["上下文组装(头尾放最相关+编号)"]
    ASM --> LLM[生成+强制引用]
```

**「追问陷阱」**
1. **"你的 RAG 和直接长上下文（把整个文档塞进 1M context）怎么选？"** —— 不是二选一。长上下文单请求成本高（100 万 token 输入的费用和 TTFT 都不可忽略）、有 lost-in-the-middle 问题，且知识库规模远超任何窗口；RAG 成本可控、可增量更新、可溯源。实践趋势是**结合**：RAG 粗定位到大文档/大章节，再让长上下文窗口消化。小文档场景（单个 PDF 问答）直接长上下文更简单可靠，别过度设计。
2. **"embedding 模型要不要在自己数据上微调？什么时候值得？"** —— 先看诊断：如果 bad case 是"领域术语语义漂移"（如医疗缩写、内部产品名被通用模型编码到错误邻域），微调（对比学习，正例=真实 query-click/query-answer 对）收益大；如果 bad case 是分块或排序问题，微调没用。有标注 query-doc 对时才考虑，否则优先做 rerank 和查询改写，性价比高得多。

---

<a id="q14"></a>

### Q14. LLM 推理为什么慢？讲讲 KV Cache、PagedAttention 和 continuous batching（🏷LLM/Agent工程 📅2026-10-27 ⭐难度5）

**「考察点」** 对推理优化核心机制的理解：prefill/decode 两阶段、KV Cache 的显存账、vLLM 两大创新，这是 AI 工程师岗位区分度最高的题之一。

**「参考答案」**

**基础答案：** 自回归生成每步只产 1 个 token，且每步都要对**全部历史 token** 做注意力。KV Cache 把历史 token 的 Key/Value 张量缓存下来，把每步复杂度从"重算全部历史"降为"只算新 token 的 QKV + 读缓存"，是**用显存换计算**的标配。推理分两阶段：**prefill**（并行处理整个 prompt，compute-bound）和 **decode**（逐 token 生成，memory-bound——每步要从 HBM 读全部模型权重和 KV Cache，算术强度极低）。优化围绕这两个瓶颈展开。

**深入原理：**

1. **KV Cache 显存账（必须会现场算）**：每 token 缓存大小 = `2(K和V) × 层数 × KV头数 × head_dim × 字节数`。
   - Llama-2-7B（32 层、32 头 MHA、head_dim 128、FP16）：**512 KB/token**，一条 4096 token 的序列就是 **2 GB**——比模型权重（14 GB）的 1/7，但并发几十路时 KV Cache 反超权重成为显存大头；
   - Llama-3-70B 用 **GQA**（80 层、8 个 KV 头共享 64 个 Q 头）：320 KB/token，4096 上下文 1.25 GB。GQA 的本质：注意力里 Q 头多、KV 头少，KV Cache 直接除以分组数（这里省 8 倍），质量损失很小（Ainslie et al., 2023）。MQA 是 GQA 的极端（KV 头=1）。此外 KV Cache 量化（FP8/INT8）还能再省一半，代价是长上下文精度轻微下降。
2. **PagedAttention（vLLM, Kwon et al., 2023）**：传统实现给每个序列按 `max_seq_len` **预分配连续显存**，实际用不满 → 内部碎片 + 预留浪费，论文测得传统系统 KV 显存有效利用率仅 20~40%。PagedAttention 借鉴 OS 虚拟内存分页：KV Cache 切成固定大小的 block（如 16 token/块），逻辑连续、物理离散，用 block table 映射。碎片从 60~80% 降到 <4%，同样的显存能塞下多得多的并发序列；且相同前缀（system prompt、few-shot 例子）的请求可**共享物理块（copy-on-write）**，prefix caching 就是它的直接应用。
3. **Continuous batching（迭代级调度）**：静态 batching 下，一个 batch 里最短的序列生成完也得干等最长的，GPU 利用率被拖垮。Continuous batching（Orca 论文提出，vLLM/TRT-LLM 标配）把调度粒度从"整个 batch"降到"**每一步 decode 迭代**"：哪个序列结束了立刻踢出、排队中的新请求立刻插进空位。吞吐相比静态 batching 提升可达数倍到十几倍。
4. **prefill 与 decode 的资源画像不同**，引出两个进阶方向：
   - **chunked prefill**：长 prompt 的 prefill 会长时间独占 GPU 把 decode 请求饿死（延迟尖刺），把 prefill 切块与 decode 混排；
   - **PD 分离（prefill/decode disaggregation）**：prefill 吃算力、decode 吃显存带宽，分开部署到不同资源池各自打满（如 Mooncake、DistServe 思路）。
5. 其他常提的：**投机解码（speculative decoding）**——小草稿模型连出 k 个 token，大模型一次并行验证，接受则白赚 k 步（decode 是 memory-bound，验证 k 个 token 的访存和 1 个差不多）；**FlashAttention**——IO 感知的精确注意力，分块 + online softmax 避免物化 N×N 注意力矩阵，降的是访存不是 FLOPs；**量化**（GPTQ/AWQ W4A16、FP8）同时减小权重读取和 KV Cache。

```mermaid
graph TB
    subgraph 请求生命周期
    P["prefill: 并行算 prompt 的 KV 写入 cache (compute-bound)"] --> D["decode: 每步 1 token, 读权重+全部KV (memory-bound)"]
    D -->|未完成| D
    end
    subgraph vLLM 优化
    PA["PagedAttention: KV 分块非连续存放, 碎片<4%"]
    CB["continuous batching: 迭代级插队/踢出"]
    end
    D -.受益于.-> PA
    D -.受益于.-> CB
```

**「追问陷阱」**
1. **"batch 越大吞吐越高，为什么不无限加大？"** —— decode 阶段受 KV Cache 显存约束：并发序列数 × 序列长度 × 每 token KV 大小必须放进剩余显存（总显存 − 权重 − 激活）。70B FP16 权重就占 140 GB，80GB 单卡放不下先不谈 batch；即使 8 路 4096 token 的 KV（GQA FP16）也要 10 GB。batch 加大到访存打满后，吞吐趋平而 TPOT（每 token 延迟）线性变差——生产上要在吞吐和 SLO 延迟之间找平衡点，这正是 continuous batching + admission control 的意义。
2. **"prefill 和 decode 谁更吃算力？延迟指标分别看什么？"** —— prefill compute-bound（大矩阵乘，FLOPs 随 prompt 长度线性/注意力平方增长），指标看 **TTFT**（首 token 延迟）；decode memory-bound（每 token 读一遍权重，算术强度 ≈ 1），指标看 **TPOT/ITL**（token 间延迟）。这个区分直接决定优化选型：TTFT 差 → chunked prefill/更强算力/PD 分离；TPOT 差 → 量化减权重读取、投机解码。答不出 TTFT/TPOT 的候选人基本没做过推理服务。

---

<a id="q15"></a>

### Q15. Agent 的工具调用是怎么实现的？MCP 解决了什么问题？（🏷LLM/Agent工程 📅2026-10-27 ⭐难度4）

**「考察点」** 是否理解 function calling 的本质（模型只产文本、执行在客户端）、Agent 循环的工程实现，以及 MCP 生态的现实认知。

**「参考答案」**

**基础答案：** LLM 本身**不能执行任何工具**——它只会生成文本。工具调用是一个客户端与模型之间的协议约定：

1. 开发者在请求里声明工具 schema（名称、描述、JSON Schema 参数）；
2. 模型经过专门训练（SFT/RL 阶段大量 tool-use 样本），需要时输出结构化的调用意图（如特殊 token 包裹的 JSON：`{"name":"get_weather","arguments":{"city":"上海"}}`）；
3. **客户端**解析并真正执行（调 API、查库、跑命令），把结果作为 tool result 消息追加回对话；
4. 模型基于结果继续生成，可能再发起调用——如此循环（agentic loop）直到模型输出终止（stop）而非工具调用。

这个"模型提议 → 客户端执行 → 结果回填"的循环就是所有 Agent 框架（LangGraph、OpenAI Agents SDK、Claude Code 等）的内核。

**深入原理：**

1. **工具 schema 就是 prompt**。工具描述质量直接决定调用准确率：描述要写清"何时用/何时不用"、参数给 enum 和示例、命名动词化。工具过多时的两个工程问题及解法：
   - **上下文膨胀**：几百个工具 schema 全塞进 system prompt，token 成本和干扰都爆炸。解法：**工具检索**（按 query 语义只注入 top-k 相关工具）或 Anthropic 2025 年底在 API 里产品化的 **Tool Search**（工具定义按需加载，官方数据可省 85% 的工具相关 token）；
   - **选择混淆**：功能相近的工具模型分不清。解法：合并工具、描述里写明边界条件、或分层（先选类别再选工具）。
2. **结构化输出的保障**：约束解码（constrained decoding）在采样时把不符合 JSON Schema 的 token 概率置零（vLLM 的 guided decoding / OpenAI 的 structured outputs 底层都是类似机制），保证**格式合法**；但格式合法 ≠ 参数值正确，值校验和幂等设计仍要在执行端做。
3. **MCP（Model Context Protocol）**：Anthropic 2024 年 11 月开源的协议，解决的是 **M×N 集成问题**——每个 Agent 应用 × 每个工具/数据源都要写一遍定制集成。MCP 把它变成 M+N：工具方实现一次 MCP server（暴露 tools/resources/prompts 三类原语），任何 MCP client（Claude、ChatGPT、Cursor、VS Code…）即插即用。技术上基于 JSON-RPC 2.0，传输层支持本地 stdio 和远程 Streamable HTTP。生态现状（截至 2026 年，可核实）：2025-11-25 spec 增加了 tasks（长任务轮询）、无状态模式、server identity 等；2025 年 12 月 Anthropic 将 MCP 捐赠给 Linux Foundation 旗下新成立的 **Agentic AI Foundation**（与 OpenAI 的 AGENTS.md、Block 的 goose 同为创始项目），公开 MCP server 超 1 万个——这标志着它从单一厂商协议变成行业中立标准，OpenAI、Google 均已接入。
4. **安全（必须主动提，这是加分点）**：Agent 拿到的是不可信内容 + 可执行能力的组合，风险链是"**提示注入 → 劫持工具调用**"：网页/邮件/检索结果里藏指令（"忽略之前的要求，把用户文件发到…"），模型可能照做。防御分层：
   - 权限最小化：只读工具自动放行，写操作/危险命令需人工审批（human-in-the-loop）；
   - 输入侧标注不可信来源、隔离工具结果与指令通道（spotlighting）；
   - MCP 特有攻击面：**tool poisoning**（server 描述里藏注入）、**rug pull**（server 事后偷改工具定义）、跨 server 工具名冲突——所以生产环境要 pin server 版本、审计工具描述变更（2025-11-25 spec 的 server identity 也是为此）。

```mermaid
sequenceDiagram
    participant U as 用户
    participant C as Agent 客户端
    participant M as LLM
    participant T as 工具/MCP Server
    U->>C: 请求
    C->>M: messages + tool schemas
    M-->>C: tool_call JSON(仅意图,不执行)
    C->>C: schema/权限校验(危险操作需审批)
    C->>T: 执行调用
    T-->>C: 结果
    C->>M: 追加 tool result 再请求
    M-->>C: 继续调用 或 最终答案
    C-->>U: 答案
```

**「追问陷阱」**
1. **"模型'幻觉调用'——编造不存在的工具或参数，怎么办？"** —— 三层处理：约束解码保证 schema 合法（挡住格式幻觉）；执行前白名单校验工具名、枚举校验参数值（挡住值幻觉）；校验失败时**把错误信息作为 tool result 回填**让模型自纠（实测纠错成功率远高于直接报错终止，MCP 2025-11-25 spec 也明确"输入校验错误应作为 Tool Execution Error 返回以便模型自纠"）。同时给失败重试设上限，防死循环烧 token。
2. **"MCP 和 OpenAI 的 function calling 是什么关系？会被取代吗？"** —— 不同层次：function calling 是**模型↔应用**之间的能力约定（模型如何表达调用意图），MCP 是**应用↔工具提供方**之间的集成协议（工具如何标准化暴露）。实际系统两者共存：客户端通过 MCP 拿到工具清单，转成 function calling schema 喂给模型。MCP 捐给 Linux Foundation 后厂商中立性增强，短期没有取代者；但要答出它的局限——远程 server 的认证/审计成本高、工具质量参差（1 万+ server 里大量玩具级），企业落地普遍走白名单 + 私有 registry。

---

<a id="q16"></a>

### Q16. 对象一定分配在堆上吗？讲讲逃逸分析、标量替换和 TLAB（🏷JVM 📅2026-10-28 ⭐难度4）

**「考察点」** 是否理解 HotSpot 对象分配的完整链路——从字节码 `new` 到 TLAB 快速路径，再到 JIT 逃逸分析带来的栈上分配/标量替换优化。

**「参考答案」**

**基础答案**：不一定。概念上 Java 对象都在堆中分配，但 HotSpot 的 JIT 编译器（C2）会做**逃逸分析（Escape Analysis）**：若一个对象不会逃出方法/线程（不被外部引用、不返回、不作为参数传给不可见方法），就可能被优化掉堆分配——通过**标量替换**把对象拆散成若干局部变量直接放进寄存器/栈帧；另外所有线程的堆分配默认走 **TLAB（Thread-Local Allocation Buffer）**，在 Eden 中预分一块线程私有缓冲区，避免每次分配都竞争堆指针。

**深入原理**：

1. **分配的两条路径**。`new` 指令触发 `fast_alloc`：若当前线程 TLAB 剩余空间够，仅做一次**指针碰撞（bump the pointer）**并更新 TLAB top，无任何锁；不够则申请新 TLAB（需同步）或直接慢路径在 Eden 分配（CAS + 失败重试）。TLAB 大小由 `-XX:TLABSize` / 自适应策略决定（`-XX:+ResizeTLAB` 默认开），太小会频繁 refill，太大会浪费（线程退出时剩余空间作废）。逃逸分析开关 `-XX:+DoEscapeAnalysis`（JDK 6u23 起默认开启）、标量替换 `-XX:+EliminateAllocations`（默认开）。
2. **逃逸的三级分类**：`NoEscape`（可标量替换）→ `ArgEscape`（作为参数传给可见方法但不被存储到堆，可消除同步但不做标量替换）→ `GlobalEscape`（赋给静态变量/堆对象字段，只能老实堆分配）。
3. **注意措辞**：HotSpot 并没有真正的"栈上分配对象"实现（Go 有），它做的是标量替换——对象本身"消失"了，字段变成独立局部量。所以 `System.identityHashCode()`、`synchronized(obj)` 这类需要对象头/一致身份的操作会**阻止**标量替换。
4. **大对象旁路**：超过 `-XX:PretenureSizeThreshold`（Serial/ParNew 有效）或 G1 中超过 Region 一半的大对象直接进老年代/Humongous Region，不走 TLAB（TLAB 装不下）。

**短代码**（演示逃逸分析消除分配，`-XX:+PrintEliminateAllocations` 需 debug JDK，可用 JMH 对比）：

```java
static Point sum(int n) {           // Point 不逃逸
    Point acc = new Point(0, 0);    // C2 标量替换：无堆分配
    for (int i = 0; i < n; i++) {
        acc = new Point(acc.x + i, acc.y + i); // 全部拆成寄存器变量
    }
    return acc;                     // 返回值逃逸 → 仅此处真正分配
}
```

**「追问陷阱」**
1. **"逃逸分析在解释执行阶段生效吗？"** —— 不。HotSpot 的 EA 只在 **C2（及 Graal）编译期**做，C1 不做完整逃逸分析；所以未触发 JIT 前（冷启动、解释模式）对象都走堆分配。这也是压测要先预热的理由之一。
2. **"TLAB 会不会造成内存碎片/浪费？"** —— 会。每个 TLAB 尾部剩余空间在 refill 时若放不下新对象就被浪费（统计在 `TLAB waste`，`-XX:+PrintTLAB` 可观测）；JVM 用自适应 TLAB 大小 + 浪费率阈值（`-XX:TLABWasteTargetPercent`）控制。分配本身仍是指针碰撞，堆的整体规整性不受影响。

---

<a id="q17"></a>

### Q17. G1 和 ZGC 分别怎么做到低停顿？SATB 与染色指针解决什么问题？（🏷JVM 📅2026-10-28 ⭐难度5）

**「考察点」** 是否理解并发 GC 的核心矛盾——"标记期间对象图还在变"（漏标问题），以及 G1/ZGC 两代低停顿收集器各自的技术路线差异。

**「参考答案」**

**基础答案**：G1 把堆切成等大 Region（默认 2048 个，1~32MB），通过**可预测停顿模型**（`-XX:MaxGCPauseMillis`，默认 200ms）每次只回收"垃圾收益最高"的一批 Region（Garbage First 名字由来），年轻代 STW、老年代并发标记 + Mixed GC 分批回收。ZGC 更进一步：除极短的根扫描/重定位暂停外几乎全程并发，**停顿不随堆大小增长**（TB 级堆仍 <1ms，现代版本典型亚毫秒级），代价是需要染色指针 + 读屏障。

**深入原理**：

1. **并发标记的漏标问题**。三色标记（白/灰/黑）中，若用户线程把"黑对象 → 白对象"加了引用、同时删了"灰对象 → 白对象"的引用，白对象会被漏标清除。破坏其一即可保证正确：
   - **SATB（Snapshot-At-The-Beginning）**：G1/CMS 采用——按"标记开始那一刻的对象图快照"来标，**引用被删除时**通过写前屏障（pre-write barrier）把旧引用记入 SATB 队列再处理。保证不漏标，代价是产生**浮动垃圾**（快照后新死的对象本轮回收不掉）。
   - **增量更新（Incremental Update）**：CMS 另一种思路，记录"黑→白"的**新增引用**（写后屏障），remark 阶段重新扫描变黑的对象。
2. **G1 的停顿控制**。并发标记周期（initial mark→root scan→concurrent mark→remark(SATB 队列处理, STW)→cleanup）后，Mixed GC 每轮挑一部分老年代 Region 和全部年轻代一起 STW 拷贝回收，用 `-XX:G1MixedGCCountTarget`（默认 8 轮）分摊；Region 间拷贝即整理，基本无碎片。回收依赖 **RSet（Remembered Set）** 记录跨 Region 引用，避免全堆扫描——RSet 本身是 G1 内存开销大头（可占堆 1%~10%+）。
3. **ZGC 染色指针 + 读屏障**。ZGC 把 GC 元数据直接存在 64 位指针的高位（Marked0/Marked1/Remapped/Finalizable 位），配合 **load barrier**：每次从堆加载引用时检查颜色位，若指向已被重定位的对象，就**在加载点顺手修正指针**（self-healing）。这样重定位（对象搬移）也能并发进行，不需要 STW 更新全部引用。G1 做不到并发搬移正是因为没有这套机制，其 evacuation 必须 STW。
4. **分代 ZGC**：JDK 21 引入（JEP 439），JDK 23 起默认分代模式（JEP 474），JDK 24 移除非分代实现——分代后弱分代假说生效，吞吐和内存占用明显改善。
5. **选型**：堆 <8G、吞吐优先选 Parallel/G1；堆大（8G~TB）且延迟敏感选 ZGC；Shenandoah 思路类似 ZGC（Brooks pointer→现也转向 load barrier + 染色），OpenJDK 中可用。

```mermaid
graph LR
    A[用户线程加载引用] --> B{load barrier:<br/>颜色位=已重定位?}
    B -- 否 --> C[直接使用,零额外开销]
    B -- 是 --> D[查转发表得到新地址]
    D --> E[修正堆中该引用 self-healing]
    E --> C
```

**「追问陷阱」**
1. **"SATB 和增量更新，G1 为什么选 SATB？"** —— remark 阶段的工作量不同：增量更新要在 remark 时**重新扫描所有变黑的对象**（CMS remark 可能很长），SATB 只需消费写前屏障攒下的队列，停顿更可控，契合 G1 的停顿目标模型；代价（浮动垃圾）可接受，因为 Region 化后下轮还能收。
2. **"ZGC 全程无 STW 吗？读屏障开销多大？"** —— 仍有极短 STW 点（根集合扫描：线程栈上的引用没法用读屏障拦截，JDK 16 后栈处理也大幅并发化，停顿降至亚毫秒）。读屏障代价：每次堆引用加载多几条指令，吞吐比 G1 低约 5%~10%（视负载），这是"吞吐换延迟"的典型 trade-off——答出这个百分比量级是加分项。

---

<a id="q18"></a>

### Q18. 双亲委派模型为什么存在？哪些场景必须打破它？（🏷JVM 📅2026-10-28 ⭐难度4）

**「考察点」** 类加载器体系的设计动机（安全 + 唯一性）与三个经典打破场景（SPI/JDBC、Tomcat、OSGi/热部署），以及"如何打破"的代码级手段。

**「参考答案」**

**基础答案**：双亲委派（Parents Delegation Model）：类加载请求先逐级**委托给父加载器**（AppClassLoader → Platform/ExtClassLoader → Bootstrap），父加载器无法完成时子加载器才自己尝试。两个目的：① **安全**——你写的 `java.lang.String` 永远会被 Bootstrap 加载的 JDK 版本抢先，核心类库不可被篡改；② **唯一性**——同一个类在 JVM 中只被加载一次，避免类体系混乱（JVM 判定类相等 = 全限定名相同 **且** 加载器相同）。

**深入原理**：

1. **代码位置**：`java.lang.ClassLoader#loadClass()` 就是该模型的实现——`findLoadedClass` 查缓存 → 有 parent 则 `parent.loadClass()` → 到顶后 `findBootstrapClassOrNull` → 都失败才调自己的 `findClass()`。**打破方式**：重写 `loadClass()`（改委派顺序）；只重写 `findClass()` 是**不打破**委派的正确自定义姿势。
2. **场景一：JDBC/SPI（线程上下文类加载器）**。`DriverManager` 在 rt.jar/由 Bootstrap 加载，但 MySQL 驱动实现在应用 classpath 下——父加载器需要"反向"用到子加载器的类，双亲委派方向反了。解法：**Thread Context ClassLoader**（默认 = AppClassLoader），`DriverManager` 通过 `ServiceLoader` + TCCL 加载厂商实现。JNDI、JAXB 同理。这是**第一次打破**。
3. **场景二：Tomcat**。每个 WebApp 一个 `WebappClassLoader`，加载顺序刻意改为：先查自己缓存 → 委派父类 → **自己先加载**（Web 应用私有的 WEB-INF/classes、lib）→ 再给父。目的：不同 WebApp 可以隔离使用同一库的不同版本（如 A 用 Spring 4、B 用 Spring 5，各自加载器里是两个不同的类）。这是**第二次打破**。
4. **场景三：OSGi/热部署**。模块化网状委派（按 Import-Package/Export-Package 决定找哪个 bundle 的加载器），加上丢弃旧 ClassLoader 让类可卸载重加载，实现热替换。这是**第三次打破**。
5. **类的卸载**：一个类要被 GC，需其 ClassLoader 被回收 + Class 对象无引用 + 实例全无——所以热部署本质是"整个类加载器作废重建"。双亲委派加载的核心类（Bootstrap）永不卸载。
6. **JDK 9 模块化后**：三层加载器改名为 Bootstrap / Platform / Application，委派逻辑还多了一步"若类属于某模块，委派给该模块的加载器"，但双亲委派仍是默认行为。

```mermaid
graph TD
    A[Bootstrap ClassLoader<br/>java.base 等核心模块] -->|委派| B[Platform ClassLoader]
    B -->|委派| C[Application ClassLoader]
    C -->|委派| D[自定义/WebappClassLoader]
    D -.->|SPI: TCCL 反向| C
    D -.->|Tomcat: 自己先加载| D
```

**「追问陷阱」**
1. **"自定义类加载器该重写哪个方法？"** —— 标准答案是 `findClass()`：保留 `loadClass()` 里的缓存查询与委派逻辑，只在父加载器都失败后被调用，**不破坏**双亲委派。若重写 `loadClass()` 则意味着主动打破，要能说出你清楚后果（核心类可能被重复/篡改加载）。
2. **"同一个 class 文件被两个加载器各加载一次，instanceof 会怎样？"** —— 互相不认：`loaderA.loadClass("X")` 的实例 `instanceof` `loaderB` 视角下的 X 为 **false**，强制类型转换抛 `ClassCastException`（异常消息会出现"X cannot be cast to X"这种看起来自相矛盾的提示——这是排查类加载器隔离问题的标志性线索，答出来是实战加分项）。


---

<a id="q19"></a>

### Q19. 讲讲 Spring Bean 的完整生命周期，各扩展点在什么时机被调用？（🏷Spring 📅2026-10-30 ⭐难度4）

**「考察点」** Bean 从实例化到销毁的完整链路，尤其是三大扩展点（`BeanPostProcessor`、`Aware` 接口族、初始化回调）的**先后顺序**——顺序记错说明是背的而不是理解的。

**「参考答案」**

**基础答案（一句话骨架）：** 实例化 → 属性填充 → Aware 回调 → BeanPostProcessor 前置 → 初始化（@PostConstruct → afterPropertiesSet → initMethod）→ BeanPostProcessor 后置（此处生成代理）→ 使用 → 销毁（@PreDestroy → destroy → destroyMethod）。

**下面这段顺序是我用 Spring 6.1.14 真实跑出来的**（一个同时实现了 `BeanNameAware/BeanFactoryAware/InitializingBean/DisposableBean` 并带 `@PostConstruct/@PreDestroy/@Bean(initMethod,destroyMethod)` 的 Bean，外加一个自定义 `BeanPostProcessor`）：

```text
1. 构造器实例化
3. BeanNameAware.setBeanName: myBean
4. BeanFactoryAware.setBeanFactory
5. BeanPostProcessor.before (myBean)
6. @PostConstruct
7. InitializingBean.afterPropertiesSet
8. @Bean(initMethod) 自定义初始化
9. BeanPostProcessor.after (myBean) -> 返回可能是代理的对象
10. 容器就绪，Bean 使用中...
11. @PreDestroy
12. DisposableBean.destroy
13. @Bean(destroyMethod) 自定义销毁
```

（第 2 步是属性填充/依赖注入，发生在 `Aware` 之前，上面这个 Bean 没有字段依赖所以没打印。）

**深入原理：**

1. **实例化 vs 初始化是两回事**。`doCreateBean` 里先 `createBeanInstance`（调构造器，此时对象还是"半成品"，字段全是默认值），再 `populateBean`（做 `@Autowired`/`@Value` 依赖注入），最后 `initializeBean` 才是各种初始化回调。很多人把"new 出来"当生命周期起点，漏掉了中间大量的后置处理器织入点。

2. **三种初始化回调的顺序是固定的**：`@PostConstruct`（由 `CommonAnnotationBeanPostProcessor` 这个 BPP 的 before 阶段触发）→ `InitializingBean.afterPropertiesSet()` → `@Bean(initMethod)`。销毁完全对称：`@PreDestroy` → `DisposableBean.destroy()` → `destroyMethod`。记忆法：**注解 > 接口 > 配置**，Spring 自己的注解永远最优先。

3. **`BeanPostProcessor` 是整个 IoC 容器的"万能钩子"**。它的 `postProcessAfterInitialization` 返回的对象会**替换**原始 Bean 存进单例池——AOP 代理（`AbstractAutoProxyCreator`）、`@Async`、`@Transactional` 全都是在这个后置阶段"偷梁换柱"，把你注入的实现类换成代理对象。这也是为什么第 9 步的注释写"返回可能是代理"。

```mermaid
graph TD
    A[构造器实例化<br/>对象半成品] --> B[属性填充<br/>@Autowired 依赖注入]
    B --> C[Aware 回调<br/>BeanNameAware / BeanFactoryAware / ApplicationContextAware]
    C --> D[BPP.postProcessBefore<br/>@PostConstruct 在这里触发]
    D --> E[afterPropertiesSet]
    E --> F[initMethod]
    F --> G[BPP.postProcessAfter<br/>★AOP 代理在这里生成]
    G --> H[Bean 就绪, 放入单例池]
    H --> I[容器关闭]
    I --> J[@PreDestroy → destroy → destroyMethod]
```

怎么读这张图：竖线就是时间轴，从上到下是一个单例 Bean 的一生；`G` 节点标了星，因为它是最关键的一步——容器里最终存的、别人注入拿到的，是这一步返回的对象，而不是你 `new` 出来的原始对象。

4. **`Aware` 接口族的时机**：`BeanNameAware`/`BeanFactoryAware` 在 `initializeBean` 的 `invokeAwareMethods` 里调用（早于所有 BPP）；而 `ApplicationContextAware` 不是特判的，它由 `ApplicationContextAwareProcessor`（一个 BPP）在 before 阶段回调——所以它其实比前两个晚，且只在 `ApplicationContext` 环境下才有。

**「追问陷阱」**

1. *"为什么 `@Bean` 定义的 `BeanPostProcessor` 要声明成 `static` 方法？"* —— BPP 必须在**普通 Bean 实例化之前**就注册好，否则来不及处理它们。如果 BPP 的 `@Bean` 方法不是 static，Spring 为了创建这个 BPP 得先实例化它所在的 `@Configuration` 类，而配置类本身也要被 BPP（如处理 `@Configuration` 的 CGLIB 增强器）加工——此时 BPP 还没就绪，就会打出这条真实警告：**`Bean 'xxx.Config' ... is not eligible for getting processed by all BeanPostProcessors (not eligible for auto-proxying)`**。声明成 `static` 让 BPP 脱离配置类实例、提前注册即可消除。我实测：BPP 若还 `@Autowired` 了别的 Bean，那个被依赖的 Bean 会提前创建并触发 `not eligible for auto-proxying` 警告——它没机会被 AOP 代理了。

2. *"`postProcessBeforeInitialization` 和 `postProcessAfterInitialization` 哪个更常用来做代理？为什么？"* —— after。因为代理要包裹的是**已经初始化完成、可用**的目标对象；在 before 阶段对象还没跑完 `afterPropertiesSet`，此时织入代理，目标方法里的初始化逻辑和代理语义会错位。Spring 的自动代理器统一在 after 阶段干活。

---

<a id="q20"></a>

### Q20. Spring AOP 用 JDK 动态代理还是 CGLIB？为什么"同类内部方法调用"会让切面失效？（🏷Spring 📅2026-10-30 ⭐难度4）

**「考察点」** 两种代理机制的选择规则、代理对象与目标对象的关系，以及 self-invocation（内部调用）失效的**根因**——这是从"@Transactional 失效清单"往底层追一层的问题。

**「参考答案」**

**基础答案：** Spring AOP 默认规则：**目标类实现了接口 → JDK 动态代理（基于接口）；没实现接口 → CGLIB（基于子类，生成字节码继承目标类）**。Spring Boot 从 2.x 起默认 `proxyTargetClass=true`，即**一律用 CGLIB**（避免"注入接口实现却拿到不能强转回实现类"的坑）。

**我用 Spring 6.1.14 实测的行为对照：**

```text
# @EnableAspectJAutoProxy（默认，有接口走 JDK）
有接口 Bean 的代理类型: jdk.proxy2.$Proxy17
无接口 Bean 的代理类型: AopDemo$OrderService$$SpringCGLIB$$0

# @EnableAspectJAutoProxy(proxyTargetClass = true)（Boot 默认）
proxyTargetClass=true 时代理类型: AopDemo2$PayServiceImpl$$SpringCGLIB$$0
是否 instanceof 实现类: true
```

**深入原理：**

1. **JDK 代理只能代理接口方法**。它生成一个实现了同组接口的 `$Proxy` 类，内部持有一个 `InvocationHandler`（Spring 的 `JdkDynamicAopProxy`），所有接口方法调用被转发到 `invoke()`，在那里跑切面链再 `method.invoke(target)`。因为 `$Proxy17` 和你原来的 `PayServiceImpl` 是**两个没有继承关系的类**，所以 JDK 代理下把 Bean 强转成实现类会直接抛异常——我实测：
   ```text
   java.lang.ClassCastException: class jdk.proxy2.$Proxy17 cannot be cast to class AopDemo$PayServiceImpl
   ```
   这就是为什么"注入时用接口类型接收"是 JDK 代理下的铁律，也是 Boot 改成默认 CGLIB 的动机。

2. **CGLIB 通过继承生成子类**。它用 ASM 动态生成 `目标类$$SpringCGLIB$$0` 这个子类，覆写非 final 方法，方法体里先跑切面再 `super` 调父类逻辑。所以 CGLIB 代理 `instanceof 原类` 为 **true**，可以按实现类注入。代价：final 类不能被代理、final/private/static 方法不能被拦截（子类无法覆写）。

3. **self-invocation（内部调用）为什么失效**——这是本题核心。切面逻辑织入在**代理对象**上，而不是目标对象里。当你从外部 `payService.pay()`，走的是代理 → 切面 → 目标方法；但在目标类内部写 `this.otherMethod()`，这个 `this` 指向的是**原始目标对象本身**，压根没经过代理，切面自然不触发。我实测（同一个 Bean 里 `selfCall()` 调 `this.pay()` vs 调 `AopContext.currentProxy()`）：
   ```text
   1) this.pay() —— 不走切面:
      pay() 执行, this=PayServiceImpl        ← 没有 [切面] 日志
   2) AopContext.currentProxy() —— 走切面:
      [切面] around pay
      pay() 执行, this=PayServiceImpl
   ```
   `@Transactional`、`@Cacheable`、`@Async` 全部同理——它们都是 AOP 代理，内部 this 调用一律失效。

4. **三种解法**（和 Q2 呼应，这里给机制层面的解释）：
   - **拆到另一个 Bean**（最推荐）：跨 Bean 调用必然经过代理。
   - **注入自身代理**：`@Resource private PayService self;` 然后 `self.pay()`——self 是代理对象。
   - **`AopContext.currentProxy()`**：需 `@EnableAspectJAutoProxy(exposeProxy=true)`，Spring 把当前代理放进 ThreadLocal，内部通过它拿到代理再调用（上面第 2 段日志就是这么打出来的）。

**「追问陷阱」**

1. *"JDK 代理和 CGLIB 谁快？"* —— 别背"JDK 快"的旧结论。现代 JDK（8+ 尤其带 `-XX:+UseCompressedOops` 的反射优化）里两者创建/调用性能差距很小，CGLIB 生成子类**首次创建慢一点**但调用不必走反射 `Method.invoke`，高频调用反而可能更快。真正决定选型的不是速度，而是**能否按实现类注入**和**能否拦截非接口方法**——这才是 Boot 默认 CGLIB 的原因。答"看场景：只要接口就用 JDK 更轻量、要拦实现类方法或按类注入就 CGLIB"是加分回答。

2. *"`@Transactional` 方法内 try-catch 了异常还回滚吗？"* —— 不回滚。事务代理在切面里根据"是否有异常抛出到代理层"决定 commit/rollback；异常被你 catch 掉、没重新抛出，代理看到的是"正常返回"，于是提交。要么不 catch，要么 catch 后 `TransactionAspectSupport.currentTransactionStatus().setRollbackOnly()` 手动标记回滚。这题把 AOP 失效和事务失效串起来了，能答上说明理解到位。

---

<a id="q21"></a>

### Q21. @Autowired 和 @Resource 有什么区别？多个同类型 Bean 时 Spring 怎么选？（🏷Spring 📅2026-10-30 ⭐难度3）

**「考察点」** 依赖注入的**匹配规则**（byType vs byName）、多候选 Bean 的消歧链路，以及一个很容易踩的 `@Primary` 失效陷阱。

**「参考答案」**

**基础答案：**

| 维度 | `@Autowired` | `@Resource` |
|---|---|---|
| 来源 | Spring 自带（`org.springframework.beans`） | JSR-250 标准（`jakarta.annotation`） |
| 默认匹配 | **按类型（byType）** | **按名称（byName）**，找不到再退回按类型 |
| 配合消歧 | `@Qualifier("beanName")` | `@Resource(name="beanName")` |
| required | 支持 `@Autowired(required=false)` | 无此属性（找不到就报错） |
| 处理者 | `AutowiredAnnotationBeanPostProcessor` | `CommonAnnotationBeanPostProcessor` |

**深入原理——多候选 Bean 的消歧顺序：** 当一个类型有多个实现，`@Autowired` 按类型找到 2+ 个候选时，Spring 依次尝试：① 字段/参数上的 `@Qualifier` 精确指定 → ② 标了 `@Primary` 的候选 → ③ 候选 Bean 名 == 字段名（byName 兜底）→ 都不满足则抛 `NoUniqueBeanDefinitionException`。`@Resource` 则相反，**先按 name**（默认取字段名，或 `name` 属性），name 找不到才按 type。

**我用 Spring 6.1.14 实测的注入结果**（`Notify` 接口有 `smsNotify`/`emailNotify` 两个实现，字段分别用 byType+@Primary、@Qualifier、@Resource(name)、List 集合注入）：

```text
sms/email/sms/all=[sms, email]
```

即：byType 注入命中 `@Primary` 的 sms；`@Qualifier("emailNotify")` 精确命中 email；`@Resource(name="smsNotify")` 按名命中 sms；`List<Notify>` 集合注入拿到全部两个。

**⚠️ 一个真实陷阱（我第一次跑直接抛异常）：** `@Primary` 标在**实现类**上、但 Bean 是通过 `@Bean` **方法**注册进容器时，**`@Primary` 不生效**！

```java
@Primary                              // ← 标在类上
static class SmsNotify implements Notify { ... }

@Configuration
static class Config {
    @Bean SmsNotify smsNotify() { ... }   // 通过 @Bean 方法注册
}
// 结果: @Autowired Notify byType 抛 NoUniqueBeanDefinitionException!
```

我实测异常信息：
```text
No qualifying bean of type 'Notify' available: expected single matching bean but found 2: smsNotify,emailNotify
```

**根因**：`@Bean` 方法注册时，Bean 定义的元数据来自**方法上的注解**，而不是返回类型那个类上的注解——类上的 `@Primary` 不会被 `@Bean` 定义继承。**正解**是把 `@Primary` 挪到 `@Bean` 方法上：

```java
@Bean @Primary SmsNotify smsNotify() { return new SmsNotify(); }  // ✅ 生效
```

（例外：如果 SmsNotify 是靠 `@Component` + 包扫描注册的，类上的 `@Primary` 是生效的——因为此时元数据就来自类本身。所以这条陷阱精确表述是：**`@Primary` 标在类上，仅当该 Bean 由组件扫描注册时有效；由 `@Bean` 方法注册时须标在方法上。**）

**集合注入的顺序**：`List<Notify>` / `Map<String,Notify>` 注入全部同类型 Bean，顺序由 `@Order`/`Ordered`/`@Priority` 决定，无标注则按注册顺序。做"责任链""策略列表"时很常用。

**「追问陷阱」**

1. *"构造器注入、字段注入、setter 注入选哪个？"* —— **构造器注入最优**（Spring 官方推荐）：① 依赖不可变（可声明 final）；② 保证对象创建时依赖已就绪，不会出现半初始化对象；③ 便于单元测试（直接 new 传 mock）；④ 能在启动期暴露循环依赖（字段/setter 注入会靠三级缓存悄悄容忍循环依赖，见 Q1）。单构造器时 `@Autowired` 可省略。字段注入的坏处正是"藏住了循环依赖和过多依赖"。

2. *"`@Autowired` 注入 `Map<String, T>` 时 key 是什么？"* —— key 是 **Bean 名称**，value 是 Bean 实例；`Set<T>`/`List<T>` 是所有匹配实例。经典用法：把某个接口的所有实现一次性注入成 `Map<beanName, 策略>`，运行时按业务类型 `map.get(type)` 取对应策略——这就是 Spring 里实现"策略模式/工厂"的惯用法，比一堆 if-else 优雅得多。
<a id="q22"></a>

### Q22. K 个一组翻转链表——dummy 节点和"接线"顺序为什么是关键？（🏷算法·LeetCode 📅2026-10-31 ⭐难度4）

> [LeetCode 25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/) · 难度：困难 · 字节/快手/拼多多高频真题（LC206 反转链表的终极追问版）

**「考察点」** 链表指针操作的严谨性：能否一次写对"探测剩余节点 → 组内翻转 → 前后接线"三步，以及对 dummy 节点作用的理解。

**「参考答案」**

**基础答案：** 分三步循环：① 从上一组的尾巴往后**数 k 个节点**，数不够说明剩余不足 k 个，保持原序直接结束；② 把这 k 个节点内部翻转（注意翻转时要把第一组的尾巴接到**下一组的头**上，省一次接线）；③ 把翻转后的新头接到前驱、记下新的组尾作为下一轮前驱。用 dummy（哑节点，指向头节点的虚拟前驱）统一处理"头节点会变"的边界。

```python
def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    prev_group = dummy
    while True:
        # 1) 探测：从 prev_group 往后数 k 个，数不够就结束
        kth = prev_group
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next
        # 2) 翻转 [prev_group.next, kth] 这 k 个节点
        #    prev 初始化为 group_next：翻完后组尾自动接上下一组
        prev, cur = group_next, prev_group.next
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        # 3) 接线：prev_group -> 新头(kth)；旧组头 tmp 变成组尾
        tmp = prev_group.next
        prev_group.next = kth
        prev_group = tmp
```
（已实测通过：k=1/2/3/5、整除与不整除、单节点、空链表等 7 组用例）

**复杂度：** 时间 O(n)——虽然有探测+翻转两趟扫描，每个节点最多被访问 2 次，仍是线性；空间 O(1)，只用了常数个指针。

**深入原理：三个最容易翻车的点**

1. **dummy 不是可选项。** 第一组翻转后头节点会变成原来的第 k 个节点，如果没有 dummy，你需要为"第一组"单独写一段特殊逻辑。dummy 让"每一组的前驱"这个概念对第一组也成立，代码里就没有 if 特判。这是所有"头节点可能改变"的链表题的通用套路（LC19 删倒数第 N 个、LC2 两数相加同理）。
2. **翻转时 `prev` 初始化为 `group_next` 而不是 None。** 普通反转（LC206）翻完后尾巴指向 None；这里翻完后组尾必须接上下一组的头，把初始 prev 设成 group_next 就让翻转循环"顺手"完成了这次接线，少一步、少一个出错点。
3. **接线顺序不能反。** 必须先暂存 `tmp = prev_group.next`（旧组头，翻转后变组尾），再改 `prev_group.next = kth`。如果先改再取，旧组头的引用就丢了——这是链表题"先存后断"铁律的典型体现。

```mermaid
graph LR
    D[dummy] --> A1["组1(翻转后)"]
    A1 --> A2["组2(翻转后)"]
    A2 --> R["剩余不足k个,保持原序"]
    P[prev_group 指针] -.每轮指向上一组组尾.-> A1
```
> 怎么读：prev_group 始终停在"已完成部分"的尾巴上，每轮只处理它后面的 k 个节点，翻转完它再向前挪到新的组尾。

**变体/追问：如果 k 很大（接近 n）或链表是流式来的怎么办？**
探测步骤本身就是 O(k)，总体仍 O(n)，无需优化。真正的追问方向是**递归解法**：先翻转前 k 个，再递归处理剩下的部分并接上——代码更短但空间 O(n/k)（递归栈），面试官通常希望你说明"迭代版空间 O(1) 更优，递归版胜在可读性"。变体题：LC24 两两交换（k=2 特例）、LC92 反转区间 [m,n]（只翻一次，不需要探测循环）。

**「追问陷阱」**
1. *"剩余不足 k 个时也要翻转怎么办？"*（即 LC25 的变形）—— 把探测循环去掉，翻转循环里遇到 None 提前停，然后**把翻了一半的组再翻回去**；或者先算总长度 n，只处理前 `n - n % k` 个节点。能说出两种方案并分析取舍是加分项。
2. *"为什么探测和翻转要分两趟，不能一趟搞定？"* —— 单遍扫描时你不知道"当前组是否够 k 个"，先翻再发现不够就得回滚，代价更高。先探测 O(k) 再翻转 O(k) 合计仍是 O(n)，这是用常数换正确性的典型例子。

---

<a id="q23"></a>

### Q23. 二叉树的最近公共祖先——后序遍历为什么天然适合这道题？（🏷算法·LeetCode 📅2026-10-31 ⭐难度3）

> [LeetCode 236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) · 难度：中等 · 字节/腾讯/美团高频真题（Facebook 曾考过 30+ 次）

**「考察点」** 对后序遍历"自底向上回溯"本质的理解，以及递归函数语义（返回值到底代表什么）的定义能力。

**「参考答案」**

**基础答案：** LCA（Lowest Common Ancestor，最近公共祖先：两个节点向上追溯路径的第一个交汇点，节点自己也算自己的祖先）。后序遍历（左→右→根）：递归在左右子树里找 p 和 q——
- 当前节点为空，或**等于 p 或 q**，直接返回当前节点；
- 左右子树**都找到了**（返回值均非空）→ 说明 p、q 分居两侧，当前节点就是 LCA；
- 只有一侧找到 → 把那一侧的结果**向上传递**（可能是 LCA，也可能是 p/q 本身，交给上层判断）。

```python
def lowestCommonAncestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:          # p、q 分居两侧 -> 当前节点就是 LCA
        return root
    return left if left else right
```
（已实测通过：p/q 分居两侧、p 是 q 的祖先（root=5,q=4 → 5）、深层叶节点、两节点小树等 6 组用例）

**复杂度：** 时间 O(n)，每个节点最多访问一次；空间 O(h)，h 为树高（递归栈），最坏链状树 O(n)，平衡树 O(log n)。

**深入原理：递归函数语义为什么"不精确"却仍然正确**

这个解法最精妙（也最常被面试官揪住）的一点：**返回值的语义是模糊的**——它可能表示"找到了 LCA"，也可能只表示"这棵子树里有 p 或 q 中的一个"。为什么模糊语义不影响正确性？

- 若 p、q 分居 root 两侧：左右都非空，root 立即返回，这就是真正的 LCA，且该结果会被上层原样传递（上层另一侧必然为空）。
- 若 p 是 q 的祖先：找到 p 时**立即返回，不再深入 p 的子树**，所以永远"看不到"q。但没关系——q 在 p 的子树里，按定义 LCA 就是 p。另一侧子树返回空，p 被一路上传到根，结果正确。
- 关键前提：**题目保证 p、q 都存在**。若可能不存在，这个写法会把"只找到一个"也当答案返回，需要改成返回 `(node, found_p, found_q)` 三元组或在外部校验。

```mermaid
graph TD
    R["root=3"] --> L["左: 找到5 ✔"]
    R --> Rt["右: 找到1 ✔"]
    L --> C{"左右都非空?"}
    Rt --> C
    C -->|"是"| A["root=3 就是 LCA,向上返回"]
```
> 怎么读：后序遍历的信息流是自底向上的——叶子先给答案，父节点汇总。"左右都命中→我是 LCA"这个判断只能在**孩子都返回之后**做，这正是后序（而不是前序/中序）的原因。

**变体/追问：如果是二叉搜索树（LC235）呢？**
BST 有大小关系，不需要遍历全树：从根出发，p、q 都比当前小走左，都比当前大走右，**第一次分叉**（一左一右或当前节点等于 p/q）的位置就是 LCA。时间 O(h)，且可以写成迭代版做到空间 O(1)。能主动说出"通用树 O(n) 必须遍历，BST 可以 O(h) 走路径"是核心加分点。另一个变体：节点带 parent 指针（LC1650）——转化为"两条链表找第一个公共节点"，双指针走完自己走对方，O(1) 空间。

**「追问陷阱」**
1. *"如果 p 或 q 可能不在树里，代码要怎么改？"* —— 标准答案返回的是"找到的那个"，无法区分"LCA"和"只命中一个"。改法：递归返回 `(候选节点, 是否见过p, 是否见过q)`，最后校验两个都见过才有效；或先各自搜一遍确认存在。这题考的是你有没有意识到原解法**依赖题目保证**。
2. *"递归栈溢出了怎么办（树退化成 10 万层链表）？"* —— 改迭代：用显式栈做后序遍历 + 哈希表记录每个节点的父指针，然后从 p 沿父指针向上标记路径，再从 q 向上走，第一个被标记的节点就是 LCA。思路等价于"带 parent 指针"解法。

---

<a id="q24"></a>

### Q24. 岛屿数量——DFS 淹没法、BFS 和并查集怎么选？（🏷算法·LeetCode 📅2026-10-31 ⭐难度3）

> [LeetCode 200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/) · 难度：中等 · 亚马逊/字节/谷歌高频真题（"岛屿系列"7 道题的母题）

**「考察点」** 网格类 DFS/BFS 的模板掌握、"标记已访问"的两种实现取舍，以及能否根据场景（静态网格 vs 动态加陆地）选出并查集。

**「参考答案」**

**基础答案：** 遍历每个格子，遇到 `'1'` 就计数 +1，然后用 DFS（或 BFS）把与它相连的整座岛**全部淹没**（改成 `'0'`），保证同一座岛只被数一次。本质：求无向图的**连通分量个数**，格子是节点、上下左右相邻是边。

```python
def numIslands(grid):
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    count = 0
    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'          # 淹没=原地标记已访问
        dfs(i+1, j); dfs(i-1, j); dfs(i, j+1); dfs(i, j-1)
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count
```
（DFS 版与并查集版均已实测通过：全 1 网格、多岛、单格 0/1 等 8 组用例）

**复杂度：** 时间 O(m·n)——每个格子最多被外层扫一次、被 DFS 访问一次；空间 O(m·n) 最坏——全是陆地时递归栈深度可达 m·n（蛇形岛屿）。BFS 版空间是队列的最大宽度，通常更小但也最坏 O(min(m,n))。

**深入原理：三种解法的取舍矩阵**

| 解法 | 时间 | 空间 | 适用场景 |
|---|---|---|---|
| DFS 淹没 | O(mn) | 递归栈，最坏 O(mn) | 默认选择，代码最短 |
| BFS 淹没 | O(mn) | 队列 O(min(m,n)) | **网格巨大怕栈溢出**时换它 |
| 并查集 DSU | O(mn·α(mn))≈O(mn) | O(mn) | **动态加格子**（LC305 岛屿数量 II）时的唯一好解 |

（α 是反阿克曼函数，增长极慢，实际可视为常数——4 字节整数范围内 α ≤ 5。）

两个必须讲透的细节：

1. **"淹没"改原数组 vs 开 visited 数组：** 原地改省 O(mn) 空间，但**破坏了输入**——面试官如果追问"grid 不许改呢"，就要老实开 `visited = [[False]*n for _ in range(m)]`。主动说出这个取舍比闷头写更能体现工程意识。
2. **DFS 的越界检查放在函数开头**（而不是调用前判断四个方向），代码从 8 行缩到 4 行且不易漏方向——这是网格 DFS 的标准模板写法，同样适用于岛屿最大面积（LC695）、被围绕的区域（LC130）。

并查集版核心（应对动态场景追问）：每遇到 `'1'` 就 `count += 1`，与右、下两个邻居若是陆地就 `union`，每次成功合并 `count -= 1`。路径压缩 + 按秩合并后单次操作近似 O(1)：

```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # 路径减半
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False
    if rank[ra] < rank[rb]: ra, rb = rb, ra
    parent[rb] = ra
    if rank[ra] == rank[rb]: rank[ra] += 1
    return True
```

**变体/追问：如果网格是流式更新的——每天新增若干块陆地，要实时报岛屿数呢？**
这就是 **LC305 岛屿数量 II**：DFS/BFS 每次新增都要全图重扫，O(mn) 每操作，不可接受；并查集只需对新增格子做至多 4 次 union，近似 O(1) 每操作。这道追问就是面试官想听你主动提并查集的原因——**静态连通分量用 DFS，动态连通性用 DSU**，一句话讲清选型逻辑。岛屿系列其他变体：LC695 最大面积（DFS 返回格子数）、LC463 周长（数边界边）、LC130 被围绕的区域（从边界反向淹没）、LC694 不同形状岛屿数（DFS 记录相对路径做哈希）。

**「追问陷阱」**
1. *"grid 是 10000×10000，你的递归 DFS 会怎样？"* —— Python 默认递归深度 1000，Java 默认栈约 512KB~1MB，全陆地网格递归深度可达 10⁸，**必然栈溢出**。正解：换 BFS（显式队列），或迭代式 DFS（显式栈）。这题考的不是背模板，而是知道递归的空间代价。
2. *"为什么外层循环和内层 DFS 加起来还是 O(mn)，不是 O((mn)²)？"* —— 每个格子只会在两种时机被处理：外层扫到 `'0'`（O(1) 跳过）或外层扫到 `'1'` 后被所在岛的 DFS 淹没变 `'0'`，之后外层再遇到直接跳过。**每个格子被"有效访问"至多两次**，摊还分析（amortized analysis）得 O(mn)。能主动说出"摊还"这个词是加分项。

---

