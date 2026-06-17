# quick sort 알고리즘 작성하기 시험문제 출제
def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [ x for x in arr[1:] if x > pivot]

    # print (pivot, left, right)
    return quick_sort(left) + [pivot] +