from multiprocessing import Pool
import os

# purpose: remove drug entries with mostly empty values ("")


def clean(infile, file_path_prefix, entries_per_f):
    line_list = []
    file_num = 0
    done = False

    with open(infile, "r", encoding="utf-8") as f:
        while not done:
            outf = f"{file_path_prefix}{file_num}.json"
            file_num += 1

            entries = 0
            done = True

            with open(outf, "a", encoding="utf-8") as o:
                for line in f:
                    line_list.append(line)
        
                    if line[2] == "}":
                        o.writelines(line_list)
                        line_list.clear()
                        entries += 1

                        if entries >= entries_per_f:
                            done = False
                            break

    print(f"Done splitting \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [
        ("new-data/otc-drugs.json", "new-data/otc-", 7000),
        ("new-data/prescription-drugs.json", "new-data/prescription-", 4000)
    ]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])