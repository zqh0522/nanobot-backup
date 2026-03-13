#!/usr/bin/env python3
"""
AI辅助历史分析脚本
每周自动分析HISTORY.md，识别模式、趋势、改进点
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sys

# 添加父目录到路径，以便导入nanobot模块（如果需要）
sys.path.insert(0, str(Path(__file__).parent.parent))

class HistoryAnalyzer:
    """历史记录分析器"""

    def __init__(self, history_file: str = None):
        """初始化分析器

        Args:
            history_file: HISTORY.md文件路径
        """
        if history_file is None:
            workspace = Path(__file__).parent.parent
            history_file = workspace / "memory" / "HISTORY.md"

        self.history_file = Path(history_file)
        self.entries = []
        self.load_history()

    def load_history(self) -> None:
        """加载历史记录"""
        if not self.history_file.exists():
            print(f"[ERR] 历史文件不存在: {self.history_file}")
            self.entries = []
            return

        content = self.history_file.read_text(encoding='utf-8')
        # 按时间戳分割条目（格式：[YYYY-MM-DD HH:MM] ...）
        # 使用正则匹配时间戳行
        pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]\s*(.*?)(?=\n\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\]|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)

        self.entries = []
        for timestamp_str, body in matches:
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                self.entries.append({
                    'timestamp': timestamp,
                    'timestamp_str': timestamp_str,
                    'body': body.strip()
                })
            except ValueError as e:
                print(f"[WARN] 解析时间戳失败: {timestamp_str} - {e}")

        print(f"[OK] 加载 {len(self.entries)} 条历史记录")

    def filter_entries(self, days: int = 7) -> List[Dict[str, Any]]:
        """筛选最近N天的记录

        Args:
            days: 天数

        Returns:
            筛选后的记录列表
        """
        cutoff = datetime.now() - timedelta(days=days)
        return [e for e in self.entries if e['timestamp'] > cutoff]

    def analyze_error_patterns(self, recent_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析错误模式

        Args:
            recent_entries: 最近的历史记录

        Returns:
            错误模式列表
        """
        error_keywords = [
            '失败', '错误', 'exception', 'error', 'failed', 'cannot',
            '未找到', '不存在', '权限', 'permission', 'denied',
            '连接失败', 'timeout', '超时', '404', '403'
        ]

        error_entries = []
        for entry in recent_entries:
            body_lower = entry['body'].lower()
            if any(keyword in body_lower for keyword in error_keywords):
                error_entries.append(entry)

        # 聚类错误类型
        error_categories = {
            '网络问题': ['连接失败', 'timeout', '超时', 'cannot connect'],
            '权限问题': ['权限', 'permission', 'denied', '认证失败'],
            '文件问题': ['未找到', '不存在', 'file not found'],
            '工具错误': ['exception', 'error', 'failed', '404', '403'],
            '配置问题': ['配置', 'config', '设置', 'environment']
        }

        categorized = {cat: [] for cat in error_categories}
        categorized['其他错误'] = []  # 添加"其他"类别

        for entry in error_entries:
            body_lower = entry['body'].lower()
            matched = False
            for cat, keywords in error_categories.items():
                if any(k in body_lower for k in keywords):
                    categorized[cat].append(entry)
                    matched = True
                    break
            if not matched:
                categorized['其他错误'].append(entry)

        # 生成错误模式报告
        patterns = []
        for cat, entries in categorized.items():
            if entries:
                patterns.append({
                    'category': cat,
                    'count': len(entries),
                    'percentage': len(entries) / len(recent_entries) * 100 if recent_entries else 0,
                    'recent_examples': [e['body'][:200] for e in entries[:3]],
                    'suggested_fix': self._suggest_fix_for_category(cat)
                })

        # 按频率排序
        patterns.sort(key=lambda x: x['count'], reverse=True)

        return patterns

    def _suggest_fix_for_category(self, category: str) -> str:
        """为错误类别建议修复方案"""
        suggestions = {
            '网络问题': '检查网络连接、代理设置、防火墙；使用agent-browser作为备用方案；增加重试机制',
            '权限问题': '检查token权限范围；使用gh auth refresh重新认证；遵循最小权限原则',
            '文件问题': '使用list_dir验证路径存在；检查文件锁；使用绝对路径',
            '工具错误': '验证工具安装状态；检查版本兼容性；查看工具文档',
            '配置问题': '验证环境变量；检查配置文件语法；重启服务使配置生效',
            '其他错误': '详细记录错误信息；搜索类似问题；分步骤调试'
        }
        return suggestions.get(category, '需要进一步分析')

    def analyze_skill_usage(self, recent_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析技能使用情况

        Args:
            recent_entries: 最近的历史记录

        Returns:
            技能使用统计
        """
        # 技能关键词映射
        skill_patterns = {
            'web_search': ['web_search', 'Brave Search', '网络搜索'],
            'agent-browser': ['agent-browser', 'browser', '浏览器', 'clawdbot'],
            'akshare-stock': ['akshare', 'akshare-stock', '股票数据'],
            'china-stock-analysis': ['china-stock-analysis', '股票分析', '投资建议'],
            'github': ['gh ', 'GitHub', 'github', 'repo'],
            'cron': ['cron', '提醒', '定时任务', 'schedule'],
            'memory': ['memory', 'MEMORY.md', '历史记录', 'HISTORY'],
            'self-improving': ['self-improving', '自我改进', 'domains'],
            'pytdx': ['pytdx', '通达信', '实时行情'],
            'exec': ['exec', '命令执行', 'batch', 'powershell']
        }

        skill_counts = {skill: 0 for skill in skill_patterns}
        skill_contexts = {skill: [] for skill in skill_patterns}

        for entry in recent_entries:
            body = entry['body']
            for skill, keywords in skill_patterns.items():
                if any(kw.lower() in body.lower() for kw in keywords):
                    skill_counts[skill] += 1
                    if len(skill_contexts[skill]) < 3:  # 只保留前3个上下文
                        skill_contexts[skill].append(body[:200])

        # 转换为列表并排序
        skill_usage = []
        for skill, count in skill_counts.items():
            if count > 0:
                skill_usage.append({
                    'skill': skill,
                    'count': count,
                    'percentage': count / len(recent_entries) * 100 if recent_entries else 0,
                    'contexts': skill_contexts[skill]
                })

        skill_usage.sort(key=lambda x: x['count'], reverse=True)

        return skill_usage

    def analyze_user_satisfaction(self, recent_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """推断用户满意度

        Args:
            recent_entries: 最近的历史记录

        Returns:
            满意度分析
        """
        positive_keywords = ['好', '不错', '谢谢', '感谢', '满意', '正确', '成功', '[OK]', '✓', '赞']
        negative_keywords = ['不对', '错误', '失败', '问题', '麻烦', '重新', '纠正', '[ERR]', '✗', '失望']

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for entry in recent_entries:
            body = entry['body']
            # 检查用户输入（假设用户消息包含"USER:"或特定格式）
            # 这里简化处理：分析整个条目
            body_lower = body.lower()

            is_positive = any(kw in body_lower for kw in positive_keywords)
            is_negative = any(kw in body_lower for kw in negative_keywords)

            if is_positive and not is_negative:
                positive_count += 1
            elif is_negative and not is_positive:
                negative_count += 1
            else:
                neutral_count += 1

        total = len(recent_entries)
        satisfaction_score = (positive_count - negative_count) / total * 100 if total > 0 else 0

        return {
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total': total,
            'satisfaction_score': round(satisfaction_score, 2),
            'positive_rate': positive_count / total * 100 if total > 0 else 0,
            'negative_rate': negative_count / total * 100 if total > 0 else 0,
            'interpretation': self._interpret_satisfaction(satisfaction_score)
        }

    def _interpret_satisfaction(self, score: float) -> str:
        """解释满意度分数"""
        if score > 30:
            return "非常积极"
        elif score > 10:
            return "积极"
        elif score > -10:
            return "中性"
        elif score > -30:
            return "消极"
        else:
            return "非常消极"

    def analyze_performance_bottlenecks(self, recent_entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """识别性能瓶颈

        Args:
            recent_entries: 最近的历史记录

        Returns:
            瓶颈列表
        """
        # 查找耗时长的任务（通过关键词推断）
        time_keywords = ['耗时', 'time', '秒', '分钟', 'slow', '等待', 'wait']
        bottleneck_entries = []

        for entry in recent_entries:
            body = entry['body']
            if any(kw in body.lower() for kw in time_keywords):
                # 尝试提取时间信息
                time_match = re.search(r'(\d+)\s*(秒|分钟|min|s)', body.lower())
                estimated_time = None
                if time_match:
                    value = int(time_match.group(1))
                    unit = time_match.group(2)
                    if unit in ['分钟', 'min']:
                        estimated_time = value * 60
                    else:
                        estimated_time = value

                bottleneck_entries.append({
                    'timestamp': entry['timestamp_str'],
                    'body_preview': body[:300],
                    'estimated_time_seconds': estimated_time
                })

        # 按时间排序（最近的在前）
        bottleneck_entries.sort(key=lambda x: x['timestamp'], reverse=True)

        return bottleneck_entries[:10]  # 只返回前10个

    def generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成改进建议

        Args:
            analysis: 包含各种分析结果的字典

        Returns:
            改进建议列表
        """
        suggestions = []

        # 基于错误模式
        for pattern in analysis['error_patterns'][:3]:  # 前3个高频错误
            if pattern['count'] >= 2:
                suggestions.append({
                    'priority': 'HIGH',
                    'type': '错误修复',
                    'problem': f"高频错误: {pattern['category']} ({pattern['count']}次)",
                    'suggested_action': pattern['suggested_fix'],
                    'source': 'error_pattern_analysis'
                })

        # 基于技能使用
        skill_usage = analysis['skill_usage']
        total_entries = analysis['total_entries_analyzed']
        if skill_usage and total_entries > 0:
            top_skill = skill_usage[0]
            if top_skill['count'] > total_entries * 0.3:
                suggestions.append({
                    'priority': 'MEDIUM',
                    'type': '技能优化',
                    'problem': f"高频技能 {top_skill['skill']} 使用率{top_skill['percentage']:.1f}%",
                    'suggested_action': '考虑预编译功能回路，减少决策开销',
                    'source': 'skill_usage_analysis'
                })

        # 基于满意度
        satisfaction = analysis['user_satisfaction']
        if satisfaction['satisfaction_score'] < 0:
            suggestions.append({
                'priority': 'HIGH',
                'type': '用户体验',
                'problem': f"用户满意度偏低 (分数: {satisfaction['satisfaction_score']})",
                'suggested_action': '检查负面反馈的具体任务类型，针对性改进',
                'source': 'satisfaction_analysis'
            })

        # 基于性能瓶颈
        bottlenecks = analysis['performance_bottlenecks']
        if bottlenecks:
            slow_tasks = [b for b in bottlenecks if b.get('estimated_time_seconds') and b['estimated_time_seconds'] > 10]
            if slow_tasks:
                suggestions.append({
                    'priority': 'MEDIUM',
                    'type': '性能优化',
                    'problem': f"发现{len(slow_tasks)}个耗时>10秒的任务",
                    'suggested_action': '分析慢任务特征，考虑异步处理或预加载',
                    'source': 'performance_analysis'
                })

        return suggestions

    def analyze(self, days: int = 7) -> Dict[str, Any]:
        """执行完整分析

        Args:
            days: 分析最近N天的记录

        Returns:
            分析结果字典
        """
        print(f"[i] 分析最近 {days} 天的历史记录...")

        recent_entries = self.filter_entries(days)

        if not recent_entries:
            print("[WARN] 没有找到最近的历史记录")
            return {'error': 'no_recent_entries'}

        print(f"[i] 筛选出 {len(recent_entries)} 条记录进行分析")

        analysis = {
            'analysis_date': datetime.now().isoformat(),
            'period_days': days,
            'total_entries_analyzed': len(recent_entries),
            'error_patterns': self.analyze_error_patterns(recent_entries),
            'skill_usage': self.analyze_skill_usage(recent_entries),
            'user_satisfaction': self.analyze_user_satisfaction(recent_entries),
            'performance_bottlenecks': self.analyze_performance_bottlenecks(recent_entries)
        }

        # 生成改进建议
        analysis['improvement_suggestions'] = self.generate_improvement_suggestions(analysis)

        return analysis

    def export_to_json(self, analysis: Dict[str, Any], output_file: str = None) -> str:
        """导出分析结果为JSON

        Args:
            analysis: 分析结果
            output_file: 输出文件路径

        Returns:
            输出文件路径
        """
        if output_file is None:
            workspace = Path(__file__).parent.parent
            reports_dir = workspace / "reports"
            reports_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
            output_file = reports_dir / f"weekly_analysis_{timestamp}.json"

        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)

        print(f"[OK] 分析结果已保存到: {output_path}")
        return str(output_path)

    def generate_markdown_report(self, analysis: Dict[str, Any]) -> str:
        """生成Markdown格式的周报

        Args:
            analysis: 分析结果

        Returns:
            Markdown报告内容
        """
        report = f"""# 每周历史分析报告

**生成时间**: {analysis['analysis_date']}  
**分析周期**: 最近 {analysis['period_days']} 天  
**记录总数**: {analysis['total_entries_analyzed']} 条

---

## [CHART] 概览

### 用户满意度
- **满意度分数**: {analysis['user_satisfaction']['satisfaction_score']:.1f} ({analysis['user_satisfaction']['interpretation']})
- 积极反馈: {analysis['user_satisfaction']['positive_count']} 条 ({analysis['user_satisfaction']['positive_rate']:.1f}%)
- 消极反馈: {analysis['user_satisfaction']['negative_count']} 条 ({analysis['user_satisfaction']['negative_rate']:.1f}%)

### 技能使用排行
| 技能 | 使用次数 | 占比 |
|------|---------|------|
"""
        for skill in analysis['skill_usage'][:10]:
            report += f"| {skill['skill']} | {skill['count']} | {skill['percentage']:.1f}% |\n"

        report += """
---

## [ALERT] 高频错误模式

| 类别 | 次数 | 占比 | 建议修复 |
|------|------|------|---------|
"""
        for pattern in analysis['error_patterns'][:5]:
            report += f"| {pattern['category']} | {pattern['count']} | {pattern['percentage']:.1f}% | {pattern['suggested_fix']} |\n"

        report += """
---

## [WARN] 性能瓶颈

最近发现的耗时任务：
"""
        for i, bottleneck in enumerate(analysis['performance_bottlenecks'][:5], 1):
            time_info = f" ({bottleneck['estimated_time_seconds']}秒)" if bottleneck.get('estimated_time_seconds') else ""
            report += f"{i}. {time_info}\n   {bottleneck['body_preview']}\n\n"

        report += """
---

## [IDEA] 改进建议

| 优先级 | 类型 | 问题 | 建议行动 |
|--------|------|------|---------|
"""
        for suggestion in analysis['improvement_suggestions']:
            report += f"| {suggestion['priority']} | {suggestion['type']} | {suggestion['problem']} | {suggestion['suggested_action']} |\n"

        report += """
---

## [STATS] 详细数据

- 错误模式完整列表: 见JSON文件
- 技能使用上下文: 见JSON文件
- 周度审查报告: 运行 `python scripts/rule_weight_manager.py review`

---

*报告生成于 nanobot weekly_history_analysis*  
*下次运行: 每周日 02:00*
"""
        return report

    def save_markdown_report(self, report: str) -> str:
        """保存Markdown报告

        Args:
            report: Markdown内容

        Returns:
            保存路径
        """
        workspace = Path(__file__).parent.parent
        reports_dir = workspace / "reports"
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
        report_file = reports_dir / f"weekly_report_{timestamp}.md"

        report_path = Path(report_file)
        report_path.write_text(report, encoding='utf-8')

        print(f"[OK] Markdown报告已保存到: {report_path}")
        return str(report_path)


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='每周历史记录分析工具')
    parser.add_argument('--days', type=int, default=7, help='分析最近N天（默认7）')
    parser.add_argument('--output', type=str, help='JSON输出文件路径')
    parser.add_argument('--report', action='store_true', help='生成Markdown报告')
    parser.add_argument('--all', action='store_true', help='执行完整分析（JSON+报告）')

    args = parser.parse_args()

    analyzer = HistoryAnalyzer()

    if not analyzer.entries:
        print("[ERR] 无历史记录可分析")
        sys.exit(1)

    # 执行分析
    analysis = analyzer.analyze(days=args.days)

    if 'error' in analysis:
        print(f"[ERR] 分析失败: {analysis['error']}")
        sys.exit(1)

    # 打印摘要
    print("\n" + "="*60)
    print("[CHART] 分析摘要")
    print("="*60)
    print(f"总记录数: {analysis['total_entries_analyzed']}")
    print(f"用户满意度: {analysis['user_satisfaction']['satisfaction_score']:.1f} ({analysis['user_satisfaction']['interpretation']})")
    print(f"高频错误: {len(analysis['error_patterns'])} 类")
    print(f"技能使用: {len(analysis['skill_usage'])} 种")
    print(f"改进建议: {len(analysis['improvement_suggestions'])} 条")
    print("="*60 + "\n")

    # 输出JSON
    if args.all or args.output:
        output_file = args.output if args.output else None
        json_path = analyzer.export_to_json(analysis, output_file)
        print(f"JSON文件: {json_path}")

    # 生成Markdown报告
    if args.all or args.report:
        report = analyzer.generate_markdown_report(analysis)
        report_path = analyzer.save_markdown_report(report)
        print(f"Markdown报告: {report_path}")

        # 同时打印到控制台
        print("\n" + "="*60)
        print("[REPORT] 报告预览（前500字符）")
        print("="*60)
        print(report[:500] + "...\n")


if __name__ == '__main__':
    main()
