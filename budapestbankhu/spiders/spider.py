import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import BudapestbankhuItem
from itemloaders.processors import TakeFirst


class BudapestbankhuSpider(scrapy.Spider):
	name = 'budapestbankhu'
	start_urls = ['https://www.budapestbank.hu/apps/top-news?labels=BB,BBM,BBV,BBKV,BBD,BBMP,BBP,BBMNY,BBONY&from=0&size=999999&type=press-release&highlighted=false&list=true']

	def parse(self, response):
		data = json.loads(response.text)
		for item in data['hits']:
			title = item['card']['title']
			date = item['date']
			url = item['url']
			yield response.follow(url, self.parse_post, cb_kwargs={'title': title, 'date': date})
	def parse_post(self, response, title, date):
		description = response.xpath('//div[@class="sf-column sf-column"][1]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BudapestbankhuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
