import wx
import wx.grid

import date_time_thread
import quote_handler_thread
import plot_stock_history

# GUI frame
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="sstream",size=(825,400))
        self.panel = wx.Panel(self)

        # text box for entering stock symbols
        self.enter_symbol_box = wx.TextCtrl(self.panel)
        
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
        self.grid.CreateGrid(self.newest_row,9)
        self.grid.SetColLabelValue(0, "Ticker")
        self.grid.SetColLabelValue(1, "Last")
        self.grid.SetColLabelValue(2, "Net Chg")
        self.grid.SetColLabelValue(3, "Exchange")
        self.grid.SetColLabelValue(4, "Bid")
        self.grid.SetColLabelValue(5, "Ask")
        self.grid.SetColLabelValue(6, "Vol")
        self.grid.SetColLabelValue(7, "Open")
        self.grid.SetColLabelValue(8, "Prev Close")
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnSymbolClick)
        
        # layout the gui
        symbol_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        date_time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer for input
        symbol_input_sizer.Add(self.enter_symbol_box, 0, wx.ALL, 5)
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
        
        # start a thread to handle date/time updates
        date_time_thread.DateTimeThread(self)
        
        # start getting quotes for AAPL by default
        self.symbol_set = {"AAPL"}
        quote_handler_thread.QuoteHandlerThread(self,'AAPL',0)
       
    def OnAdd(self,event):
        symbol = self.enter_symbol_box.GetValue().upper()
        # check to see if already monitoring that stock
        if symbol not in self.symbol_set:
            # add a row to grid
            self.grid.AppendRows(1)
            self.newest_row += 1
            # add the symbol to the set
            self.symbol_set.add(symbol)
            # start a new thread
            quote_handler_thread.QuoteHandlerThread(self,symbol,self.newest_row-1)
        # clear the text box
        self.enter_symbol_box.Clear()
        self.enter_symbol_box.SetFocus()
    
    def OnSymbolClick(self, event):
         if event.GetCol() == 0:
            if plot_stock_history.PlotCurrentlyDisplayed():
               wx.MessageBox('Only one plot at a time!', 'Warning', wx.OK|wx.ICON_INFORMATION)
            else:
              plot_stock_history.PlotClosingPrices(self.grid.GetCellValue(event.GetRow(),0))
         self.enter_symbol_box.SetFocus()
        
    def DisplayTickerSymbol(self,row,symbol):
        self.grid.SetCellValue(row, 0, symbol)
    
    def UpdateStockDataDisplay(self,row,quote,quote_color,change,change_color,exchange,volume,prev):
        self.grid.SetCellValue(row,1,quote)
        self.grid.SetCellBackgroundColour(row,1,quote_color)
        self.grid.SetCellValue(row,2,change)
        self.grid.SetCellBackgroundColour(row,2,change_color)
        self.grid.SetCellValue(row,3,exchange)
        self.grid.SetCellValue(row,6,volume)
        self.grid.SetCellValue(row,8,prev)
        
    def SetQuoteCellColorWhite(self,row):
        self.grid.SetCellBackgroundColour(row,1,"White")
        self.grid.ForceRefresh()
    
    def UpdateDateTimeDisplay(self,hour,minute,second,am_pm,date):
        self.time_display.SetValue(hour + ':' + minute + ':' + second + ':' + am_pm)
        self.date_display.SetValue(date)

class SStream(wx.App):
    def OnInit(self):
        self.frame = MainFrame()
        self.frame.Show(True)
        return True
           
if __name__ == '__main__':
    app = SStream(0)
    app.MainLoop()

