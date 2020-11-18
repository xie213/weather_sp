# -*- coding:utf-8 -*-
import requests
import time
import json
import re
import demjson
import xlwt
from multiprocessing.pool import ThreadPool   #线程池

class History_weather():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        #self.f = xlwt.Workbook(encoding='utf-8')

        # 创建一个单表  sheet1, 在单表里面插入
        #self.sheet1 = self.f.add_sheet(u'sheet1', cell_overwrite_ok=True)


    def join_url(self):

        #http://tianqi.2345.com/t/wea_history/js/201803/57048_201803.js
        #http://tianqi.2345.com/t/wea_history/js/201802/57048_201802.js
        #http://tianqi.2345.com/t/wea_history/js/201710/57048_201710.js

        li = ['57048', '70561', '70569', '60549', '53845', '60387', '70575', '70593', '71030', '60386', '57036', '60540', '60967', '60384', '70598', '70590', '57245', '70566', '70580', '70597', '70574', '60968', '60969', '71031', '60964', '60956', '71270', '57127', '60542', '70602', '71664', '70595', '70599', '57016', '71225', '70582', '70581', '70564', '60328', '70565', '70579', '70603', '60958', '71660', '71665', '60546', '70560', '70586', '71667', '60538', '60963', '70600', '60960', '70594', '70604', '71653', '70576', '60385', '60961', '70577', '71663', '70584', '60541', '60547', '60383', '53646', '71662', '71658', '70572', '70559', '70591', '71656', '70596', '71657', '70558', '60970', '71275', '71273', '60544', '70567', '71269', '70570', '70571', '71651', '70585', '71654', '60545', '60537', '53947', '70589', '60679', '71652', '60543', '71199', '60536', '70573', '57045', '60966', '60548', '71666', '70588', '60965', '70568', '60957', '70592', '70601', '70587', '71655', '60539', '60329', '70557', '70583', '70563', '70562', '60331', '60962', '71661', '71650', '60330', '71659']
        #print(li)
        url_start = 'http://tianqi.2345.com/t/wea_history/js/'
        url_year = '_'
        url_l = '/'
        li_year = [2017,2018]
        li_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
        url_js = '.js'
        for i in li:
            i = str(i)
            for j in li_year:
                j = str(j)
                for k in li_month:
                    url = url_start + j + k + url_l + i + url_year + j + k + url_js
                    print(url)
                    self.get_url(url)
    def get_url(self,url):
        #print(url)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                self.parser_url(r.text)
            else:
                time.sleep(0.1)
                r = requests.get(url, headers=self.headers)
                if r.status_code == 200:
                    self.parser_url(r.text)
                else:
                    time.sleep(0.1)
                    r = requests.get(url, headers=self.headers)
                    if r.status_code == 200:
                        pass
                        self.parser_url(r.text)
                    else:
                        return 0
        except Exception as e:  # except BaseException  这个也可以     e是打印出错误的原因
            # print("json问题",e)
            pass
        # print("url:",url)
        # try:
        #     r = requests.get(url,headers = self.headers)
        #     if r.status_code == 200:
        #         self.parser_url(r.text)
        #     else:
        #         time.sleep(0.1)
        #         return self.get_url(url)
        # except Exception as e:  # except BaseException  这个也可以     e是打印出错误的原因
        #     #print("json问题",e)
        #     pass



    def parser_url(self,r):
        global num
        r = re.findall(r'var weather_str=(.*?);',r)[0]
        json_r = demjson.decode(r)
        li_dict = json_r['tqInfo']
        for i in li_dict:
            li = []
            #print("i***********------------",type(i))
            li.append(json_r['city'])
            li.append(i['ymd'])  #时间
            li.append(i['tianqi'])   #天气
            li.append(i['bWendu'])  #最高温
            li.append(i['yWendu'])  #最低温
            li.append(i['fengli'])  #风力
            li.append(i['fengxiang'])  #风向
            print('/'*99)
            print(li)
            # num+=1
            # j = 0
            # for i in li:
            #     #self.sheet1.write(num, j, i)  # 把li的数据按照  num行来插入， （这三个参数分别是行、列、值）
            #     j += 1
        #print("天气情况",li)




if __name__ == '__main__':
    num = 0
    aa = History_weather()
    pool = ThreadPool(32)  # 实现一个线程池 ，参数是线程的数量, 这里就是两个线程等待调用
    pool.apply_async(aa.join_url)  # 这个线程池传参很精髓
    pool.close()  # 关闭线程池， 不在提交任务，
    pool.join()  # 等待线程池里面的任务 运行完毕
    # aa.f.save(r'e:\excel_finally_3.xls')  # 保存