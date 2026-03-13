from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

print('Scanning Shenzhen market for normal A-shares (000/001/002/003)...')
found_normal = []
for start in range(0, 10000, 1000):
    stocks = api.get_security_list(0, start)
    if not stocks:
        break
    for stock in stocks:
        code = stock['code']
        if code.startswith(('000', '001', '002', '003')):
            found_normal.append((start, code, stock['name'], stock['pre_close']))

print(f'Found {len(found_normal)} normal A-shares:')
for offset, code, name, pre_close in found_normal[:20]:
    print(f'  Offset {offset}: {code} {name} {pre_close}')

api.disconnect()
