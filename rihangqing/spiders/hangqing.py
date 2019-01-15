import threading
import time
import multiprocessing
from multiprocessing import Process,Pool
import requests
from bs4 import BeautifulSoup
import  scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from rihangqing.items import SmppItem
#from dayhq.items import MysqlTwistedPipline
import tushare as ts
import json
import re
import datetime
from scrapy.spiders import CrawlSpider, Rule
list_urls = []
class DmozSpider(CrawlSpider):
    name = "riday"
    #allowed_domains = ["dmoz.org"]
    #codess = ['000166', '601211', '601375', '000002']
    codess = ts.get_today_all()['code']
    list_sh = []
    list_sz = []
    list_all = []
    for code in codess:
        print(code)
        if code[0] == '6':
            list_sh.append('http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=' \
                           '4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18308283880836601216_1547106073540&id=' + code + '1&type=k&authorityType=&_=1547106074467')
        else:
            list_sz.append(
                'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305135314321457163_1547107241758&id=' \
                + code + '2&type=k&authorityType=&_=1547107243264')
    list_all = list_sh + list_sz
    start_urls = list_all
    print(start_urls)





    def parse(self,response):
        #print('www',response)

        # try:
        #     r = requests.get(response)
        # except:
        #     list_urls.append(response)

            # driver.get(self.url)
        infos = response.text

        p1 = re.compile(r'[(](.*?)[)]', re.S)
        list_all = re.findall(p1, infos)
        # info = eval(list_all[0])
        info = json.loads(list_all[0])
        names = info['name']
        print(names)
        codes = info['code']
        dates = info['data']
        #item = DmozItem()
        list_times = []
        for date in dates:
            item = SmppItem()
            dts = date.split(',')
            times = dts[0]
            timess = datetime.datetime.strptime(times, '%Y-%m-%d')
            item['time'] = timess
            list_times.append(times)
            item['opens'] = dts[1]

            item['closes'] = dts[2]

            item['high'] = dts[3]

            item['low'] = dts[4]

            item['volume'] = dts[5]

            item['volumemoney'] = dts[6]

            item['huanshou'] = dts[7]
            item['names'] = names
            item['codes'] = codes
            #print('wwwwwwwwwwwwwwwwwww',item['codes'],item['names'])

            print('vvvvvvvvv',len(list_times))

            yield item