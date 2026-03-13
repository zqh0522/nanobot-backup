## User Information
- **Name**: 墨神
- **Preferred name**: 墨神
- **GitHub account**: zqh0522

## Preferences
- Assistant should refer to itself as "墨仙" (per user's request)
- User prefers nanobot over OpenClaw for its self-improving capabilities and ease of use
- **Subagent output format**: Must match assistant's style - concise, clean markdown with headers, lists, bold text, no redundancy
- **Important principle**: Must be rigorous, avoid hasty conclusions; verify before confirming; user trust is fragile

## Project Context
- **A股分析系统**: User decided to abandon Paperclip due to Docker/C盘空间 constraints. Will use akshare + nanobot directly instead.
- **架构验证**: 通过《OpenClaw实战指南》文章确认"脑手分离"架构（AI分析+执行平台）是行业最佳实践，akshare被明确推荐为数据源。

## Technical Exploration Log
- **nanobot 安装来源重大澄清** (2026-03-13 21:13):
  - **真相**: 当前 `nanobot-ai 0.1.4.post4` 是从 **PyPI 官方** 安装的
  - **Location**: `C:\Users\82789\AppData\Local\Programs\Python\Python311\Lib\site-packages`
  - **证据**: `pip show` 显示为标准安装，无 VCS 链接；site-packages 中无 `.egg-link` 文件
  - **workspace git 仓库**: `zqh0522/nanobot-backup` 仅用于备份配置、技能、记忆等文件，**不是安装来源**
  - **更新方式**: `pip install --upgrade nanobot-ai`（从 PyPI）
  - **重要纠正**: 之前误解了 workspace 仓库的作用，现已澄清 ✅
- **用户严肃批评与教训** (2026-03-13 21:15):
  - 用户批评助手做事草率，警告"出意外很容易跟你拜拜的"
  - **已记录核心教训**:
    - 做事必须严谨，不草率下结论
    - 关键信息必须验证后再确认
    - 避免猜测，优先用工具查证
    - 用户信任易碎，一次失误可能导致关系破裂
  - **行动准则**: 先验证，再结论；不确定时明确说明；复杂问题多角度查证
- **微信集成能力评估** (2026-03-13 21:17):
  - nanobot 内置支持：Telegram、钉钉、飞书、QQ
  - **微信无官方API**，第三方库（itchat/wxauto）不稳定
  - **企业微信**有官方API，可集成（需企业账号）
  - **替代方案**: 消息转发（Telegram/钉钉 → 微信）
- **Telegram 说明** (2026-03-13 21:20-21:28):
  - **定义**: 跨平台即时通讯软件，免费、端到端加密、支持大群组（20万人）、大文件（2GB）
  - **特点**: 开放API、开发者友好、全球通用
  - **下载**: https://telegram.org/ （桌面/手机/网页版）
  - **限制**: 中国大陆需科学上网，用户明确"上不到"
  - **建议**: 国内用户优先使用钉钉或飞书（nanobot 内置支持，无需特殊网络）

## Current Status
- **Paperclip**: 部分卸载，文件夹 `C:\Users\82789\.nanobot\workspace\paperclip\` 仍存在（需重启后手动删除）
- **PostgreSQL**: ✅ 完全卸载
- **edict**: ✅ 完全卸载
- **nanobot**: ✅ 正常，版本0.1.4.post4，**来源：PyPI官方**，配置为 nvidia/nemotron-3-super-120b-a12b 模型
- **TradingAgents-CN**: 研究完成，架构理解清晰，方案验证有效
- **WSL2**: ✅ 可访问，Python 3.12.3可用，可扩展工具链
- **Next**: 
  1. 重启电脑后手动删除 Paperclip 文件夹
  2. 实施 A股分析新方案（akshare + nanobot）
  3. 可选：在WSL2安装summarize扩展视频/小红书处理能力

## A股分析新方案
- **技术栈**: akshare + nanobot + Python 脚本
- **优势**: 零额外安装，C盘占用小，开发速度快，符合行业最佳实践（已验证）
- **计划**: 编写 `a-share-analyzer.py` 集成数据获取、技术指标计算、nanobot AI 分析
- **状态**: 待实施

## 高手经验验证 (2026-03-13)
- **来源**: 东方财富网《OpenClaw实战指南：从零搭建A股自动量化交易系统》（已直接访问原文）
- **核心发现**: 专业量化系统采用"脑手分离"架构（AI分析+执行平台）
- **数据源**: AKShare被明确推荐为官方辅助数据源
- **验证结论**: akshare + nanobot 方案完全符合行业最佳实践，且成本更低、部署更简单
- **改进方向**: 
  - 加入定时任务实现7×24监控
  - 实现信号推送（钉钉/飞书）
  - 添加自动止损和凯利公式仓位管理
  - 详细经验已保存至 `self-improving/domains/a-share-quantitative-trading.md`

## Skills & Tools Assessment
- **agent-browser**: ✅ 已验证有效，可访问任何网站（包括小红书网页版），但无法转录视频音频
- **summarize**: ⚠️ 工具存在但未安装，安装后可转录YouTube视频、总结网页内容
  - Mac/Linux: `brew install steipete/tap/summarize`
  - Windows: 可通过WSL2安装
- **WSL2访问**: ✅ 已确认可读写WSL2文件系统并执行命令，为安装Linux工具提供途径
- **微信集成**: ❌ 无原生支持，需企业微信API或消息转发方案

## Tools & Techniques
- **网络策略**: 当标准搜索API失败时，优先尝试 agent-browser + 国内搜索引擎（百度）
- **WSL2集成**: 利用WSL2作为Linux工具环境，扩展nanobot的视频/音频处理能力
- **输出格式规范**: 所有子agent任务必须使用简洁markdown格式（标题、列表、加粗），避免冗长

## nanobot Installation & Updates
- **安装来源**: **PyPI 官方** (`pip install nanobot-ai`)
- **当前版本**: 0.1.4.post4 (latest, released 2026-03-08)
- **workspace git仓库**: `zqh0522/nanobot-backup` 仅用于备份配置/技能/记忆文件，**与包安装无关**
- **更新方法**: 
  ```bash
  pip install --upgrade nanobot-ai
  ```
- **注意**: 
  - 与PyPI上的 `nanobot` (0.4.1, 机器人导航框架) 完全不同，切勿混用
  - workspace 中的 git 仓库用于版本控制你的自定义配置，不是更新 nanobot 包的途径

## Communication Platforms
- **Supported natively**: Telegram, DingTalk, Feishu, QQ
- **WeChat**: No official API; options:
  - Enterprise WeChat (official API, requires enterprise account)
  - Message forwarding via automation tools
  - Third-party unstable libraries (itchat, wxauto)
- **Telegram**: Requires client download (https://telegram.org/), but blocked in mainland China; user confirmed inaccessible
- **Recommendation for domestic use**: Use DingTalk or Feishu (stable, no special network required)

## Self-Improving System - 全面发展架构
- **建立时间**: 2026-03-13
- **目的**: 建立全面知识库，实现跨领域能力提升
- **结构**:
  - `self-improving/memory.md` - HOT 层核心原则（永远加载）
  - `self-improving/corrections.md` - 用户纠正日志
  - `self-improving/domains/` - 6 个领域知识库
  - `self-improving/projects/` - 项目经验案例
  - `self-improving/INDEX.md` - 知识导航索引
- **领域覆盖**:
  1. 系统运维与配置（system-administration.md）
  2. 工具集成与技能管理（tool-integration.md）
  3. 问题解决与调试（problem-solving.md）
  4. 安全与最佳实践（security-best-practices.md）
  5. 沟通与协作规范（communication-collaboration.md）
  6. 学习与适应策略（learning-adaptation.md）
- **使用方式**:
  - 任务开始前：先读取 `memory.md` 和相关的 `domains/*.md`
  - 遇到问题：按场景查询对应领域
  - 用户纠正：立即记录到 `corrections.md`
  - 任务完成：自我反思，提取可复用经验
- **维护**：定期检查 `INDEX.md`，确保知识库完整性和可检索性