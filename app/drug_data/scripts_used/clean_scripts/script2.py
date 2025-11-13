from multiprocessing import Pool
import os
import re

# purpose: turning values that are one-item arrays into just the values

pattern = re.compile(r'".+": \[')

def clean(infile, outfile):
    content = ""
    next_after_content = ""

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            match = pattern.search(line)

            if not match: o.write(line)
            else:
                content = f.readline()
                next_after_content = f.readline()

                # if next_after_content[6] == "]":
                if next_after_content[8] == "]":
                    o.write(line[:match.end()-1]+content.strip()+",\n")
                else:
                    o.writelines([line, content, next_after_content])

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v2.json", f"new-data/drugs-{i:02d}-v3.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])