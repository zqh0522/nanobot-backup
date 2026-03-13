# Problem Solving - 问题解决与调试

> 来源：2026-03-12 至 2026-03-13 历史记录
> 范围：故障诊断、调试技巧、多方案尝试

## 通用排查流程

```
问题现象 → 复现步骤 → 错误信息 → 日志分析 → 假设验证 → 解决方案
```

### 第一步：精确描述问题
- **现象**：什么行为不符合预期？
- **触发条件**：执行了什么操作？
- **错误信息**：完整复制错误输出（包括堆栈）
- **环境**：操作系统、Python 版本、相关包版本

### 第二步：检查基础状态
```batch
:: 服务是否运行
sc query <service-name>

:: 端口是否监听
netstat -ano | findstr :<port>

:: 进程是否存在
tasklist | findstr <process>

:: 文件是否存在
dir <path>

:: 环境变量
echo %<VARNAME>%
```

### 第三步：查看日志
- **nanobot**：`workspace/logs/`
- **应用日志**：项目根目录 `logs/` 或 `stdout` 输出
- **系统日志**：Event Viewer（Windows）

### 第四步：缩小范围
- 最小化复现：移除无关因素，保留最小触发条件
- 二分法：注释代码/功能，定位问题模块
- 对比测试：与已知正常环境对比

## 常见问题模式

### 网络连接问题

**现象**：`Connection reset`、`Could not connect to server`、超时

**可能原因**：
1. 防火墙阻止
2. 代理设置
3. DNS 解析失败
4. 目标服务器不稳定
5. 本地网络波动

**解决方案**：
- 测试基础连接：`ping <host>`、`telnet <host> <port>`
- 检查代理：`echo %HTTP_PROXY%`、`echo %HTTPS_PROXY%`
- 临时关闭防火墙测试
- 更换网络（如切到手机热点）
- 使用镜像源（如 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple`）

**案例**：GitHub 克隆失败
- 错误：`fatal: unable to access 'https://github.com/...': Could not connect to server`
- 解决：等待网络恢复，或使用镜像 `git clone https://ghproxy.com/https://github.com/...`

### 权限与认证问题

**现象**：`403 Forbidden`、`401 Unauthorized`、`Missing required scope`

**排查步骤**：
1. 检查 token 是否过期：`gh auth status`
2. 验证 scopes：`repo`、`read:org`、`gist` 等
3. 确认账户权限：是否有目标仓库的访问权？
4. 检查环境变量：`GH_TOKEN` 是否覆盖了 keyring 存储？

**解决方案**：
- 重新生成 token（GitHub Settings → Developer settings → Personal access tokens）
- 使用 `gh auth refresh --with-token` 更新
- 删除 `GH_TOKEN` 环境变量，让 gh 使用 keyring

**案例**：GitHub Push Protection 拦截
- 现象：推送失败，提示检测到暴露的 token
- 原因：`HISTORY.md` 中包含 `[REDACTED]` 但仍被检测
- 解决：彻底清理历史记录中的敏感信息，重新提交

### 依赖安装失败

**现象**：`pip install` 失败、`npm install` 失败

**常见原因**：
1. 网络超时
2. 版本冲突
3. 缺少编译工具（如 Visual C++ Build Tools）
4. 平台不支持（纯二进制包无 Windows 版本）

**解决方案**：
- 使用国内镜像源
- 指定版本：`pip install package==1.2.3`
- 升级 pip：`python -m pip install --upgrade pip`
- 安装编译工具（Windows：Visual Studio Build Tools）
- 寻找替代包（如 `akshare-stock` vs `akshare`）

**案例**：`cli-anything` 安装失败
- 错误：PyPI 上无 `cli-anything` 包
- 原因：项目未发布到 PyPI，需从 GitHub 安装
- 解决：`pip install git+https://github.com/HKUDS/cli-anything.git`

### Windows 兼容性问题

**现象**：`cp: command not found`、文件锁、路径错误

**解决方案**：
- **cp 命令**：改用 `copy`（Windows）或 `shutil.copy()`（Python）
- **rm 命令**：改用 `del` 或 `Remove-Item`
- **文件锁**：停止相关进程，或重启后删除
- **路径**：使用原始字符串 `r"C:\path"` 或双反斜杠 `"C:\\path"`

**案例**：Paperclip 构建失败
- 错误：`cp: command not found` 在 package.json 脚本中
- 解决：修改脚本使用跨平台命令（如 `copy` 或 Node.js `fs.copyFileSync`）

### 服务启动失败

**现象**：`npm start` 失败、端口占用、数据库连接失败

**排查清单**：
- [ ] 端口是否被占用？`netstat -ano | findstr :<port>`
- [ ] 数据库是否运行？`pg_isready`（PostgreSQL）
- [ ] 环境变量是否设置？`echo %DATABASE_URL%`
- [ ] 配置文件是否正确？检查 JSON 语法
- [ ] 日志文件是否有详细错误？

**解决方案**：
- 更换端口（如 3100 → 3103）
- 停止占用端口的进程
- 修复配置文件（如添加 `$meta` 字段）
- 调整数据库连接参数

**案例**：Paperclip 服务器启动超时
- 现象：尝试连接嵌入式 PostgreSQL 超时
- 原因：Windows 不支持嵌入式 PostgreSQL 的 fcntl 文件锁
- 解决：使用外部 PostgreSQL 服务，设置 `DATABASE_URL`

## 多方案尝试策略

当单一方案失败时，按优先级尝试：

1. **官方方案**：README、文档、官方教程
2. **社区方案**：GitHub Issues、Stack Overflow
3. **变通方案**：绕过问题（如用 agent-browser 替代 API）
4. **降级方案**：简化需求，先实现核心功能
5. **放弃方案**：评估成本，考虑替代工具

### 决策树示例：安装软件失败
```
pip install <pkg> 失败
    ↓
检查错误类型
    ├─ 网络问题 → 换镜像源 / 等网络恢复
    ├─ 包不存在 → 搜索 GitHub / 找替代
    ├─ 编译错误 → 找预编译二进制 / 换平台
    └─ 版本冲突 → 指定版本 / 创建虚拟环境
```

## 调试工具清单

### Windows 原生
- `tasklist` / `taskkill` - 进程管理
- `netstat` - 网络连接
- `sc` - 服务控制
- `reg query` - 注册表查询
- `PowerShell` - 高级脚本（`Get-Process`、`Get-Service`）

### Python 调试
- `pdb` - 交互式调试器
- `logging` - 结构化日志
- `pytest` - 单元测试
- `python -m pdb <script.py>` - 启动调试

### 网络诊断
- `ping` - ICMP 测试
- `tracert` - 路由追踪
- `telnet` - 端口测试
- `curl` / `wget` - HTTP 测试

### 数据库
- `psql` - PostgreSQL 命令行
- `pgAdmin` - GUI 工具
- `SELECT pg_reload_conf();` - 重载配置

---

*关键教训：问题解决要有系统化流程；先检查基础状态再深入；多方案并行尝试；Windows 环境需特别注意兼容性；每次失败都要记录教训。*