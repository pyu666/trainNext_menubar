#-*- coding:utf-8 -*-
import rumps
from datetime import datetime, date, timedelta, time
import webDriver
import jpholiday


class TrainNext(rumps.App):
    def __init__(self):
        super(TrainNext, self).__init__("TrainNext")
        rumps.debug_mode(True)
        self.menu = ['Show text', 'Notification']
        self.enable_text = False

    def chk_train(list,hour,min):
        for train in list:
            if train[2] < hour:
                continue
            if train[3] < min:
                continue
            return train[2],train[3],train[4],train[5]
        return None

    def chk_now_time():
        print("hoge")
        now = datetime.today()

        hour = now.hour
        minute = now.minute
         # [0-6],[月-日]
        #表示するダイヤを決定

        if 0 <= hour <= 2:
            hour += 24
            weekday = (now-timedelta(days=1)).weekday()
        else:
            weekday = now.weekday()
        if(jpholiday.is_holiday(train_date)):
            weekday = 6 # 祝日の場合,祝日ダイヤにする
        if weekday == 6:
            today_list = hd_list
        elif weekday == 5:
            today_list = sd_list
        else:
            today_list = wd_list

        first = chk_train(today_list,hour,minute)
        second = chk_train(today_list,first[2],first[3])
        third = chk_train(today_list,second[2],second[3])
        print(first,second,third)


    @ rumps.timer(1)
    def update(self,_):

        print("hoge")
        chk_now_time()
        self.title = str(first)
        self.menu = [str(second), str(third)]

    # 終電までは日付変わってもそのままにしなければならない！
        # 日本一遅い終電は1時台，日本一は早い始発は4時台
        # なので0~3時までは前日の時刻表を参照する

if __name__ == "__main__":

    wd_list = webDriver.weekday_List
    sd_list = webDriver.saturday_List
    hd_list = webDriver.holiday_List
    #print(hd_list)
    app = TrainNext()
    app.run()
