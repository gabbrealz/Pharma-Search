from multiprocessing import Pool
import os
import re
from sort_funcs import merge_sort

# purpose: sort each individual file

word_pattern = re.compile(r"(?<!\()\b\w+\b(?!\))")

def clean(infile, outfile):
    entries = []
    byte_pos = 0
    brand_name = ""

    with open(infile, "rb") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            if len(line) > 20 and line[7:17] == b"brand_name":
                brand_name = word_pattern.search(line[21:].decode("utf-8")).group()

            elif line[4] == ord("}"):
                entries.append((brand_name, byte_pos))
                byte_pos = f.tell()

        merge_sort(entries, 0, len(entries)-1)

        for _, byte_pos in entries:
            f.seek(byte_pos)
            for line in f:
                o.write(line.decode("utf-8").replace("\r\n", "\n")[2:])
                if line[4] == ord("}"): break

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v5.json", f"new-data/drugs-{i:02d}-v6.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])