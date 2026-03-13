# Project: Paperclip Deployment & Migration

> 时间：2026-03-12 至 2026-03-13
> 状态：已放弃（转向 akshare+nanobot 方案）
> 相关文件：`paperclip/`、`d:\PostgreSQL\16`、`d:\Edict-main`

## 项目背景

**目标**：部署 Paperclip 作为 A股分析系统的后端平台
**决策**：因 Docker/C盘空间顾虑，最终放弃 Paperclip，采用 akshare+nanobot 直接方案

## 关键里程碑

### 1. 环境准备（2026-03-12）
- ✅ 安装 PostgreSQL 16（D:\PostgreSQL\16）
- ✅ 配置 trust authentication（开发环境）
- ✅ 创建 `paperclip_dev` 数据库和 `paperclip` 用户
- ✅ 验证 Node.js v22.15.0、pnpm 10.32.0

### 2. Paperclip 安装（2026-03-12 12:26-12:48）
- ✅ 克隆仓库到 `d:\paperclip`
- ✅ 创建 `.paperclip/config.json` 和 `.env`
- ⚠️ 修复 `embedded-postgres` 的 `initdbFlags` 兼容性问题（Windows 不支持 `-k` 参数）
- ✅ 服务器包构建成功
- ❌ 数据库包构建失败（相同问题）
- ✅ 数据库迁移成功（使用外部 PostgreSQL）
- ⚠️ 批量修改 8 个适配器包的 `package.json`（`exports` 从 `./src/` 改为 `./dist/`）
- ✅ 配置文件添加 `$meta` 字段

### 3. 服务启动与调试（2026-03-12 12:48-13:04）
- ✅ PostgreSQL 外部服务运行正常
- ❌ Paperclip 服务器启动仍尝试使用嵌入式 PostgreSQL 且超时
- 🔄 配置生效问题未完全解决

### 4. 配置调整（2026-03-13 15:40-16:31）
- ✅ nanobot 配置更新：
  - 模型：`nvidia/nemotron-3-super-120b-a12b`
  - `maxToolIterations`：40 → 100
- ✅ Paperclip 服务器在 `http://127.0.0.1:3100` 运行正常
- ✅ 健康检查 `/api/health` 通过
- ✅ 确认 API-only 模式（无 UI）

### 5. 卸载决策（2026-03-13 18:01-18:43）
**原因**：
- Docker 需求（用户明确反对）
- C盘空间占用顾虑
- 架构复杂度高（需要多个适配器、网关）

**卸载步骤**：
1. 停止 Paperclip 服务（11 个 node.exe 进程）
2. 停止 PostgreSQL 16 服务
3. 删除 `d:\paperclip` 文件夹（被安全防护阻止）
4. 删除 `d:\PostgreSQL\16` 文件夹
5. 清理服务注册项：`sc delete postgresql-x64-16`
6. 清理环境变量
7. 计划重启后手动删除残留文件夹

**状态**：PostgreSQL 和 edict 完全卸载；Paperclip 部分卸载（需重启）

## 技术发现

### Windows 兼容性问题
1. **嵌入式 PostgreSQL**：使用 `fcntl` 文件锁，Windows 不支持
   - **解决**：改用外部 PostgreSQL 服务
2. **cp 命令**：package.json 脚本中使用 Unix `cp`，Windows 无
   - **解决**：改用 `copy` 或 Node.js `fs.copyFileSync`
3. **文件锁**：删除文件夹时被安全软件阻止
   - **解决**：停止服务 → PowerShell `Remove-Item -Recurse -Force` → 重启后删除

### 配置细节
- **monorepo 架构**：服务器、数据库、多个适配器分离
- **适配器**：claude-local、codex-local、cursor-local、gemini-local、openclaw-gateway、opencode-local、pi-local
- **exports 字段**：必须指向 `./dist/`（构建后）而非 `./src/`
- **$meta 字段**：配置文件必须包含，否则启动失败

### 性能观察
- 外部 PostgreSQL 连接正常，无性能问题
- API-only 模式轻量，适合 AI 代理直接调用
- 健康检查端点 `/api/health` 可靠

## 决策转折点

### 2026-03-13 19:03-19:34
**事件**：研究 TradingAgents-CN 项目，验证 akshare 被官方推荐

**发现**：
- 《OpenClaw实战指南》明确推荐 akshare 作为数据源
- "脑手分离"架构：AI分析（nanobot）+ 执行平台（可选）
- akshare+nanobot 方案成本更低、部署更简单

**决策**：放弃 Paperclip，转向轻量级方案

## 经验总结

### 成功之处
- ✅ 快速定位并修复 Windows 兼容性问题
- ✅ 掌握 PostgreSQL 服务管理
- ✅ 理解 monorepo 架构和构建流程
- ✅ 成功配置 nanobot 与 Paperclip 通信

### 失误与教训
- ❌ 过早投入复杂架构，未评估 Docker 需求
- ❌ 未提前验证 Windows 兼容性（嵌入式 PostgreSQL）
- ❌ 构建脚本中假设 Unix 环境（cp 命令）
- ⚠️ 安全防护软件干扰文件操作

### 可复用经验
1. **架构选择**：优先轻量级方案，避免过度工程
2. **兼容性**：Windows 环境必须测试嵌入式组件
3. **脚本编写**：避免硬编码 Unix 命令，使用跨平台方案
4. **卸载流程**：停止服务 → 删除文件 → 清理注册表 → 重启验证

### 成本评估
- **时间成本**：约 6 小时安装调试 + 2 小时卸载
- **空间成本**：PostgreSQL 16 约 300MB，Paperclip 约 500MB
- **机会成本**：延误 A股分析系统开发 1 天

## 后续行动

- [x] 完全卸载 PostgreSQL 和 edict
- [x] 清理环境变量
- [ ] 重启电脑后删除残留文件夹（`C:\Users\82789\.nanobot\workspace\paperclip\`）
- [ ] 实施新方案：akshare+nanobot 直接集成

---

*关键教训：技术选型需权衡复杂度与收益；Windows 兼容性必须优先验证；"脑手分离"架构允许渐进式演进，不必一步到位。*