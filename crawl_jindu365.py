#!/usr/bin/env python
#encoding=utf-8

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

login_page = "http://www.jindu365.com/index.php?s=/Login/checkLogin"
user = 'test01'
password = 'test01'
url = 'http://www.jindu365.com/index.php?s=/Exam/winner'

def login():
    # 登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark
    try:
        # 获得一个cookieJar实例
        cj = cookielib.CookieJar()

        # cookieJar作为参数，获得一个opener的实例
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        # 伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]

        # 生成Post数据，含有登陆用户名密码。
        data = urllib.urlencode({"username": user, "password": password, "button": '', "__hash__": '13d942992c1de43c30fc92a9b3ac9fad_cc5f1e34bf69940f8f2768f8aa06a1ac'})

        # 以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        opener.open(login_page, data)

        return opener

        # 以带cookie的方式访问页面
        op = opener.open(url)

        # 读取页面源码
        data1 = op.read()

        op = opener.open(url)

        data2 = op.read()

        return data

    except Exception, e:
        print str(e)
        return None


duplicate_count = 0

def parse(data, question_all):
    soup = BeautifulSoup(data, "html.parser")
    lis = soup.find_all('li', style="display:block;")
    for i in lis:
        is_question = True
        options = []
        question = ''

        h4 = i.find('h4')
        question_type = h4.b.next_sibling.next_sibling.text

        div = i.find('div', class_="change")
        for c in div.children:
            if c.name == 'p':
                text = c.text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
                if is_question:
                    question = text
                    is_question = False
                else:
                    options.append(text)

        if question not in question_all:
            question_all[question] = {'type': question_type, 'options': options}

            print '-------------------'
            print question
            print question_type
            for o in options:
                print o

        else:
            global duplicate_count
            duplicate_count += 1


if __name__ == '__main__':
    try:
        question_all = {}

        # with open('/Users/kangtianhao/Downloads/questions.html') as fp:
        #     data = fp.read()
        #
        # parse(data, question_all)

        opener = login()
        if opener is not None:
            while True:
                op = opener.open(url)
                data = op.read()

                parse(data, question_all)

    except Exception, e:
        print str(e)

