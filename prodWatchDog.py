import os
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import logging
import datetime

# WebhookのURL
WEBHOOK_URL = ''
WEBHOOK_LOGURL = ''

def send_webhook_message(message, url):
    data = {
        "content": message
    }
    response = requests.post(url, json=data)
    if response.status_code != 204:
        raise Exception(f"Failed to send message: {response.status_code}, {response.text}")

def load_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def get_initial_cookies():
    session = requests.Session()
    url = 'https://www.mandarake.co.jp/index2.html'
    response = session.get(url)
    return session.cookies

def check_website(url, cookies):
    session = requests.Session()
    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://order.mandarake.co.jp/',
        'Accept-Language': 'ja-JP,ja;q=0.9'
    }

    try:
        response = session.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')

        # div.entryを取得（1要素前提）
        entry = soup.find('div', class_='entry')
        if not entry:
            return False, None

        # div.thumlargeを取得
        thumlarge = entry.find('div', class_='thumlarge')
        if not thumlarge:
            return False, None

        # div.block adultItemまたはdiv.blockを取得
        blocks = thumlarge.find_all('div', class_='block') + thumlarge.find_all('div', class_='block adultItem')

        for block in blocks:
            # class=addcartが存在するかをチェック
            if block.find('div', class_='addcart'):
                img = block.find('img')
                img_url = img['src'] if img else '画像なし'
                return True, img_url
    except requests.exceptions.TooManyRedirects:
        print(f'Too many redirects: {url}')
        send_webhook_message('エラー：Too many redirects', WEBHOOK_LOGURL)

    except requests.exceptions.RequestException as e:
        print(f'Error checking {url}: {e}')
        send_webhook_message('エラー：Error checking '+e, WEBHOOK_LOGURL)

    return False, None

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'urls.txt')
    urls = load_urls(file_path)
    cookies = get_initial_cookies()

    # ログファイルの設定
    log_file_path = current_directory+'/prodWatchDog.log'
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')


    while True:
        for url in urls:
            # URLからクエリパラメータを解析してデコード
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            keyword = query_params.get('keyword', [''])[0]
            decoded_keyword = urllib.parse.unquote(keyword)

            found, img_url = check_website(url, cookies)
            if found:
                message = f'商品が入荷しました！URL: {url}\nキーワード: 「{decoded_keyword}」\n{img_url}'
                print(message)
                logging.info(message)
                send_webhook_message(message, WEBHOOK_URL)
                print('10分後にもう一度通知します...')
                logging.info('10分後にもう一度通知します...')
                time.sleep(600)  # 10分待つ
                send_webhook_message('[再通知]'+message, WEBHOOK_URL)
        print('1分後に再チェックします...')
        logging.info('1分後に再チェックします...')
        time.sleep(60)  # 1分待つ
        if datetime.datetime.now().minute == 0 and len(WEBHOOK_LOGURL) != 0:
            send_webhook_message('監視中・・・', WEBHOOK_LOGURL)

if __name__ == "__main__":
    main()
