import time
import threading
import json
import urllib2

determine_cell_color = lambda x,y: (x>y  and ("Green",True)) or\
                                   (x<y  and ("Red",True)) or\
                                   (x==y and ("White",False))

class QuoteHandlerThread(threading.Thread):
    def __init__(self,gui,symbol,row):
        threading.Thread.__init__(self)
        self.gui = gui
        self.symbol = symbol
        self.row = row
        self.quote = float(GetStockData(self.symbol)['l'])
        self.gui.DisplayTickerSymbol(self.row, self.symbol)
        self.start()
        
    def run(self):
        while 1:
            try:
                # get and set values
                stock_data = GetStockData(self.symbol)
                prev_quote = self.quote
                self.quote = stock_data['l']
                prev_close = float(self.quote) - float(stock_data['c'])
                # determine cell colors
                quote_color = determine_cell_color(float(self.quote),float(prev_quote))[0]
                net_change_color = determine_cell_color(float(stock_data['c']),0.0)[0]
                self.gui.UpdateStockDataDisplay(self.row,\
                                                self.quote,\
                                                quote_color,\
                                                stock_data['c'],\
                                                net_change_color,\
                                                stock_data['e'],\
                                                '--',\
                                                str(prev_close))
                # wait 3 seconds
                time.sleep(1)
                self.gui.SetQuoteCellColorWhite(self.row)
                time.sleep(2)
            except:
                return

def GetStockData(symbol):   
    url = 'http://finance.google.com/finance/info?q=%s' % symbol
    lines = urllib2.urlopen(url).read().splitlines()
    return json.loads(''.join([x for x in lines if x not in ('// [', ']')]))
