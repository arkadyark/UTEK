def get_value(trades, stock_prices):
    # Helper function to get the value of a set of trades
    value = 0
    for i in range(len(trades)/2):
        value -= trades[2*i][1]
        value += trades[2*i + 1][1]
    return value

def get_max_trades(stock_prices, n = 5):
    '''
    Function to compute the best 'n' buys and sells

    Alternates between minima and maxima, buying at minima
    and selling at maxima. Computes extreme stock_prices by comparing
    a stock price to its 'nearest_neighbors' nearest neighbors
    '''
    nearest_neighbors = 10
    trades = []
    previous_state = None
    while True:
        minima = get_extremes(stock_prices, nearest_neighbors, False)
        maxima = get_extremes(stock_prices, nearest_neighbors, True)
        trades = get_trades(minima, maxima)
        if trades != -1:
            if previous_state == 'able to find trades' or previous_state == None:
                # Increment the nearest neighbor threshold, 
                previous_state = 'able to find trades'
                nearest_neighbors += 1
            else:
                # Switched from being unable to find n alternating peaks and valleys
                # to being able, terminate and return
                minima = get_extremes(stock_prices, nearest_neighbors, False)
                maxima = get_extremes(stock_prices, nearest_neighbors, True)
                trades = get_trades(minima, maxima)
                break
        else:
            if previous_state == 'unable to find trades' or previous_state == None:
                previous_state = 'unable to find trades'
                nearest_neighbors -= 1
            else:
                # Switched from being able to find 5 alternating peaks and valleys
                # to being unable, terminate and return
                minima = get_extremes(stock_prices, nearest_neighbors - 1, False)
                maxima = get_extremes(stock_prices, nearest_neighbors - 1, True)
                trades = get_trades(minima, maxima)
                break

    return trades, get_value(trades, stock_prices)

def get_trades(minima, maxima, n = 5):
    '''
    Alternates between minima and maxima, if possible, 
    to get a legal set of 5 trades
    '''
    # Check immediately if we can stop early
    if len(minima) < n or len(maxima) < n:
        return -1

    trades = []
    buy_index = 0
    sell_index = 0

    # Check if we can alternate between minima and maxima for n trades
    for trade_number in range(n):
        # Initialize the stocks to trade
        buy = minima[buy_index]
        sell = maxima[sell_index]

        if len(trades) > 0 and buy[0] < trades[-1][0]:
            # You can't buy/sell twice in a row!
            # Try incrementing the buy_index so we can buy before we sell
            while (buy_index < len(minima) and minima[buy_index][0] < trades[-1][0]):
                buy_index += 1
            if buy_index >= len(maxima):
                return -1
            else:
                trades.append(minima[buy_index])
                trades.append(sell)

        elif sell[0] < buy[0]:
            # You can't sell before you buy!
            while (sell_index < len(maxima) and minima[buy_index][0] > maxima[sell_index][0]):
                sell_index += 1
            if sell_index >= len(maxima):
                return -1
            else:
                trades.append(buy)
                trades.append(maxima[sell_index])
                buy_index += 1
                sell_index += 1
        else:
            # Just simple alternating
            trades.append(buy)
            trades.append(sell)
            buy_index += 1
            sell_index += 1

    # Return the jumps between maxima and minima
    return trades

def get_extremes(stock_prices, num_neighbors = 10, get_maxima = True):
    '''
    Get all extreme stock_prices in the stock prices, where extremes are defined
    as points that are greater than all num_neighbors of their nearest neighbors
    '''
    peaks = []
    for value_index in range(num_neighbors, len(stock_prices) - num_neighbors):
        value = stock_prices[value_index]
        not_a_peak = False
        for neighbor_index in range(num_neighbors):
            if get_maxima:
                if value < stock_prices[value_index - neighbor_index]:
                    not_a_peak = True
                    break
                if value < stock_prices[value_index + neighbor_index]:
                    not_a_peak = True
                    break
            else:
                if value > stock_prices[value_index - neighbor_index]:
                    not_a_peak = True
                    break
                if value > stock_prices[value_index + neighbor_index]:
                    not_a_peak = True
                    break
        if not_a_peak:
            continue
        else:
            peaks.append((value_index, stock_prices[value_index]))

    return peaks


def get_value(trades, stock_prices):
    # Helper function to get the value of a set of trades
    value = 0
    for i in range(len(trades)/2):
        value -= trades[2*i][1]
        value += trades[2*i + 1][1]
    return value
