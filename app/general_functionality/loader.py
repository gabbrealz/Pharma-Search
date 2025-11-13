from os import path
from pickle import load as load_pkl
from multiprocessing import Pool
from json import loads as load_json
from data_reader import get_drug_entry

from reader import Reader


class Loader:
    ENTRIES_PER_PAGE = 30
    DIR_PATH = path.dirname(__file__)

    def __init__(self, pool, posting_list=[]):
        self.pool = pool
        self.reader = Reader(pool)
        self.posting_list = posting_list


    def load_results(self, page_num: int = 1) -> list:
        # Step 1: Get the list of entries which corresponds to the page number
        postings = self.posting_list[(page_num-1)*Loader.ENTRIES_PER_PAGE : page_num*Loader.ENTRIES_PER_PAGE]

        # Step 2: Replace all posting[1] values with their corresponding byte positions
        postings = self.pool.starmap(Loader.get_bytepos, [(posting, Loader.DIR_PATH) for posting in postings])

        # Step 3: Take all postings and get their json string from the files
        json_strings = self.pool.map(Loader.get_drug_entry_wrapper, [(*posting, Loader.DIR_PATH) for posting in postings])

        # Step 4: Update the reader's entry list with a list of python dicts from all the json strings
        self.reader.entry_list = [load_json(json_str) for json_str in json_strings]

        # Step 5: Return the content that will be displayed in the GUI (result headers)
        return self.reader.get_result_headers()
    

    # Static method which returns the byte position of the drug entry in the json file
    @staticmethod
    def get_bytepos(postingID: tuple, path: str) -> int:
        with open(f"{path}/bytepos_files/{postingID[0]}-bytepos.pkl", "rb") as pkl:
            return postingID[0], load_pkl(pkl)[postingID[1]]
    
    # Static method which gets the json string from a file given a byte position (see cpp_files/data_reader.cpp)
    @staticmethod
    def get_drug_entry_wrapper(args):
        return get_drug_entry(*args)
    

ENTRIES_PER_PAGE = Loader.ENTRIES_PER_PAGE