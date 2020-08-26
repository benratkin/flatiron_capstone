# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


# ----------------START TEST (QUOTE) SPIDER-----------------------------------------------------------------------------

class Quote(Item):
    date = Field()
    quote = Field()
    by = Field()

# ----------------END TEST (QUOTE) SPIDER-------------------------------------------------------------------------------
