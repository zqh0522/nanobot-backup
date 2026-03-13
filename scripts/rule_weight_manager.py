#!/usr/bin/env python3
"""
动态规则权重管理器
实现"突触可塑性"：规则权重随使用频率和效果动态调整
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Tuple

class RuleWeightManager:
    """规则权重管理器"""

    def __init__(self, weights_file: str = None):
        """初始化权重管理器

        Args:
            weights_file: 权重存储文件路径，默认在workspace/rule_weights.json
        """
        if weights_file is None:
            workspace = Path(__file__).parent.parent
            weights_file = workspace / "rule_weights.json"

        self.weights_file = Path(weights_file)
        self.weights: Dict[str, Dict[str, Any]] = {}
        self.load_weights()

    def load_weights(self) -> None:
        """从文件加载权重数据"""
        if self.weights_file.exists():
            try:
                with open(self.weights_file, 'r', encoding='utf-8') as f:
                    self.weights = json.load(f)
                print(f"[OK] 加载 {len(self.weights)} 条规则权重")
            except (json.JSONDecodeError, IOError) as e:
                print(f"[ERR] 加载权重文件失败: {e}")
                self.weights = {}
        else:
            print("[INFO] 权重文件不存在，创建新的")
            self.weights = {}

    def save_weights(self) -> None:
        """保存权重数据到文件"""
        try:
            self.weights_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.weights_file, 'w', encoding='utf-8') as f:
                json.dump(self.weights, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"[ERR] 保存权重文件失败: {e}")

    def apply_rule(self, rule_id: str, success: bool, rule_text: str = None,
                   location: str = None) -> None:
        """应用规则后更新权重

        Args:
            rule_id: 规则唯一标识（建议使用规则内容的hash或简短描述）
            success: 应用是否成功
            rule_text: 规则原文（首次记录时需要）
            location: 规则所在文件路径（如 domains/problem-solving.md）
        """
        now = datetime.now().isoformat()

        if rule_id not in self.weights:
            # 新规则，初始化
            self.weights[rule_id] = {
                'text': rule_text or rule_id,
                'weight': 0.5,  # 初始权重
                'last_used': now,
                'success_count': 0,
                'failure_count': 0,
                'created': now,
                'location': location
            }

        rule = self.weights[rule_id]
        rule['last_used'] = now

        if success:
            rule['weight'] = min(1.0, rule['weight'] + 0.01)
            rule['success_count'] += 1
        else:
            rule['weight'] = max(0.0, rule['weight'] - 0.05)
            rule['failure_count'] += 1

        # 更新文本和位置（如果提供）
        if rule_text:
            rule['text'] = rule_text
        if location:
            rule['location'] = location

        self.save_weights()

    def get_rule_weight(self, rule_id: str) -> float:
        """获取规则权重"""
        return self.weights.get(rule_id, {}).get('weight', 0.5)

    def decay_old_rules(self, days: int = 30) -> int:
        """衰减长期未使用的规则权重

        Args:
            days: 未使用天数阈值

        Returns:
            被衰减的规则数量
        """
        cutoff = datetime.now() - timedelta(days=days)
        decayed = 0

        for rule_id, rule in self.weights.items():
            last_used = datetime.fromisoformat(rule['last_used'])
            if last_used < cutoff:
                old_weight = rule['weight']
                rule['weight'] *= 0.9
                if rule['weight'] < 0.01:
                    rule['weight'] = 0.01  # 保留最低权重
                decayed += 1
                print(f"[INFO] 衰减规则: {rule_id[:50]}... {old_weight:.3f} → {rule['weight']:.3f}")

        if decayed > 0:
            self.save_weights()

        return decayed

    def auto_upgrade(self, memory_file: str = None) -> List[str]:
        """自动升级高权重规则到HOT层（memory.md）

        Args:
            memory_file: memory.md文件路径

        Returns:
            被升级的规则ID列表
        """
        if memory_file is None:
            workspace = Path(__file__).parent.parent
            memory_file = workspace / "memory" / "MEMORY.md"

        memory_path = Path(memory_file)

        # 读取现有memory.md内容
        existing_content = ""
        if memory_path.exists():
            existing_content = memory_path.read_text(encoding='utf-8')

        upgraded = []

        for rule_id, rule in self.weights.items():
            if rule['weight'] > 0.8:
                # 检查是否已在memory.md中
                if rule['text'] not in existing_content:
                    # 添加到memory.md
                    self._add_to_memory(memory_path, rule, existing_content)
                    upgraded.append(rule_id)
                    print(f"[OK] 升级规则到HOT层: {rule_id[:50]}... (权重={rule['weight']:.3f})")

        return upgraded

    def _add_to_memory(self, memory_path: Path, rule: Dict[str, Any],
                       existing_content: str) -> None:
        """添加规则到memory.md"""
        # 确定插入位置（在文件末尾或特定section）
        new_entry = f"\n## 自动升级规则\n\n- **{rule['text']}**\n  - 来源：权重系统自动升级（权重={rule['weight']:.3f}）\n  - 触发次数：{rule['success_count'] + rule['failure_count']}\n  - 成功率：{rule['success_count']}/{rule['success_count'] + rule['failure_count']}\n  - 最后使用：{rule['last_used']}\n"

        with open(memory_path, 'a', encoding='utf-8') as f:
            f.write(new_entry)

    def auto_downgrade(self, threshold: float = 0.3) -> List[str]:
        """自动降级/标记低权重规则

        Args:
            threshold: 权重阈值，低于此值考虑降级

        Returns:
            低权重规则ID列表
        """
        low_weight = [
            rule_id for rule_id, rule in self.weights.items()
            if rule['weight'] < threshold
        ]

        if low_weight:
            print(f"[INFO] 发现 {len(low_weight)} 条低权重规则（<{threshold}）:")
            for rule_id in low_weight[:10]:  # 只显示前10条
                rule = self.weights[rule_id]
                print(f"  - {rule_id[:50]}... (权重={rule['weight']:.3f}, 使用={rule['success_count']+rule['failure_count']}次)")

        return low_weight

    def weekly_review(self) -> Dict[str, Any]:
        """生成周度审查报告

        Returns:
            包含审查结果的字典
        """
        if not self.weights:
            return {"error": "无规则数据"}

        total_rules = len(self.weights)
        avg_weight = sum(r['weight'] for r in self.weights.values()) / total_rules

        # 按权重排序
        sorted_rules = sorted(
            self.weights.items(),
            key=lambda x: x[1]['weight'],
            reverse=True
        )

        # 最近使用（7天内）
        week_ago = datetime.now() - timedelta(days=7)
        recently_used = [
            rule_id for rule_id, rule in self.weights.items()
            if datetime.fromisoformat(rule['last_used']) > week_ago
        ]

        # 高权重规则（>0.8）
        high_weight = [rid for rid, r in self.weights.items() if r['weight'] > 0.8]

        # 低权重规则（<0.3）
        low_weight = [rid for rid, r in self.weights.items() if r['weight'] < 0.3]

        # 成功率最高的规则
        top_success = sorted(
            self.weights.items(),
            key=lambda x: (
                x[1]['success_count'] / (x[1]['success_count'] + x[1]['failure_count'])
                if (x[1]['success_count'] + x[1]['failure_count']) > 0 else 0
            ),
            reverse=True
        )[:5]

        return {
            'timestamp': datetime.now().isoformat(),
            'total_rules': total_rules,
            'avg_weight': round(avg_weight, 3),
            'high_weight_rules': len(high_weight),
            'low_weight_rules': len(low_weight),
            'recently_used': len(recently_used),
            'top_success_rules': [
                {
                    'id': rid,
                    'text': r['text'][:100],
                    'success_rate': r['success_count'] / (r['success_count'] + r['failure_count']) if (r['success_count'] + r['failure_count']) > 0 else 0,
                    'uses': r['success_count'] + r['failure_count']
                }
                for rid, r in top_success
            ],
            'recommendations': {
                'upgrade_candidates': [rid for rid, r in self.weights.items() if r['weight'] > 0.75 and r['success_count'] > 5],
                'downgrade_candidates': low_weight[:10],
                'review_needed': [rid for rid, r in self.weights.items() if 0.4 <= r['weight'] <= 0.6 and r['success_count'] + r['failure_count'] > 10]
            }
        }

    def get_recently_used(self, days: int = 7) -> List[Tuple[str, Dict[str, Any]]]:
        """获取最近使用的规则

        Args:
            days: 天数

        Returns:
            (rule_id, rule) 元组列表，按使用时间排序
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            (rid, rule) for rid, rule in self.weights.items()
            if datetime.fromisoformat(rule['last_used']) > cutoff
        ]
        return sorted(recent, key=lambda x: x[1]['last_used'], reverse=True)

    def export_stats(self) -> Dict[str, Any]:
        """导出统计信息"""
        if not self.weights:
            return {}

        total_uses = sum(r['success_count'] + r['failure_count'] for r in self.weights.values())
        total_success = sum(r['success_count'] for r in self.weights.values())

        # 按location分组
        by_location = {}
        for rule in self.weights.values():
            loc = rule.get('location', 'unknown')
            if loc not in by_location:
                by_location[loc] = {'count': 0, 'total_uses': 0, 'total_success': 0}
            by_location[loc]['count'] += 1
            by_location[loc]['total_uses'] += rule['success_count'] + rule['failure_count']
            by_location[loc]['total_success'] += rule['success_count']

        return {
            'total_rules': len(self.weights),
            'total_uses': total_uses,
            'overall_success_rate': total_success / total_uses if total_uses > 0 else 0,
            'by_location': by_location,
            'generated_at': datetime.now().isoformat()
        }


