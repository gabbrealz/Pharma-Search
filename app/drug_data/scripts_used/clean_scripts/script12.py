from multiprocessing import Pool
import os

# purpose: removing drug entries that have duplicate keys


def clean(infile, outfile):
    line_list = []
    route_found = False
    include = True

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        next(f)

        for line in f:
            if len(line) < 3: break

            line_list.append(line)

            if line.find(r'"route":') != -1:
                if route_found: include = False
                else: route_found = True

            elif line[2] == "}":
                if include: o.writelines(line_list)
                include = True
                route_found = False
                line_list.clear()

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/otc-{i}-v1.json", f"new-data/otc-{i}-v2.json") for i in range(7)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[0] for arg in args])