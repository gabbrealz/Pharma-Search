from multiprocessing import Pool
import os

# purpose: remove drug entries which have an empty "openfda" key


def clean(infile, outfile):
    line_list = []
    include = True

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            line_list.append(line)

            if line.find(r'"openfda": {}') != -1:
                include = False

            elif line[4] == "}":
                if include: o.writelines(line_list)
                else: include = True
                line_list.clear()

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)


if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}.json", f"new-data/drugs-{i:02d}-v1.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[0] for arg in args])