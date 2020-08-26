import datetime
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

# Helper functions
def re_extract(css_sel_list, regex, data_type):
    """Extracts regex from first item in css_sel_list.

    :param css_sel_list: Collected css selectors from item loader in spider.
    :param regex: Regular expression to extract match, requires one capture group.
    :param data_type: type casting to integer or string by specifying int or str.
    :return: Returns the extracted int or string or, if no matches, None.
    """
    if css_sel_list:
        matches = re.findall(regex, css_sel_list[0])
        if matches:
            return data_type(matches[0])

# Input processors
def extract_doc_id(css_sel_list):
    if css_sel_list:
        doc_id = css_sel_list[0].strip()
        return doc_id

def extract_doc_type_text_in(css_sel_list):
    if css_sel_list:
        doc_type_text = ''.join(css_sel_list).strip()
        return doc_type_text

def extract_recording_date(css_sel_list):
    if css_sel_list:
        # TODO: Review if I meant to say .strip instead of .split(), why would I index though?
        date_string = css_sel_list[0].partition(' ')[0]
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
        return date_obj

def extract_instrument_date(css_sel_list):
    if css_sel_list:
        # TODO: Review if I meant to say .strip instead of .split(), why would I index though?
        date_string = css_sel_list[0].encode('ascii', 'ignore').decode('utf-8').partition(' ')[0]
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
        return date_obj

def extract_grantor(css_sel_list):
    if css_sel_list:
        grantor = css_sel_list[0].strip()
        return grantor

def extract_grantee(css_sel_list):
    if css_sel_list:
        grantee = css_sel_list[1].strip()
        return grantee

def extract_parcel_id(css_sel_list):
    if css_sel_list:
        parcel_id = css_sel_list[0].encode('ascii', 'ignore').decode('utf-8').strip()
        return parcel_id

def extract_fee(css_sel_list):
    fee = re_extract(css_sel_list, '\$(\d+)', int)
    return fee

def extract_consideration(css_sel_list):
    consideration = re_extract(css_sel_list, '\$(\d+)', int)
    return consideration

def extract_account_id(css_sel_list):
    if css_sel_list:
        account_id = css_sel_list[0]
        return account_id

# Output processors


class RecordLoader(ItemLoader):

    default_output_processor = TakeFirst()

    doc_id_in = extract_doc_id
    doc_type_text_in = extract_doc_type_text_in
    recording_date_in = extract_recording_date
    grantee_in = extract_grantee
    grantor_in = extract_grantor
    parcel_id_in = extract_parcel_id
    fee_in = extract_fee
    consideration_in = extract_consideration
    instrument_date_in = extract_instrument_date
    account_id_in = extract_account_id