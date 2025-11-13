from math import log
from multiprocessing import cpu_count, Pool, Manager
import pickle
import re
import os


# Exclude meaningless words
exclude = {
    # General words
    'a', 'about', 'above', 'again', 'all', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'been', 'being', 'both',
    'but', 'by', 'can', 'could', 'did', 'do', 'does', 'down', 'each', 'else', 'even', 'few', 'for', 'from', 'further',
    'had', 'has', 'have', 'here', 'in', 'is', 'it', 'its', 'may', 'might', 'more', 'most', 'must', 'no', 'nor', 'not',
    'now', 'of', 'on', 'once', 'only', 'or', 'own', 'over', 'same', 'so', 'some', 'such', 'shall', 'should', 'than',
    'that', 'the', 'then', 'there', 'these', 'they', 'this', 'to', 'too', 'under', 'up', 'very', 'was', 'were', 'will',
    'with', 'would', 'due', 'if', 'other', 'case',

    # CSS keywords
    'table', 'id', 'cellpadding', 'width', 'caption', 'col', 'tbody', 'tr', 'td', 'align', 'stylecode', 'valign', 
    'paragraph', 'content', 'rrule', 'botrule', 'lrule', 'toprule', 'bold', 'style', 'class', 'color', 'font', 
    'size', 'margin', 'padding', 'border', 'background',

    # Found in every drug entry
    'indications', 'usage', 'dosage', 'administration', 'forms', 'strengths', 'warnings', 'precautions', 'adverse',
    'reactions', 'uses', 'specific', 'populations', 'pregnancy', 'risk', 'summary', 'use', 'dose', 'description',
    'uses', 'clinical', 'pharmacology', 'patient', 'information', 'caused', 'drug'
}


N = 82800


data_files = [
    [f"../drug_data/otc_drugs/otc-{i}.json" for i in range(7)],
    [f"../drug_data/prescription_drugs/prescription-{i}.json" for i in range(9)]
]

pickle_files = [f"idf_files/{chr(i)}-IDF.pkl" for i in range(65,91)]

one_item_pattern = re.compile(r'".+": "(.+)"')
word_pattern = re.compile(r"[a-zA-Z]+")


def build_idf_from_file(fileName: str, idfs: list) -> None:
    tokens = set()

    with open(fileName, "r") as inFile:
        next(inFile)

        for line in inFile:
            if len(line) < 3: break

            match = one_item_pattern.search(line)
            if match: tokens.update(word_pattern.findall(match.group(1).lower()))

            if line[2] == "}":
                tokens.difference_update(exclude)
                for token in tokens: 
                    idfs[ord(token[0])-97].append(token)

    print(f"Finished building IDF for file: {fileName}")


def update_pickle_files(locks: list, idfs: list) -> None:
    for i in range(len(idfs)):
        idf = idfs[i]

        with locks[i]:
            if os.path.exists(pickle_files[i]):
                with open(pickle_files[i], "rb") as pkl:
                    idf = pickle.load(pkl)

                for token in idfs[i]:
                    if token in idf: idf[token] += 1
                    else: idf[token] = 1
            
            else:
                idf = {token: 1 for token in idf}

            with open(pickle_files[i], "wb") as pkl:
                pickle.dump(idf, pkl)


def build_idf_inprocess(locks, curr_file):
    idfs = [[] for _ in range(26)]

    build_idf_from_file(curr_file, idfs)
    update_pickle_files(locks, idfs)
    print(f"Finished pickling IDF for {curr_file}")


def compute_IDF(pkl_file):
    with open(pkl_file, "rb") as pkl:
        idf = pickle.load(pkl)

    for token, freq in idf.items():
        idf[token] = log(N/freq)

    with open(pkl_file, "wb") as pkl:
        pickle.dump(idf, pkl)    


def build_pickles_with_idf() -> None:
    if os.path.basename(os.getcwd()) != "inverted_index":
        raise RuntimeError("Program ran in the wrong directory, run it in \"inverted_index\" cwd")
    
    with Manager() as manager: 
        locks = [manager.Lock() for i in range(26)]
        pool = Pool(processes=max(1,cpu_count()-2))

        args = []
        for folder_num in range(len(data_files)):
            for file_num in range(len(data_files[folder_num])):
                args.append(data_files[folder_num][file_num])

        pool.starmap(build_idf_inprocess, [(locks, arg) for arg in args])
        pool.map(compute_IDF, pickle_files)

        pool.close()
        pool.join()


def remove_pickles() -> None:
    if os.path.basename(os.getcwd()) != "inverted_index":
        raise RuntimeError("Program ran in the wrong directory, run it in \"inverted_index\" cwd")
    
    for f in pickle_files:
        if os.path.exists(f): os.remove(f)



if __name__ == "__main__":
    # remove_pickles()
    build_pickles_with_idf()