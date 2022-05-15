# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def description_prep(value):
    value = remove_tags(value).strip()
    return value.lower


class RemotarItem(scrapy.Item):

    title = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    type = scrapy.Field()
    link = scrapy.Field()
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, description_prep),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
    date = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst()
    )
