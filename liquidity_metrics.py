from load_data import *
import matplotlib.pyplot as plt

def dollar_volume(trade_dat, currency='USD'):
    '''
    even though the currency may not be USD, we still call it 'dollar' volume
    if need daily|hour|minute dollar volume, feed in the slice as argument
    '''
    return (trade_dat['price'] * trade_dat['size']).sum()

def mean_trade_dolar_size(trade_dat, currency='USD'):
    '''
    even though the currency may not be USD, we still call it 'dollar' volume
    if need daily|hour|minute trade size, feed in the slice as argument
    '''
    return (trade_dat['price'] * trade_dat['size']).mean()

def num_of_trades(trade_dat, currency='USD'):
    '''
    even though the currency may not be USD, we still call it 'dollar' volume
    if need daily|hour|minute trade size, feed in the slice as argument
    '''
    return trade_dat['size'].count()

def mean_baspread(depth_dat, currency='USD'):
    '''
    mean bid ask spread
    if need daily|hour|minute dollar volume, feed in the slice as argument
    '''
    return (depth_dat['ask1_price'] - depth_dat['bid1_price']).mean()

def mean_baspread_basispoint(depth_dat, currency='USD'):
    '''
    mean bid ask spread in basis point
    if need daily|hour|minute dollar volume, feed in the slice as argument
    '''
    midquote = (depth_dat['ask1_price'] + depth_dat['bid1_price'])/2.
    return ((depth_dat['ask1_price'] - depth_dat['bid1_price']) / midquote).mean()*1e4

def merge_trade_depth(trade_dat, depth_dat):
    dat = trade.set_index('time_exchange')[['price','size']]\
            .join(depth.set_index('time_exchange')[['bid1_price','ask1_price']],how='outer')
    dat[['bid1_price','ask1_price']] = dat[['bid1_price','ask1_price']].ffill()
    dat.dropna(inplace=True)
    return dat

def volume_weighted_ave_baspread(dat, currency='USD'):
    dat['baspread'] = dat['ask1_price'] - dat['bid1_price']
    dat['midquote'] = (dat['ask1_price'] + dat['bid1_price'])/2.
    dat['basbp'] = dat['baspread'] / dat['midquote'] * 1e4
    dat['volume'] = dat['price'] * dat['size']
    ret = {
    'bid_ask_spread': (dat['baspread'] * dat['volume']).sum() / dat['volume'].sum(),
    'bid_ask_spread_basis_point': (dat['basbp'] * dat['volume']).sum() / dat['volume'].sum()
    }
    return ret

def main():
    quote = load_quote(20180101)
    depth = load_depth(20180101)
    trade = load_trade(20180101)

    hourly_dollar_volume = trade.groupby(trade['time_exchange'].dt.hour).apply(dollar_volume)
    plt.plot(hourly_dollar_volume, marker='*')

    hourly_meanbaspread = depth.groupby(depth['time_exchange'].dt.hour).apply(mean_baspread)
    plt.plot(hourly_meanbaspread, marker='*')

    hourly_basbp = depth.groupby(depth['time_exchange'].dt.hour).apply(mean_baspread_basispoint)
    plt.plot(hourly_basbp, marker='*')
    
    dat = merge_trade_depth(trade,depth)
    dat.groupby(dat.index.hour)\
            .apply(lambda x: pd.Series(volume_weighted_ave_baspread(x))).plot(marker='*')


