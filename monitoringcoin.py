from pycoingecko import CoinGeckoAPI
from datetime import datetime
import pandas as pd
import numpy as np
import time 
import pytz
import gspread

cg = CoinGeckoAPI()

credentials = {
  "type": "service_account",
  "project_id": "micro-shoreline-356004",
  "private_key_id": "f027bb8a83bd73aeeced0243093daeba4b8e9dad",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC6Dh6py29v2Yyu\n1/0Mws9LzSlBBrsK+X24nU3mBadWl08Zhbfshkz91SC023G2qYZHF9H9seZk3IGR\nGbhJlVqlUmsIKUeXfTn5sqyrSk4jZTDCgNNMhD3xfS7ySaDE2RbSmxpXl2o7dq4k\n4ts7Q7RE9mCGVCsJ/WoOOrs8Oa8SVDZGn7oIIA3ZgydYDfyytfinG7r5tVnmgRFO\nS3s80Lpx9OPdeGv9xNo8zyviahKTnjmSkdW1ILgT8i3NBlS0wjM2oWoLxcpZAQMs\nMR77WGR4jiajkvLVLTFOVqKwejR1eNzioTVwd98ah6nBtGFIbFsQIP1K3CcMhuSm\npcckg9+fAgMBAAECggEAAzeMSIOiendzVcXunlezTYxkwAxAPq6AAdRXzPg1uQBm\nbJAMf+lLOoECuZh+bQSdtEFRWbFyROCFLapEA/hc+Ap78Z5ZGmGewiut4vZRceOQ\nMMTDzTO6KHXxfQdQjCbJchHJe6Xmvyl3AF9Fys60YWmLKLdwLmeJ0ROAj52Ft+uM\n5fce59SY7N+M5Yh2ymqSizU5HoJhPsNaqC2F12/Ju/PsRHhwHDkH5KZmEAat6E89\nXk4BUxpKbGYa8FMKxnYBoX2Lt0ybCla2A/3jD77Igv+obWlSZjuvTw+5A0Nf2Y7B\npcMttbt3n6vvFzZmeR/g9l9hjqcDcGubDPq0+TH2fQKBgQD3g2INgtQpyZhFO7/B\nzJTsTTR86G1Jns1oHLFZ8z73pOO4rznzadJWcxGzs1KbJud6xaB8gDG56hW8hKU1\njWegzqkaXedSJeH2xWmcQ3eKdy9j3h5DctkcaPK6NUxUq4nuDcws6RsZ8IjtkBWs\n8/EZYEQdZZGTFgec2xwUujHZnQKBgQDAb0V1ol0T9oHsEdT9qkraBYnw08HjNxy6\nztYbMmI+DxMAZMs8X21/6Bj0dFr+HErUl2RFypOapH031zzW+RcnLBmf8634uHe3\nL31cUgaFfKTi/Hw4gJ6pdInOuuAO8fjAZsZ3z/RHcsO2P9EnlDkednC27A2FvsLf\nl1SxWHMnawKBgQCrxJDCgZ2NVmsG+P0NmFVtW/LmEELvyXYRH4BwxR9YqySh4XDd\nHP4sonSRegwEwk34ZLgITsqzk+D70C366SQWc/Tk6HAFEWcsYzn0iNmnzSilLNth\nwY0saySv1xce12DERO0B6c+2A7hy7QAt46jZDHaY1Ajfw3ULBQAK3mCD/QKBgQCF\nBmaFww+E1UtK3ajXEflcbafFixzk7Rw3JvRrKJExRUplY0f7HByd5twZYLXmI7i2\n7VCrzjXrGPpWt7ue/+I5egrcv57r6NkZEQMf5rQLYva40sEsbf1ANwdsmVJ6Altq\n5aEdAexj17njKopzScuSe12/lb5jTlN4LSymy/YOsQKBgQC40NAbAlbq0oiQ14P9\npQuv2Xm3PcDviwAxUQwdnYtl5FS26m4Obq2GNT95wdArNg6eKmzZIagcqOkRQrTw\nD9EURfcyuSKmVFnpadvO9N8gVKVtyfHTZqiJ8P2/pxKGNkerTY0ojpIG/l6nJR3m\nHf7YNc5PQkCAcFiJn3LOqmf0Xw==\n-----END PRIVATE KEY-----\n",
  "client_email": "weighteddatabase@micro-shoreline-356004.iam.gserviceaccount.com",
  "client_id": "118253635217672896363",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/weighteddatabase%40micro-shoreline-356004.iam.gserviceaccount.com"
}

sa = gspread.service_account_from_dict(credentials)
sh = sa.open('CoinMonitoring')
wks = sh.worksheet('Top10')

