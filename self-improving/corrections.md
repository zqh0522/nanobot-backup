# Corrections Log - 用户纠正记录

> **重要**：每次用户纠正必须立即记录在此

## 2026-03

### 2026-03-13 21:15 - nanobot 安装来源误解
**用户原话**："之前误解了 workspace 仓库的作用，现已澄清 ✅"

**错误陈述**：
- 误以为 workspace git 仓库是 nanobot 安装来源
- 混淆了 PyPI 安装与本地仓库的关系

**正确事实**：
- nanobot 0.1.4.post4 从 **PyPI 官方** 安装
- Location: `C:\Users\82789\AppData\Local\Programs\Python\Python311\Lib\site-packages`
- workspace 仓库仅用于备份配置、技能、记忆文件
- 更新命令：`pip install --upgrade nanobot-ai`

**教训**：
- 关键信息必须用工具验证（pip show）
- 不凭猜测下结论
- 用户信任易碎，一次失误可能导致关系破裂

**行动**：
- ✅ 已记录到 MEMORY.md
- ✅ 更新了 nanobot 安装说明文档

---

### 2026-03-13 21:13 - 微信集成能力误判
**用户纠正**：微信无官方 API，第三方库不稳定；企业微信有官方 API

**错误陈述**：
- 未明确区分微信、企业微信的 API 差异
- 未强调第三方库的不稳定性

**正确认知**：
- 微信：无官方 API，itchat/wxauto 不稳定
- 企业微信：有官方 API，可集成（需企业账号）
- 替代方案：消息转发（Telegram/钉钉 → 微信）

**教训**：
- 区分相似概念时需明确边界
- 稳定性评估必须包含风险提示

---

*格式：日期时间 - 主题 | 用户原话 | 错误 | 正确 | 教训 | 行动*
*新增纠正时，按此格式追加*