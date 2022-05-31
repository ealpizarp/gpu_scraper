# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from unittest import result
from itemadapter import ItemAdapter
from datetime import datetime

import pymongo


class GpuScraperPipeline:

    collection_name = 'scraped-data-registers'
    audit_name = 'scraped-data-audit'

    def __init__(self, mongo_uri, mongo_db, stats):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            stats=crawler.stats
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        register = ItemAdapter(item).asdict()
        num_registers = len(register)
        url = spider.current_url
        date = datetime.now()
        stats = self.stats.get_stats()

        audit = {
            "num_registers": num_registers,
            "url": url,
            "date": date,
            "state": "Finished",
            "errors": "None",
        }
        audit.update(stats)


        self.db[self.audit_name].insert_one(audit)
        self.db[self.collection_name].insert_one(register)
        return item