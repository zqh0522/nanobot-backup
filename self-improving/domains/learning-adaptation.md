# Learning & Adaptation - 学习与适应策略

> 来源：2026-03-12 至 2026-03-13 历史记录
> 范围：知识提取、模式识别、持续改进

## 学习信号识别

### 信号优先级排序
1. **用户纠正**（最高权重）
   - 触发：用户说"不对"、"应该是"、"你错了"
   - 行动：立即记录到 `corrections.md`
   - 后续：分析是否可升级为通用规则

2. **自我反思**（主动学习）
   - 触发：任务完成后的自我评估
   - 行动：记录 `CONTEXT/REFLECTION/LESSON` 结构
   - 后续：定期汇总到对应领域

3. **重复模式**（模式升级）
   - 触发：同一场景/问题出现 3 次
   - 行动：评估升级为 HOT 规则（`memory.md`）
   - 示例：网络搜索失败 → 备用方案流程

4. **专家验证**（权威学习）
   - 触发：阅读行业文章、官方文档
   - 行动：提取核心观点，保存到 `domains/`
   - 示例：《OpenClaw实战指南》→ 脑手分离架构

5. **工具反馈**（边界认知）
   - 触发：工具成功/失败
   - 行动：记录能力边界和限制
   - 示例：summarize 未安装 → 需 WSL2

### 学习信号捕获时机
- **任务开始时**：明确目标和约束
- **任务进行中**：遇到障碍时记录
- **任务结束后**：强制自我反思
- **用户交互后**：无论成功失败都复盘

## 知识提取与组织

### 从历史记录提取
```
原始记录 → 摘要关键点 → 分类 → 去重 → 结构化
```

**示例**：从 200+ 条历史记录提取
1. 筛选与"网络"相关的条目
2. 提取具体错误和解决方案
3. 归纳为"网络连接问题"模式
4. 写入 `domains/problem-solving.md`

### 领域分类原则
- **单一职责**：一个领域文件只覆盖一个主题
- **粒度适中**：200-500 行，避免过大
- **可搜索**：标题清晰，便于 `grep`

**当前领域**：
- `system-administration.md` - 系统运维
- `tool-integration.md` - 工具集成
- `problem-solving.md` - 问题解决
- `security-best-practices.md` - 安全规范
- `communication-collaboration.md` - 沟通协作
- `learning-adaptation.md` - 本文件

### 知识结构模板
```markdown
# <领域名称>

> 来源：<时间范围>
> 范围：<覆盖的子主题>

## 核心概念
- 概念1：定义
- 概念2：定义

## 常见模式
- 模式1：描述 + 案例
- 模式2：描述 + 案例

## 最佳实践
- 实践1：步骤 + 原理
- 实践2：步骤 + 原理

## 陷阱与规避
- 陷阱1：现象 + 原因 + 解决方案
- 陷阱2：现象 + 原因 + 解决方案

## 工具与命令
- 工具1：用途 + 示例
- 工具2：用途 + 示例

---
*关键教训：<1-2 句总结>*
```

## 模式识别与升级

### 识别重复模式
```bash
# 搜索历史记录中的重复关键词
grep -i "network" memory/HISTORY.md | wc -l
grep -i "permission" memory/HISTORY.md | wc -l
```

### 升级决策树
```
出现次数 ≥ 3 次？
    ↓ 是
是否通用（跨项目）？
    ↓ 是
是否经过验证？
    ↓ 是
    → 升级到 memory.md（HOT 层）
```

### 升级示例
**模式**：网络搜索失败 → 使用 agent-browser 替代
**出现**：3 次（Brave API 未配置、GitHub 404、百度搜索）
**决策**：升级为通用规则，写入 `memory.md`

## 自我反思机制

### 任务后反思模板
```
【任务回顾】
- 目标：<原定目标>
- 结果：<实际结果>
- 耗时：<时间>

【过程分析】
- 关键决策点：<列出 2-3 个>
- 正确之处：<什么做得好>
- 失误之处：<什么可以改进>

【根本原因】
- 技术原因：<如工具限制>
- 认知原因：<如知识盲区>
- 流程原因：<如缺少检查>

【可复用教训】
- 规则：<如果...就...>
- 检查清单：<下次必做事项>
- 避免：<下次不做什么>

【行动项】
- 记录到：<corrections.md 或 domains/>
- 更新：<哪些文件需要更新>
```

