from array import array
from multiprocessing import Pool, Manager, cpu_count
import pickle
import re
import os


# Exclude meaningless words
exclude = {
    # General words
    'about', 'above', 'again', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'being', 'both',
    'but', 'by', 'can', 'could', 'did', 'do', 'does', 'down', 'each', 'else', 'even', 'few', 'for', 'from', 'further',
    'had', 'has', 'have', 'here', 'in', 'is', 'it', 'its', 'may', 'might', 'more', 'most', 'must', 'no', 'nor', 'not',
    'now', 'of', 'on', 'once', 'only', 'or', 'own', 'over', 'same', 'so', 'some', 'such', 'shall', 'should', 'than',
    'that', 'the', 'then', 'there', 'these', 'they', 'this', 'to', 'too', 'under', 'up', 'very', 'was', 'were', 'will',
    'with', 'would', 'due', 'if', 'other', 'case',

    # Single letters
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',

    # CSS keywords
    'table', 'id', 'cellpadding', 'width', 'caption', 'col', 'tbody', 'tr', 'td', 'align', 'stylecode', 'valign', 
    'paragraph', 'content', 'rrule', 'botrule', 'lrule', 'toprule', 'bold', 'style', 'class', 'color', 'font', 
    'size', 'margin', 'padding', 'border', 'background',

    # Found in every drug entry
    'indications', 'usage', 'dosage', 'administration', 'forms', 'strengths', 'warnings', 'precautions', 'adverse',
    'reactions', 'uses', 'specific', 'populations', 'pregnancy', 'risk', 'summary', 'use', 'dose', 'description',
    'uses', 'clinical', 'pharmacology', 'patient', 'information', 'caused', 'drug'
}


data_files = [
    [f"../drug_data/otc_drugs/otc-{i}.json" for i in range(7)],
    [f"../drug_data/prescription_drugs/prescription-{i}.json" for i in range(9)],
]

pickle_files = [
    [f"index_files/{chr(i)}-part1.pkl" for i in range(65,91)],
    [f"index_files/{chr(i)}-part2.pkl" for i in range(65,91)],
]

one_item_pattern = re.compile(r'"(.+)": "(.+)"')
word_pattern = re.compile(r"[a-zA-Z]+")


def convert_to_tuples(pkl_file: str) -> None:
    with open(pkl_file, "rb") as pkl:
        inv_index = pickle.load(pkl)

    for token, postings in inv_index.items():
        inv_index[token] = tuple(postings)

    with open(pkl_file, "wb") as pkl:
        pickle.dump(inv_index, pkl)


def build_invertedindex_from_file(fileName: str, indexes: list) -> None:
    tokens = []
    token_freq = {}
    relevant_tokens = set()
    i = -1

    print(f"About to build inverted index for: \"{fileName}\"")

    with open(fileName, "rb") as inFile:
        next(inFile)

        for line in inFile:
            line = line.decode("utf-8")
            if len(line) < 3: break

            match = one_item_pattern.search(line)
            if match: 
                token_list = word_pattern.findall(match.group(2).lower())
                tokens.extend(token_list)

                if match.group(1) == "brand_name" or match.group(1) == "generic_name":
                    relevant_tokens.update(token_list)

            elif line[2] == "{": i += 1
                
            elif line[2] == "}":
                # exclude meaningless tokens
                tokens = [token for token in tokens if token not in exclude]

                # count token frequency
                for token in tokens:
                    frequency = 1
                    if token in relevant_tokens: frequency += 5

                    if token not in token_freq: token_freq[token] = frequency
                    else: token_freq[token] += frequency
                
                for token, freq in token_freq.items():
                    index = indexes[(0 if ord(token[1])<110 else 1)][ord(token[0])-97]

                    if token in index: index[token].extend([i, freq])
                    else: index[token] = array('H', [i, freq])
    
                tokens.clear()
                token_freq.clear()
                relevant_tokens.clear()
                
    print(f"Finished building inverted index for: \"{fileName}\"")


def update_pickle_files(locks: list, file_num: int, indexes: list) -> None:
    for i in range(len(indexes)):
        for j in range(len(indexes[i])):

            inverted_index = indexes[i][j]
            pkl_file = pickle_files[i][j]

            with locks[j]:
                if os.path.exists(pkl_file):
                    with open(pkl_file, "rb") as pkl:
                        inverted_index = pickle.load(pkl)

                    for token, arr in indexes[i][j].items():
                        if token in inverted_index: inverted_index[token].append((file_num, arr))
                        else: inverted_index[token] = [(file_num, arr)]

                else:
                    for token, arr in inverted_index.items():
                        inverted_index[token] = [(file_num, arr)]

                with open(pkl_file, "wb") as pkl:
                    pickle.dump(inverted_index, pkl)


def build_pickles_inprocess(lock, folder_num, file_num) -> None:
    indexes = [[{} for _ in range(26)], [{} for _ in range(26)]]

    curr_file = data_files[folder_num][file_num]
    file_num += folder_num*10

    build_invertedindex_from_file(curr_file, indexes)
    update_pickle_files(lock, file_num, indexes)


def build_pickles_with_indexes() -> None:
    if os.path.basename(os.getcwd()) != "inverted_index":
        raise RuntimeError("Program ran in the wrong directory, run it in \"inverted_index\" cwd")

    with Manager() as manager:
        locks = [manager.Lock() for i in range(26)]
        pool = Pool(processes=max(1,cpu_count()-2))
        args = []

        for folder_num in range(len(data_files)):
            for file_num in range(len(data_files[folder_num])):
                args.append((locks, folder_num, file_num))

        pool.starmap(build_pickles_inprocess, args)

        args = pickle_files[0].copy()
        args.extend(pickle_files[1])

        pool.map(convert_to_tuples, args)

        pool.close()
        pool.join()


def rename_pickles():
    if os.path.basename(os.getcwd()) != "inverted_index":
        raise RuntimeError("Program ran in the wrong directory, run it in \"inverted_index\" cwd")
    
    new_names = [
        [f"inverted_index/index_files/{chr(i)}-part1.pkl" for i in range(65,91)],
        [f"inverted_index/index_files/{chr(i)}-part2.pkl" for i in range(65,91)],
    ]
    
    for i in range(len(pickle_files)):
        for j in range(len(pickle_files[i])):
            pkl = pickle_files[i][j]
            if os.path.exists(pkl): os.rename(pkl, new_names[i][j])


def remove_pickles() -> None:
    if os.path.basename(os.getcwd()) != "inverted_index":
        raise RuntimeError("Program ran in the wrong directory, run it in \"inverted_index\" cwd")
    
    for pkl_list in pickle_files:
        for pkl in pkl_list:
            if os.path.exists(pkl): os.remove(pkl)



if __name__ == "__main__":
    # remove_pickles()
    # rename_pickles()
    build_pickles_with_indexes()