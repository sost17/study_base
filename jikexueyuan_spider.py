# coding=UTF-8

import requests
import re

class spider(object):
    def __init__(self):
        print(u'开始爬取内容...')

    def getsource(self,url,headers):
        html = requests.get(url,headers)
        return html.text

    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=(\d+)','pageNum={}'.format(i),url,re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self,html):
        everyclass = re.findall('<li id=(.*?)</li>',html,re.S)
        return everyclass

    def getinfo(self,each):
        info = {}

        lesson_info_h2 = re.search('<h2 class="lesson-info-h2">(.*?)</h2>',each,re.S).group(1)
        info['class_name'] = re.search('<a href=.+?>(.*?)</a>',lesson_info_h2,re.S).group(1)

        content = re.search('<p.+?>(.*?)</p>',each,re.S).group(1)
        p = re.compile('[\S\s]*')
        info['content'] = p.search(content).group().strip()

        time_dl = re.search('<div class="cf">.+?<dl>(.*?)</dl>',each,re.S).group(1)
        time_em = re.findall('<em>(.*?)</em>',each,re.S)
        info['time'] = re.sub('\s','',time_em[0],re.S)
        info['level'] = time_em[1]

        info['learn_number'] = re.search('<em class="learn-number.+?>(.*?)</em>',each,re.S).group(1)

        return info

    def saveinfo(self,classinfo):
        with open('info.txt','a',encoding='utf-8') as f:
            for each in classinfo:
                f.writelines('title:' + each['class_name'] + '\n')
                f.writelines('content:' + each['content'] + '\n')
                f.writelines('time:' + each['time'] + '\n')
                f.writelines('level:' + each['level'] + '\n')
                f.writelines('learn_number:' + each['learn_number'] + '\n\n')

if __name__ == '__main__':
    classinfo = []
    url = 'https://www.jikexueyuan.com/course/?pageNum=1'
    headers = {
        "User-Agent":"Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/80.0.3987.87 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    jikespider = spider()
    all_links = jikespider.changepage(url,101)
    for link in all_links:
        print('正在处理页面：' +link)
        html = jikespider.getsource(link,headers)
        everyclass = jikespider.geteveryclass(html)
        for each in everyclass:
            info = jikespider.getinfo(each)
            classinfo.append(info)
    jikespider.saveinfo(classinfo)
