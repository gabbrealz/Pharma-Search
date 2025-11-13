from functools import partial
from line_breaker import insert_linebreaks


class Reader:
    # List of keys in the OTC data set that will be displayed in the GUI.
    OTC_KEYS_LIST = (
        ("brand_name", "Brand Name"),
        ("manufacturer_name", "Manufacturer Name"),
        ("generic_name", "Generic Name"),
        ("product_type", "Product Type"), 
        ("purpose", "Purpose"), 
        ("indications_and_usage", "Indications and Usage"),
        ("dosage_and_administration", "Dosage and Administration"),
        ("route", "Route"),
        ("warnings", "Warnings"),
        ("stop_use", "Stop Use")
    )

    # List of keys in the Prescription data set that will be displayed in the GUI.
    PRESCRIPTION_KEYS_LIST = (
        ("brand_name", "Brand Name"),
        ("manufacturer_name", "Manufacturer Name"),
        ("generic_name", "Generic Name"),
        ("product_type", "Product Type"),
        ("description", "Description"),
        ("information_for_patients", "Information for Patients"),
        ("spl_medguide", "Medical Guide"),
        ("indications_and_usage", "Indications and Usage"),
        ("dosage_and_administration", "Dosage and Administration"),
        ("overdosage", "Overdosage"),
        ("route", "Route"),
        ("warnings_and_cautions", "Warnings and Cautions"),
        ("adverse_reactions", "Adverse Reactions"),
        ("pregnancy", "Pregnancy"),
        ("use_in_specific_populations", "Use In Specific Populations")
    )

    def __init__(self, pool, entry_list: list = None):
        self.pool = pool
        self.entry_list = entry_list


    # Method which returns the search result headers or search snippets
    def get_result_headers(self) -> list:
        headers = []
        for entry in self.entry_list:
            headers.append((entry["brand_name"], entry["manufacturer_name"], entry["product_type"]))

        return headers
    

    # The most important method in this class.
    # Takes a page number and gets the drug data for that specific set of drug entries.
    def load_page(self, entry_num: int) -> list:
        entry = self.entry_list[entry_num]
        get_value_partial = partial(Reader.get_value, entry=entry)

        if entry["product_type"] == "HUMAN OTC DRUG":
            return self.pool.starmap(get_value_partial, Reader.OTC_KEYS_LIST)
        else:
            return self.pool.starmap(get_value_partial, Reader.PRESCRIPTION_KEYS_LIST)
        

    # Static method which takes a python dict and returns the appropriate values to be used by the GUI
    @staticmethod
    def get_value(key: str, display_name: str, entry: dict) -> tuple:
        is_html = False

        if key+"_table" in entry:
            key += "_table"
            display_name += " Table"
            is_html = True
        elif key not in entry:
            return (display_name, False, False)

        val = entry[key]
        # val here can only be two types: str or list

        if type(val) == str:
            # if val is a str and it is not an html table, insert line breaks
            if val and not is_html: return (display_name, insert_linebreaks(val), False)
            else: return (display_name, val, True)
        
        # val is a list. pop items at the end if the last items are empty
        while len(val) > 1 and not val[-1]: val.pop()

        if not val: return (display_name, False, False)

        if not is_html:
            for i in range(len(val)):
                val[i] = insert_linebreaks(val[i])
        
        return (display_name, val, is_html)