"""
Some rules:
    Naming convention is {item_name}_item.py (Because items aren't county specific)
    Don't specify input or output processors in the item definitions, those go in the item loader
    No more than 2 different fields can go into one input processor. This keeps CSS selectors as specific as possible
        and goes with the general idea of cleaning/parsing as early as possible
"""