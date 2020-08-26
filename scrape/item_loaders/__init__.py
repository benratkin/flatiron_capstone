"""
Some rules:
    Naming convention is {county}_{state_abbr}_{item_name}_loader.py
    Put input and output processors for items in this directory for spider-specific item loader
    Put as much of parsing/cleaning into the input processor. Always clean as soon as possible in the pipeline
    Loader processors should check if the css_list is empty first and implicitly return None otherwise
"""
