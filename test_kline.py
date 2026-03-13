from pytdx.hq import TdxHq_API
import datetime

api = TdxHq_API()
api.connect('115.238.90.165', 7709)

# Try to get K-line data for 600519
# Parameters: market, code, start_date, end_date
# Market: 1 for Shanghai, 0 for Shenzhen
# Date format: YYYYMMDD as integer

today = datetime.date.today()
start_date = int((today - datetime.timedelta(days=7)).strftime('%Y%m%d'))
end_date = int(today.strftime('%Y%m%d'))

print(f'Fetching K-line for 600519, market=1, from {start_date} to {end_date}')

try:
    klines = api.get_k_line(1, '600519', start_date, end_date)
    if klines:
        print(f'Got {len(klines)} K-line records')
        for k in klines[:3]:
            print(k)
    else:
        print('No K-line data returned')
except Exception as e:
    print(f'Error: {e}')

api.disconnect()