def main():
    """命令行接口"""
    import sys

    manager = RuleWeightManager()

    if len(sys.argv) < 2:
        print("用法: rule_weight_manager.py <command> [args...]")
        print("\n命令:")
        print("  apply <rule_id> <success|failure> [rule_text] [location]")
        print("    应用规则并更新权重")
        print("  decay [days]")
        print("    衰减长期未使用的规则（默认30天）")
        print("  upgrade [memory_file]")
        print("    自动升级高权重规则到memory.md")
        print("  downgrade [threshold]")
        print("    列出低权重规则（默认阈值0.3）")
        print("  review")
        print("    生成周度审查报告")
        print("  stats")
        print("    导出统计信息")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'apply':
        if len(sys.argv) < 4:
            print("错误: apply需要rule_id和success|failure参数")
            sys.exit(1)
        rule_id = sys.argv[2]
        success = sys.argv[3].lower() == 'success'
        rule_text = sys.argv[4] if len(sys.argv) > 4 else None
        location = sys.argv[5] if len(sys.argv) > 5 else None
        manager.apply_rule(rule_id, success, rule_text, location)
        print(f"[OK] 规则 '{rule_id}' 权重已更新")

    elif command == 'decay':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        count = manager.decay_old_rules(days)
        print(f"[OK] 衰减了 {count} 条规则")

    elif command == 'upgrade':
        memory_file = sys.argv[2] if len(sys.argv) > 2 else None
        upgraded = manager.auto_upgrade(memory_file)
        print(f"[OK] 升级了 {len(upgraded)} 条规则到HOT层")

    elif command == 'downgrade':
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
        low = manager.auto_downgrade(threshold)
        print(f"[INFO] 共 {len(low)} 条规则权重低于{threshold}")

    elif command == 'review':
        report = manager.weekly_review()
        print(json.dumps(report, indent=2, ensure_ascii=False))

    elif command == 'stats':
        stats = manager.export_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))

    else:
        print(f"错误: 未知命令 '{command}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
