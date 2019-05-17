import requests
import re
from bs4 import BeautifulSoup
import datetime


weekday_List,saturday_List,holiday_List = [],[],[]

#[00時00分からの経過時間,時,分,行き先,列車種別]のリストが生成

# 平日のURL
weekday_URL = "https://transit.yahoo.co.jp/station/time/22828/?gid=1171&pref=13&done=time"
# 土曜日のURL
saturday_URL = "https://transit.yahoo.co.jp/station/time/22828/?kind=2&gid=1171&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time"
# 休日（祝日）のURL
holiday_URL = "https://transit.yahoo.co.jp/station/time/22828/?kind=4&gid=1171&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time"
# 運行情報のURL
info_URL = "https://transit.yahoo.co.jp/traininfo/detail/27/0/"

# 列車種別．列車名が無印の場合に代入する文字
noneType_type = "普"
# 行き先・経由が無印の場合に代入する文字
noneType_for = "品"
# 平日，土休日によってURL変更
def main():
    #ダイヤごとにリスト作成，処理
    perse_list(weekday_URL,weekday_List)
    perse_list(saturday_URL,saturday_List)
    perse_list(holiday_URL,holiday_List)
    print(get_trainfo())

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

def get_trainfo():
    html = requests.get(info_URL)
    soup = BeautifulSoup(html.text, "html.parser")
    sp = soup.find(id="mdServiceStatus")
    about = sp.find("dt").text
    detail = judge_detail(sp.find("p").text)
    if "運転状況" in about:
        about = judge_trainfo(detail)
    return about,detail

def judge_detail(data):
    if re.search("情報はありません|平常通り",data) is not None:
        return None
    else:
        #start = data.find(list("した","での","で"))+2
        start = re.search("した|での",data)
        if start is None:
            start=0
        else:
            start = start.end()
        end = data.find("影響")
        return data[start:end+2]

def judge_trainfo(data):
    icon ="[△]"
    if "直通運転を中止" in data:
        about="直通運転中止"
    elif "一部列車" in data:
        if "運休" in data:
            about="一部運休"
        elif "遅れ" in data:
            about="一部遅延"
        else:
            about="運転変更等"
    else:
        about="列車遅延"
    return icon+about
main()
