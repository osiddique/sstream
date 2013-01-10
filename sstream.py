import wx
import wx.grid
import time
import datetime
import thread
import ystockquote

#import matplotlib
#matplotlib.use('WXAgg')
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import \
#    FigureCanvasWxAgg as FigCanvas, \
#    NavigationToolbar2WxAgg as NavigationToolbar

class SStream(wx.Frame):   
    def __init__(self):
        wx.Frame.__init__(self, None, title="sstream",size=(800,500))    
        self.panel = wx.Panel(self)  

        # text box for entering stock symbols
        self.txt_box = wx.TextCtrl(self.panel)
        
        # 'Add' button to add stock data to a grid
        add_btn = wx.Button(self.panel, label='Add')
        add_btn.Bind(wx.EVT_BUTTON, self.OnAdd)
        
        # date and time display
        self.time_display = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.time_display.SetBackgroundColour("Cyan")
        self.date_display = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        self.date_display.SetBackgroundColour("Yellow")
        
        # grid for displaying data
        self.newest_row = 1
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(self.newest_row,8)
        self.grid.SetColLabelValue(0, "Symbol")
        self.grid.SetColLabelValue(1, "Last")
        self.grid.SetColLabelValue(2, "Net Chg")
        self.grid.SetColLabelValue(3, "Bid")
        self.grid.SetColLabelValue(4, "Ask")
        self.grid.SetColLabelValue(5, "Vol")
        self.grid.SetColLabelValue(6, "Open")
        self.grid.SetColLabelValue(7, "Prev Close")
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.ChartHistoricPrices)
        
        # layout the gui
        symbol_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        date_time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer for input
        symbol_input_sizer.Add(self.txt_box, 0, wx.ALL, 5)
        symbol_input_sizer.Add(add_btn, 0, wx.ALL, 5)
        # sizer for date and time
        date_time_sizer.Add(self.time_display, 0, wx.ALL, 5)
        date_time_sizer.Add(self.date_display, 0, wx.ALL, 5)
        # sizer for the grid
        grid_sizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 5)
        # sizer for entire gui
        main_sizer.Add(symbol_input_sizer, 0, wx.ALL, 5)
        main_sizer.Add(date_time_sizer, 0, wx.ALL, 5)
        main_sizer.Add(grid_sizer, 1, wx.ALL, 5)   
        self.panel.SetSizer(main_sizer)
        
        # display date/time and then start a thread to handle updates
        thread.start_new_thread(self.UpdateDateTime,())
        
        # start getting quotes for AAPL by default
        thread.start_new_thread(self.QuoteHandler,('AAPL',0))
       
    def OnAdd(self,event): 
        # add a row to grid
        self.grid.AppendRows(1)
        self.newest_row += 1   
        # start a thread
        thread.start_new_thread(self.QuoteHandler,(self.txt_box.GetValue().upper(),self.newest_row-1)) 
        # clear the text box
        self.txt_box.Clear()
        self.txt_box.SetFocus()
        
    def QuoteHandler(self,symbol,row):
        self.grid.SetCellValue(row, 0, symbol)
        # get initial price
        quote = float(ystockquote.get_price(symbol))
        set_cell_color = lambda x,y: (x>y and ("Green",True)) or (x<y and ("Red",True)) or (("White",False))
        while 1:
            # get and set values
            stock_data = ystockquote.get_all(symbol)
            prev_quote = quote 
            quote = stock_data['price']
            prev_close = float(quote) - float(stock_data['change'])
            # determine cell colors
            quote_color = set_cell_color(float(quote),float(prev_quote))[0]
            net_change_color = set_cell_color(float(stock_data['change']),0.0)[0]
            # update the grid
            self.grid.SetCellValue(row,1,quote)
            self.grid.SetCellBackgroundColour(row,1,quote_color)
            self.grid.SetCellValue(row,2,stock_data['change'])
            self.grid.SetCellBackgroundColour(row,2,net_change_color)
            self.grid.SetCellValue(row,5,stock_data['volume'])
            self.grid.SetCellValue(row,7,str(prev_close))
            # wait
            time.sleep(1)
            self.grid.SetCellBackgroundColour(row,1,"White")
            self.grid.ForceRefresh()
            time.sleep(2)
    
    def UpdateDateTime(self):
        format_time = lambda x, c: (x < 10 and (c + str(x), True)) or (str(x), False)
        while 1:
           # set time values
           now = datetime.datetime.now()
           str_hour = format_time(now.hour,' ')[0]
           str_minute = format_time(now.minute,'0')[0]
           str_second = format_time(now.second,'0')[0]
           am_pm = ((now.hour >= 12 and ('PM',True)) or ('AM',False))[0]
           # update the date and time
           self.time_display.SetValue(str_hour + ':' + str_minute + ':' + str_second + ' ' + am_pm)
           self.date_display.SetValue(str(datetime.date.today()))
           # wait   
           time.sleep(1)       
    
    def ChartHistoricPrices(self, event):
        pass
        #if event.GetCol() == 0:
            #thread.start_new_thread(self.PlotData,())
        #self.txt_box.SetFocus()
 
    def PlotData(self):
        pass
        #matplotlib.interactive( True )
        #matplotlib.use( 'WXAgg' )
        #plt.plot([1,2,3,4])
        #plt.ylabel('some numbers')
        #plt.title('AAPL')
        #plt.show()
                    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = SStream()
    frame.Show()
    app.MainLoop()
