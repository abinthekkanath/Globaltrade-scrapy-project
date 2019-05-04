import scrapy
from scrapy import Selector
from w3lib.html import remove_tags
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
			if targeturl:
				yield scrapy.Request(url=targeturl, callback=self.targetPage)
		nextpagelink=response.css('.next-page::attr(href)').get()
		if nextpagelink is not None:
			nextpageurl=response.urljoin(nextpagelink)
			yield scrapy.Request(url=nextpageurl, callback=self.innerPages)

	def targetPage(self, response):
		items=GlobaltradescraperItem()

		items['logo_url']=response.css('.image .lazy::attr(data-original)').get()

		items['title']=response.css('.sp-title span::text').get()

		items['sub_title']=response.css('.sub::text').get()

		primary_location=response.css('.profile-details span span::text').getall()
		if len(primary_location)==0:
			primary_location=response.css('span span::text')[:1].getall()
		items['primary_location']="".join(primary_location).replace("\n","")

		items['area_of_expertise']=response.css('.mainExp::text').get()

		about=remove_tags("".join(response.css('.details tr:nth-child(1) td+ td::text').getall()).replace("\n",""))
		if len(about)<=1:
			about=remove_tags("".join(response.css('.details p::text').getall()).replace("\n",""))
			if len(about)<=1:
				about=remove_tags("".join(response.css('.details p strong::text').getall()).replace("\n",""))
		items['about']=about

		website="".join(response.css('.details a:nth-child(1)::text').getall()[:1]).replace("\n","")
		if 'www.' not in website:
			website=""
		items['website']=website

		language_spoken="".join(response.css('tr:nth-child(4) td+ td::text').getall()).replace("\n","")
		if 'English' not in language_spoken:
			language_spoken="".join(response.css('tr:nth-child(5) td+ td::text').getall()).replace("\n","")
			if 'English' not in language_spoken:
				language_spoken="".join(response.css('tr:nth-child(6) td+ td::text').getall()).replace("\n","")
				if 'English' not in language_spoken:
					language_spoken=""
		items['language_spoken']=language_spoken

                items['page_url']=response.url
		
		yield items
		
		
