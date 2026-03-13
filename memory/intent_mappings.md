# 高频意图功能回路映射表

> **创建时间**: 2026-03-14
> **数据来源**: weekly_history_analysis (最近7天19条记录)
> **目标**: 预编译高频意图的技能链，减少决策开销，提升响应速度30%+

---

## 📊 高频意图排行（基于历史数据）

| 排名 | 意图类型 | 出现次数 | 占比 | 相关技能 |
|------|---------|---------|------|---------|
| 1 | GitHub操作 | 11 | 57.9% | github, memory, exec |
| 2 | 股票数据分析 | 8 | 42.1% | akshare-stock, china-stock-analysis |
| 3 | 记忆管理 | 5 | 26.3% | memory, exec |
| 4 | 网络搜索 | 4 | 21.1% | web_search, agent-browser |
| 5 | 实时行情 | 4 | 21.1% | pytdx, akshare-stock |
| 6 | 投资分析 | 4 | 21.1% | china-stock-analysis, akshare-stock |

**阈值设定**：占比>20%的意图进入功能回路（前6名）

---

## 🔄 功能回路设计

### **回路1：GitHub仓库操作**（优先级：P0）

**触发意图**：
- "备份到GitHub"
- "推送到远程"
- "创建GitHub仓库"
- "GitHub认证"
- "查看GitHub状态"

**预编译技能链**：
```
1. exec: git status (检查当前状态)
2. exec: git add -A (添加所有变更)
3. exec: git commit -m "自动备份: YYYY-MM-DD HH:MM" (提交)
4. exec: git push origin main (推送)
5. memory: 记录操作到HISTORY.md
```

**预期指标**：
- 响应时间：<5秒
- 成功率：>98%
- 失败处理：如果push被拦截（Push Protection），自动触发token清理流程

**失败回退**：
- 如果push失败 → 检查token泄露 → 自动清理 → 重试
- 如果网络失败 → 切换到agent-browser检查GitHub状态

---

### **回路2：股票数据查询**（优先级：P0）

**触发意图**：
- "查询股票行情"
- "贵州茅台价格"
- "600519实时数据"
- "股票K线"
- "财务数据"

**预编译技能链**：
```
1. akshare-stock: 获取实时行情 (stock_zh_a_spot_em)
2. akshare-stock: 获取历史K线 (stock_zh_a_hist)
3. china-stock-analysis: 技术分析 (MACD, RSI, 均线)
4. china-stock-analysis: 生成投资建议 (买入/持有/卖出)
5. memory: 缓存结果（24小时有效期）
```

**预期指标**：
- 实时行情：<3秒
- 历史数据：<5秒
- 分析报告：<8秒
- 成功率：>95%

**数据源优先级**：
1. akshare（首选，免费）
2. pytdx（备用，需要配置服务器）
3. agent-browser（兜底，访问网页）

---

### **回路3：投资分析报告**（优先级：P1）

**触发意图**：
- "分析这只股票"
- "投资建议"
- "技术面分析"
- "基本面分析"

**预编译技能链**：
```
1. akshare-stock: 获取实时行情 + 历史数据（最近60天）
2. akshare-stock: 获取财务指标 (roe, pe, pb, revenue)
3. akshare-stock: 获取资金流向 (主力资金, 散户资金)
4. china-stock-analysis: 综合评分 (0-100分)
5. china-stock-analysis: 风险提示
6. markdown: 格式化报告（表格+图表）
```

**预期指标**：
- 完整分析：<10秒
- 报告质量：包含5+个技术指标 + 3+个基本面指标
- 成功率：>90%

---

### **回路4：网络搜索与信息获取**（优先级：P1）

**触发意图**：
- "搜索最新新闻"
- "查找相关资料"
- "了解某个概念"
- "获取网页内容"

**预编译技能链**：
```
1. web_search: 尝试Brave Search (首选)
2. 如果失败 → agent-browser: 访问百度/Google
3. agent-browser: 提取页面正文
4. memory: 缓存结果（1小时有效期）
```

**预期指标**：
- 搜索成功：>95%
- 响应时间：<5秒（web_search） / <10秒（agent-browser）
- 内容提取准确率：>90%

**备用方案**：
- 如果web_search失败（Brave API未配置），自动切换到agent-browser
- 如果agent-browser失败（网站反爬），尝试更换User-Agent

---

### **回路5：记忆与历史查询**（优先级：P2）

**触发意图**：
- "我之前说过什么"
- "查看历史记录"
- "回忆之前的对话"
- "HISTORY.md内容"

**预编译技能链**：
```
1. memory: 搜索关键词（最近30天）
2. memory: 如果未找到，扩展搜索（全部历史）
3. exec: grep辅助搜索（精确匹配）
4. markdown: 格式化结果（时间线展示）
```

