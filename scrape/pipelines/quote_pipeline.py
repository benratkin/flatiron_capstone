# -*- coding: utf-8 -*-
import datetime
import psycopg2

# ----------------START TEST (QUOTE) SPIDER-----------------------------------------------------------------------------

class QuotePipelineAddDate:
    def process_item(self, item, spider):
        item['date'] = datetime.date.today()
        print(item['date'], item['quote'], item['by'])
        return item


class QuotePipelineDbInsert:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host='recorder.cqhgw5k5cbjk.us-east-2.rds.amazonaws.com',
            dbname='recorder'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
        insert into quote (date, text, by) 
        values (%s, %s, %s);
        ''', (item['date'], item['quote'], item['by']))
        return item

# ----------------END TEST (QUOTE) SPIDER-------------------------------------------------------------------------------
