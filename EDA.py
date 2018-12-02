import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path = '/media/bowang/FREECOM HDD/crypto_liquidity/'
trade = pd.read_csv(data_path + 'BINANCE_SPOT_BTC_USDT_trade_01012018.csv',sep=';')
depth = pd.read_csv(data_path + 'BINANCE_SPOT_BTC_USDT_depth_01012018.csv',sep=';')

trade['time_exchange'] = pd.to_datetime(trade['time_exchange'])
trade['time_coinapi'] = pd.to_datetime(trade['time_coinapi'])
trade['taker_side']=trade['taker_side'].astype('category')

depth['time_exchange'] = pd.to_datetime(depth['time_exchange'])
depth['time_coinapi'] = pd.to_datetime(depth['time_coinapi'])
depth['is_buy'] = depth['is_buy'].astype(bool)
depth['update_type'] = depth['update_type'].astype('category')
