# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class SmppPipeline(object):
    #def process_item(self, item, spider):
        #return item
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi
from scrapy import log

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port= settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)


    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        try:
            SQL = """ insert into codeday4(times, opens, closes, high, low, volume, volumemoney, huanshou, codes, namess) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s) """
            cursor.execute(SQL, (item['time'], item['opens'], item['closes'], item['high'], item['low'], item['volume'],
                  item['volumemoney'], item['huanshou'], item['codes'], item['names']))

        except Exception as e:
            print('***** Logging failed with this error:', str(e))
            #log.msg('***** Logging failed with this error:', str(e), level=log.INFO, spider=None)