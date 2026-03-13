from pytdx.hq import TdxHq_API

servers = [
    ('115.238.90.165', 7709),
    ('60.191.117.167', 7709),
    ('119.147.212.81', 7709),
    ('119.147.212.83', 7709),
    ('218.80.248.229', 7709),
    ('180.153.39.51', 7709),
    ('180.153.18.171', 7709),
    ('61.152.107.141', 7709),
]

for ip, port in servers:
    print(f'\n=== Testing {ip}:{port} ===')
    api = TdxHq_API()
    try:
        api.connect(ip, port)
        print('  Connected!')

        # Try to get 600519 quotes with market=1
        quotes = api.get_security_quotes([('1', '600519')])
        if quotes:
            print(f'  SUCCESS! Got quotes for 600519: {quotes[0]["price"]}')
        else:
            print('  No quotes for 600519 (market 1)')

        # Check if Shanghai market has any stocks
        sh_list = api.get_security_list(1, 0)
        if sh_list:
            print(f'  Shanghai market has {len(sh_list)} stocks at offset 0')
        else:
            print('  Shanghai market empty at offset 0')

        api.disconnect()
    except Exception as e:
        print(f'  Error: {e}')