### 反思时机
- **每个任务结束**：强制 2 分钟反思
- **用户纠正后**：立即反思并记录
- **工具失败时**：失败后立即分析
- **每日结束**：汇总当天经验

## 持续改进循环

### PDCA 循环
```
Plan（计划）
  ↓
Do（执行）
  ↓
Check（检查）
  ↓ 自我反思 + 用户反馈
Act（调整）
  ↓ 更新规则、流程、知识库
  ↓
回到 Plan
```

### 改进频率
- **实时**：用户纠正 → 立即记录
- **每日**：检查 `corrections.md` 是否有新条目
- **每周**：审查 `domains/` 是否需要新领域
- **每月**：评估 `memory.md` 规则是否仍有效

### 改进指标
- **错误率下降**：同类错误是否重复出现？
- **效率提升**：任务耗时是否减少？
- **用户满意度**：反馈是否更积极？
- **知识覆盖**：`domains/` 是否覆盖主要场景？

## 工具能力边界认知

### 能力评估框架
```
功能需求 → 工具A → 工具B → 工具C
    ↓         ↓         ↓         ↓
测试验证 → 成功/失败 → 记录边界 → 更新知识
```

### 边界记录格式
```markdown
## 工具：<tool-name>

### 能力
- ✅ 可以：<功能列表>
- ❌ 不可以：<限制列表>

### 边界案例
- 案例1：<场景> → <结果>
- 案例2：<场景> → <结果>

### 替代方案
- 当 <场景> 时，使用 <其他工具>
```

**示例**：summarize 工具
- ✅ 可以：转录 YouTube 视频、总结网页
- ❌ 不可以：Windows 原生支持（需 WSL2）
- 边界：未安装 → 需要 `brew install` 或 WSL2

## 知识验证流程

### 新信息验证清单
- [ ] **来源可信**：A/B 级来源？
- [ ] **多源确认**：至少 2 个独立来源？
- [ ] **时效性**：信息是否过时？（检查日期）
- [ ] **可复现**：能否自己验证？
- [ ] **无冲突**：与现有知识是否矛盾？

### 验证方法
1. **工具查证**：用 `web_search`、`agent-browser` 验证
2. **实验验证**：小规模测试（如 `pytdx` 连接测试）
3. **交叉引用**：查找其他文档是否一致
4. **专家确认**：寻找权威观点

### 验证失败处理
- **标记为"待确认"**：在文件中标注不确定性
- **不传播**：不将未验证信息用于决策
- **持续追踪**：定期重新验证

## 知识检索与使用

### 检索策略
```bash
# 全局搜索（小文件）
cat memory/HISTORY.md | grep "keyword"

# 领域搜索
grep -r "keyword" self-improving/domains/

# 精确查找
findstr /s /i "keyword" self-improving\domains\*.md
```

### 使用场景
- **配置问题**：查 `system-administration.md`
- **工具选择**：查 `tool-integration.md`
- **故障排查**：查 `problem-solving.md`
- **安全决策**：查 `security-best-practices.md`
- **格式规范**：查 `communication-collaboration.md`

### 自动加载（未来）
- 任务开始时，根据关键词自动加载相关领域文件
- 例如：涉及"安装" → 加载 `system-administration.md`

---

*关键教训：学习是持续过程，不是一次性事件；每次失败都是学习机会；知识必须结构化才能复用；验证是质量的底线。*

---

## 🚀 果蝇连接组启发的三大核心改进（2026-Q2）

> **灵感来源**：FlyGM、ConnectomeBench、神经形态计算、数字孪生
> **目标**：从"被动响应"升级为"主动进化"的AI助手

### 1️⃣ 功能回路设计：高频意图预编译

**问题**：每次用户请求都重新规划技能链，决策开销大，响应慢。

**果蝇启示**：连接组直接作为控制器，无需任务特定架构调整，产生稳定行为。

**解决方案**：
- **识别高频意图**：分析HISTORY.md，统计前10高频问题类型
- **预编译技能链**：为每个高频意图创建固定技能组合
- **直接映射**：意图识别 → 直接执行预编译链，跳过决策中间层

