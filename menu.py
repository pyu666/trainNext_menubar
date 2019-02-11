#-*- coding:utf-8 -*-
import rumps
from datetime import datetime, date, timedelta, time
import webDriver
import jpholiday


class TrainNext(rumps.App):
    info=["a","b"]
    def __init__(self):
        #初期設定
        super(TrainNext, self).__init__("TrainNext")
        rumps.debug_mode(True)
        self.menu = ["そのつぎ"]
        self.menu["そのつぎ"].add("なし")
        self.menu["そのつぎ"].add("なし")
        self.menu = ["運行情報"]
        self.menu["運行情報"].add("未取得")
        self.enable_text = False
        self.icon="./icon.png"
    #20秒毎に更新

    def hoge(self,sender):
        print("hugahuga")


    @ rumps.timer(20)
    def chk_now_time(self,sender):
        print("start check")

        # 標準では5分後，各自変更を
        now = datetime.today() + timedelta(minutes = 5)

        print("now + 5min ",now)
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
        #chk_trainの返却値は[00時00分からの経過時間,時,分,行き先,列車種別]
        self.menu["そのつぎ"].clear()
        if first is None:
            self.menu["そのつぎ"].add("なし")
            self.title = (" ")
        else:
            second = chk_train(today_list,first[1],first[2])
            print("次発",second)
            if second is not None:
                self.menu["そのつぎ"].add(str(second[1]).zfill(2)+":"+str(second[2]).zfill(2)+" "+str(second[3]))
                third = chk_train(today_list,second[1],second[2])
                print("次々発",third)
                if third is not None:
                    self.menu["そのつぎ"].add(str(third[1]).zfill(2)+":"+str(third[2]).zfill(2)+" "+str(third[3]))
            else:
                self.menu["そのつぎ"].add("なし")

            for i in self.menu["そのつぎ"].values():
                i.set_callback(hoge)

            self.title = (str(first[1]).zfill(2)+":"+str(first[2]).zfill(2)+"  "+str(first[3]))



    @ rumps.timer(60)
    def chk_trainfo(self,sender):
        global info
        print("start check train info")
        info = list(webDriver.get_trainfo())
        print("get train info")
        self.menu["運行情報"].clear()
        self.menu["運行情報"].add(info[0])
        self.menu["運行情報"][info[0]].set_callback(hoge)
        if info[1] is not None:
            self.menu["運行情報"].add(info[1])
            self.menu["運行情報"][info[1]].set_callback(hoge)
        print(info)

    def printer():
        print("hogehoge")
        self.alert("hoge")

def hoge():
    print("huga")
    TrainNext.printer()
    #ramps.alert("hoge")

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
