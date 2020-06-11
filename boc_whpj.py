import requests
from bs4 import BeautifulSoup
import bs4
import re

def getHTMLText(url):
    '''
    获取网页源代码并返回
    :param url: 网址
    :return: 网页源代码
    '''
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist, html):
    '''
    解析网页
    外汇数据存储到ulist中
    :param ulist: 储存外汇数据数组
    :param html: 网页源代码
    :return:
    '''
    soup=BeautifulSoup(html,"html.parser")

    for i in soup.find('table',{'align':'left'}).children:

        if isinstance(i, bs4.element.Tag):
            tds=i('td')

            if list(tds) != []:
                ulist.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string,tds[4].string,tds[5].string])


def outToFiles(fname,ulist,num):
    '''
    将数据输出至文件
    :param fname: 文件名，限定csv格式
    :param ulist: 外汇数据列表
    :param num: 获取外汇数据数目，最大值为网页显示最大数目（27个）
    :return:
    '''
    import csv
    f=open(fname,'w',encoding='utf-8')
    csv_writer=csv.writer(f)
    csv_writer.writerow(["货币名称","现汇买入价","现钞买入价","现汇卖出价","现钞卖出价","中行折中价"])
    for i in range(num):
        u=ulist[i]
        for j in range(6):
            if u[j] is None:
                u[j]='None'
        csv_writer.writerow([u[0], u[1], u[2], u[3], u[4], u[5]])

    f.close()



def main():
    uinfo=[]
    url="https://www.boc.cn/sourcedb/whpj/"
    html=getHTMLText(url)
    fillUnivList(uinfo,html)
    filename='boc_whpj.csv'
    outToFiles(filename,uinfo,27)


if __name__=="__main__":
    main()