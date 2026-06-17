# arr: 사용할 원소가 있는 리스트
# used: 각 인데스(i)의 원소를 순열에 사용했는지의 여부를 확인하는 리스트
# current: 특정 시점까지 순열로 선택한 원소의 리스트(길이 r)
# depth: 특정 시점까지 선택한 원소의 개수
# n: 전체 원소의 개수, r: 뽑을 개수
def perm(arr, used, current, depth, n, r):
    # 1) 종료조건: r개를 모두 골랐으면 curent를 출력
    if depth == r:
        print(current)
        return
    # 2) 모든 인덱스 i ( 0 ~ n-1)를 순회하면서 위치(depth)에 들어갈 값을 정함
    for i in range(n):
        if not used[i]:
            used[i] = True
            current[depth] = arr[i] # 가정 처음의 i=0, current = [A, None]
            #print("i = ", i, "depth =", depth, used, current)
            perm(arr, used, current, depth+1, n, r)
            used[i] = False

def perm2(arr, r):
    if r == 0:
        return [[]]
    result = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        print(rest)
        for p in perm2(rest, r-1):
            result.append([arr[i]] + p)
    return result

arr = ['A','B','C']
used = [False] * len(arr)
current = [None] * 2
perm(arr, used, current, 0, len(arr), 2)
print()
result = perm2(arr, 2)
print(result)