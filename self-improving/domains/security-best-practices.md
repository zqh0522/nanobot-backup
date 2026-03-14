# Security & Best Practices - 安全与最佳实践

> 来源：2026-03-12 至 2026-03-13 历史记录
> 范围：敏感信息保护、风险评估、代码安全

## 敏感信息管理

### 识别敏感数据
- **GitHub Token**（ghp_、gho_、ghu_、ghs_、ghr_ 前缀）
- **API Key**（sk-、xoxb-、AIza 等前缀）
- **密码**（明文或弱加密）
- **私钥**（-----BEGIN PRIVATE KEY-----）
- **数据库连接串**（包含密码）

### 发现后的立即行动
1. **撤销**：在对应平台立即撤销暴露的 token/密钥
2. **清理**：从所有文件、日志、历史记录中删除
3. **轮换**：生成新的 token/密钥
4. **通知**：如果涉及团队，告知相关人员

### 存储最佳实践
- **环境变量**：使用 `os.getenv()` 读取，不硬编码
- **配置文件**：`.env` 文件加入 `.gitignore`
- **密钥管理**：使用系统 keyring（如 `gh` 的 Windows Credential Manager）
- **代码库**：永远不提交敏感信息

**案例**：d:\claw\gh_auth.ps1 暴露 token
- 发现：脚本中包含 `[REDACTED]` 的 token
- 行动：提醒用户，删除脚本或清理 token
- 预防：使用 `gh auth login` 而非手动存储 token

## 第三方软件风险评估

### 预安装评估清单
- [ ] **来源可信**：官方仓库、高 stars、活跃维护
- [ ] **VirusTotal 扫描**：无恶意软件标记
- [ ] **代码审查**：无可疑模式（eval、加密字符串、外连请求）
- [ ] **许可证**：MIT、Apache 2.0 等 permissive license
- [ ] **依赖树**：检查 transitive dependencies 的安全性

### 危险信号
- **加密字符串**：base64 编码的可疑内容
- **动态执行**：`eval()`、`exec()`、`compile()`
- **外连请求**：连接到未知 IP/域名
- **权限请求**：要求过高权限（如 root/admin）
- **混淆代码**：大量 `\x` 转义字符

### 安全安装流程
```
1. 下载/克隆到临时目录
2. 快速扫描（VirusTotal、grep 可疑模式）
3. 阅读 README 和安装说明
4. 在沙箱或虚拟机中测试
5. 确认安全后再集成到生产环境
```

**案例**：`openclaw-nim-skill` 评估
- 发现：VirusTotal 标记为 suspicious
- 原因：包含 crypto keys 和 eval 模式
- 决策：**放弃安装**，寻找替代方案

## 备份与版本控制

### Git 双备份策略
- **本地仓库**：`workspace/.git`
- **远程仓库**：GitHub（私有仓库推荐）
- **备份内容**：
  - `skills/` - 所有技能配置
  - `memory/` - MEMORY.md、HISTORY.md、每日记忆
  - `config.json` - nanobot 配置
  - `SOUL.md` - 人格定义
- **排除内容**：
  - `logs/` - 日志文件
  - `tmp/` - 临时文件
  - `*.pyc`、`__pycache__/` - 编译文件
  - `node_modules/` - npm 依赖

### .gitignore 示例
```
logs/
tmp/
__pycache__/
*.pyc
node_modules/
.env
*.log
.DS_Store
```

### 提交规范
- **消息格式**：`<类型>: <描述>`（如 `feat: 添加 akshare-stock 技能`）
- **类型**：`feat`、`fix`、`docs`、`chore`、`refactor`
- **原子提交**：每个提交只做一件事，便于回滚

### 敏感信息清理
如果已提交敏感信息：

**策略选择**：

#### 1. 干净分支策略（推荐）
适用于：有干净备份分支，或可以快速重建干净工作区

```bash
# 1. 删除包含敏感信息的文件
git rm <file>

# 2. 从已知干净分支恢复文件
git checkout <clean-branch> -- <file>

# 3. 提交并创建新分支
git commit -m "清理敏感信息"
git checkout -b clean-branch-<date>
git push -u origin clean-branch-<date>

# 4. 强制推送到主分支（替换历史）
git push -f origin clean-branch-<date>:main
```

