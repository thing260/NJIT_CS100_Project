import re

def parse_time_to_minutes(time_str: str):

    if not isinstance(time_str, str):
        return None
    time_str = time_str.strip().upper()
    match = re.fullmatch(r"(1[0-2]|[1-9])(?::([0-5][0-9]))?(AM|PM)", time_str)
    if not match:
        return None
    
    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    meridiem = match.group(3)
    
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:  
        if hour != 12:
            hour += 12
            
    return hour * 60 + minute


def sleep_to_static_tasks(sleep_time: list):

    if not isinstance(sleep_time, list) or len(sleep_time) != 2:
        return None
    
    wake_mins = parse_time_to_minutes(sleep_time[0])
    bed_mins = parse_time_to_minutes(sleep_time[1])
    
    if wake_mins is None or bed_mins is None or wake_mins == bed_mins:
        return None
    
    sleep_color = "#4B0082"  
    
    if bed_mins > wake_mins:
        return [
            StaticTask(sleep_time[1], "11:59PM", sleep_color, "1111111"),
            StaticTask("12:00AM", sleep_time[0], sleep_color, "1111111")
        ]
    else:
        return [
            StaticTask(sleep_time[1], sleep_time[0], sleep_color, "1111111")
        ]


def calculate(tasks, dynamicTasks, staticTasks, sleepTime):
    """
    Validates inputs, places static/sleep tasks, and schedules dynamic tasks
    into a 7-day list of `task` objects. Returns None if invalid/impossible.
    """
    sleep_statics = sleep_to_static_tasks(sleepTime)
    if sleep_statics is None:
        return None

    all_statics = list(staticTasks) + sleep_statics

    parsed_statics = []
    for st in all_statics:
        if st.endTime.strip().upper() == "11:59PM":
            end_m = 1440
        else:
            end_m = parse_time_to_minutes(st.endTime)
            
        start_m = parse_time_to_minutes(st.startTime)
        
        if start_m is None or end_m is None or start_m >= end_m:
            return None
        if not isinstance(st.dayOfWeek, str) or len(st.dayOfWeek) != 7 or not set(st.dayOfWeek).issubset({"0", "1"}):
            return None
            
        parsed_statics.append((start_m, end_m, st.color, st.dayOfWeek))

    for dt in dynamicTasks:
        if not isinstance(dt.duration, int) or dt.duration <= 0:
            return None
        if not isinstance(dt.priority, int):
            return None
        if not isinstance(dt.amount, int) or dt.amount < 0:
            return None

    weekly_schedule = [[] for _ in range(7)]

    for start_m, end_m, color, days in parsed_statics:
        for day_idx in range(7):
            if days[day_idx] == "1":
                for existing in weekly_schedule[day_idx]:
                    if start_m < existing.endTime and end_m > existing.startTime:
                        return None  
                weekly_schedule[day_idx].append(task(start_m, end_m, color))

    for day_idx in range(7):
        weekly_schedule[day_idx].sort(key=lambda t: t.startTime)

    sorted_dynamics = sorted(dynamicTasks, key=lambda d: d.priority)
    dynamic_instances = []
    for dt in sorted_dynamics:
        for _ in range(dt.amount):
            dynamic_instances.append(dt)

    day_search_order = [0, 1, 2, 3, 4, 5, 6]

    for dt in dynamic_instances:
        placed = False
        for day_idx in day_search_order:
            day_tasks = weekly_schedule[day_idx]
            current_time = 0
            
            for existing in day_tasks:
                if existing.startTime - current_time >= dt.duration:
                    day_tasks.append(task(current_time, current_time + dt.duration, dt.color))
                    day_tasks.sort(key=lambda t: t.startTime)
                    placed = True
                    break
                current_time = max(current_time, existing.endTime)
                
            if not placed and (1440 - current_time >= dt.duration):
                day_tasks.append(task(current_time, current_time + dt.duration, dt.color))
                day_tasks.sort(key=lambda t: t.startTime)
                placed = True
                
            if placed:
                break
                
        if not placed:
            return None  

    tasks.clear()
    tasks.extend(weekly_schedule)
    return tasks
