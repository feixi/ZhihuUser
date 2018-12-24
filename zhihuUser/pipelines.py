# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import redis
from scrapy.exceptions import CloseSpider


class ZhihuuserPipeline(object):

    def __init__(self, mongo, redis_conf):
        self.cli = pymongo.MongoClient(*mongo,)
        self.collection = self.cli.zhihu.userInfo
        self.con = redis.Redis(*redis_conf)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist("MONGO"), crawler.settings.getlist("REDIS"))

    def process_item(self, item, spider):
        # 检查爬取的数量，到达十万时停止爬取，关闭爬虫
        if int(self.collection.find().count()) > 100000:
            spider.crawler.engine.close_spider(spider, '没有新数据关闭爬虫')
            raise CloseSpider(f"数据量到达十万")
        self.collection.insert(dict(item))
        return item
