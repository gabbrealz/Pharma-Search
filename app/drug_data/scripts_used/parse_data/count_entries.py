
args = ["new-data/otc-drugs.json", "new-data/prescription-drugs.json"]
total = 0

for arg in args:
    entries = 0

    with open(arg, "r", encoding="utf-8") as f:
        for line in f:
            if line[2] == "{":
                entries += 1

        total += entries
        print(f"\"{arg}\": {entries} drug entries")

print(f"Total: {total} drug entries")