def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    comps = 0 # 비교횟수
    swaps = 0 # 얼마나 많이 버블로 스왑 했는지

    for end in range(n-1, 0, -1):
        swapped = False # 실제로 swap이 일어났는지 여부를 판단

        for j in range(end):
            comps += 1
            if a[j] > a[j+1]: #동일값은 교환하지 않음
                a[j], a[j+1] = a[j+1], a[j]
                print(swaps +1, a)
                swaps += 1
                swapped = True

        if not swapped:
            break

    return a, comps, swaps

def selection_sort(arr):
    a = arr[:]
    n = len(a)
    comps = 0
    swaps = 0

    for j in range(n-1):
        min_pos = j
        for k in range(j+1, n):
            comps += 1
            if a[k] < a[min_pos]:
                min_pos = k
        if min_pos != j:
            a[j], a[min_pos] = a[min_pos], a[j]
            swaps += 1

    return a, comps, swaps

def insertion_sort(arr):
    a = arr[:]
    n = len(a)
    comps = 0
    shifts = 0 # 원소를 오른쪽으로 민 횟수

    for j in range(1, n):
        key = a[j]
        k = j-1 #key값 보다 큰 값을 오른쪽으로 밀기

        while k >= 0:
            comps += 1
            print(comps, a)
            if a[k] > key:
                a[k+1] = a[k]
                shifts += 1
                k -= 1
            else:
                break
        a[k+1] = key

    return a, comps, shifts

arr = [1, 10, 8, 2, 4]
sorted_arr, comps, swaps = bubble_sort(arr)
print("버블정렬: " ,sorted_arr, comps, swaps)
sorted_arr, comps, swaps = selection_sort(arr)
print("선택정렬: " ,sorted_arr, comps, swaps)
sorted_arr, comps, shifts = insertion_sort(arr)
print("삽입정렬: ", sorted_arr, comps, shifts)

