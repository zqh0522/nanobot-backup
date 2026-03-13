#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 pytdx 实时行情 - 简化版"""

from pytdx.hq import TdxHq_API
import time

def main():
    api = TdxHq_API()
    print("连接 115.238.90.165:7709...")

    if api.connect('115.238.90.165', 7709):
        print("连接成功！")

        # 方法1: 获取股票列表（尝试不同参数）
        print("\n测试 get_security_list (市场1, 起始0, 数量10)...")
        stocks = api.get_security_list(1, 0, 10)
        print(f"返回类型: {type(stocks)}")
        if stocks:
            print(f"股票数量: {len(stocks)}")
            for s in stocks[:3]:
                print(f"  {s}")
        else:
            print("返回为空")

        # 方法2: 获取实时行情（直接使用）
        print("\n测试 get_security_quotes (600519)...")
        quotes = api.get_security_quotes([(1, '600519')])
        print(f"返回类型: {type(quotes)}")
        if quotes:
            print(f"数据条数: {len(quotes)}")
            df = api.to_df(quotes)
            print("\nDataFrame 列:")
            print(df.columns.tolist())
            print("\n数据:")
            print(df.to_string())
        else:
            print("返回为空")

        # 方法3: 获取日线数据
        print("\n测试 get_security_bars (日线, 600519, 最近10条)...")
        bars = api.get_security_bars(9, 1, '600519', 0, 10)  # 9=日线, 市场1=沪市
        print(f"返回类型: {type(bars)}")
        if bars:
            print(f"K线数量: {len(bars)}")
            df = api.to_df(bars)
            print("\n最近3条K线:")
            print(df[['datetime', 'open', 'close', 'high', 'low', 'vol']].head(3).to_string())
        else:
            print("返回为空")

        api.disconnect()
        print("\n断开连接")
    else:
        print("连接失败")

if __name__ == '__main__':
    main()
