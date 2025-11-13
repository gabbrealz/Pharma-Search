from multiprocessing import Pool
import os

# purpose: removing the extra commas at the end of arrays


def clean(infile, outfile):
    line_list = []

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            line_list.append(line)

            if line[2] == "}":
                if line_list[-2][-2] == ",":
                    line_list[-2] = f"    {line_list[-2].strip()[:-1]}\n"

                o.writelines(line_list)
                line_list.clear()

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/otc-{i}.json", f"new-data/otc-{i}-v1.json") for i in range(7)]
    args.extend([(f"new-data/prescription-{i}.json", f"new-data/prescription-{i}-v1.json") for i in range(9)])

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[0] for arg in args])