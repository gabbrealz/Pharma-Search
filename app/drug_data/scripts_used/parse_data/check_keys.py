from multiprocessing import Pool, cpu_count
import re

OTC_FILES = [f"otc_drugs/otc-{i}.json" for i in range(7)]
PRESCRIPTION_FILES = [f"prescription_drugs/prescription-{i}.json" for i in range(9)]

pattern = re.compile(r'"(.+)": ')

def get_key(line) -> str|bool:
    if line[4] != r'"': return False
    i = 5
    while line[i] != r'"': 
        i += 1
    return line[5:i]


def get_keys(file_name) -> set:
    key_set = set()

    with open(file_name, "r", encoding="utf-8") as f:
        next(f)

        for line in f:
            if len(line) < 3: break
            if len(line) < 6: continue
            key = pattern.search(line)
            if not key: continue
            key_set.add(key.group(1))
    
    print(f"Done getting keys for {file_name}")
    return key_set


def combine_sets(sets) -> set:
    new_set = set()
    for s in sets: new_set.update(s)
    return new_set


if __name__ == "__main__":
    with Pool(processes=cpu_count()-1) as pool:
        otc_keys = pool.map(get_keys, OTC_FILES)
        prescription_keys = pool.map(get_keys, PRESCRIPTION_FILES)

    otc_keys = combine_sets(otc_keys)
    prescription_keys = combine_sets(prescription_keys)
    
    print(f"OTC KEYS: {otc_keys}")
    print(f"PRESCRIPTION KEYS: {prescription_keys}")