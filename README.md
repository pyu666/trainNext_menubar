# trainNext_menubar

## 概要
メニューバーに次の列車を表示するアプリ

## 環境
python3.7で動作確認
内容的には以下のライブラリが動作する環境ならば動作するはず

+ rumps
+ BeautifulSoup
+ requests
+ jpholiday
+ py2app


## セットアップ
まず，webDriver.py内の変数を各自の環境に合わせて設定
また，必要に応じてmenu.pyの時間も変更を

使用前に起動時に表示するアイコンをicon.pngとしてmenu.pyと同じ階層に追加すること！


## 使い方

`python menu.py`
で起動


## アプリ化
py2app を利用してアプリ化します

icon.png(アプリに表示されるアイコン)およびicon.icns(アプリ本体のアイコンセット)を各自追加

`python menu.py py2app`

で作成完了
完成したmenu.appをダブルクリックし，起動できる


## アイコン
上の動作例に使用したアイコン
[電車、駅のフリーアイコン - ICOON MONO](http://icooon-mono.com/11945-%E9%9B%BB%E8%BB%8A%E3%80%81%E9%A7%85%E3%81%AE%E3%83%95%E3%83%AA%E3%83%BC%E3%82%A2%E3%82%A4%E3%82%B3%E3%83%B3/)

## その他
ハードコーディング良くない．
