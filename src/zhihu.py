# -*- coding:utf-8 -*-
import requests
import time
import json
import os
import re
import sys
import MySQLdb
import subprocess
import pickle
from bs4 import BeautifulSoup
import logging

class userprofile:
    def __init__(self):
        self.company=''
        self.nick=''
        self.sex=''
        self.agree_num=0
        self.thank_num=0
        self.name='parseException'
        self.position=''
        self.topics= ''
        self.avatar=''
        self.loc=''
        self.business=''

# def get_nick_from_url(url):
#     if len(url) == 0:
#         return 'url_is_null'
#     nick = url[url.rfind('/')+1:]
#     return nick

def logger(logfile):
    mylogger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    hdlr.setFormatter(formatter)
    mylogger.addHandler(hdlr)
    mylogger.setLevel(logging.NOTSET)
    return  mylogger

def get_url_from_nick(nick):
    return 'http://www.zhihu.com/people/'+nick

def existed(nick):
    existed=False
    try:
        cursor.execute("select * from profile where nick='%s'" % (nick))
        if cursor.rowcount > 0:
            existed =   True
        else:
            existed = False
    except:
        log.info("db error happen"+str(MySQLdb.Error))
        db.rollback()

    return existed


def store(profile):
    sql ="insert into profile(company,nick,sex,agree_num,thank_num,name,position,topics,avatar,loc,business)\
          VALUES ('%s','%s','%s','%d','%d','%s','%s','%s','%s','%s','%s')"%\
          (profile.company,profile.nick,profile.sex,profile.agree_num,profile.thank_num,profile.name,profile.position,profile.topics,profile.avatar,profile.loc,profile.business)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        log.info("db error happen"+str(MySQLdb.Error))
        db.rollback()



def parse_profile(nick):
    url = get_url_from_nick(nick)
    profile = userprofile()

    """用户nick,相当于UID,必须要先解析.否则可能导致多个人有相同nick"""
    profile.nick = nick

    content = session.get(url,timeout=10).text
    bs = BeautifulSoup(content,"html.parser")
    """用户擅长话题"""
    # profile.description = str(bs.find('span', class_='content').contents)
    topics = bs.find_all('a',class_='zg-gray-darker')
    for each in topics:
        profile.topics+=each.string+','
    profile.topics = profile.topics[0:profile.topics.rfind(',')-1]

    """获得用户中文名"""
    try:

        for each in  bs.find('div',class_='title-section ellipsis').children:
            if each.name == 'span':
                profile.name = each.string
                break
    except:
        log.info("exception happened when parse __name__ " + url)




        """获得性别"""
    try:
        sex = bs.find('i',class_='icon icon-profile-male')
        # print(sex)
        if sex is not  None:
            profile.sex = '男'
        else:
            profile.sex = '女'
    except:
        log.info("exception happened when parse __sex__ " + url)

        """公司信息"""
    try:
        profile.company = bs.find('span',class_='employment item')['title']
    except:
        log.info("exception happened when parse __company__ " + url)



    try:
        """职业信息"""
        profile.position = bs.find('span',class_='position item')['title']
    except:
        log.info("exception happened when parse __position__ " + url)



    try:
        """赞数"""
        for one in bs.find('span',class_='zm-profile-header-user-agree').children:
            if one.name == 'strong':
                profile.agree_num = int(one.string)
    except:
        log.info("exception happened when parse __agree_num__ " + url)


    try:
        """感谢数"""
        for one in bs.find('span',class_='zm-profile-header-user-thanks').children:
            if one.name == 'strong':
                profile.thank_num = int(one.string)
    except:
        log.info("exception happened when parse __thank_num__ " + url)


    """获得头像"""
    try:
        profile.avatar = bs.find('img',class_='avatar avatar-l')['src']
    except:
        log.info('exception happened when parse __avatar')

    """地区"""
    try:
        profile.loc = bs.find('span',class_='location item')['title']
    except:
        log.info('exception happened when parse __location')

    """所在行业"""
    try:
        profile.business = bs.find('span',class_='business item')['title']
    except:
        log.info('exception happened when parse __business ')




    return profile

def get_followee(nick):
    followees=list()
    followee_url = get_url_from_nick(nick) + '/followees'
    content = session.get(followee_url,timeout=10).text
    bs = BeautifulSoup(content)
    for one in bs.find_all('a',class_="zm-item-link-avatar"):
        followee = one['href']
        followees.append(followee[followee.rfind('/')+1:])
    return  followees

