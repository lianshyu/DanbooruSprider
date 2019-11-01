import urllib.request
import re
import os
import time
import threading
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import requests
# pip install requests   安装库
                                        # # # # # # # # 
                                        # 高清图爬取版 #
                                        # # # # # # # #  
# 从第几页开始爬取
start = 1
# 搜爬取多少页   
page = 2
# 爬取关键字,空 则默认爬取网站页面全部图片 || 可以搜画师名,人物罗马音(izayoi_miku),英文单词(tattoo)
# 禁止“/”等字符输入 , 支持下划线 fate_stay_night
keyword = "karory"
starttime = time.time()
print('爬取进程开始...')
print('起始页:'+str(start)+' 爬取页数:'+str(page)+' 爬取关键字:'+str(keyword))
while start <= page:
    if(start==1):
        if(keyword==""):
            baseurl = "https://danbooru.donmai.us/"
        else:
            baseurl = "https://danbooru.donmai.us/posts?tags="+str(keyword)
    else:
        if(keyword==""):
            baseurl = "https://danbooru.donmai.us/posts?page="+str(start)
        else:
            baseurl = "https://danbooru.donmai.us/post?page="+str(start)+'&tags='+str(keyword)
    print('爬取页面地址: '+baseurl)
    print('开始第'+str(start)+'页爬取中...')
    start+=1
    def pagedownload(baseurl,start):
        def gethtml(url):
            headers={'User-Agent':'Mozilla/5.0'}
            page1=urllib.request.Request(url,headers=headers)
            page=urllib.request.urlopen(page1)
            basehtml=page.read().decode("UTF-8")
            return basehtml
        basehtml = gethtml(baseurl)
        def basereg(html):
            reg = r'(data-id=")([0-9]+?)(")'
            all = re.compile(reg)
            alllist = re.findall(all, html)
            return alllist
        baseimgurls = basereg(basehtml)
        
        def download(baseurl,start,num):
            url = "https://danbooru.donmai.us/posts/"+str(baseurl)
            # print('当前图片爬取地址 '+url)
            os.makedirs('./image/', exist_ok=True)
            def gethtml(url):
                headers={'User-Agent':'Mozilla/5.0'}
                page1=urllib.request.Request(url,headers=headers)
                page=urllib.request.urlopen(page1)
                basehtml=page.read().decode("UTF-8")
                return basehtml
            html = gethtml(url)
            def reg(html):
                reg = r'(id="image")(.+?)(src=")(.+?)(")'
                all = re.compile(reg)
                alllist = re.findall(all, html)
                return alllist
            imgurls = reg(html)
            def urllib_download():
                for imgurl in imgurls:
                    from urllib.request import urlretrieve
                    IMAGE_URL = imgurl[3]
                    IMAGE_URL = IMAGE_URL.replace("/sample", "", 1);
                    IMAGE_URL = IMAGE_URL.replace("sample-", "", 1);
                    IMAGE_URL = IMAGE_URL.replace("jpg", "jpg?download=1", 1);
                    def cbk(a,b,c):  
                        '''''回调函数 
                        @a:已经下载的数据块 
                        @b:数据块的大小 
                        @c:远程文件的大小 
                        '''  
                        per=100.0*a*b/c  
                        if per>100:  
                            per=100  
                        print('%.2f%%' % per)
                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)             
                        urlretrieve(IMAGE_URL, './image/danimg'+str(baseurl)+'.jpg')
                        print('第'+str(start-1)+'页 '+'第'+str(num)+'张图 下载成功')
                    except:
                        IMAGE_URL = IMAGE_URL.replace("jpg", "png?download=1", 1);
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)
                        urlretrieve(IMAGE_URL, './image/danimg'+str(baseurl)+'.png')
                        print('第'+str(start-1)+'页 '+'第'+str(num)+'张图 下载成功')
                    else:
                        pass               
            urllib_download()
        length = len(baseimgurls)
        if(length==0):
            print('第'+str(start-1)+'页 无数据')
        else:
            print('第'+str(start-1)+'页 共'+str(length)+'张图片')   
            num = 1
            pool=ThreadPoolExecutor(max_workers=11)
            for baseimgurl in baseimgurls:
                pool.submit(download,baseimgurl[1],start,num)              
                num+=1
            pool.shutdown()
    pagedownload(baseurl,start)
print('爬取进程完成!!!')
endtime = time.time()
print('程序运行时间为：%.3f 秒'% (endtime-starttime))

