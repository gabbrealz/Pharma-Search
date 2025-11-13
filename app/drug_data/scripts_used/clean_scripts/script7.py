from multiprocessing import Pool
import os

# purpose: remove drug entries with mostly empty values ("")

def clean(infile, outfile):
    line_list = []
    lines = -1
    empty_vals = 0

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            line_list.append(line)

            if line.find(r'""') != -1: empty_vals += 1
            elif line[2] == "}":
                if empty_vals/lines < 0.48: o.writelines(line_list)

                lines = -1
                empty_vals = 0
                line_list.clear()

            lines += 1

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v7.json", f"new-data/drugs-{i:02d}-v8.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])