class zh_login(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.zhihu.com",
        "Upgrade-Insecure-Requests": "1",
    }

    cookieFile = os.path.join(sys.path[0], "cookie")

    # 检查是否已经登陆
    def logined(self,username,password):
        os.chdir(sys.path[0])  #设置脚本所在目录为当前工作目录
        self.__session = requests.Session()
        self.__session.headers = self.headers  # 用self调用类变量是防止将来类改名
        # 若已经有 cookie 则直接登录
        self.__cookie = self.__loadCookie()
        if self.__cookie:#已经登陆
            print("检测到cookie文件，直接使用cookie登录")
            self.__session.cookies.update(self.__cookie)
            return True;
        else:
            return False;

    def __init__(self, username, password):
        if self.logined(username,password):
            return
        self.login(username,password)

    def get_xsrf(self):
        homeURL = r"http://www.zhihu.com"
        html = self.open(homeURL).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("input", {"name": "_xsrf"})["value"]

    def login(self,username,password):
        xsrf = self.get_xsrf()
        captcha = self.get_captcha()
        data = {
            "_xsrf": xsrf,
            "password":password,
            "remember_me": "true",
            "email": username,
            "captcha": captcha
        }

        loginURL = r"http://www.zhihu.com/login/email"
        res = self.__session.post(loginURL, data=data)
        if res.json()["r"] == 0:
            print("登录成功")
            self.__saveCookie()
        else:
            print("登录失败")
            print("错误信息 --->", res.json()["msg"])

    def get_captcha(self):
        captchaURL = r"http://www.zhihu.com/captcha.gif"
        captchaFile = os.path.join(sys.path[0], "captcha.gif")
        with open(captchaFile, "wb") as outfile:
            captcha = self.open(captchaURL).content
            outfile.write(captcha)
            outfile.close()
            # 人眼识别
            print("已打开验证码图片，请识别！")
            text = input("请输入验证码：")
            print(text)
            return text



    def __saveCookie(self):
        """cookies 序列化到文件
        即把dict对象转化成字符串保存
        """
        with open(self.cookieFile, "w") as output:
            cookies = self.__session.cookies.get_dict()
            json.dump(cookies, output)
            print("=" * 50)
            print("已在同目录下生成cookie文件：", self.cookieFile)

    def __loadCookie(self):
        """读取cookie文件，返回反序列化后的dict对象，没有则返回None"""
        if os.path.exists(self.cookieFile):
            print("=" * 50)
            with open(self.cookieFile, "r") as f:
                cookie = json.load(f)
                return cookie
        return None

    def open(self, url, delay=0, timeout=10):
        """打开网页，返回Response对象"""
        if delay:
            time.sleep(delay)
        return self.__session.get(url, timeout=timeout)

    def getSession(self):
        return self.__session


def work():
    #当前队列中是否还有没有处理的用户
    while len(peoples) > 0:
        dump(peoples)
        log.info("==========size of peoples is "+str(len(peoples))+" ===============")
        #开始处理队首的用户
        first = peoples.pop()
        if existed(first):
            continue
        #获得该用户的个人信息
        profile  = parse_profile(first)
        log.info("store user "+profile.name+" nick: "+profile.nick)
        #持久化存储该用户的个人信息
        store(profile)
        #获得该用户关注的人
        followees = get_followee(first)
        #将该用户关注的人加入待处理队列中
        for each in followees:
            peoples.add(each)
            log.info( each +" added to queue")

def dump(obj):
    df = open('dump.txt','wb')
    pickle.dump(obj,df)
    df.close()

def load():
    df = open('dump.txt','rb')
    try:
        ret = pickle.load(df,encoding='utf8')
    except:
        ret = False
    df.close()
    return ret

if __name__ == '__main__':
    try:
        login = zh_login("che3vinci@me.com", "your_pass_word")
    except:
        print("login failed")
        exit()
    log = logger('log.txt')
    session = login.getSession()
    # 用这个session进行其他网络操作，详见requests库

    ##建立数据库连接
    db = MySQLdb.connect(host="localhost", port=3306, user="jinbowang", passwd="", db="test")
    cursor = db.cursor()


    peoples = load()
    if peoples == False:
        peoples = set()
        if(len(sys.argv) == 2):
            che3vinci = sys.argv[1]
        else:
            che3vinci = 'wang-jin-bo-87'
        peoples.add(che3vinci)
    work()
    cursor.close()