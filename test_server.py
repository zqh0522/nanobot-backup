from pytdx.hq import TdxHq_API

servers = [
    ('115.238.90.165', 7709),
    ('60.191.117.167', 7709),
    ('119.147.212.81', 7709),
    ('119.147.212.83', 7709),
]

for ip, port in servers:
    print(f'\n=== Testing {ip}:{port} ===')
    api = TdxHq_API()
    try:
        api.connect(ip, port)
        print('  Connected!')

        # Try to get security list
        stocks = api.get_security_list(1, 0)
        if stocks:
            print(f'  Shanghai market: {len(stocks)} stocks at offset 0')
            for stock in stocks[:3]:
                print(f"    Code: {stock['code']}, Name: {stock['name']}")
        else:
            print('  Shanghai market: Empty at offset 0')

        stocks = api.get_security_list(0, 0)
        if stocks:
            print(f'  Shenzhen market: {len(stocks)} stocks at offset 0')
            for stock in stocks[:3]:
                print(f"    Code: {stock['code']}, Name: {stock['name']}")
        else:
            print('  Shenzhen market: Empty at offset 0')

        api.disconnect()
    except Exception as e:
        print(f'  Error: {e}')
