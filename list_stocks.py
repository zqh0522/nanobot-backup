from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

print('=== Shanghai Market (1) ===')
for start in [0, 1000]:
    stocks = api.get_security_list(1, start)
    if not stocks:
        break
    print(f'Offset {start}:')
    for stock in stocks[:5]:
        print(f"  Code: {stock['code']}, Name: {stock['name']}, PreClose: {stock['pre_close']}")

print('\n=== Shenzhen Market (0) ===')
for start in [0, 1000]:
    stocks = api.get_security_list(0, start)
    if not stocks:
        break
    print(f'Offset {start}:')
    for stock in stocks[:5]:
        print(f"  Code: {stock['code']}, Name: {stock['name']}, PreClose: {stock['pre_close']}")

api.disconnect()
