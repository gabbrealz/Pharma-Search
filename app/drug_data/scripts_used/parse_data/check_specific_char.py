from multiprocessing import Pool
import regex


DATA = [
    [f"drug_data/otc-drugs/otc-{i}.json" for i in range(5)],
    [f"drug_data/prescription-drugs/prescription-{i}.json" for i in range(5)],
    ["drug_data/other-drugs/other-0.json"]
]

unicode_pattern = regex.compile(r"[\p{S}\p{P}]")


def get_unicode_inprocess(file_name: str) -> set:
    lines = 0

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.encode('utf-8').decode('unicode_escape')
            lines += 1

            if line.find("▆") != -1: print(f"\"{file_name}\" at line {lines}:  {line}")



if __name__ == "__main__":
    args = DATA[0].copy()
    args.extend(DATA[1])
    args.extend(DATA[2])

    for arg in args:
        get_unicode_inprocess(arg)