**实施步骤**：
1. **数据收集**：分析最近1000条HISTORY.md，统计意图分布
2. **阈值设定**：出现频率>5%的意图进入候选列表
3. **设计回路**：为每个候选意图设计最优技能链
4. **性能测试**：对比新旧流程的响应时间和成功率
5. **部署上线**：更新 `memory.md` 添加意图映射表

**示例映射表**：
```markdown
## 高频意图功能回路（memory.md）

| 用户意图 | 技能链 | 预期耗时 | 成功率目标 |
|---------|-------|---------|-----------|
| "查询股票行情" | akshare获取 → china-stock-analysis → markdown格式化 | <3秒 | >95% |
| "设置提醒" | cron add → 确认 → memory记录 | <2秒 | >98% |
| "搜索信息" | web_search → 结果筛选 → 摘要生成 | <5秒 | >90% |
| "文件操作" | list_dir/read_file/edit_file → 验证 | <2秒 | >99% |
```

**验证指标**：
- 响应时间减少：目标30%
- 决策错误率：目标<1%
- 用户满意度：目标提升20%

---

### 2️⃣ AI辅助历史分析：每周自动洞察

**问题**：自我改进依赖人工阅读HISTORY.md，无法规模化，容易遗漏模式。

**果蝇启示**：LLM辅助连接组校对，准确率52-82%，远超随机。AI能发现人类忽略的模式。

**解决方案**：
- **周度自动分析**：每周日凌晨2点运行，分析上周历史
- **多维度洞察**：错误模式、技能使用、用户满意度、瓶颈任务
- **结构化输出**：JSON格式，自动更新对应domains/文件

**实施步骤**：
1. **创建分析脚本**：`scripts/weekly_history_analysis.py`
2. **设计Prompt模板**：针对不同分析目标定制
3. **设置cron任务**：每周自动执行
4. **结果处理**：自动识别需要升级的规则
5. **人工审核**：每周一早上我向你汇报关键发现

**Prompt模板示例**：
```python
prompt = f"""
分析以下对话历史（最近100条），提取结构化洞察：

【任务】：
1. 错误模式识别：
   - 用户最常纠正的错误类型（前3类）
   - 每个错误类型的出现频率和典型场景
   - 建议的规避措施

2. 技能使用分析：
   - 各技能使用频率排名
   - 技能组合模式（哪些技能常一起使用）
   - 技能失败率排名

3. 用户满意度推断：
   - 显式正面反馈（点赞、表扬）的任务特征
   - 显式负面反馈（批评、纠正）的任务特征
   - 隐式满意度信号（追问、重复提问）

4. 性能瓶颈：
   - 响应时间>10秒的任务类型
   - 需要多次工具调用的复杂任务
   - 网络/IO密集型操作

5. 改进建议：
   - 哪些规则应升级为HOT（memory.md）
   - 哪些规则应降级或删除
   - 哪些新领域需要创建

输出格式：JSON，包含上述5个键，每个键对应列表或字典。

历史记录：
{recent_history}
"""
```

**输出处理逻辑**：
```python
# 解析JSON输出
insights = json.loads(llm_response)

# 自动更新domains/
for rule in insights['rules_to_upgrade']:
    add_to_memory(rule)  # 升级到HOT层

for pattern in insights['new_patterns']:
    update_domain('learning-adaptation', pattern)  # 记录新模式

# 生成周报
generate_weekly_report(insights)
```

**验证指标**：
- 分析覆盖率：100%历史记录被分析
- 模式识别准确率：人工抽检>90%
- 规则升级有效性：升级的规则实际使用率>50%

---

### 3️⃣ 动态规则权重系统：知识的"突触可塑性"

**问题**：规则一旦写入memory.md就固定不变，无法根据实际效果动态调整。

**果蝇启示**：真实大脑突触强度每小时变化，可塑性是适应性的核心。

**解决方案**：
- **权重量化**：每条规则有0-1的置信度分数
- **使用反馈**：成功应用→权重+0.01；失败→权重-0.05
- **自动衰减**：30天未使用→权重×0.9
- **自动升级/降级**：权重>0.8→升级HOT；权重<0.3→降级/删除

**实施步骤**：
1. **创建权重存储**：`workspace/rule_weights.json`
2. **实现权重管理类**：`scripts/rule_weight_manager.py`
3. **集成到决策流程**：每次应用规则时更新权重
4. **定期审查**：每周自动生成权重报告
5. **自动迁移**：权重>0.8且不在memory.md→自动添加

