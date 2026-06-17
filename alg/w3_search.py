def linear_search(arr, target):
    for j, v in enumerate(arr):
        if v == target:
            return j
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        print(left, right, mid)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
        return -1


arr = [8, 3, 7, 2, 9, 4]
print(linear_search(arr, target=7))

sorted_arr = sorted(arr)
print(sorted_arr)
print(binary_search(sorted_arr, target=7))

