import requests
import re
from bs4 import BeautifulSoup
import datetime


weekday_List,saturday_List,holiday_List = [],[],[]

#[00時00分からの経過時間,時,分,行き先,列車種別]のリストが生成

# 平日のURL
weekday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=1&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time"
# 土曜日のURL
saturday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=2&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time%22"
# 休日（祝日）のURL
holiday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=4&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time%22"
# 列車種別．列車名が無印の場合に代入する文字
noneType_for = "取"
# 行き先・経由が無印の場合に代入する文字
noneType_type = "普"

# 平日，土休日によってURL変更
def main():
    #ダイヤごとにリスト作成，処理
    perse_list(weekday_URL,weekday_List)
    perse_list(saturday_URL,saturday_List)
    perse_list(holiday_URL,holiday_List)


def perse_list(html,time_list):
    html = requests.get(html)
    soup = BeautifulSoup(html.text, "html.parser")
    # 時刻表データを取得
    sp = soup.find_all(class_="timeNumb")
    for i in sp:
        p = i.find("a")
        index_h = str(p).find("lh")
        index_m = str(p).find("lm")
        train_for = i.find(class_="trainFor")
        train_type = i.find(class_="trainType")
        # 無印のとき種別および行き先追加
        if train_for is None:
            train_for = noneType_for
        else:
            train_for = train_for.text
        if train_type is None:
            train_type = noneType_type
        else:
            train_type = re.sub("\[|\]","",train_type.text)

        hour = int(re.sub("\D","",str(p)[index_h+3:index_h+5]))
        minute = int(re.sub("\D","",str(p)[index_m+3:index_m+5]))
        time = datetime.timedelta(hours=hour,minutes=minute)
        time_list.append([time,hour,minute,train_for,train_type])

main()
