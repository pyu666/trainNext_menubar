#-*- coding:utf-8 -*-
import rumps
from datetime import datetime, date, timedelta, time
import webDriver
import jpholiday


class TrainNext(rumps.App):
    def __init__(self):
        #初期設定
        super(TrainNext, self).__init__("TrainNext")
        rumps.debug_mode(True)
        self.menu = ["その次の電車"]
        self.menu["その次の電車"].add("なし")
        self.menu["その次の電車"].add("なし")
        self.enable_text = False
        self.icon="./icon.png"

    @ rumps.timer(20)
    #20秒毎にアップデート
    def chk_now_time(self,sender):
        print("start check")
        now = datetime.today() + timedelta(minutes = 5)
        print("now+5min",now)
        today = date.today()
        hour = now.hour
        minute = now.minute
         # [0-6],[月-日]
        #表示するダイヤを決定
        if 0 <= hour < 2: # 日付回った場合，前日のダイヤを参照する必要がある
            hour += 24 #データ形式は0~26時，Time型は0~23で持つため
            weekday = (now-timedelta(days=1)).weekday()
        else:
            weekday = now.weekday()
        if(jpholiday.is_holiday(today)):
            weekday = 6 # 祝日の場合,祝日ダイヤにする

        if weekday == 6: # 休日ダイヤ
            today_list = hd_list
        elif weekday == 5: #土曜ダイヤ
            today_list = sd_list
        else: # 平日ダイヤ
            today_list = wd_list

        #print(today_list)

        first = chk_train(today_list,hour,minute)
        print("先発",first)

        #clear しないと増え続ける
        #以下冗長な表現，できれば修正するべき
        self.menu["その次の電車"].clear()
        if first is None:
            self.menu["その次の電車"].add("なし")
            self.title = (" ")
        else:
            second = chk_train(today_list,first[1],first[2])
            print("次発",second)
            if second is not None:
                self.menu["その次の電車"].add(str(second[1]).zfill(2)+":"+str(second[2]).zfill(2)+" "+str(second[3]))
                third = chk_train(today_list,second[1],second[2])
                print("次々発",third)
                if third is not None:
                    self.menu["その次の電車"].add(str(third[1]).zfill(2)+":"+str(third[2]).zfill(2)+" "+str(third[3]))
            else:
                self.menu["その次の電車"].add("なし")
            self.title = (str(first[1]).zfill(2)+":"+str(first[2]).zfill(2)+"  "+str(first[3]))



#    @ rumps.timer(1)
#    def update(self,_):
#        print("hoge")
#        chk_now_time()
#        self.title = str(first)
#        self.menu = [str(second), str(third)]

    # 終電までは日付変わってもそのままにしなければならない！
        # 日本一遅い終電は1時台，日本一は早い始発は4時台
        # なので0~3時までは前日の時刻表を参照する


#次の列車を検索
def chk_train(list,hour,minute):
    for train in list:
        if train[1] < hour:
            continue
        if train[1] == hour and train[2] <= minute:
            continue
        return train
    return None
if __name__ == "__main__":

    wd_list = webDriver.weekday_List
    sd_list = webDriver.saturday_List
    hd_list = webDriver.holiday_List
    #print(hd_list)
    app = TrainNext()
    app.run()
