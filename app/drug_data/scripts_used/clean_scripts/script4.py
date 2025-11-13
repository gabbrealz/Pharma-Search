from multiprocessing import Pool
import os
import re

# purpose: remove certain keys

pattern = re.compile(r'"(.+)": ')

keys_to_remove = {
    "boxed_warning", "laboratory_tests", "drug_interactions", "how_supplied", "package_label_principal_display_panel",
    "set_id", "id", "effective_time", "version", "application_number", "product_ndc", "rxcui", "questions", "nui", 
    "spl_id", "spl_set_id", "package_ndc", "is_original_packager", "upc", "unii", "substance_name", "references",
    "animal_pharmacology_and_or_toxicology", "original_packager_product_ndc"
}


def clean(infile, outfile):
    in_array = False

    with open(infile, "r", encoding="utf-8") as f, open(outfile, "a", encoding="utf-8") as o:
        for line in f:
            if not in_array:
                match = pattern.search(line)
                if match and match.group(1) in keys_to_remove:
                    if line[match.end()] == "[": in_array = True
                else: o.write(line)

            elif line[6] == "]": in_array = False

    print(f"Done Cleaning \"{infile}\".")



def remove(outfile):
    if os.path.exists(outfile): os.remove(outfile)

if __name__ == "__main__":
    args = [(f"new-data/drugs-{i:02d}-v4.json", f"new-data/drugs-{i:02d}-v5.json") for i in range(1,14)]

    with Pool(processes=6) as pool:
        pool.starmap(clean, args)
        # pool.map(remove, [arg[1] for arg in args])