# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ..items import ZhihuuserItem
from scrapy_redis.spiders import RedisCrawlSpider


class UserSpider(RedisCrawlSpider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']
    redis_key = "zhihu:start_urls"

    def parse(self, response):
        """
        分析返回的response，并且根据新的用户id构建写的request
        :param response:
        :return:
        """
        temp_data = json.loads(response.body.decode("utf-8"))['data']
        for u in temp_data:
            item = ZhihuuserItem(
                name=u['name'],
                url_token=u['url_token'],
                headline=u['headline'],
                follower_count=u['follower_count'],
                answer_count=u['answer_count'],
                articles_count=u['articles_count'],
                uid=u['id'],
                gender=u['gender'],
                type=u['type']
            )
            yield item
            # 新的用户关注者列表
            new_user_url = f'https://www.zhihu.com/api/v4/members/{u["url_token"]}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
            yield scrapy.Request(new_user_url)
        # 翻页
        if len(temp_data) == 20:
            old_offset = re.findall("offset=(\d+)&", response.url)[0]
            new_offset = str(int(old_offset) + 20)
            new_offset_url = response.url.replace(f"offset={old_offset}&", f"offset={new_offset}&")
            yield scrapy.Request(new_offset_url)
