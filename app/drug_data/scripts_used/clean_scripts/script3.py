from multiprocessing import Pool
import os

# purpose: removing the "openfda" key, but keeping the values nested under it


def clean(infile, outfile):
    is_openfda = False

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            if not is_openfda:
                if line.find("\"openfda\":") == -1: o.write(line)
                else: is_openfda = True
            else:
                if line[6] != "}": o.write(line[2:])
                else: is_openfda = False

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v3.json", f"new-data/drugs-{i:02d}-v4.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])