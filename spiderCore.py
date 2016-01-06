# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import imp
import sys

from pymongo import MongoClient

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的


user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

dic = {}
menuName = "menu"
ingredient = "ingredient"
cookbook = "cookbook"

#搜索材料 主料 牛肉 500克 辅。。。
def findIngredient():
    patternIngred = re.compile(r'<div class="dl clearfix.*?">\n+.*?<div class="dt cg2">(.*?)</div>\n.*?<div class="dl clearfix.*?">', re.S)
    itemsIngredKey = re.findall(patternIngred, content)
    if itemsIngredKey:
        print itemsIngredKey[0] + ": "

    patternIngredValue = re.compile(r'<div class="dl clearfix.*?">\n+.*?<div class="dd">(.*?)<div class="dl clearfix.*?">',re.S)
    itemsIngredValue = re.findall(patternIngredValue, content)
    #print itemsIngredValue[0]
    if itemsIngredValue:
        pchinese=re.compile(u">[\d\u4e00-\u9fa5]+") #判断是否为中文的正则表达式
        chineseWords = re.findall(pchinese,itemsIngredValue[0])
        text = ''
        for item in chineseWords:
             text += item[1:] + ' '
        print text
        dic[ingredient] = text


 # 搜索做法
def findCookWay():
    patternIngred = re.compile(r'<div class="dl clearfix mt20.*?">\n+.*?<div class="dt cg2">(.*?)</div>\n.*?', re.S) # print 做饭细节
    itemsIngredKey = re.findall(patternIngred, content)
    if itemsIngredKey:
        print itemsIngredKey[0] + ": "

    patternIngredValue = re.compile(r'<div class="dd" itemprop="recipeInstructions">\n+(.*?)<script.*?>',re.S)
    itemsIngredValue = re.findall(patternIngredValue, content)
    if itemsIngredValue:
        pchinese=re.compile(u"[\d\u4e00-\u9fa5]+") #判断是否为中文的正则表达式
        chineseWords = re.findall(pchinese,itemsIngredValue[0])
        text = ''
        for item in chineseWords:
             text += item + ' '
        print text
        dic[cookbook] = text

# 打印菜名
def findMenu():
    patternKey = re.compile(r'<div class="re-up">\n+.*?<h1 class.*?>(.*?)</h1>\n.*?',re.S)  # 四川水煮牛肉
    items = re.findall(patternKey, content)
    if items:
        print items[0]
        dic[menuName] = items[0]


def main():
    client = MongoClient()
    db = client.pacai
    global content
    global menuIndex
    global page
    page = 155
    menuIndex = 0

    for i in range(155, 999):
        page = page + 1 # get next page
        print "page: " + str(page)
        try:
            url = 'http://www.xinshipu.com/zuofa/' + str(page)
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')


            findMenu()
            findIngredient()
            findCookWay()
            result = db.test.insert_one(
              {
                  menuName: dic.get(menuName),
                  ingredient: dic.get(ingredient),
                  cookbook: dic.get(cookbook),
                  "index": menuIndex
              }
            )
            menuIndex = menuIndex + 1
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

main()

