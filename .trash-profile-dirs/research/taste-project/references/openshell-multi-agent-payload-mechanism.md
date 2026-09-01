# 案例：OpenShell「多 Agent 载荷」机制定位路径（2026-09-01）

任务类型：用户问「某项目的 X 能力是怎么实现的，是统一接口吗？」——需要在已克隆仓库里定位实现机制，并把结论写回已有的项目分析文档。仓库：`~/github/OpenShell`（Rust workspace，crates/ 布局）。

## 定位路径（对这种「能力封装机制」问题通用）

1. **先从文档里的名词反查代码符号**。分析文档里叫「Agent 载荷」，代码里没有这个词；实际入口是 `detect_provider_from_command`（从 CLI 命令 basename 推断 provider 类型）。用文档名词的近似英文（payload / harness / plugin / profile / registry）+ 已知产品名（claude / codex / opencode）做 grep 交叉定位。
2. **找注册表（Registry）就是找扩展点**。`ProviderRegistry::new()` 里 `registry.register(...)` 的列表直接给出全部内置支持对象——这比读 README 列举的「支持列表」可靠，且能看出哪些是简单声明（SPEC 常量）、哪些是复杂实现（独立 struct + trait impl）。
3. **trait 定义 = 抽象边界**。`ProviderPlugin` trait 的 4 个方法就是「接入一种新对象需要做什么」的最小完整答案；引用时直接贴 trait 签名，比转述准确。
4. **声明式配置和代码插件是两种不同扩展机制，要分开写**。OpenShell 同时有 Rust 插件（`crates/openshell-providers/src/providers/*.rs`）和内嵌 YAML Profile（`providers/*.yaml` 经 `include_str!` 编译进二进制）。回答「是不是统一接口」时，结论往往是「不是单一接口，而是 N 层各自独立的抽象点」——把每层的差异维度、抽象方式、位置列成对照表收尾。
5. **注意「仓库内部工具链」和「平台 API」的区分**。`scripts/agents/` 下有一套 harness 适配器机制（`agent.yaml` 清单 + `runtime/harnesses/<name>/exec.sh` bash 适配器，用 `OPENSHELL_AGENT_HARNESS` 环境变量选择），看起来像平台能力，实际只是仓库自用的启动器约定。写文档时必须标注它不属于平台 API，避免读者高估其通用性。
6. **写回已有分析文档时，节的位置跟着原文结构走**。新增「机制」一节放在「使用场景」之后、「用户故事」之前，并给已有「名词表」里的对应词条补一句指针，保持文档内部互相引用。

## grep 关键词备忘（Rust workspace 查扩展机制）

- `grep -rn "fn detect_\|Registry\|register(" crates/` — 找注册与自动检测
- `grep -rn "include_str!" crates/` — 找编译期内嵌的声明式配置
- `find scripts -name "*.yaml" -o -name "agent.yaml"` — 找仓库自用清单格式
- 读 trait 文件时连带看它的 blanket impl（如 `impl ProviderPlugin for ProviderDiscoverySpec`），能解释「简单情况只需一个常量」是怎么做到的。
