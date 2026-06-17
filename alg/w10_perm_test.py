# TSP 문제를 풀어보자
# A, B, C 세 개의 도시가 있다.
# 출발지점으로 들어오는 것까지 계산
# A -> B : 3
# A -> C : 5
# B -> C : 4
# B -> A : 2
# C -> A : 3
# C -> B : 6

cities = ['A', 'B', 'C']
cost = {
    ('A','B'): 3, ('A','C'): 5,
    ('B','C'): 4, ('B','A'): 2,
    ('C','A'): 3, ('C','B'): 6
}

min_cost = float('inf')
min_path = None

#다음 루틴을 작성하시오
routes = perm2(cities, 3)
for path in (routes):
    total = 0
    for i in range(len(path)-1):
        total += cost[(path[i], path[i+1])]
    total += cost[(path[-1], path[0])]
    # 아래는 최소값 업데이트 하기
    if total < min_cost:
        min_cost = total
        min_path = path
    print(path, total  )

print(f"최단 경로: {min_path}, 비용: {min_cost}")

