import requests
import re
from bs4 import BeautifulSoup
import datetime
import time

weekday_List,saturday_List,holiday_List = [],[],[]

#[00時00分からの経過時間,時,分,行き先,列車種別]のリストが生成

# 平日のURL
weekday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=1&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time"
# 土曜日のURL
saturday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=2&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time%22"
# 休日（祝日）のURL
holiday_URL = "https://transit.yahoo.co.jp/station/time/22630/?kind=4&gid=991&pref=13&prefname=%E6%9D%B1%E4%BA%AC&tab=time&done=time%22"
# 運行情報のURL
info_URL = "https://transit.yahoo.co.jp/traininfo/detail/57/0/"
# 列車種別．列車名が無印の場合に代入する文字
noneType_for = "取"
# 行き先・経由が無印の場合に代入する文字
noneType_type = "普"

is_network_connection = False

is_maked_list = False

# 平日，土休日によってURL変更
def main():
	#ダイヤごとにリスト作成，処理
    check_network(1)
    global is_network_connection, weekday_List,saturday_List,holiday_List
    if is_network_connection:
        make_perse()
        print(get_trainfo())
        is_network_connection = True
    else:
        time,hour,minute,train_for,train_type = None,0,0,"ネットワークエラー",""
        weekday_List,saturday_List,holiday_List = [[time,hour,minute,train_for,train_type]],[[time,hour,minute,train_for,train_type]],[[time,hour,minute,train_for,train_type]]
        print("network connection faild")

def make_perse():
    global is_maked_list, weekday_List,saturday_List,holiday_List
    perse_list(weekday_URL,weekday_List)
    perse_list(saturday_URL,saturday_List)
    perse_list(holiday_URL,holiday_List)
    is_maked_list = True
    print("list OK")
    # print(weekday_List)

def check_network(count):
    global is_maked_list,is_network_connection
    for i in range(count):
        try:
            html = requests.get("http://yahoo.co.jp")
            print("network OK")
            is_network_connection = True
            if is_maked_list is False:
                make_perse()
            return True
        except:
            print("network disconnect retry")
            return False


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
    if "運転状況" in about:
        about = judge_trainfo(sp.find("p").text)
    detail = judge_detail(sp.find("p").text)
    return about,detail

def judge_detail(data):
    if re.search("情報はありません|平常通り",data) is not None:
        return None
    else:
        #start = data.find(list("した","での","で"))+2
        #print(data)
        start = re.search("した|での",data)
        if start is None:
            start=0
        else:
            start = start.end()
        end = data.find("影響")
        #print(data[start:end+2])
        return data[start:end+2]

def judge_trainfo(data):
    print(data)
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
