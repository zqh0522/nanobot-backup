# Tool Integration - 工具集成与技能管理

> 来源：2026-03-12 至 2026-03-13 历史记录
> 范围：技能安装、工具使用、平台集成

## 技能管理

### 技能发现与安装
- **技能目录**：`C:\Users\82789\.nanobot\workspace\skills\`
- **自动检测**：nanobot 启动时扫描 `skills/` 目录下的 `SKILL.md`
- **ClawHub 搜索**：使用 `clawhub` 技能搜索公共技能库
  ```bash
  clawhub search <keyword>
  ```
- **安装方式**：
  - 从 ClawHub：`clawhub install <skill-name>`
  - 手动：克隆仓库到 `skills/` 目录，确保包含 `SKILL.md`

### 技能评估标准
- **评分**：ClawHub 上的安装量、星标数（如 274 stars, 695 installs）
- **维护状态**：最后更新时间、issue 响应速度
- **安全性**：VirusTotal 扫描结果（警惕可疑模式）
- **兼容性**：Windows/Linux 支持、依赖要求

### 已安装技能清单
- ✅ `self-improving`（v1.2.16）- 自我改进核心
- ✅ `agent-browser-clawdbot` - 浏览器自动化
- ✅ `akshare-stock` - A股数据获取
- ✅ `china-stock-analysis` - A股分析推荐
- ⚠️ `summarize` - 未安装（需 Linux 环境）
- ❌ `tmux` - 未安装（需 Linux 环境）

## 核心工具使用模式

### agent-browser（浏览器自动化）
- **适用场景**：网页数据抓取、交互测试、搜索备用
- **核心能力**：
  - 获取页面快照（accessibility tree）
  - 基于 ref 的元素选择
  - 点击、输入、滚动
  - 提取结构化数据
- **典型流程**：
  1. `agent-browser open <url>`
  2. `agent-browser snapshot` → 获取元素列表
  3. `agent-browser click <ref>`
  4. `agent-browser extract` → 提取内容
  5. `agent-browser close`
- **优势**：绕过 API 限制，直接操作网页
- **局限**：无法处理视频/音频转录，需要人工解析页面结构

### akshare-stock（A股数据）
- **数据源**：AKShare 库（新浪、东方财富、腾讯等）
- **核心接口**：
  - `get_real_time_quotes(code)` - 实时行情
  - `get_historical_k_lines(code, period)` - K线历史
  - `get_financial_data(code)` - 财务报表
  - `get_sector_analysis()` - 板块分析
  - `get_fund_flows(code)` - 资金流向
- **依赖**：`pip install akshare`（首次需安装）
- **网络要求**：需要稳定连接，可能受防火墙影响

### china-stock-analysis（A股分析）
- **功能**：基于数据生成分析报告和买卖建议
- **输入**：股票代码（如 `600519.SH`）
- **输出**：技术指标、趋势判断、操作建议
- **使用建议**：与 `akshare-stock` 配合使用（前者提供数据，后者提供分析）

### pytdx（通达信数据接口）
- **用途**：连接通达信服务器获取实时行情
- **服务器列表**（已验证）：
  - 主服务器：`115.238.90.165:7709`（移动线路，最快，95%+成功率）
  - 备用服务器：7个其他 7709 端口 + 3个期货 7727 端口
- **数据限制**：
  - 实时 tick 数据仅限当天（无历史 tick）
  - 20 分钟线可获取历史数据
- **安装**：`pip install pytdx`
- **Windows 注意**：需确保防火墙允许出站连接

## 网络搜索策略

### 标准搜索失败时的备用方案
```
标准搜索（web_search）失败
    ↓
使用 agent-browser + 国内搜索引擎（百度）
    ↓
直接访问已知权威网站（如东方财富网、GitHub）
```

### 搜索技巧
- **精确查询**：使用引号 `"OpenClaw实战指南"`
- **多关键词**：`A股 量化 nanobot akshare`
- **排除干扰**：添加 `-spam -ad`
- **验证来源**：优先访问 .github.io、.org、官方文档

## 平台集成限制

### 支持的通信平台
- ✅ **Telegram**：需客户端，国内需科学上网
- ✅ **钉钉**：国内可用，官方 API
- ✅ **飞书**：国内可用，官方 API
- ✅ **QQ**：内置支持
- ❌ **微信**：无官方 API
  - 企业微信：有官方 API（需企业账号）
  - 个人微信：第三方库（itchat/wxauto）不稳定

### 集成建议
- **国内用户**：优先使用钉钉或飞书
- **消息推送**：通过钉钉/飞书 webhook 发送分析报告
- **指令接收**：设置群组机器人监听特定命令

## 安全评估工具

### VirusTotal 扫描
- **用途**：检测第三方软件/技能的安全性
- **使用**：上传文件到 virustotal.com 或使用 API
- **警惕信号**：
  - 加密字符串（crypto keys）
  - `eval()` 或动态代码执行
  - 可疑的网络连接
- **案例**：`openclaw-nim-skill` 因包含加密密钥和 eval 模式被标记

### GitHub 仓库评估
- **检查项**：
  - Stars 和 forks 数量
  - 最后更新时间
  - Issue 和 PR 处理情况
  - 作者信誉
  - README 完整性
- **风险信号**：
  - 无描述或文档
  - 大量未解决的 security alerts
  - 依赖可疑包

## 备份策略

### Git 双备份方案
- **本地仓库**：`C:\Users\82789\.nanobot\workspace\.git`
- **远程仓库**：`git@github.com:zqh0522/nanobot-backup.git`
- **备份内容**：`skills/`、`memory/`、`config.json`、`SOUL.md`
- **排除内容**：日志、临时文件、测试脚本
- **操作流程**：
  ```bash
  git add .
  git commit -m "描述"
  git push origin main
  ```
- **敏感信息处理**：推送前检查是否包含 token、密码等

---

*关键教训：工具集成前必须评估安全性和兼容性；网络搜索要有备用方案；Windows 环境需特别注意路径和权限；所有第三方代码都要扫描。*