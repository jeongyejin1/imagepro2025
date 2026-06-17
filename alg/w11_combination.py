# 재귀적인 조합 함수를 쉽게 이해하는 형태로 구현
# arr: 사용할 원소 리스트
# start: 이번 단계에서 선택을 시작할 인덱스 (0부터 시작함, 이전 선택의 이후 위치)
# current: 현재까지 선택한 원소들을 저장하는 리스트 (길이 r)
# depth : 현재까지 선택한 원소의 개수
# n, r: 전체 원소 개수, 뽑을 개수

def comb(arr, start, current, depth, n, r):
    # 1) 종료 조건: r개를 모두 골랐으면 하나의 조합이 완성
    if depth == r:
        print(current)
        return

    # 2) start부터 n-1까지 순서대로 선택 시도
    #    이미 확인한 인덱스에서 이전으로 돌아가지는 않기 때문에 start로 i+1을 사용하고,
    #    이에 따라 같은 조합이 중복 생성되지 않음
    for i in range(start, n):
        # (1) 현재 위치 depth에 arr[i]를 선택
        current[depth] = arr[i]
        # (2) start 증가, depth 증가하여 comb함수를 다수 호출 (다음번 원소 선택)
        comb(arr, i+1, current, depth+1, n, r)

arr = ['A', 'B', 'C', 'D', 'E', 'F']
current = [None] * 3
comb(arr, 0, current, 0, len(arr), 3 )

def comb2(arr, r):
    if r == 0:
        return [[]]

    if len(arr) < r:
        return []

    with_first = [[arr[0]] + c for c in comb2(arr[1:], r-1)]
    without_first = comb2(arr[1:], r)

    return with_first + without_first

arr = ['A', 'B', 'C', 'D']
comb_list = comb2(arr, 3)
