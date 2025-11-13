from array import array
from multiprocessing import Pool, cpu_count
import pickle
import os


data_files = [
    [f"../drug_data/otc_drugs/otc-{i}.json" for i in range(7)],
    [f"../drug_data/prescription_drugs/prescription-{i}.json" for i in range(9)]
]

out_files = [
    [f"bytepos_files/{i}-bytepos.pkl" for i in range(7)],
    [f"bytepos_files/{i}-bytepos.pkl" for i in range(10,19)]
]


def build_bytepos_from_file(fileName: str, outFile: str) -> None:

    bytepos_lst = array('I')

    with open(fileName, "rb") as inFile:
        next(inFile)
        bytepos = inFile.tell()

        for line in inFile:
            line = line.decode("utf-8", errors="replace")
            if len(line) < 3: break

            if line[2] == "{": bytepos_lst.append(bytepos)
            bytepos = inFile.tell()

    with open(outFile, "wb") as outf:
        pickle.dump(bytepos_lst, outf)


def build_pickles_with_bytepos() -> None:
    if os.path.basename(os.getcwd()) != "general_functionality":
        raise RuntimeError("Program ran in the wrong directory, run it in \"general_functionality\" cwd")
    
    pool = Pool(processes=max(1,cpu_count()-2))

    args = [(data_files[0][i], out_files[0][i]) for i in range(7)]
    args.extend([(data_files[1][i], out_files[1][i]) for i in range(9)])

    pool.starmap(build_bytepos_from_file, args)

    pool.close()
    pool.join()



if __name__ == "__main__":
    build_pickles_with_bytepos()