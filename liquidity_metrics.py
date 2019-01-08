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

def market_depth(depth_dat, currency='USD'):
    bid_depth =  (depth_dat.loc[:,['bid{}_price'.format(l) for l in range(1,21)]] *\
                depth_dat.loc[:,['bid{}_size'.format(l) for l in range(1,21)]].values).cumsum(axis=1).mean()
    bid_depth.rename(lambda col: 'cum_depth' + col[3:-6], inplace=True)
    ask_depth =  (depth_dat.loc[:,['ask{}_price'.format(l) for l in range(1,21)]] *\
                depth_dat.loc[:,['ask{}_size'.format(l) for l in range(1,21)]].values).cumsum(axis=1).mean()
    ask_depth.rename(lambda col: 'cum_depth' + col[3:-6], inplace=True)
    return pd.DataFrame({'bid': bid_depth, 'ask': ask_depth})

def plot_market_depth(bid_depth, ask_depth):
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ask_depth.plot(legend=False, ax=ax1)
    ax1.set_title('ask', loc='left')
    ax2.invert_yaxis()
    bid_depth.plot(legend=False, ax=ax2)
    ax2.set_title('bid', loc='left')
    ylim = ax1.get_ylim()
    ax2.set_ylim(ylim[1],ylim[0])
    f.suptitle('market depth')

def price_change_percent(depth_dat, currency='USD'):
    bid_prcpct = depth_dat.loc[:,['bid{}_price'.format(l) for l in range(1,21)]]\
                .apply(lambda col: col / depth_dat.loc[:,'bid1_price'].values-1).mean()
    bid_prcpct.rename(lambda col: 'prcpct' + col[3:-6], inplace=True)
    ask_prcpct = depth_dat.loc[:,['ask{}_price'.format(l) for l in range(1,21)]]\
                .apply(lambda col: col / depth_dat.loc[:,'ask1_price'].values-1).mean()
    ask_prcpct.rename(lambda col: 'prcpct' + col[3:-6], inplace=True)
    return pd.DataFrame({'bid': bid_prcpct, 'ask': ask_prcpct})

def shape_of_order_book(depth_dat, currency='USD'):
    midquote = (depth_dat['ask1_price'] + depth_dat['bid1_price'])/2.
    bid_side = depth_dat.loc[:,['bid{}_price'.format(l) for l in range(1,21)]]\
                .apply(lambda col: col / midquote.values-1).mean() * 100
    ask_side = depth_dat.loc[:,['ask{}_price'.format(l) for l in range(1,21)]]\
                .apply(lambda col: col / midquote.values-1).mean() * 100
    ret = pd.DataFrame(np.nan, \
            index=['bid{}'.format(l) for l in range(20,0,-1)]+['ask{}'.format(l) for l in range(1,21)],\
            columns=['price_change_from_mq', 'cum_shares', 'cum_dollar'])
    ret.loc[['bid{}'.format(l) for l in range(1,21)],'price_change_from_mq'] = bid_side.values
    ret.loc[['ask{}'.format(l) for l in range(1,21)],'price_change_from_mq'] = ask_side.values
    ret.loc[['bid{}'.format(l) for l in range(1,21)],'cum_shares'] =\
            -depth_dat.loc[:,['bid{}_size'.format(l) for l in range(1,21)]].cumsum(axis=1).mean().values
    ret.loc[['ask{}'.format(l) for l in range(1,21)],'cum_shares'] =\
            depth_dat.loc[:,['ask{}_size'.format(l) for l in range(1,21)]].cumsum(axis=1).mean().values
    ret.loc[:,'cum_dollar'] = ret.loc[:,'cum_shares'] * midquote.mean()
    return ret


def plot_prcpct(bid_prcpct, ask_prcpct):
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ask_prcpct.plot(legend=False, ax=ax1)
    ax1.set_title('ask', loc='left')
    ax1.set_yticklabels(['{:,.2%}'.format(x) for x in ax1.get_yticks()])
    bid_prcpct.plot(legend=False, ax=ax2)
    ax2.set_title('bid', loc='left')
    ylim = ax1.get_ylim()
    ax2.set_yticklabels(['{:,.2%}'.format(x) for x in ax2.get_yticks()])
    #ax2.set_ylim(-ylim[1],-ylim[0])
    f.suptitle('price change percent')


def merge_trade_quote(trade_dat, quote_dat):
    dat = trade_dat.set_index('time_exchange')[['price', 'size','taker_side']]\
            .join(quote_dat.set_index('time_exchange')[['ask_price', 'ask_size', 'bid_price', 'bid_size']]\
            ,how='outer')

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

def kyle_lambda(trade, freq='T'):
    trade['dollar_volume'] = trade['price'] * trade['size']
    tmp = trade.set_index('time_exchange').resample(freq).agg({'price':'first','dollar_volume':'sum'})
    del trade['dollar_volume']
    tmp['price_delta'] = tmp['price'].diff()
    tmp['price_pct_change'] = tmp['price_delta'] / tmp['price']
    tmp.dropna(inplace=True)
    from scipy import stats
    import seaborn as sns
    sns.regplot(tmp['dollar_volume'], tmp['price_pct_change'].abs())
    return stats.linregress(tmp['dollar_volume'], tmp['price_pct_change'].abs())


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
    
    hourly_depth = depth.groupby(depth['time_exchange'].dt.hour).apply(market_depth).unstack()
    plot_market_depth(hourly_depth.loc[:,'bid'],hourly_depth.loc[:,'ask'])

    hourly_prcpct = depth.groupby(depth['time_exchange'].dt.hour).apply(price_change_percent).unstack()
    plot_prcpct(hourly_prcpct.loc[:,'bid'],hourly_prcpct.loc[:,'ask'])

    dat = merge_trade_depth(trade,depth)
    dat.groupby(dat.index.hour)\
            .apply(lambda x: pd.Series(volume_weighted_ave_baspread(x))).plot(marker='*')


