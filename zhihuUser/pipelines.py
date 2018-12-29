# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from zhihuUser.BloomFilter import BloomFilter


class ZhihuuserPipeline(object):

    def __init__(self, mongo):
        self.collection = pymongo.MongoClient(*mongo).zhihu.user
        self.f = BloomFilter("BloomFilter_zhihu")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist("MONGO"))

    def process_item(self, item, spider):
        if not self.f.contains(item['url_token']):
            self.collection.insert(dict(item))
        return item