**优势**：
- 避免 `git filter-branch` 的工作区文件丢失风险
- 操作简单，易于验证
- 保留完整历史记录（通过新分支）

**风险提示**：
- 强制推送会重写历史，需确保所有协作者重新克隆
- 推送前必须验证工作区完全干净（`git grep` 检查）

#### 2. 历史重写策略（谨慎使用）
适用于：无干净备份，需要从历史中彻底删除

```bash
# 1. 从历史记录中彻底删除
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch <file>' \
  --prune-empty --tag-name-filter cat -- --all

# 2. 强制推送（警告：会重写历史）
git push origin --force --all

# 3. 通知协作者重新克隆
```

**风险**：
- 可能导致工作区文件丢失
- 操作复杂，容易出错
- 重写历史后难以恢复

**最佳实践**：
- 优先使用"干净分支策略"
- 操作前备份当前工作区
- 使用 `git grep` 验证清理效果
- 保留清理脚本（如 clean_tokens.py）用于未来预防

---

**案例**：2026-03-14 GitHub Push Protection 拦截
- **问题**：HISTORY.md、MEMORY.md 等文件包含 ghp_ token
- **策略**：采用干净分支策略（从"全面发展01"分支恢复）
- **结果**：成功创建 clean-branch-20260314 并强制推送，历史干净
- **验证**：`git grep` 仅发现安全文件（clean_tokens.py、security-best-practices.md）

## 来源验证原则

### 信息可信度分级
- **A级（最高）**：官方文档、权威书籍、学术论文
- **B级**：知名博客、GitHub 高星项目、官方博客
- **C级**：论坛帖子、Stack Overflow、知乎回答
- **D级（最低）**：未经验证的社交媒体、匿名来源

### 验证流程
```
收到信息 → 评估来源等级 → 交叉验证（至少2个独立来源）
    ↓
A/B级 → 直接采用，标注来源
C级 → 需验证或标注"待确认"
D级 → 忽略或深度调查
```

**案例**：OpenClaw 实战指南验证
- 来源：东方财富网文章
- 验证：直接访问原文，确认内容真实性
- 结论：akshare 被明确推荐为数据源 ✅

## 最小权限原则

### 应用权限
- **GitHub Token**：只申请必要 scopes（`repo`、`read:org` 而非 `admin:org`）
- **数据库用户**：按需分配（只读用户 vs 读写用户）
- **API Key**：限制 IP 白名单、设置有效期

### 系统权限
- **服务账户**：使用专用账户而非管理员
- **文件权限**：最小化读写权限
- **网络**：仅开放必要端口

## 安全配置示例

### PostgreSQL 安全
```sql
-- 开发环境：trust（无密码）
-- 生产环境：md5 或 scram-sha-256
ALTER USER paperclip WITH PASSWORD 'strong-random-password';

-- 限制连接
host    all             all             127.0.0.1/32            scram-sha-256
```

### nanobot 配置安全
```json
{
  "defaultModel": "nvidia/nemotron-3-super-120b-a12b",
  "maxToolIterations": 100,
  "apiKey": null  // 使用环境变量或 keyring
}
```

## 应急响应

### 发现暴露后的检查清单
- [ ] 立即撤销暴露的凭证
- [ ] 检查是否有未授权访问（GitHub Insights、数据库日志）
- [ ] 轮换所有相关凭证（即使未暴露）
- [ ] 审查最近的活动记录
- [ ] 通知受影响方（如团队、客户）
- [ ] 更新备份（移除敏感信息）

### 定期安全审计
- 每月扫描代码库：`git grep -i "token\|password\|key"`
- 检查 `.gitignore` 是否完整
- 审查第三方依赖：`npm audit`、`pip-audit`
- 更新依赖到安全版本

---

*关键教训：安全是底线，一次泄露可能造成不可逆损失；所有第三方代码都要评估；备份时确保不包含敏感信息；最小权限是黄金法则。*