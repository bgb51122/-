# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 22:55:43 2022

@author: kinos
"""

import discord
import json
from flask import Flask
from threading import Thread

#讀取BOT token
with open('token.json', "r", encoding="utf8") as file:
    data = json.load(file)

client = discord.Client()


@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #句子中含有BST才進入換算程序
    if "BST" in message.content:
        #去除:外之標點符號
        sentence = message.content
        punctuation_string = "!\"#$%&'()*+,-./;<=>?@[\]^_`{|}~"
        for i in punctuation_string:
            sentence = sentence.replace(i, " ")
        #抓出句中時間
        sentence = sentence.split(" ")
        BST_index = sentence.index("BST")
        BST_time = sentence[BST_index - 1]
        #12小時制
        if "AM" in BST_time or "PM" in BST_time:
            #有寫分鐘
            if ":" in BST_time:
                if "AM" in BST_time:
                    BST_time_noam = BST_time.replace("AM", "")
                    time = BST_time_noam.split(":")
                    BST_oclock = time[0]
                    BST_minute = time[1]
                    CST_oclock = int(BST_oclock) + 7
                    CST_minute = int(BST_minute)
                    #處理小時
                    if CST_oclock > 12:
                        oclock = "下午" + str(CST_oclock - 12)
                    elif CST_oclock == 12:
                        oclock = "中午" + str(CST_oclock)
                    else:
                        oclock = "上午" + str(CST_oclock)
                    #處理分鐘
                    if CST_minute == 0:
                        minute = "整"
                    elif CST_minute == 30:
                        minute = "半"
                    else:
                        minute = str(CST_minute) + "分"
                    #組合發送句子
                    send = "{} BST是台北時間 {}點{}。".format(BST_time, oclock,
                                                       minute)
                elif "PM" in BST_time:
                    BST_time_nopm = BST_time.replace("PM", "")
                    time = BST_time_nopm.split(":")
                    BST_oclock = time[0]
                    BST_minute = time[1]
                    CST_oclock = int(BST_oclock) + 7
                    CST_minute = int(BST_minute)
                    #處理小時
                    if CST_oclock > 12:
                        oclock = "明天上午" + str(CST_oclock - 12)
                    elif CST_oclock == 12:
                        oclock = "午夜" + str(CST_oclock)
                    else:
                        oclock = "下午" + str(CST_oclock)
                    #處理分鐘
                    if CST_minute == 0:
                        minute = "整"
                    elif CST_minute == 30:
                        minute = "半"
                    else:
                        minute = str(CST_minute) + "分"
                    #組合發送句子
                    send = "{} BST是台北時間 {}點{}。".format(BST_time, oclock,
                                                       minute)
            #只寫小時
            else:
                if "AM" in BST_time:
                    BST_oclock = BST_time.replace("AM", "")
                    CST_oclock = int(BST_oclock) + 7
                    if CST_oclock > 12:
                        oclock = CST_oclock - 12
                        send = "{} BST是台北時間 下午{}點".format(BST_time, oclock)
                    elif CST_oclock == 12:
                        send = "{} BST是台北時間 中午{}點".format(BST_time, CST_oclock)
                    else:
                        send = "{} BST是台北時間 上午{}點".format(BST_time, CST_oclock)
                elif "PM" in BST_time:
                    BST_oclock = BST_time.replace("PM", "")
                    CST_oclock = int(BST_oclock) + 7
                    if CST_oclock > 12:
                        oclock = CST_oclock - 12
                        send = "{} BST是台北時間 明天上午{}點".format(BST_time, oclock)
                    elif CST_oclock == 12:
                        send = "{} BST是台北時間 午夜{}點".format(BST_time, CST_oclock)
                    else:
                        send = "{} BST是台北時間 下午{}點".format(BST_time, CST_oclock)
        #24小時制
        else:
            time = BST_time.split(":")
            BST_oclock = time[0]
            BST_minute = time[1]
            CST_oclock = int(BST_oclock) + 7
            CST_minute = int(BST_minute)
            #處理小時
            oclock = ""
            if CST_oclock >= 24:
                CST_oclock -= 24
                oclock += "明天"
            if CST_oclock > 12:
                oclock += "下午" + str(CST_oclock - 12)
            elif CST_oclock == 12:
                oclock += "中午" + str(CST_oclock)
            else:
                oclock += "上午" + str(CST_oclock)
            #處理分鐘
            if CST_minute == 0:
                minute = "整"
            elif CST_minute == 30:
                minute = "半"
            else:
                minute = str(CST_minute) + "分"
            #組合發送句子
            send = "{} BST是台北時間 {}點{}。".format(BST_time, oclock, minute)
        await message.channel.send(send)

app = Flask('')

@app.route('/')
def main():
	return 'Bot is aLive!'

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()
client.run(data['token'])
