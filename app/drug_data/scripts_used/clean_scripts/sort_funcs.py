
# purpose: contains functions used to sort files

def compare_string(a: str, b: str) -> int:
    a, b = a.lower(), b.lower()

    i = 0
    minLen = min(len(a), len(b))
    while i < minLen and a[i] == b[i]: i += 1

    if i == minLen or ord(a[i]) == ord(b[i]): return 0
    elif ord(a[i]) > ord(b[i]): return 1
    else: return -1


def merge(arr: list, l: int, m: int, r: int) -> None:
    n1 = m-l+1
    n2 = r-m

    L = [None]*n1
    R = [None]*n2
    for i in range(n1): L[i] = arr[l+i]
    for j in range(n2): R[j] = arr[m+j+1]

    i = j = 0
    k = l

    while i < n1 and j < n2:

        if compare_string(L[i][0], R[j][0]) <= 0:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort(arr: list, l: int, r: int):
    if l >= r: return
    m = (l+r) // 2

    merge_sort(arr, l, m)
    merge_sort(arr, m+1, r)
    merge(arr, l, m, r)