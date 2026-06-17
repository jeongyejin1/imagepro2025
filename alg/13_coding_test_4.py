def solution(players, m, k):
    answer = 0
    # 운영 중인 서버
    active = []

    for time in range(24):
        # 만료된 서버는 제거
        alive = []
        for end_time in active:
            if end_time > time:
                alive.append(end_time)
        active = alive
        users = players[time]
        needed = users // m

        current = len(active)
        if needed > current:
            add = needed - current
            answer += add

            for _ in range(add):
                active.append(time+k)
        print(time, alive, active)

    return answer

players = [0, 2, 3, 3, 1, 2, 0, 0, 0, 0, 4, 2, 0, 6, 0, 4, 2, 13, 3, 5, 10,0, 1, 5]
m = 3
k = 5

print(solution(players, m, k))