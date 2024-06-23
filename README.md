# ProdWatchDog

# Description
自分用に、ある2次流通商品サイトを監視し自分が欲しいものを監視するPythonツール

通知先はDiscordにしています

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

## cronの設定
```
0 * * * * flock -n /tmp/ProdWatchDog.lock -c "python /your_directory/prodWatchDog.py"
```
