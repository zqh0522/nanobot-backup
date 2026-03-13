from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

print('Scanning Shanghai market for normal A-shares (600/601/603)...')
found_normal = []
for start in range(0, 20000, 1000):
    stocks = api.get_security_list(1, start)
    if not stocks:
        print(f'Offset {start}: No more stocks')
        break
    print(f'Offset {start}: {len(stocks)} stocks')
    for stock in stocks:
        code = stock['code']
        if code.startswith(('600', '601', '603')):
            found_normal.append((start, code, stock['name'], stock['pre_close']))

print(f'\nFound {len(found_normal)} normal Shanghai A-shares:')
for offset, code, name, pre_close in found_normal[:20]:
    print(f'  Offset {offset}: {code} {name} {pre_close}')

if not found_normal:
    print('No 600/601/603 codes found!')

api.disconnect()
