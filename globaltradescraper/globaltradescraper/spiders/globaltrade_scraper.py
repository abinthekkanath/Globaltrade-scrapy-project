import scrapy
from ..items import GlobaltradescraperItem
class GlobalTradeSpider(scrapy.Spider):
	name="globaltradespider"
	
        start_urls = [
		'https://www.globaltrade.net/expert-service-provider.html'
	]
		

	def parse(self, response):
		
		nextLink=response.css('.sp_country_71::attr(href)').get()
		nexturl=response.urljoin(nextLink)
		
		yield scrapy.Request(url=nexturl, callback=self.innerPages)

	def innerPages(self, response):
		links=response.css('.profileNavigator::attr(href)').getall()
		for link in links:
			targeturl=response.urljoin(link)
			yield scrapy.Request(url=targeturl, callback=self.targetPage)

	def targetPage(self, response):
		items=GlobaltradescraperItem()
		items['title']=response.css('.sp-title span::text').get()
		items['sub_title']=response.css('.sub::text').get()
		items['primary_location']=response.css('.profile-details span span::text').get()
		
		yield items
		
