# Self-Improving System - 知识索引

> 快速查找所有领域知识和项目经验

## 📚 核心文件

| 文件 | 说明 | 加载时机 |
|------|------|----------|
| `memory.md` | HOT 层：通用原则、核心规则 | 永远加载 |
| `corrections.md` | 用户纠正日志 | 需要时查阅 |
| `INDEX.md` | 本文件，知识导航 | 需要时查阅 |

## 🗂️ 领域知识（domains/）

| 领域文件 | 主题 | 适用场景 | 行数 |
|---------|------|---------|------|
| `system-administration.md` | 系统运维与配置 | GitHub CLI、服务管理、Windows 兼容性 | ~150 |
| `tool-integration.md` | 工具集成与技能管理 | 技能安装、agent-browser、akshare、平台限制 | ~180 |
| `problem-solving.md` | 问题解决与调试 | 故障排查、网络问题、权限问题 | ~220 |
| `security-best-practices.md` | 安全与最佳实践 | 敏感信息、风险评估、备份策略 | ~190 |
| `communication-collaboration.md` | 沟通与协作规范 | 输出格式、用户偏好、严谨性要求 | ~140 |
| `learning-adaptation.md` | 学习与适应策略 | 知识提取、模式识别、持续改进 | ~220 |

**总计**：6 个领域，约 1100 行结构化知识

## 📁 项目经验（projects/）

| 项目文件 | 项目名称 | 状态 | 关键收获 |
|---------|---------|------|---------|
| `paperclip-deployment.md` | Paperclip 部署与卸载 | 已放弃 | Windows 兼容性、架构选型、成本评估 |

## 🔍 快速查询指南

### 场景：如何做 X？
```bash
# 1. 先查 memory.md（通用原则）
grep -i "X" self-improving/memory.md

# 2. 再查相关领域
grep -i "X" self-improving/domains/*.md

# 3. 最后查项目经验（具体案例）
grep -i "X" self-improving/projects/*.md
```

### 场景：用户纠正了 Y，如何记录？
1. 打开 `corrections.md`
2. 按模板追加：
   ```markdown
   ### 2026-03-13 HH:MM - 主题
   **用户原话**："..."
   **错误**：...
   **正确**：...
   **教训**：...
   **行动**：...
   ```

### 场景：任务完成后如何反思？
1. 使用 `learning-adaptation.md` 中的模板
2. 评估是否可升级为规则（出现 ≥3 次）
3. 记录到对应领域或 `corrections.md`

### 场景：遇到新问题如何解决？
1. 查 `problem-solving.md` 通用流程
2. 查 `system-administration.md` 系统相关
3. 查 `tool-integration.md` 工具相关
4. 如未找到，解决问题后**创建新经验**并分类

## 📊 知识统计

- **领域覆盖**：6 个核心领域
- **项目案例**：1 个完整项目
- **总知识量**：~4000 行 markdown
- **历史记录**：200+ 条交互事件

## 🔄 维护流程

### 日常
- 每次用户纠正 → 更新 `corrections.md`
- 每次任务完成 → 自我反思 → 可能更新 `domains/`

### 每周
- 检查 `corrections.md` 是否有重复模式
- 评估是否需要新领域文件

### 每月
- 审查 `memory.md` 规则是否仍有效
- 归档不活跃的领域或项目

## 🎯 知识升级路径

```
corrections.md（具体纠正）
    ↓ 重复 3 次
domains/（领域经验）
    ↓ 验证通用性
memory.md（核心规则）
```

## 📝 贡献指南

当发现新经验时：
1. **判断类型**：
   - 用户纠正 → `corrections.md`
   - 通用模式 → `domains/<domain>.md`
   - 具体项目 → `projects/<project>.md`
2. **使用模板**：参考对应文件的格式
3. **保持简洁**：一经验一条目，避免冗长
4. **标注来源**：日期、事件、关键引用

---

*最后更新：2026-03-13 创建初始索引*