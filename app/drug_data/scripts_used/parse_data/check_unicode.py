from multiprocessing import Pool
import regex


DATA = [
    [f"drug_data/otc_drugs/otc-{i}.json" for i in range(7)],
    [f"drug_data/prescription_drugs/prescription-{i}.json" for i in range(9)],
]

unicode_pattern = regex.compile(r"[\p{S}\p{P}]")

def get_unicode_inprocess(file_name: str) -> set:
    symbols_found = set()

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.encode('utf-8').decode('unicode_escape')
            symbols_found.update(unicode_pattern.findall(line))

    return symbols_found


if __name__ == "__main__":
    args = DATA[0].copy()
    args.extend(DATA[1])

    with Pool(processes=6) as pool:
        unicode_sets = pool.map(get_unicode_inprocess, args)
    
    all_unicode_chars = set()

    for unicode_set in unicode_sets: 
        all_unicode_chars.update(unicode_set)

    print(all_unicode_chars)
                    