**预期指标**：
- 查询速度：<2秒（30天内）
- 召回率：>99%
- 准确率：>95%

---

### **回路6：系统状态检查**（优先级：P2）

**触发意图**：
- "系统状态"
- "服务是否运行"
- "检查配置"
- "诊断问题"

**预编译技能链**：
```
1. exec: 检查进程 (tasklist)
2. exec: 检查端口 (netstat)
3. exec: 检查服务 (sc query)
4. exec: 检查磁盘空间 (dir)
5. memory: 记录检查结果
6. markdown: 生成状态报告
```

**预期指标**：
- 检查耗时：<3秒
- 信息完整度：覆盖CPU、内存、磁盘、网络、服务

---

## 🎯 实施计划

### **阶段1：基础回路（本周）**
- [x] 设计映射表（本文件）
- [ ] 实现意图识别模块（基于关键词匹配）
- [ ] 实现回路执行器（预编译技能链）
- [ ] 测试回路1（GitHub）和回路2（股票）

### **阶段2：优化与扩展（下周）**
- [ ] 性能测试（对比新旧流程）
- [ ] 添加失败回退逻辑
- [ ] 实现回路3（投资分析）
- [ ] 实现回路4（网络搜索）

### **阶段3：完善与监控（下月）**
- [ ] 实现回路5、6
- [ ] 添加回路性能监控（响应时间、成功率）
- [ ] 自动优化：根据实际使用频率动态调整回路优先级
- [ ] 用户反馈：询问用户是否觉得响应更快

---

## 📈 性能目标

| 回路 | 当前平均耗时 | 目标耗时 | 提升目标 |
|------|------------|---------|---------|
| GitHub操作 | ~15秒 | <5秒 | 66% |
| 股票查询 | ~8秒 | <3秒 | 62% |
| 投资分析 | ~20秒 | <10秒 | 50% |
| 网络搜索 | ~10秒 | <5秒 | 50% |
| 记忆查询 | ~3秒 | <2秒 | 33% |
| 系统检查 | ~5秒 | <3秒 | 40% |

**综合目标**：整体响应时间减少40-60%

---

## 🔧 技术实现要点

### **意图识别**
```python
def detect_intent(user_query: str) -> str:
    """检测用户意图，返回回路名称"""
    intent_patterns = {
        'github': ['git', 'github', '推送', '提交', '备份', '远程'],
        'stock': ['股票', '行情', '价格', 'K线', '600519', '贵州茅台'],
        'analysis': ['分析', '建议', '投资', '技术面', '基本面'],
        'search': ['搜索', '查找', '资料', '新闻', '了解'],
        'memory': ['历史', '之前', '说过', '回忆', 'HISTORY'],
        'system': ['状态', '检查', '诊断', '服务', '运行']
    }

    query_lower = user_query.lower()
    for intent, keywords in intent_patterns.items():
        if any(kw in query_lower for kw in keywords):
            return intent
    return 'default'  # 使用原有决策流程
```

### **回路执行器**
```python
class IntentRouter:
    def __init__(self):
        self.loops = {
            'github': self.execute_github_loop,
            'stock': self.execute_stock_loop,
            'analysis': self.execute_analysis_loop,
            'search': self.execute_search_loop,
            'memory': self.execute_memory_loop,
            'system': self.execute_system_loop
        }

    def route(self, intent: str, context: dict):
        """路由到对应的功能回路"""
        if intent in self.loops:
            start_time = time.time()
            result = self.loops[intent](context)
            elapsed = time.time() - start_time

            # 记录性能指标
            self.record_metrics(intent, elapsed, success=True)

            return result
        else:
            # 回退到标准流程
            return self.default_flow(context)
```

---

## 🧪 测试计划

### **单元测试**
- [ ] 意图识别准确率 > 90%
- [ ] 每个回路的成功率 > 95%
- [ ] 响应时间达标率 > 90%

### **集成测试**
- [ ] 连续100次GitHub操作，无失败
- [ ] 连续100次股票查询，数据准确
- [ ] 回路间切换无冲突

### **A/B测试**
- [ ] 50%流量走新回路，50%走旧流程
- [ ] 对比响应时间、成功率、用户满意度
- [ ] 如果新回路显著优于旧流程（p<0.05），全量切换

---

## 📊 监控指标

| 指标 | 目标值 | 监控频率 | 告警阈值 |
|------|-------|---------|---------|
| 回路响应时间 | <目标值 | 实时 | >目标值×1.5 |
| 回路成功率 | >95% | 每小时 | <90% |
| 意图识别准确率 | >90% | 每日 | <85% |
| 用户满意度 | >80% | 每周 | <70% |
| 规则权重平均增长 | >0.01/次 | 每周 | <0.005/次 |

---

*关键教训：高频意图预编译能显著减少决策开销；失败回退机制保证可靠性；性能监控确保持续优化。*