**数据结构**：
```json
{
  "规则ID": {
    "text": "规则原文",
    "weight": 0.75,
    "last_used": "2026-03-13T00:50:00",
    "success_count": 12,
    "failure_count": 2,
    "location": "domains/problem-solving.md",
    "metadata": {
      "created": "2026-03-10",
      "source": "用户纠正",
      "trigger_count": 14
    }
  }
}
```

**核心算法**：
```python
class RuleWeightManager:
    def __init__(self, weights_file='workspace/rule_weights.json'):
        self.weights = self.load_weights()
    
    def apply_rule(self, rule_id, success=True):
        """应用规则后更新权重"""
        if rule_id not in self.weights:
            self.weights[rule_id] = {
                'weight': 0.5,  # 初始权重
                'last_used': now(),
                'success_count': 0,
                'failure_count': 0
            }
        
        rule = self.weights[rule_id]
        rule['last_used'] = now()
        
        if success:
            rule['weight'] = min(1.0, rule['weight'] + 0.01)
            rule['success_count'] += 1
        else:
            rule['weight'] = max(0.0, rule['weight'] - 0.05)
            rule['failure_count'] += 1
        
        self.save_weights()
    
    def decay_old_rules(self, days=30):
        """衰减长期未使用的规则权重"""
        cutoff = now() - timedelta(days=days)
        for rule_id, rule in self.weights.items():
            if rule['last_used'] < cutoff:
                rule['weight'] *= 0.9
        self.save_weights()
    
    def auto_upgrade(self):
        """自动升级高权重规则到HOT层"""
        for rule_id, rule in self.weights.items():
            if rule['weight'] > 0.8:
                if not self.is_in_memory(rule_id):
                    self.promote_to_memory(rule_id)
    
    def weekly_review(self):
        """每周审查：生成报告，建议删除低权重规则"""
        low_weight_rules = [
            (rid, r) for rid, r in self.weights.items()
            if r['weight'] < 0.3
        ]
        return {
            'total_rules': len(self.weights),
            'avg_weight': sum(r['weight'] for r in self.weights.values()) / len(self.weights),
            'low_weight_rules': low_weight_rules,
            'recently_used': self.get_recently_used(7)
        }
```

**集成到决策流程**：
```python
# 原有决策逻辑
selected_rule = select_rule_based_on_context(context)

# 新增：应用规则并更新权重
success = execute_rule(selected_rule)
weight_manager.apply_rule(selected_rule.id, success)

# 如果权重高且不在memory，考虑升级
if weight_manager.weights[selected_rule.id]['weight'] > 0.8:
    weight_manager.auto_upgrade()
```

**验证指标**：
- 规则淘汰率：每月自动删除<10%的低权重规则
- 规则升级率：每月自动升级5-10条高权重规则
- 决策准确率：高权重规则的失败率<5%

---

## 📋 本周行动计划（2026-03-14 至 2026-03-20）

### 立即（今天）
- [ ] 创建 `scripts/weekly_history_analysis.py`（AI辅助分析）
- [ ] 创建 `scripts/rule_weight_manager.py`（权重系统）
- [ ] 扩展 `domains/learning-adaptation.md`（已完成本部分）
- [ ] 分析HISTORY.md，识别前10高频意图（功能回路基础数据）

### 明天
- [ ] 运行首次历史分析，生成洞察报告
- [ ] 设计意图映射表草案（3-5个高频意图）
- [ ] 测试权重系统：模拟100次规则应用，验证权重变化

### 本周内
- [ ] 设置cron周度任务：每周日2点自动运行分析
- [ ] 完成功能回路设计，部署前3个高频意图
- [ ] 性能测试：对比新旧流程，记录基线数据
- [ ] 生成第一份周报，包含：
  - 规则权重分布
  - 新识别模式
  - 建议升级/删除的规则列表

### 本周末评估
- [ ] 检查权重系统是否正常更新
- [ ] 验证AI分析结果质量（人工抽检）
- [ ] 测量功能回路的性能提升
- [ ] 决定是否扩大意图映射范围

---

*关键教训：果蝇连接组研究教会我——结构决定功能，但可塑性决定适应性。这三大改进正是将我的知识系统从"静态化石"变为"活体神经网络"的关键步骤。立即行动，用代码实现进化！*