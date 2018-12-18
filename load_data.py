'''
Seems like the time given in each file are all in UTC.
'''
import pandas as pd
import numpy as np

data_dir = '/media/bowang/FREECOM HDD/crypto_liquidity/'
file_template = '{exchange}_SPOT_{crypto}_{currency}_{date}_{data_type}.csv'

def load_quote(the_date, the_exchange='BINANCE', the_crypto='BTC', the_currency='USDT'):
    '''
    the_date: str or int like 20180101
    the_exchange: {'BINANCE', 'BITFINEX', 'HUOBIPRO', 'BITMEX', 'POLONIEX', ...}
    the_crypto: {'BTC', 'ETH', ...}
    the_currency: {'USDT', 'USD', ...}
    '''
    formatted_date = str(the_date)
    formatted_date = formatted_date[4:] + formatted_date[:4]
    the_file = data_dir + file_template.format(exchange=the_exchange, crypto=the_crypto,\
                                               currency=the_currency, date=formatted_date,\
                                               data_type='quote')
    dat = pd.read_csv(the_file, index_col=0)
    dat['time_coinapi'] = pd.to_datetime(dat['time_coinapi'])
    dat['time_exchange'] = pd.to_datetime(dat['time_exchange'])
    return dat

def load_depth(the_date, the_exchange='BINANCE', the_crypto='BTC', the_currency='USDT'):
    '''
    the_date: str or int like 20180101
    the_exchange: {'BINANCE', 'BITFINEX', 'HUOBIPRO', 'BITMEX', 'POLONIEX', ...}
    the_crypto: {'BTC', 'ETH', ...}
    the_currency: {'USDT', 'USD', ...}
    '''
    formatted_date = str(the_date)
    formatted_date = formatted_date[4:] + formatted_date[:4]
    the_file = data_dir + file_template.format(exchange=the_exchange, crypto=the_crypto,\
                                               currency=the_currency, date=formatted_date,\
                                               data_type='depth')
    dat = pd.read_csv(the_file)
    dat['time_exchange'] = pd.to_datetime(dat['time_exchange'])
    return dat

def load_trade(the_date, the_exchange='BINANCE', the_crypto='BTC', the_currency='USDT'):
    '''
    the_date: str or int like 20180101
    the_exchange: {'BINANCE', 'BITFINEX', 'HUOBIPRO', 'BITMEX', 'POLONIEX', ...}
    the_crypto: {'BTC', 'ETH', ...}
    the_currency: {'USDT', 'USD', ...}
    '''
    formatted_date = str(the_date)
    formatted_date = formatted_date[4:] + formatted_date[:4]
    the_file = data_dir + file_template.format(exchange=the_exchange, crypto=the_crypto,\
                                               currency=the_currency, date=formatted_date,\
                                               data_type='trade')
    dat = pd.read_csv(the_file, index_col=0)
    dat['time_exchange'] = pd.to_datetime(dat['time_exchange'])
    dat['time_coinapi'] = pd.to_datetime(dat['time_coinapi'])
    dat['taker_side'] = dat['taker_side'].astype('category')
    return dat

def combine_trade_quote(*args, **kwargs):
    quote = load_quote(*args, **kwargs)
    trade = load_trade(*args, **kwargs)
    ret = trade.set_index('time_exchange').join(quote.set_index('time_exchange')\
                [['ask_price', 'ask_size','bid_price','bid_size']], how='outer').reset_index()
    return ret

def main():
    quote = load_quote(20180101)
    depth = load_depth(20180101)
    trade = load_trade(20180101)

if __name__ == '__main__':
    main()
