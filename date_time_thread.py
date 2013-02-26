import time
import datetime
import threading

format_time = lambda x, c: (x < 10 and (c + str(x), True)) or (str(x), False)

class DateTimeThread(threading.Thread):
    def __init__(self,gui):
        threading.Thread.__init__(self)
        self.gui = gui
        self.start()
        
    def run(self):
        while 1:
            try:
                # set time values
                now = datetime.datetime.now()
                str_hour = format_time(now.hour,' ')[0]
                str_minute = format_time(now.minute,'0')[0]
                str_second = format_time(now.second,'0')[0]
                am_pm = ((now.hour >= 12 and ('PM',True)) or ('AM',False))[0]
                # update the date and time
                self.gui.UpdateDateTimeDisplay(str_hour,\
                                               str_minute,\
                                               str_second,\
                                               am_pm,\
                                               str(datetime.date.today()))
                # wait
                time.sleep(1)
            except:
                return
                