from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

print('=== Shanghai Market (1) - Full Scan ===')
for start in range(0, 5000, 1000):
    stocks = api.get_security_list(1, start)
    if not stocks:
        print(f'Offset {start}: No more stocks')
        break
    print(f'Offset {start}: {len(stocks)} stocks')
    for stock in stocks[:10]:
        print(f"  Code: {stock['code']}, Name: {stock['name']}, PreClose: {stock['pre_close']}")

api.disconnect()
