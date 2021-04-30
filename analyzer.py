def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = int((total_won / total_closed) * 100)
    
    #Designate the rows
    h1 = ['Total Open',   'Total Won',  'Win Streak',   'Strike Rate']
    h2 = ['Total Closed', 'Total Lost', 'Losing Streak','PnL Net']
    r1 = [total_open,     total_won,     win_streak,     strike_rate]
    r2 = [total_closed,   total_lost,    lose_streak,    pnl_net]
    
    from tabulate import tabulate

        
    table_values= [h1,
                   r1,
                   h2,
                   r2]        

    print("\n\nTrade Analysis Results:")
    print (tabulate(table_values,))

def printSQN(analyzer):
    sqn = round(analyzer.sqn,2)
    print('SQN: {}'.format(sqn))
