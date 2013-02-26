import wx
import matplotlib
matplotlib.use('WXAgg')

import datetime
from matplotlib.finance import quotes_historical_yahoo
import matplotlib.pyplot as plt

def PlotClosingPrices(symbol):
    # get dates
    today = datetime.date.today()
    one_year_ago = today - datetime.timedelta(days=365)

    # get historic data
    historic_data = quotes_historical_yahoo(symbol, one_year_ago, today, asobject=True)
 
    # plot the data
    fig, ax = plt.subplots(1)
    ax.plot(historic_data.date, historic_data.close)
    fig.canvas.set_window_title(symbol + ' price data')
    fig.autofmt_xdate()
    plt.title(symbol + ' 1 year closing history')
    plt.get_current_fig_manager().window.SetPosition((500,50))
    plt.show()
   
def PlotCurrentlyDisplayed():
    return plt.fignum_exists(1)

