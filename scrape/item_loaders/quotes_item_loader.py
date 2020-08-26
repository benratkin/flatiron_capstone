from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose, Compose

# Input processors
# Defining normal function to use with MapCompose
def remove_quotations_marks_func(quote_str):
    return quote_str[1:-1]


# Alternatively, defining my own custom processors. Uncomment below to enable.
def strip_quotations_marks_proc(quote_iter):
    for quote_str in quote_iter:
        return quote_str[1:-1]

# Output processors


# ----------------START TEST (QUOTE) SPIDER-----------------------------------------------------------------------------

class QuoteLoader(ItemLoader):


    # Commented, below line uses the custom processor above
    quote_in = strip_quotations_marks_proc
    # quote_in = MapCompose(str.upper, remove_quotations_marks_func)
    quote_out = TakeFirst()

    by_in = Compose()
    by_out = TakeFirst()

# ----------------END TEST (QUOTE) SPIDER-------------------------------------------------------------------------------
