# Create time:2018-12-27 21:06
# Author:Chen
import redis
import functools
import mmh3


class BloomFilter:

	def __init__(self, key_name):
		self.seed = [7, 11, 17, 31, 41, 47, 57, 61]
		self.bit_len = 1 << 32
		self.server = redis.Redis("127.0.0.1", 6379)
		# redis中的key名字
		self.key_name = key_name
		# 哈希函数列表
		self.hash_func = self.create_function()

	def create_function(self):
		"""
		由seed生成布隆过滤器哈希函数列表，等待要过滤的字符串。
		哈希函数由mmh3第三方库提供，mmh3很火，据说性能很高，而且生成的结果在2^32之内
		:return:
		"""
		return [functools.partial(mmh3.hash, seed=i) for i in self.seed]

	def offset_list(self, str):
		"""
		获取bit位生成器
		:param str: 要去重的字符串
		:return:
		"""
		for funct in self.hash_func:
			# mmh3的取值结果是负数
			yield abs(funct(str)) % self.bit_len

	def insert(self, str):
		"""
		向redis的bit串中添加位
		:param str: 要去重的字符串
		:return:
		"""
		for offset in self.offset_list(str):
			self.server.setbit(self.key_name, offset, 1)
		return False

	def contains(self, str):
		"""
		判断字符串是否重复，也就是各个指定偏移量的bit位是否有0，只要一个是0，就认为该字符串不重复
		:param str:
		:return:
		"""
		return all(self.server.getbit(self.key_name, offset) for offset in self.offset_list(str))

	def __repr__(self):
		return f"容量m=512M, 哈希函数个数k=8, 假设加入字符串个数n=2亿，m/n=21.4, 漏失概率查表是0.000101"


if __name__ == "__main__":
	b = BloomFilter('ppp')
	print(b.contains("cheng-ying-jie-95"))
	b.insert("cheng-ying-jie-95")
	print(b.contains("cheng-ying-jie-95"))

