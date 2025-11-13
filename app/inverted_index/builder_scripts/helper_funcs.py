import pickle
from pympler import asizeof


def count_index_lengths() -> None:
    for i in range(65,91):
        file_name = f"index-files/{chr(i)}.pkl"

        with open(file_name, "rb") as f:
            inverted_index = pickle.load(f)

        print(f"\"{file_name}\" size = {len(inverted_index):,}")


def get_index_memusage() -> None:
    total = 0

    for i in range(65,91):
        file_name = f"index_files/{chr(i)}.pkl"

        with open(file_name, "rb") as f:
            inverted_index = pickle.load(f)
        
        memory_usage = asizeof.asizeof(inverted_index)
        total += memory_usage

        print(f"\"{file_name}\" dict memory usage = {memory_usage/1048576:.2f} MB")

    print(f"Total memory: {total/1048576:.2f} MB")


if __name__ == "__main__":
    get_index_memusage()