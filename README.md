# ProdWatchDog

# Description
自分用に、ある2次流通サイト(ま◯だら◯)を監視し自分が欲しいものを監視するPythonツール

>[!NOTE]
>必要以上は保管しないですが、このツールは2次流通サイトアクセス時のCookie情報を外部ファイルに生で保管するのでご留意ください

通知先はDiscordにしています
![image](https://github.com/duks2dog/ProdWatchDog/assets/12562150/c790c47d-ff48-42a8-8d78-2e6c5ea054e2)


# Install
## Discordに自分用チャンネル作成
![image](https://github.com/duks2dog/ProdWatchDog/assets/12562150/d40e40a6-039f-4c88-abeb-89807c3ed967)

## 通知を行いたいチャンネルのURLを取得
チャンネル設定を開く

![image](https://github.com/duks2dog/ProdWatchDog/assets/12562150/70f2cae0-fcdc-49c8-9537-d2d7f71f820e)

連携サービスからWebhookURLを発行しコピー

![image](https://github.com/duks2dog/ProdWatchDog/assets/12562150/71e21787-256e-44e3-95b5-71870f5e6883)

## WEBHOOK_URLを設定
コピーしたURLをコードに貼る
```
import os
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import logging
import datetime

# WebhookのURL
WEBHOOK_URL = 'HERE'
...
```
## 稼働中のログを出したい場合
ログ用にチャンネルを作成or同じチャンネルのURL
```
import os
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import logging
import datetime

# WebhookのURL
WEBHOOK_URL = 'hogehoge'
WEBHOOK_LOGURL = 'HERE'
```
## 監視したい商品の検索結果ページURLを設定
prodWatchDog.pyと同じディレクトリにURL設定ファイルを配置
改行で複数設定可能
```
touch urls.txt
```

## cronの設定
```
0 * * * * flock -n /tmp/ProdWatchDog.lock -c "python /your_directory/prodWatchDog.py"
```
