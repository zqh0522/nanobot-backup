from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

# 搜索 600519 - 同时搜索上海(1)和深圳(0)市场
found = False
for market in [1, 0]:
    print(f'Searching market {market}...')
    for start in range(0, 20000, 1000):
        stocks = api.get_security_list(market, start)
        if not stocks:
            break
        for stock in stocks:
            if stock['code'] == '600519':
                print(f'Found 600519 in market {market} at offset {start}:', stock)
                found = True
                break
        if found:
            break
    if found:
        break

if not found:
    print('600519 not found in first 20000 records of both markets')

api.disconnect()
