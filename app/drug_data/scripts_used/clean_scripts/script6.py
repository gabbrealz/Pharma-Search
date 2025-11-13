from multiprocessing import Pool
import os

# purpose: remove drug entries with no brand_name key

def clean(infile, outfile):
    line_list = []
    include = False

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            line_list.append(line)

            if line[5:15] == "brand_name": include = True
            elif line[2] == "}":
                if include: 
                    o.writelines(line_list)
                    include = False
                line_list.clear()

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v6.json", f"new-data/drugs-{i:02d}-v7.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])