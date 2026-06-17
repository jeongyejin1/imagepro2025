def solution(schedules, timelog, startday):
    def add_10_minutes(time):
        hour = time // 100 # 시각
        minute = time % 100 # 분
        minute += 10
        if minute >= 60:
            hour += 1
            minute -= 60
        return hour*100 + minute
    answer = 0
    n = len(schedules)
    # day_of_week[0]: 1일차의 요일
    day_of_week = []
    for day_index in range(7): # 0~6까지 순회하는 루프
        # - day_index 0: startday = 5 -> (5 - 1 + day_index) % 7 + 1
        weekday = (startday - 1 + day_index) % 7 + 1
        day_of_week.append(weekday)
    for j in range(n):
        wish_time = schedules[j]
        deadline = add_10_minutes(wish_time)
        on_time_all_weekdays = True
        for day