#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os

import requests
import re
class YouShuSpider():
    def __init__(self):
        self.loginurl = 'https://api.yousuu.com/api/login'
        self.user_agent = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
    def login(self):
        data = {
            'password': "axfbjm1599630",
            'userName': "18323329375"
        }
        response = requests.post(self.loginurl, data=data, headers=self.user_agent)
        print(response.status_code, response.json())
        returnData = response.json()
        if response.status_code != 200:
            print("登录失败")
            return False
        else:
            print("登录成功")
            return True

    def run(self):
        # if not self.login():
        #     return
        #抓取榜单并下载简介
        url = 'https://api.yousuu.com/api/home/channelBooks?channel=male'
        rsp = requests.get(url,headers=self.user_agent)
        rsp_data = rsp.json()
        print(rsp_data)
        if len(rsp_data['data']['books']) > 0:
            print("返回成功")
            books = rsp_data['data']['books']
            for book in books:
                author = book['author']
                coverimg = book['cover']
                bookid = book['bookId']
                wordcnt = book['countWord']
                title = book['title']
                print(author,title)
                bookurl = 'https://www.yousuu.com/book/'
                bookurl = bookurl + str(bookid)
                print(bookurl)
                book_text = requests.get(bookurl, headers=self.user_agent).text
                comment = re.compile(r'name="description" content="(.*?)"><meta', re.DOTALL)
                bookinfo = comment.findall(book_text)
                print(bookinfo)
                with open('result.csv', 'a+', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([author, title, wordcnt, bookurl, bookinfo[0]])
                    print("写入book:%s信息" % title)

        else :
            print("error")



if __name__ == '__main__':
    if not os.path.exists("./result.csv"):
        print("jinru")
        with open('./result.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["author","title","wordcnt","bookurl","bookinfo"])
    spider = YouShuSpider()
    spider.run()
