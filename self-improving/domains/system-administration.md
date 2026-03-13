# System Administration - 系统运维与配置

> 来源：2026-03-12 至 2026-03-13 历史记录
> 范围：环境配置、服务管理、故障排查

## 环境配置

### GitHub CLI 安装与认证
- **安装位置**：`d:\gh\bin\gh.exe`（需添加到 PATH）
- **PATH 配置**：使用 `pathAppend` 或系统环境变量
- **认证方式**：`gh auth login`（交互式）或 `gh auth refresh --with-token`（stdin）
- **Token 权限**：至少需要 `read:org`（组织访问）、`repo`（仓库）、`gist`、`user`
- **认证存储**：Windows 使用 Windows Credential Manager（keyring）
- **验证命令**：`gh auth status` 查看当前认证和 scopes

### nanobot 配置调整
- **配置文件**：`d:\claw\config.json` 或 `C:\Users\82789\.nanobot\workspace\config.json`
- **模型切换**：修改 `"defaultModel"` 字段（如 `"nvidia/nemotron-3-super-120b-a12b"`）
- **迭代限制**：修改 `"maxToolIterations"`（默认 40，建议 100）
- **重启生效**：配置文件修改后需重启 nanobot 服务

### 工作区迁移
- **检测当前工作区**：检查 `config.json` 中的 `workspace` 字段
- **迁移步骤**：
  1. 停止 nanobot 服务
  2. 复制整个 workspace 文件夹到新位置
  3. 更新 `config.json` 中的路径
  4. 删除旧工作区（确认无残留）
- **验证**：检查 `skills/`、`memory/` 等目录是否正常

## 服务管理

### PostgreSQL 服务
- **安装位置**：`D:\PostgreSQL\16`（默认）
- **服务名**：`postgresql-x64-16`
- **启动/停止**：
  - 命令行：`net start postgresql-x64-16` / `net stop postgresql-x64-16`
  - PowerShell：`Stop-Service postgresql-x64-16`
- **认证配置**：`pg_hba.conf` 中设置 `trust`（开发环境）或密码（生产）
- **重置密码**：以 postgres 用户登录执行 `ALTER USER postgres PASSWORD 'newpw';`
- **端口**：默认 5432
- **完全卸载**：
  1. 停止服务
  2. 删除安装目录
  3. `sc delete postgresql-x64-16` 删除服务注册
  4. 清理环境变量和 AppData

### Paperclip 服务
- **运行模式**：API-only（无 UI），端口 3100 或 3103
- **健康检查**：`GET http://127.0.0.1:3100/api/health`
- **数据库**：支持外部 PostgreSQL（推荐）或嵌入式（Windows 兼容性问题）
- **环境变量**：`DATABASE_URL`（如 `postgresql://user:pass@localhost:5432/dbname`）
- **停止服务**：查找并终止所有 `node.exe` 进程（`taskkill /f /im node.exe`）
- **完全卸载**：
  1. 停止服务
  2. 删除 `d:\paperclip` 或 `C:\Users\82789\.nanobot\workspace\paperclip`
  3. 清理环境变量
  4. 重启后删除残留文件夹（Windows 文件锁）

### Node.js 服务通用管理
- **进程查找**：`tasklist | findstr node.exe`
- **强制终止**：`taskkill /f /im node.exe`
- **端口占用**：`netstat -ano | findstr :3100`

## Windows 兼容性处理

### 文件锁问题
- **现象**：删除文件夹时提示"文件正在使用"
- **解决**：
  1. 停止相关服务/进程
  2. 使用 PowerShell `Remove-Item -Recurse -Force`
  3. 重启电脑后删除

### GNU 工具缺失
- **问题**：`cp`、`rm`、`ls` 等命令不可用
- **解决**：
  - 使用 Windows 原生命令：`copy`、`del`、`dir`
  - 或安装 Git Bash、WSL2
  - 修改脚本时避免跨平台命令

### 路径分隔符
- **使用**：`\`（Windows）而非 `/`
- **Python 代码**：使用 `os.path.join()` 或 `pathlib.Path`

## 故障排查流程

```
现象 → 检查服务状态 → 查看日志 → 验证配置 → 测试连接 → 修复
```

### 常用诊断命令
```batch
:: 服务状态
sc query postgresql-x64-16

:: 端口监听
netstat -ano | findstr :5432

:: 进程查找
tasklist | findstr <process>

:: 环境变量
echo %PATH%
set <varname>
```

### 日志位置
- **nanobot**：`C:\Users\82789\.nanobot\workspace\logs\`
- **PostgreSQL**：`D:\PostgreSQL\16\data\pg_log\`
- **Paperclip**：项目根目录 `logs/` 或控制台输出

---

*关键教训：Windows 环境需特别注意文件锁、PATH 配置、服务管理；所有配置变更后必须验证生效；卸载软件要彻底（服务+文件+环境变量）。*