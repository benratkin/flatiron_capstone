import psycopg2
import datetime


class RecordPipelineAddScrapeDate:
    def process_item(self, item, spider):
        item['scrape_date'] = datetime.date.today()
        return item


class RecordPipelineSetNulls:
    # TODO: handle if any of the fields are set to the null string '' as well. Don't insert null strings.
    def process_item(self, item, spider):
        for field in item.fields:
            if field not in item:
                item[field] = None
        return item


class RecordPipelineDbInsert:
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
        # print(item)
        # TODO: Currently if a spider raises exception the database insert still tries? Better error handling.
        self.cursor.execute('''
                insert into record (
                    scrape_date,
                    doc_id,
                    doc_type_text,
                    doc_type_code,
                    recording_date,
                    fee,
                    consideration,
                    instrument_date,
                    grantor,
                    grantee,
                    parcel_id,
                    account_id
                )
                values (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
                ''', (
            item['scrape_date'],
            item['doc_id'],
            item['doc_type_text'],
            item['doc_type_code'],
            item['recording_date'],
            item['fee'],
            item['consideration'],
            item['instrument_date'],
            item['grantor'],
            item['grantee'],
            item['parcel_id'],
            item['account_id']
        ))
        return item