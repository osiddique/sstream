import datetime
import ystockquote
import pandas
import matplotlib.pyplot as plt

def ChartPrice(symbol):
   # generate a string for today's date
   x = str(datetime.date.today())
   y = [x[i] for i in range(len(x)) if x[i] != '-']
   todays_date = "".join(y)

   # generate a string for the date a year ago today
   z = y[:]
   current_year = int("".join(z[0:4]))
   last_year = str(current_year - 1)
   z[0:4] = last_year
   one_year_ago = "".join(z)

   # get historic data
   raw_historic_data = ystockquote.get_historical_prices(symbol, one_year_ago, todays_date)
   dates = [raw_historic_data[i][0] for i in range(1,len(raw_historic_data))][::-1]
   close_prices = [float(raw_historic_data[i][4]) for i in range(1,len(raw_historic_data))][::-1]
   one_year_close_data = pandas.Series(close_prices,dates)
 
   # plot the data
   plt.figure(1)
   one_year_close_data.plot()
   plt.title(symbol)
   plt.show()

