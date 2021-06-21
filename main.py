#system libraries
import os
import asyncio
import time
import pause, datetime
from datetime import timedelta, datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import csv
from time import sleep
import threading
import signal
import sys
from sys import exit
from threading import Thread

import requests
from bs4 import BeautifulSoup
import json
import lxml
from lxml import html

def main(sku,productName):
    webhookMain = "webhook here"
    while True:
        try:
            # Enter proxy here ip:port or user:pass:ip:port
            proxies = {
                "https": "https://192.198.126.217:1234/"
            }

            URL = "https://www.memoryexpress.com/Products/" + sku
            
            headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

            page = requests.get(URL, headers=headers, proxies=proxies)

            soup = BeautifulSoup(page.content, 'html.parser')
        
            # Send Webhook
            while True:
                try:
                    # Check if atc button exists if so send webhook
                    if soup.find(class_="c-shco-grad-button c-shco-grad-button--gray").get_text():
                        webhook = DiscordWebhook(url=webhookMain, username="Memory Express")
                        embed = DiscordEmbed(title='Item', description=(productName), color=242424)
                        embed.set_author(name='Memory Express Monitor ', icon_url='https://pbs.twimg.com/profile_images/1161809234725441537/P2Nz_JZ4_400x400.jpg')
                        embed.set_footer(icon_url='https://pbs.twimg.com/profile_images/1161809234725441537/P2Nz_JZ4_400x400.jpg', text='Powered By CheemaOTB#0001')
                        embed.set_timestamp()
                        embed.add_embed_field(name='Product Page', value=(URL))
                        webhook.add_embed(embed)
                        response = webhook.execute() #pylint:disable=unused-variable;
                        print('[' + datetime.now().strftime("%H:%M:%S.%f") + '] '+sku+' IN STOCK ')
                        time.sleep(500)
                        break
                    else:
                        break
                    break
                except:
                    print('[' + datetime.now().strftime("%H:%M:%S.%f") + '] '+sku+' OOS ')
                    break

        except:
            print('[' + datetime.now().strftime("%H:%M:%S.%f") + '] ERROR ')
            break


# Store threads
threads = []

# Multithreading using the sku.csv
with open("sku.csv", "r") as fd:
    next(fd)
    for line in fd.readlines():
        line = line.strip()
        if not line:
            continue
        task = line.split(",")
        sku = task[0]
        productName = task[1]
        t = Thread(target=main, args=(sku, productName,))
        t.start()
        threads.append(t)

for t in threads:
    t.join()
