import scrapy
from ..items import GlobaltradescraperItem
class GlobalTradeSpider(scrapy.Spider):
	name="globaltradespider"
	
        start_urls = [
		'https://www.globaltrade.net/international-trade-import-exports/expert-service-provider-p/Fastfix-Inc.html'
	]
		

	def parse(self, response):
		
		items=GlobaltradescraperItem()
		items['title']=response.css('.sp-title span::text').extract()
		items['sub_title']=response.css('.sub::text').extract()
		items['primary_location']=response.css('.profile-details span span::text').extract()
		
		yield items