def get_backlog():
  df = pd.DataFrame(cg.get_coins_markets(vs_currency='usd', order='market_cap_desc'))
  df.symbol = df.symbol.str.upper()
  df = df[['id','symbol']]

  stablecoin = ['USDT','USDC','UST','BUSD','SHIB','DOGE','WBTC','DAI','STETH','LUNC']
  for k in range(len(stablecoin)):
    df.symbol.replace(to_replace=[stablecoin[k]], value = np.nan, inplace=True)
  df.dropna(inplace=True)  
  df.set_index('id',inplace=True)
  df.reset_index(inplace=True)

  df = df[:10]

  wks.update('A1','Name')
  wks.update('B1','Ticker')
  wks.update('C1','Price')
  wks.update('D1','1h percent change')
  wks.update('E1','24h percent change')
  wks.update('F1','7d percent change')
  wks.update('G1','MarketCap')
  wks.update('H1','30d percent marketcap change')
  wks.update('I1','Marketcap Criteria')
  wks.update('J1','Volume')
  wks.update('K1','30d percent volume change')
  wks.update('L1','Volume Criteria')
  wks.update('M1','Date')
  wks.update('N1','Time')

  return df

def get_data(coins):
  data = pd.DataFrame(cg.get_coins_markets(vs_currency='usd', ids=coins, order='market_cap_desc', price_change_percentage='1h,24h,7d'))
  data = data[['name','symbol','current_price','market_cap','total_volume','price_change_percentage_1h_in_currency','price_change_percentage_24h_in_currency','price_change_percentage_7d_in_currency']]
  data['symbol'] = data.symbol.str.upper()
  data.columns = ['name','symbol','price','marketcap','volume','change1h','change24h','change7d']

  mkt = pd.DataFrame(cg.get_coin_market_chart_by_id(id=coins, vs_currency='usd', days=30, interval='daily')['market_caps'])
  mkt[0] = pd.to_datetime(mkt[0], unit='ms')
  mkt30per = (mkt.iloc[-1,1] - mkt.iloc[0,1])/mkt.iloc[0,1]

  vol = pd.DataFrame(cg.get_coin_market_chart_by_id(id=coins, vs_currency='usd', days=30, interval='daily')['total_volumes'])
  vol[0] = pd.to_datetime(vol[0], unit='ms')
  vol30per = (vol.iloc[-1,1] - vol.iloc[0,1])/vol.iloc[0,1]

  return data, mkt30per, vol30per

def cap_criteria(mkt):
  cap_cri = []
  if mkt > 10000e6:
      cap_cri.append('Mega Cap')
  elif (mkt < 10000e6) & (mkt >= 1000e6):
      cap_cri.append('Large Cap')
  elif (mkt < 1000e6) & (mkt >= 200e6):
      cap_cri.append('Mid Cap')
  elif (mkt < 200e6) & (mkt >= 100e6):
      cap_cri.append('Small Cap')
  elif (mkt < 100e6) & (mkt >= 20e6):
      cap_cri.append('Micro Cap')
  elif (mkt < 20e6):
      cap_cri.append('Nano Cap')
  
  return cap_cri

def vol_criteria(vol): 
  vol_cri = []
  if vol > 10000e6:
      vol_cri.append('Criteria A')
  elif (vol < 10000e6) & (vol >= 1000e6):
      vol_cri.append('Criteria B')
  elif (vol < 1000e6) & (vol >= 300e6):
      vol_cri.append('Criteria C')
  elif (vol < 300e6) & (vol >= 50e6):
      vol_cri.append('Criteria D')
  elif (vol < 50e6) & (vol >= 10e6):
      vol_cri.append('Criteria E')
  elif (vol < 10e6) & (vol >= 1e6):
      vol_cri.append('Criteria F')    
  elif (vol < 1e6):
      vol_cri.append('Criteria G')

  return vol_cri

def add_sheet(data, mkt30per, vol30per, cap_cri, vol_cri, i):
  wks.update('A'+str(i+1),data.name[0])
  wks.update('B'+str(i+1),data.symbol[0])
  wks.update('C'+str(i+1),float(data.price))
  wks.update('D'+str(i+1),float(data.change1h/100))
  wks.update('E'+str(i+1),float(data.change24h/100))
  wks.update('F'+str(i+1),float(data.change7d/100))
  wks.update('G'+str(i+1),float(data.marketcap))
  wks.update('H'+str(i+1),float(mkt30per))
  wks.update('I'+str(i+1),cap_cri[0])
  wks.update('J'+str(i+1),float(data.volume))
  wks.update('K'+str(i+1),float(vol30per))
  wks.update('L'+str(i+1),vol_cri[0])
  time.sleep(15)

df = get_backlog()

# while True:
time.sleep(600-time.time()%600)
d = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%d/%m/%Y')
t = datetime.now(pytz.timezone('Asia/Bangkok')).strftime('%H:%M:%S')
wks.update('M2', d)
wks.update('N2', t)
for i in range(1,11):
    data, mkt30per, vol30per = get_data(df.id[i-1])
    cap_cri = cap_criteria(float(data.marketcap))
    vol_cri = vol_criteria(float(data.volume))
    add_sheet(data, mkt30per, vol30per, cap_cri, vol_cri, i)
