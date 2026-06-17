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
def comb2(arr, r):
    if r == 0:
        return [[]]

    if len(arr) < r:
        return []

    with_first = [[arr[0]] + c for c in comb2(arr[1:], r-1)]
    without_first = comb2(arr[1:], r)

    return with_first + without_first

# 문제 1 : 인접 차이의 합이 가장 큰 순열 찾기
# num = [1,4,6]
# [1, 4, 6] = |1 - 4| + |4- 6| = 5
# [1, 6, 4] = |1 - 6| + |6 - 4| = 7
# [4, 1, 6]
nums = [1,4,6]
all_perm = num (num(len(nums)))
print(all_perm)

def diff_sum(seq):
    for j in range(len(seq)-1):
        total += abs(seq[j] - seq[j+1])
    return total

max_val = 0
result = []

for seq in all_perm:
    diffsum = diff_sum(seq)
    if diffsum > max_val:
        max_val = diffsum
        resulta.append(seq)
    elif diffsum == max_val:
        result.append(seq)

print("최대값: ", max_val)
print("해당순열:" , result)

# 문제 2 : 블랙잭에 가까운 조합 만들기
# card = [5,6,7,8,9]
# card에서 3장을 뽑았을 때 합이 21인 조합을 모두 구하시오
card = [5,6,7,8,9]
M = 21

all_comb = comb2(card, 3)
print(all_comb)

result = []

for comb in all_comb:
    cardsum = sum(comb)
    if cardsum ==M:
        result.append(comb)

print("합이 21인 card의 조합:", result)
