# Create time:2018-12-16 15:52
# Author:Chen

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import redis

if __name__ == "__main__":
	# master端代码
	# slave端删除横线中代码
	# ——————————————————————————————————————————————————————————
	con = redis.Redis("localhost", 6379)
	url = "https://www.zhihu.com/api/v4/members/su-fei-17/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
	con.lpush("zhihu:start_urls", url)
	# ——————————————————————————————————————————————————————————
	p = CrawlerProcess(get_project_settings())
	p.crawl("user")
	p.start()