#!/usr/bin/env python3
"""
意图路由器 - 功能回路的核心组件
识别用户意图并路由到对应的预编译技能链
"""

import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
import json

class IntentRouter:
    """意图路由器"""

    def __init__(self, mappings_file: str = None):
        """初始化路由器

        Args:
            mappings_file: 意图映射表文件路径（默认：memory/intent_mappings.md）
        """
        if mappings_file is None:
            workspace = Path(__file__).parent.parent
            mappings_file = workspace / "memory" / "intent_mappings.md"

        self.mappings_file = Path(mappings_file)
        self.intent_patterns = self._load_patterns()
        self.loops = {}
        self.metrics = {
            'total_requests': 0,
            'intent_counts': {},
            'response_times': {},
            'success_counts': {}
        }
        self._register_default_loops()

    def _load_patterns(self) -> Dict[str, List[str]]:
        """从映射表加载意图模式"""
        # 硬编码高频模式（基于历史分析）
        patterns = {
            'github': [
                'git', 'github', '推送', '提交', '备份', '远程', '仓库',
                'commit', 'push', 'pull', 'clone', 'branch', 'merge'
            ],
            'stock': [
                '股票', '行情', '价格', 'K线', '实时', '600', '000', '300',
                '茅台', '平安', '银行', '证券', '药业', '科技'
            ],
            'analysis': [
                '分析', '建议', '投资', '技术面', '基本面', 'MACD', 'RSI',
                '均线', '买入', '卖出', '持有', '评级', '目标价'
            ],
            'search': [
                '搜索', '查找', '资料', '新闻', '了解', '查询', '资料',
                'search', 'find', 'google', 'baidu', 'bing'
            ],
            'memory': [
                '历史', '之前', '说过', '回忆', 'HISTORY', 'MEMORY',
                '记录', '说过什么', '之前说过', '记得'
            ],
            'system': [
                '状态', '检查', '诊断', '服务', '运行', '系统', '配置',
                'status', 'check', 'health', 'monitor'
            ]
        }
        return patterns

    def _register_default_loops(self):
        """注册默认功能回路"""
        self.loops = {
            'github': self._execute_github_loop,
            'stock': self._execute_stock_loop,
            'analysis': self._execute_analysis_loop,
            'search': self._execute_search_loop,
            'memory': self._execute_memory_loop,
            'system': self._execute_system_loop
        }

    def detect_intent(self, user_query: str, context: Dict[str, Any] = None) -> str:
        """检测用户意图

        Args:
            user_query: 用户查询文本
            context: 上下文信息（可选）

        Returns:
            意图名称（如 'github', 'stock'）或 'default'
        """
        query_lower = user_query.lower()
        intent_scores = {}

        # 计算每个意图的匹配分数
        for intent, keywords in self.intent_patterns.items():
            score = 0
            for kw in keywords:
                if kw.lower() in query_lower:
                    score += 1
            if score > 0:
                intent_scores[intent] = score

        if not intent_scores:
            return 'default'

        # 选择最高分的意图
        best_intent = max(intent_scores, key=intent_scores.get)

        # 特殊规则：如果包含"分析"且包含股票代码，优先analysis
        if '分析' in query_lower and any(kw in query_lower for kw in ['股票', '600', '000', '300']):
            if intent_scores.get('analysis', 0) >= 1:
                best_intent = 'analysis'

        # 记录指标
        self.metrics['total_requests'] += 1
        self.metrics['intent_counts'][best_intent] = self.metrics['intent_counts'].get(best_intent, 0) + 1

        return best_intent

    def route(self, intent: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """路由到对应的功能回路

        Args:
            intent: 意图名称
            context: 执行上下文（包含用户查询、会话信息等）

        Returns:
            执行结果字典
        """
        if context is None:
            context = {}

        start_time = time.time()
        success = True
        result = {}

        try:
            if intent in self.loops:
                # 执行预编译回路
                result = self.loops[intent](context)
            else:
                # 回退到默认流程
                result = self._execute_default_loop(context)

        except Exception as e:
            success = False
            result = {
                'error': str(e),
                'intent': intent,
                'fallback': True
            }

        elapsed = time.time() - start_time

        # 记录性能指标
        self._record_metrics(intent, elapsed, success)

        # 添加元数据
        result['intent'] = intent
        result['elapsed_time'] = round(elapsed, 3)
        result['timestamp'] = datetime.now().isoformat()

        return result

    def _record_metrics(self, intent: str, elapsed: float, success: bool):
        """记录性能指标"""
        if intent not in self.metrics['response_times']:
            self.metrics['response_times'][intent] = []
            self.metrics['success_counts'][intent] = 0

        self.metrics['response_times'][intent].append(elapsed)
        if success:
            self.metrics['success_counts'][intent] += 1

        # 保持最近100条记录
        if len(self.metrics['response_times'][intent]) > 100:
            self.metrics['response_times'][intent] = self.metrics['response_times'][intent][-100:]

    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        summary = {
            'total_requests': self.metrics['total_requests'],
            'intent_distribution': self.metrics['intent_counts'],
            'avg_response_times': {},
            'success_rates': {}
        }

        for intent in self.metrics['response_times']:
            times = self.metrics['response_times'][intent]
            if times:
                summary['avg_response_times'][intent] = round(sum(times) / len(times), 3)

            total = len(times)
            success = self.metrics['success_counts'].get(intent, 0)
            if total > 0:
                summary['success_rates'][intent] = round(success / total * 100, 1)

        return summary

    def save_metrics(self, filepath: str = None):
        """保存指标到JSON文件"""
        if filepath is None:
            workspace = Path(__file__).parent.parent
            metrics_dir = workspace / "metrics"
            metrics_dir.mkdir(exist_ok=True)
            filepath = metrics_dir / f"intent_metrics_{datetime.now().strftime('%Y-%m-%d')}.json"

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.get_metrics(), f, indent=2, ensure_ascii=False)

        print(f"[OK] 指标已保存: {filepath}")

    # ========== 预编译功能回路实现 ==========

    def _execute_github_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """GitHub操作回路（git + gh CLI）"""
        import subprocess

        query = context.get('query', '')

        # 检查git仓库状态
        try:
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if not status_result.stdout.strip():
                return {
                    'success': True,
                    'message': '无变更需要提交',
                    'skipped': True
                }

            # 执行git命令序列
            commands = [
                ['git', 'add', '-A'],
                ['git', 'commit', '-m', f'自动备份: {datetime.now().strftime("%Y-%m-%d %H:%M")}'],
                ['git', 'push', 'origin', 'main']
            ]

            results = []
            for cmd in commands:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                results.append({
                    'command': ' '.join(cmd),
                    'returncode': result.returncode,
                    'stdout': result.stdout[:500],
                    'stderr': result.stderr[:500]
                })

                if result.returncode != 0:
                    # 检查Push Protection错误
                    if 'push declined' in result.stderr.lower() or 'secret' in result.stderr.lower():
                        return {
                            'success': False,
                            'message': 'GitHub Push Protection拦截',
                            'error_type': 'secret_detected',
                            'details': result.stderr[:500],
                            'suggestion': '运行敏感信息清理流程'
                        }
                    else:
                        return {
                            'success': False,
                            'message': f'Git命令失败: {cmd[0]}',
                            'error_code': result.returncode,
                            'details': result.stderr[:500],
                            'partial_results': results
                        }

            commit_hash = None
            if len(results) >= 2:
                commit_stdout = results[1].get('stdout', '') or ''
                commit_hash = self._extract_commit_hash(commit_stdout)

            return {
                'success': True,
                'message': 'GitHub操作完成',
                'commands_executed': len(results),
                'commit_hash': commit_hash
            }

        except subprocess.TimeoutExpired as e:
            return {
                'success': False,
                'message': f'命令超时: {e.cmd}',
                'timeout': True
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'未知错误: {str(e)}'
            }

    def _extract_commit_hash(self, commit_output: str) -> str:
        """从git commit输出提取commit hash"""
        import re
        match = re.search(r'\[([a-f0-9]{7,40})\]', commit_output)
        return match.group(1) if match else None

    def _execute_stock_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """股票数据查询回路（集成akshare）"""
        try:
            import akshare as ak
            import pandas as pd

            query = context.get('query', '')

            # 提取股票代码（简单规则：6位数字）
            import re
            stock_code_match = re.search(r'[036][0-9]{5}', query)
            stock_code = stock_code_match.group() if stock_code_match else '000001'  # 默认平安银行

            # 获取实时行情
            try:
                spot_df = ak.stock_zh_a_spot_em()
                stock_data = spot_df[spot_df['代码'] == stock_code]

                if stock_data.empty:
                    return {
                        'success': False,
                        'message': f'未找到股票代码 {stock_code}',
                        'suggestion': '请检查股票代码是否正确（A股6位数字）'
                    }

                stock_info = stock_data.iloc[0].to_dict()

                # 获取最近5日K线
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - pd.Timedelta(days=7)).strftime('%Y%m%d')
                hist_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period='daily',
                    start_date=start_date,
                    end_date=end_date,
                    adjust='qfq'
                )

                recent_prices = hist_df['收盘'].tail(5).tolist() if not hist_df.empty else []

                return {
                    'success': True,
                    'message': '股票查询完成',
                    'data': {
                        'code': stock_code,
                        'name': stock_info.get('名称', ''),
                        'price': float(stock_info.get('最新价', 0)),
                        'change': float(stock_info.get('涨跌幅', 0)),
                        'volume': float(stock_info.get('成交量', 0)),
                        'turnover': float(stock_info.get('成交额', 0)),
                        'recent_prices': recent_prices
                    }
                }

            except Exception as e:
                return {
                    'success': False,
                    'message': f'akshare调用失败: {str(e)}',
                    'fallback': '请检查网络连接或akshare配置'
                }

        except ImportError:
            return {
                'success': False,
                'message': 'akshare未安装',
                'solution': '运行: pip install akshare'
            }

    def _execute_analysis_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """投资分析回路（集成akshare + 技术指标）"""
        try:
            import akshare as ak
            import pandas as pd
            import numpy as np
            from datetime import datetime, timedelta

            query = context.get('query', '')

            # 提取股票代码
            import re
            stock_code_match = re.search(r'[036][0-9]{5}', query)
            stock_code = stock_code_match.group() if stock_code_match else '000001'

            # 获取实时行情
            try:
                spot_df = ak.stock_zh_a_spot_em()
                stock_data = spot_df[spot_df['代码'] == stock_code]

                if stock_data.empty:
                    return {
                        'success': False,
                        'message': f'未找到股票代码 {stock_code}',
                        'suggestion': '请检查股票代码是否正确'
                    }

                stock_info = stock_info = stock_data.iloc[0].to_dict()
                stock_name = stock_info.get('名称', '')

                # 获取最近60日K线数据用于技术分析
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
                hist_df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period='daily',
                    start_date=start_date,
                    end_date=end_date,
                    adjust='qfq'
                )

                if hist_df.empty or len(hist_df) < 20:
                    return {
                        'success': False,
                        'message': '历史数据不足，无法进行技术分析',
                        'data': {'basic_info': stock_info}
                    }

                # 计算技术指标
                close = hist_df['收盘'].astype(float)
                high = hist_df['最高'].astype(float)
                low = hist_df['最低'].astype(float)
                volume = hist_df['成交量'].astype(float)

                # 1. 均线系统
                ma5 = close.rolling(5).mean().iloc[-1]
                ma10 = close.rolling(10).mean().iloc[-1]
                ma20 = close.rolling(20).mean().iloc[-1]
                ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20

                # 2. MACD
                ema12 = close.ewm(span=12, adjust=False).mean()
                ema26 = close.ewm(span=26, adjust=False).mean()
                dif = ema12 - ema26
                dea = dif.ewm(span=9, adjust=False).mean()
                macd = (dif - dea) * 2
                macd_val = macd.iloc[-1]
                macd_signal = dea.iloc[-1]

                # 3. RSI
                delta = close.diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                rsi_val = rsi.iloc[-1]

                # 4. 布林带
                bb_middle = close.rolling(20).mean()
                bb_std = close.rolling(20).std()
                bb_upper = bb_middle + 2 * bb_std
                bb_lower = bb_middle - 2 * bb_std
                current_price = close.iloc[-1]
                bb_position = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1]) if bb_upper.iloc[-1] != bb_lower.iloc[-1] else 0.5

                # 5. 成交量分析
                vol_ma5 = volume.rolling(5).mean()
                vol_ratio = volume.iloc[-1] / vol_ma5.iloc[-1] if vol_ma5.iloc[-1] > 0 else 1

                # 综合评分（0-100）
                score = 50  # 基础分
                factors = []

                # 均线系统（+0-20分）
                if ma5 > ma10 > ma20:
                    score += 15
                    factors.append("均线多头排列")
                elif ma5 > ma10:
                    score += 8
                    factors.append("短期均线向上")

                # MACD（+0-15分）
                if macd_val > macd_signal and macd_val > 0:
                    score += 12
                    factors.append("MACD金叉向上")
                elif macd_val > macd_signal:
                    score += 6
                    factors.append("MACD金叉")

                # RSI（+0-15分）
                if 30 < rsi_val < 70:
                    score += 10
                    factors.append("RSI健康区间")
                elif rsi_val < 30:
                    score += 12
                    factors.append("RSI超卖，可能反弹")
                elif rsi_val > 70:
                    score -= 5
                    factors.append("RSI超买，注意回调")

                # 价格位置（+0-10分）
                if bb_position < 0.2:
                    score += 8
                    factors.append("价格接近布林带下轨")
                elif bb_position > 0.8:
                    score -= 5
                    factors.append("价格接近布林带上轨")

                # 成交量（+0-10分）
                if vol_ratio > 1.5:
                    score += 7
                    factors.append("成交量放大")
                elif vol_ratio < 0.7:
                    score -= 5
                    factors.append("成交量萎缩")

                score = max(0, min(100, score))

                # 投资建议
                if score >= 70:
                    recommendation = "买入"
                    reason = "技术指标强势，多头排列"
                elif score >= 55:
                    recommendation = "持有"
                    reason = "趋势中性，等待方向"
                elif score >= 40:
                    recommendation = "减持"
                    reason = "技术指标偏弱"
                else:
                    recommendation = "卖出"
                    reason = "技术指标恶化"

                # 风险提示
                risks = []
                if rsi_val > 75:
                    risks.append("RSI超买，短期回调风险")
                if macd_val < 0:
                    risks.append("MACD负值，趋势偏空")
                if current_price > bb_upper.iloc[-1]:
                    risks.append("价格突破布林带上轨，可能回归")
                if vol_ratio < 0.8:
                    risks.append("成交量不足，动能减弱")

                return {
                    'success': True,
                    'message': '投资分析完成',
                    'data': {
                        'stock': {
                            'code': stock_code,
                            'name': stock_name,
                            'price': float(current_price),
                            'change': float(stock_info.get('涨跌幅', 0))
                        },
                        'technical_indicators': {
                            'score': score,
                            'recommendation': recommendation,
                            'reason': reason,
                            'ma5': float(ma5),
                            'ma10': float(ma10),
                            'ma20': float(ma20),
                            'macd': float(macd_val),
                            'macd_signal': float(macd_signal),
                            'rsi': float(rsi_val),
                            'bb_position': float(bb_position),
                            'volume_ratio': float(vol_ratio)
                        },
                        'factors': factors,
                        'risks': risks,
                        'analysis_period': f"{hist_df['日期'].iloc[0]} 至 {hist_df['日期'].iloc[-1]}"
                    }
                }

            except Exception as e:
                return {
                    'success': False,
                    'message': f'数据分析失败: {str(e)}',
                    'hint': '可能是股票代码错误或数据源问题'
                }

        except ImportError as e:
            return {
                'success': False,
                'message': f'依赖库缺失: {str(e)}',
                'solution': '运行: pip install akshare pandas numpy'
            }

    def _execute_search_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """网络搜索回路"""
        return {
            'success': True,
            'message': '网络搜索回路',
            'results': ['搜索结果1', '搜索结果2'],
            'note': '需要集成web_search技能'
        }

    def _execute_memory_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """记忆查询回路"""
        query = context.get('query', '')
        return {
            'success': True,
            'message': '记忆查询回路',
            'query': query,
            'results': ['历史记录1', '历史记录2'],
            'note': '需要集成memory技能'
        }

    def _execute_system_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """系统检查回路"""
        return {
            'success': True,
            'message': '系统检查回路',
            'status': {
                'cpu': '正常',
                'memory': '正常',
                'disk': '正常',
                'services': '运行中'
            },
            'note': '需要集成exec技能'
        }

    def _execute_default_loop(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """默认流程（原有决策机制）"""
        return {
            'success': True,
            'message': '使用默认流程处理',
            'intent': 'default',
            'note': '原有技能选择逻辑'
        }


def main():
    """测试入口"""
    router = IntentRouter()

    test_queries = [
        "备份到GitHub",
        "查询贵州茅台行情",
        "分析600519这只股票",
        "搜索最新的AI新闻",
        "我之前说过什么",
        "检查系统状态"
    ]

    print("="*60)
    print("意图路由测试")
    print("="*60)

    for query in test_queries:
        intent = router.detect_intent(query)
        result = router.route(intent, {'query': query})

        print(f"\n查询: {query}")
        print(f"意图: {intent}")
        print(f"耗时: {result['elapsed_time']}秒")
        print(f"结果: {result.get('message', 'N/A')}")

    print("\n" + "="*60)
    print("性能指标:")
    print(json.dumps(router.get_metrics(), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
