from os import path
from pickle import load as load_pkl
from functools import partial
from array import array
from enum import Enum
import re

import parser


# ProdFilter enum used to set drug product type constants
class ProdFilter(Enum):
    ALL = (0,18)
    OTC = (0,6)
    PRESCRIPTION = (10,18)


# This class is responsible for all searching operations.
#   This class uses an inverted index to return the top 300
#   search results from a query
class Searcher:
    
    # Set query word limit to 16 to keep time efficiency
    QUERY_WORD_lIMIT = 16
    # Get the path to this python file's directory
    #   - So that file handling is not dependent on the user's current working directory
    DIR_PATH = path.dirname(__file__)
    # Regex pattern used to tokenize the query
    token_pattern = re.compile(r"\b[a-zA-Z]{2,}\b")

    def __init__(self, pool, prod_filter: ProdFilter = ProdFilter.ALL):
        self.pool = pool
        self.prod_filter = prod_filter
    

    # This is the class' only relevant function. Takes a query and returns the top 300 relevant results
    def search(self, query: str) -> list:
        # Step 1: Tokenize the query using regex, keep the token list size <= the word limit
        tokens = Searcher.token_pattern.findall(query.lower())
        del tokens[Searcher.QUERY_WORD_lIMIT:]

        # Step 2: Get the list of postings for each token
        partial_get_postings = partial(Searcher.get_postings, prod_filter=self.prod_filter, path=Searcher.DIR_PATH)
        postings = self.pool.map(partial_get_postings, tokens)

        # Step 3: Get the list of inverse document frequencies (IDF) for each token
        partial_get_tokenIDF = partial(Searcher.get_tokenIDF, path=Searcher.DIR_PATH)
        tokenIDF_list = self.pool.map(partial_get_tokenIDF, tokens)

        # Step 4: Remove token entries that have 0 postings
        i = 0
        while i < len(postings):
            if postings[i]: i += 1
            else:
                tokenIDF_list.pop(i)
                tokens.pop(i)
                postings.pop(i)

        # Step 5: Get a list of dictionaries, each containing the scores of each posting for each token
        scoring_args = [(postings[i], tokenIDF_list[i]) for i in range(len(postings))]
        posting_scores = self.pool.map(Searcher.score_postinglists_wrapper, scoring_args)

        # Step 6: Give a score to each drug entry. Return only the top 300 results (see cpp_files/parser.cpp)
        return parser.get_topscoring_results(posting_scores)
    
        # parser.get_topscoring_results functionality:
        #   1. Merge the list of dicts from step 5, similar keys will have their values added.
        #       Purpose: If the same posting appears in different tokens, their scores will be added.
        #   2. Then, push each key-value pair into a min heap.
        #       Purpose: A min heap is used to easily remove the least relevant result
        #   3. Keep the heap size <= 300
        #   4. Return the heap in reverse order so that relevant results are at the front.


    # This static method returns the list of postings paired with their scores. (see cpp_files/parser.cpp)
    @staticmethod
    def score_postinglists_wrapper(args):
        return parser.score_postinglists(*args)


    # This static method gets the filtered postings from each token
    @staticmethod
    def get_postings(token: str, prod_filter: ProdFilter, path: str) -> list:
        # Takes a token, and returns its value in the appropriate inverted index
        # Filters the result based on the product type filter the user has enabled
        
        with open(f"{path}/index_files/{token[0].upper()}-part{1 if ord(token[1])<110 else 2}.pkl", "rb") as pkl:
            inverted_index = load_pkl(pkl)

        token = token.lower()
        if token not in inverted_index: return []

        postings = inverted_index[token]
        if prod_filter == ProdFilter.ALL: return postings

        min_range, max_range = prod_filter.value
        return [posting for posting in postings if posting[0] >= min_range and posting[0] <= max_range]


    # This static method gets the token's IDF (Inverse Document Frequency)
    @staticmethod
    def get_tokenIDF(token: str, path: str) -> int:
        with open(f"{path}/idf_files/{token[0].upper()}-IDF.pkl", "rb") as pkl:
            idf = load_pkl(pkl)

        if token in idf: return idf[token]
        return 0