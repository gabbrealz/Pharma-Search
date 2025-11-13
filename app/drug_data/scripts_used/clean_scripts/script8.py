from multiprocessing import Pool
import os
import re
from sort_funcs import compare_string

# purpose: merge sorted individual files into one file

word_pattern = re.compile(r"(?<!\()\b\w+\b(?!\))")


def get_next_entry(f, lines_processed, index) -> tuple:
    lines = []
    brand_name = ""

    for line in f:
        lines_processed[index] += 1
        lines.append(line)
        if line[2] == "}": break
        if len(line) > 18 and line[5:15] == "brand_name": 
            brand_name = word_pattern.search(line[19:]).group()

    if not brand_name:
        print(f, ": ", lines_processed[index])
        
    return lines, brand_name


def clean(in1, in2, outf):
    lines_processed = [0,0]

    with open(in1, "r", encoding="utf-8") as i1, open(in2, "r", encoding="utf-8") as i2, open(outf, "a", encoding="utf-8") as o:
        entry1 = get_next_entry(i1, lines_processed, 0)
        entry2 = get_next_entry(i2, lines_processed, 1)

        while entry1[1] and entry2[1]:
            if compare_string(entry1[1], entry2[1]) <= 0:
                o.writelines(entry1[0])
                entry1 = get_next_entry(i1, lines_processed, 0)
            else:
                o.writelines(entry2[0])
                entry2 = get_next_entry(i2, lines_processed, 1)
        while entry1[1]:
            o.writelines(entry1[0])
            entry1 = get_next_entry(i1, lines_processed, 0)
        while entry2[1]:
            o.writelines(entry2[0])
            entry2 = get_next_entry(i2, lines_processed, 1)

    print(f"\nDone Merging \"{in1}\" and \"{in2}\".\n")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    merge1_args = [(f"new-data/drugs-{i:02d}-v8.json", f"new-data/drugs-{i+1:02d}-v8.json", f"new-data/drugs-merge1-{i:02d}.json") for i in range(1,13,2)]
    merge2_args = [(f"new-data/drugs-merge1-{i:02d}.json", f"new-data/drugs-merge1-{i+2:02d}.json", f"new-data/drugs-merge2-{i:02d}.json") for i in range(1,13,4)]
    merge3_args = [("new-data/drugs-merge2-01.json", "new-data/drugs-merge2-05.json", "new-data/drugs-merge3-01.json"),
                   ("new-data/drugs-merge2-09.json", "new-data/drugs-13-v8.json", "new-data/drugs-merge3-02.json")]
    merge4_args = ["new-data/drugs-merge3-01.json", "new-data/drugs-merge3-02.json", "new-data/drugs-all.json"]

    with Pool(processes=6) as pool:
        pool.starmap(clean, merge1_args)
        pool.starmap(clean, merge2_args)
        pool.starmap(clean, merge3_args)
        # pool.map(remove, [arg[2] for arg in merge1_args])
        # pool.map(remove, [arg[2] for arg in merge2_args])
        # pool.map(remove, [arg[2] for arg in merge3_args])

    # clean(*merge4_args)