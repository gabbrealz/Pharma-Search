from multiprocessing import Pool
import os

# purpose: filter drug entries based on product type

def get_prodtype(line) -> str:
    i = 21
    while line[i] != r'"': i += 1
    return line[21:i]

def clean(outf, type_to_search: str, not_counted_as_others) -> tuple:
    others = []
    line_list = []
    prod_type = ""

    with open("new-data/drugs-all.json", "r", encoding="utf-8") as f, open(outf, "a", encoding="utf-8") as o:
        for line in f:
            line_list.append(line)

            if line[5:17] == "product_type": prod_type = get_prodtype(line)
            elif line[2] == "}":
                if prod_type == type_to_search: 
                    o.writelines(line_list)
                elif prod_type != not_counted_as_others:
                    others.append(line_list.copy())

                line_list.clear()

    print(f"Done writing to \"{outf}\".")
    return others



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [
        ("new-data/otc-drugs.json", "HUMAN OTC DRUG", "HUMAN PRESCRIPTION DRUG"),
        ("new-data/prescription-drugs.json", "HUMAN PRESCRIPTION DRUG", "HUMAN OTC DRUG")
    ]

    with Pool(processes=4) as pool:
        others = pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])

    with open("new-data/other-drugs.json", "a", encoding="utf-8") as o:
        for line_list in others[0]:
            o.writelines(line_list)