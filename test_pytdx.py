#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 pytdx 实时行情连接"""

from pytdx.hq import TdxHq_API
import sys
import time

def test_connect(ip, port):
    """测试连接"""
    print(f"[{time.strftime('%H:%M:%S')}] 测试连接 {ip}:{port}")
    sys.stdout.flush()

    api = TdxHq_API()
    start = time.time()

    try:
        # pytdx 的 connect 方法不接受 timeout 参数
        result = api.connect(ip, port)
        elapsed = time.time() - start
        print(f"[{time.strftime('%H:%M:%S')}] 连接结果: {result}, 耗时: {elapsed:.2f}s")
        sys.stdout.flush()

        if result:
            # 获取股票列表
            print(f"[{time.strftime('%H:%M:%S')}] 获取股票列表...")
            sys.stdout.flush()
            stocks = api.get_security_list(1, 0, 5)
            print(f"前5只沪市股票: {[s['code'] for s in stocks]}")
            sys.stdout.flush()

            # 获取实时行情
            print(f"[{time.strftime('%H:%M:%S')}] 获取 600519 实时行情...")
            sys.stdout.flush()
            quotes = api.get_security_quotes([(1, '600519')])
            df = api.to_df(quotes)
            print("实时行情数据:")
            print(df.to_string())
            sys.stdout.flush()

            api.disconnect()
            print(f"[{time.strftime('%H:%M:%S')}] 已断开连接")
            sys.stdout.flush()
            return True
        else:
            print(f"[{time.strftime('%H:%M:%S')}] 连接返回 False")
            sys.stdout.flush()
            return False

    except Exception as e:
        elapsed = time.time() - start
        print(f"[{time.strftime('%H:%M:%S')}] 异常: {type(e).__name__}: {e}, 耗时: {elapsed:.2f}s")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("pytdx 实时行情测试")
    print("=" * 60)

    servers = [
        ('115.238.90.165', 7709),  # 移动首选
        ('60.191.117.167', 7709),  # 电信次选
    ]

    for ip, port in servers:
        success = test_connect(ip, port)
        if success:
            print(f"\n[OK] 服务器 {ip}:{port} 工作正常")
            break
        else:
            print(f"\n[FAIL] 服务器 {ip}:{port} 失败，尝试下一个...")

    print("\n测试完成")