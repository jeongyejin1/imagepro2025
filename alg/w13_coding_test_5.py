def solution(info, n, m):
    # B의 흔적이 m 미만일 때, 최소가가 되는 A의 흔적의 수를 구하는 것이 목표
    # dp[b] --> 길이가 m이고 인덱스가 B 훔친 흔적의 수로 생각한다면,
    #           이것을 A가 갖는 최소 흔적수로 지정한다면 문제를 해결할 수 있음
    # dp[0] = 5, B의 흔적의 합이 0일 때 A의 흔적의 합을 5까지 줄일 수 있다.
    # dp[0] --> B가 하나도 훔치지 않았다. --> 모두 A가 훔쳤다. dp[0] = 5
    # dp[3] --> B가 훔친 물건들의 흔적의 합이 3, A의 흔적의 합은 3 dp[3] = 3
    # dp[x] >= n 이상인 경우에는 A가 경찰에 잡힌다.. 모든 dp가 n 이상이면 훔칠수 없다 -1 리턴
    dp = [n] * m
    dp[0] = 0

    for i in range(len(info)):
        a_trace = info[i][0]
        b_trace = info[i][1]

        new_dp = [n] * m

        for b_sum in range(m):
            if dp[b_sum] ==n:
                continue

            # 1) 이번 물건을 A가 훔치는 경우
            # - B의 흔적의 합은 그대로 b_sum
            # - A의 흔적의 합은 DP[b_sum] + a_trace
            new_a_sum = dp[b_sum] + a_trace

            if new_a_sum < n:
                if new_a_sum < new_dp[b_sum]:
                    new_dp[b_sum] = new_a_sum

            # 2) 이번 물건을 B가 훔치는 경우
            new_b_sum = b_sum + b_trace
            if new_b_sum < m:
                if dp[b_sum] < new_dp[b_sum]:
                    new_dp[new_b_sum] = dp[b_sum]
        dp = new_dp

    answer = n
    for b_sum in range(m):
        if dp[b_sum] < answer:
            answer = dp[b_sum]

    if answer == n:
        return - 1
    else:
        return answer

info = [[1, 2], [2, 3], [2, 1]]
n = 4
m = 4
result = 2
print(solution(info, n, m))