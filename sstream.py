import wx
import wx.grid
import time
import datetime
import thread
#import ystockquote

#import matplotlib
#matplotlib.use('WXAgg')
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_wxagg import \
#    FigureCanvasWxAgg as FigCanvas, \
#    NavigationToolbar2WxAgg as NavigationToolbar

import random # debug

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
        self.panel.color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
        self.grid.SetDefaultCellBackgroundColour(self.panel.color)
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
        self.DisplayDateTime()
        thread.start_new_thread(self.UpdateDateTime,())
        
        # start getting quotes for AAPL by default
        self.grid.SetCellValue(0, 0, "AAPL")
        thread.start_new_thread(self.QuoteHandler,('AAPL',0))
       
    def OnAdd(self,event): 
        self.AddRow()
        
    def AddRow(self):
        # add a row to grid
        self.grid.AppendRows(1)
        self.newest_row += 1   
        # get parameters to pass to QuoteHandler
        row = self.newest_row - 1
        symbol = self.txt_box.GetValue().upper()
        # clear the text box
        self.txt_box.Clear()
        self.txt_box.SetFocus()
        
        # start the thread
        thread.start_new_thread(self.QuoteHandler,(symbol,row))
        
    def QuoteHandler(self,symbol,row):
        self.grid.SetCellValue(row, 0, symbol)
        prev_close = 100.00
        delta = random.randrange(-10,10,1)
        delta = float(delta)/100
        open = prev_close + delta
        self.grid.SetCellValue(row, 1, str(open))
        self.grid.SetCellValue(row, 6, str(open))
        self.grid.SetCellValue(row, 7, str(prev_close))
        while 1:
            time.sleep(1)
            self.grid.SetCellBackgroundColour(row,1,"Grey")
            time.sleep(4)
            
            # set value for the latest quote
            prev_quote = float(self.grid.GetCellValue(row,1))
            delta = random.randrange(-10,10,1)
            delta = float(delta)/100
            quote = prev_quote + delta
            # set value for net change
            net_change = quote - prev_close
            
            # write value of latest quote
            if quote >= prev_quote:
                self.grid.SetCellBackgroundColour(row,1,"Green")
            else:
                self.grid.SetCellBackgroundColour(row,1,"Red")
            self.grid.SetCellValue(row,1,str(quote))
            # write value of net change
            if net_change >= 0.0:
                self.grid.SetCellBackgroundColour(row,2,"Green")
                sign = '+'
            else:
                self.grid.SetCellBackgroundColour(row,2,"Red")
                sign = ''
            self.grid.SetCellValue(row,2,sign + str(net_change))
            
    def UpdateDateTime(self):
        while 1:
            time.sleep(1)
            self.DisplayDateTime()
            
    def DisplayDateTime(self):
        now = datetime.datetime.now()
        # format the time
        if now.hour < 10:
            str_hour = ' ' + str(now.hour)
        else:
            str_hour = str(now.hour)
        if now.minute < 10:
            str_minute = '0' + str(now.minute)
        else:
            str_minute = str(now.minute)
        if now.second < 10:
            str_second = '0' + str(now.second)
        else:
            str_second = str(now.second)
        if now.hour >= 12:
            am_pm = 'PM'
        else:
            am_pm = 'AM'
        current_time = str_hour + ':' + str_minute + ':' + str_second + ' ' + am_pm
        # update the date and time
        self.time_display.SetValue(current_time)
        self.date_display.SetValue(str(datetime.date.today()))
        
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
