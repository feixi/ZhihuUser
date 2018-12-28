# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class ZhihuuserPipeline(object):

    def __init__(self, mongo):
        self.collection = pymongo.MongoClient(*mongo).zhihu.user

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist("MONGO"))

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
