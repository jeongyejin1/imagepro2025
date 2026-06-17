# 두 리스트에서 중복을 포함한 교집합 구하기
# 교집합 결과를 오름차순으로 정렬하기
# sorted 함수 사용 가능, set 연산 활용할 수 없음

def intersection_naive(A, B):
    res = []
    B_copy = B[:]
    # 채워보기
    # A의 원소를 모두 순회하면서, B를 체크하는데
    # 이미 채운 원소는 마킹을 해본다.
    # for A -> for B -> if -> break
    for a in A:
        for j in range(len(B_copy)):
            print(a, B_copy[j])
            if a == B_copy[j]:
                res.append(a)
                #B_copy[j] = None
                B_copy.pop(j)
                print(f"{a} 교집합 원소 추가. B_copy는 다음과 같이 변화 {B_copy}")
                break

    res.sort()
    return res

def intersection_efficient(A, B):
    a_sorted = sorted(A)  # 4, 4, 4, 5, 9
    b_sorted = sorted(B)  # 4, 4, 8, 9, 9
    j, k = 0, 0
    res = [] 

    while j < len(a_sorted) and j < len(b_sorted):
        print(j, k, a_sorted[j], b_sorted[k])
        if a_sorted[j] == b_sorted[k]:
            res.append(a_sorted[j])
            j += 1
            k += 1
        elif a_sorted[j] < b_sorted[k]:
            j += 1
        else:
            k += 1

    return res

# 예시
A = [4, 9, 5, 4, 4]
B = [9, 4, 9, 8, 4]

#print(intersection_naive(A, B))
print(intersection_efficient(A, B))
# 결과
# 4 4 9
