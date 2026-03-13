from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

# Try different market codes for 600519
markets_to_try = [1, 0, 2, 3]
for market in markets_to_try:
    quotes = api.get_security_quotes([(str(market), '600519')])
    print(f'Market {market}: {quotes}')

api.disconnect()
