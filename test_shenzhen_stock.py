from pytdx.hq import TdxHq_API

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

# Try to get quotes for 000001 (Ping An Bank) - Shenzhen market
quotes = api.get_security_quotes([('0', '000001')])
print('Quotes for 000001:', quotes)

if quotes:
    quote = quotes[0]
    print(f"\nDetails:")
    print(f"  Name: {quote.get('name', 'N/A')}")
    print(f"  Code: {quote.get('code', 'N/A')}")
    print(f"  Price: {quote.get('price', 'N/A')}")
    print(f"  Open: {quote.get('open', 'N/A')}")
    print(f"  High: {quote.get('high', 'N/A')}")
    print(f"  Low: {quote.get('low', 'N/A')}")
    print(f"  Volume: {quote.get('vol', 'N/A')}")
    print(f"  Amount: {quote.get('amount', 'N/A')}")

api.disconnect()
