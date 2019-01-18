#-*- coding:utf-8 -*-
import rumps
from datetime import datetime, date, timedelta
import webDriver
import jpholiday


class TrainNext(rumps.App):
    def __init__(self):
        super(TrainNext, self).__init__("TrainNext")
        rumps.debug_mode(False)

        self.enable_text = False

    @ rumps.timer(60)
    def update(self,_):

        self.title = str()
        self.menu = ['Show text', 'Notification']

    def chk_day_of_the_week():
        pass()
    # 終電までは日付変わってもそのままにしなければならない！
    def first_last_train():
        # 日本一遅い終電は1時台，日本一は早い始発は4時台
        # なので0~3時までは前日の時刻表を参照する
if __name__ == "__main__":
    #webdriver()
    wd_list = webDriver.weekday_List
    sd_list = webDriver.saturday_List
    hd_list = webDriver.holiday_List
    print(hd_list)
    app = TrainNext()
    app.run()

    return
