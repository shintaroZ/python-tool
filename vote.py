import logging
import requests
import os
import sys
import argparse

# ログフォーマットを定義
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# ログの設定
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", 
                    filename="C:/emu/100_log/vote.log",
                    level=logging.DEBUG)
# コンソールハンドラーを作成
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# コンソールハンドラーをルートロガーに追加
logging.getLogger().addHandler(console_handler)

# ログメッセージの出力
# logging.debug("This is a debug message")
# logging.info("This is an info message")
# logging.warning("This is a warning message")
# logging.error("This is an error message")
# logging.critical("This is a critical message")

# コマンドライン引数を取得
parser = argparse.ArgumentParser(description='Description of your program')

# コマンドライン引数を定義
parser.add_argument('user', help='MU UserName')
parser.add_argument('password', help='MU Password')

# コマンドライン引数をパース
args = parser.parse_args()

# MU_USER=os.environ.get("MU_USER")
# MU_PASS=os.environ.get("MU_PASS")
MU_USER=str(args.user)
MU_PASS=str(args.password)
LOGIN_URL = "https://crushmu.fun/high/ajax/login"
VOTE_URL = "https://crushmu.fun/high/ajax/vote"
HEADERS = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
LOGIN_FLAT_DATA = "&username=" + MU_USER + "&password=" + MU_PASS

##### ログイン #####
logging.info("login start.[%s]", MU_USER)
loginResponse = requests.post(LOGIN_URL, headers=HEADERS, data=LOGIN_FLAT_DATA)

if (not loginResponse.status_code == 200):
    sys.exit(1)

session=loginResponse.cookies.get("dmncmssession")
logging.info("login successful.[%s]", session)

##### VOTE #####
cokkies={"dmncmssession":session, "DmN_Current_User_Server_" + MU_USER:"DEFAULT"}

for i in range(1, 2):
    logging.info(">>>>> vote request. [%d/13] [%s]", i, MU_USER)
    vote_flat_data="vote=" + str(i)
    voteResponse = requests.post(VOTE_URL, headers=HEADERS, cookies=cokkies, data=vote_flat_data)
    logging.info("<<<<< vote response. [%s]", voteResponse.content)
