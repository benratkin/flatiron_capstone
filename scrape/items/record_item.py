# -*- coding: utf-8 -*-
from scrapy import Field, Item


class Record(Item):
    scrape_date = Field()
    doc_id = Field()
    doc_type_text = Field()
    doc_type_code = Field()
    recording_date = Field()
    fee = Field()
    consideration = Field()
    instrument_date = Field()
    grantor = Field()
    grantee = Field()
    parcel_id = Field()
    account_id = Field()