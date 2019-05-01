# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter

class GlobaltradescraperPipeline(object):
  
    def open_spider(self, spider):
        self.file = open('item.json', 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close() 
    def process_item(self, item, spider):
        return item
