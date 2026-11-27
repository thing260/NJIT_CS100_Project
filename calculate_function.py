import re


class StaticTask:
    def __init__(self, startTime, endTime, color, dayOfWeek, name="Static Task"):
        self.startTime = startTime
        self.endTime = endTime
        self.color = color
        self.dayOfWeek = dayOfWeek
        self.name = name


class DynamicTask:
    def __init__(self, duration, priority, amount, color, name="Dynamic Task"):
        self.duration = duration
        self.priority = priority
        self.amount = amount
        self.color = color
        self.name = name


class task:
    def __init__(self, startTime, endTime, color, name=""):
        self.startTime = startTime
        self.endTime = endTime
        self.color = color
        self.name = name

    def __repr__(self):
        return f"task({self.startTime}, {self.endTime}, {self.color!r}, {self.name!r})"


def parse_time_to_minutes(time_str: str):
    """Convert a 12-hour clock string (e.g. '7am', '7AM', '7:00am', '9:30 PM') to minutes (0..1439)."""
    if not isinstance(time_str, str):
        return None
    cleaned = re.sub(r"\s+", "", time_str.strip().upper())
    match = re.fullmatch(r"(1[0-2]|[1-9])(?::([0-5][0-9]))?(AM|PM)", cleaned)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    meridiem = match.group(3)

    # Convert 12AM -> 00:xx and 1PM..11PM -> 13:xx..23:xx
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:
        if hour != 12:
            hour += 12

    return hour * 60 + minute


def parse_days_of_week(days):
    """Normalize a 7-bool list/tuple (or 7-char '0'/'1' string) into a list of 7 booleans."""
    if isinstance(days, (list, tuple)) and len(days) == 7:
        if all(isinstance(d, bool) for d in days):
            return list(days)
        return None
    if isinstance(days, str) and len(days) == 7 and set(days).issubset({"0", "1"}):
        return [ch == "1" for ch in days]
    return None


def sleep_to_static_tasks(sleep_time):
    """Convert [wake_time, bed_time] into static sleep blocks across all 7 days."""
    if not isinstance(sleep_time, (list, tuple)) or len(sleep_time) != 2:
        return None

    wake_mins = parse_time_to_minutes(sleep_time[0])
    bed_mins = parse_time_to_minutes(sleep_time[1])

    # Reject invalid times or identical wake/bed times
    if wake_mins is None or bed_mins is None or wake_mins == bed_mins:
        return None

    sleep_color = "#4B0082"
    sleep_name = "Sleep"
    all_days = [True] * 7

    # Split overnight sleep across midnight into two daily spans
    if bed_mins > wake_mins:
        return [
            StaticTask(sleep_time[1], "11:59PM", sleep_color, list(all_days), sleep_name),
            StaticTask("12:00AM", sleep_time[0], sleep_color, list(all_days), sleep_name),
        ]

    return [
        StaticTask(sleep_time[1], sleep_time[0], sleep_color, list(all_days), sleep_name)
    ]


# save_file(...) and load_file(...) live as separate functions in the main file
# so calculate() stays focused on validation and in-memory scheduling.


def calculate(tasks, dynamicTasks, staticTasks, sleepTime):
    """
    Validate inputs, place static and sleep blocks, and schedule dynamic tasks
    into a 7-day list of `task(startTime, endTime, color, name)` objects.
    Returns `tasks` on success, or a descriptive failure string on invalid/impossible input.
    """
    if not isinstance(tasks, list):
        return "Failed at 'tasks' validation: expected a list."
    if not isinstance(dynamicTasks, (list, tuple)):
        return "Failed at 'dynamicTasks' validation: expected a list or tuple."
    if not isinstance(staticTasks, (list, tuple)):
        return "Failed at 'staticTasks' validation: expected a list or tuple."

    sleep_statics = sleep_to_static_tasks(sleepTime)
    if sleep_statics is None:
        return (
            f"Failed at 'sleepTime' validation: invalid sleepTime {sleepTime!r} "
            "(expected [wake_time, bed_time] with distinct valid times)."
        )

    all_statics = list(staticTasks) + sleep_statics
    num_user_statics = len(staticTasks)

    parsed_statics = []
    for idx, st in enumerate(all_statics):
        source_label = (
            f"sleep_statics[{idx - num_user_statics}]"
            if idx >= num_user_statics
            else f"staticTasks[{idx}]"
        )

        required_attrs = ("startTime", "endTime", "dayOfWeek", "color")
        if st is None or not all(hasattr(st, attr) for attr in required_attrs):
            return f"Failed at {source_label}: missing required attributes {required_attrs}."

        st_name = getattr(st, "name", None)
        if not isinstance(st_name, str) or not st_name.strip():
            st_name = "Sleep" if idx >= num_user_statics else f"Static Task {idx + 1}"

        # Treat "11:59PM" end time as end of day (1440 minutes)
        if isinstance(st.endTime, str) and re.sub(r"\s+", "", st.endTime.strip().upper()) == "11:59PM":
            end_m = 1440
        else:
            end_m = parse_time_to_minutes(st.endTime)

        start_m = parse_time_to_minutes(st.startTime)

        if start_m is None or end_m is None:
            return (
                f"Failed at {source_label} time parsing: "
                f"startTime={st.startTime!r}, endTime={st.endTime!r}."
            )
        if start_m >= end_m:
            return (
                f"Failed at {source_label} time range: "
                f"startTime ({start_m}m) must be earlier than endTime ({end_m}m)."
            )

        parsed_days = parse_days_of_week(st.dayOfWeek)
        if parsed_days is None:
            return (
                f"Failed at {source_label} dayOfWeek validation: "
                f"got {st.dayOfWeek!r} (expected 7-element list of bools)."
            )

        parsed_statics.append((start_m, end_m, st.color, parsed_days, st_name))

    for idx, dt in enumerate(dynamicTasks):
        required_dyn_attrs = ("duration", "priority", "amount", "color")
        if dt is None or not all(hasattr(dt, attr) for attr in required_dyn_attrs):
            return f"Failed at dynamicTasks[{idx}]: missing required attributes {required_dyn_attrs}."
        if isinstance(dt.duration, bool) or not isinstance(dt.duration, int) or dt.duration <= 0:
            return f"Failed at dynamicTasks[{idx}].duration: got {dt.duration!r} (expected positive int)."
        if isinstance(dt.priority, bool) or not isinstance(dt.priority, int):
            return f"Failed at dynamicTasks[{idx}].priority: got {dt.priority!r} (expected int)."
        if isinstance(dt.amount, bool) or not isinstance(dt.amount, int) or dt.amount < 0:
            return f"Failed at dynamicTasks[{idx}].amount: got {dt.amount!r} (expected non-negative int)."

    weekly_schedule = [[] for _ in range(7)]

    # Place static blocks and reject overlaps on active days
    for s_idx, (start_m, end_m, color, days, st_name) in enumerate(parsed_statics):
        for day_idx in range(7):
            if days[day_idx]:
                for existing in weekly_schedule[day_idx]:
                    if start_m < existing.endTime and end_m > existing.startTime:
                        return (
                            f"Failed placing static task '{st_name}' (#{s_idx}) on day {day_idx} "
                            f"({start_m}-{end_m}m): overlaps '{existing.name}' "
                            f"({existing.startTime}-{existing.endTime}m)."
                        )
                weekly_schedule[day_idx].append(task(start_m, end_m, color, st_name))

    for day_idx in range(7):
        weekly_schedule[day_idx].sort(key=lambda t: t.startTime)

    # Expand dynamic tasks by `amount` and schedule higher-priority (smaller number) tasks first
    sorted_dynamics = sorted(dynamicTasks, key=lambda d: d.priority)
    dynamic_instances = []
    for dt in sorted_dynamics:
        dt_name = getattr(dt, "name", None)
        if not isinstance(dt_name, str) or not dt_name.strip():
            dt_name = "Dynamic Task"
        for _ in range(dt.amount):
            dynamic_instances.append((dt, dt_name))

    for inst_idx, (dt, dt_name) in enumerate(dynamic_instances):
        placed = False
        for day_idx in range(7):
            day_tasks = weekly_schedule[day_idx]
            current_time = 0

            for existing in day_tasks:
                if existing.startTime - current_time >= dt.duration:
                    day_tasks.append(task(current_time, current_time + dt.duration, dt.color, dt_name))
                    day_tasks.sort(key=lambda t: t.startTime)
                    placed = True
                    break
                current_time = max(current_time, existing.endTime)

            if not placed and (1440 - current_time >= dt.duration):
                day_tasks.append(task(current_time, current_time + dt.duration, dt.color, dt_name))
                day_tasks.sort(key=lambda t: t.startTime)
                placed = True

            if placed:
                break

        if not placed:
            return (
                f"Failed scheduling '{dt_name}' (instance #{inst_idx}, duration={dt.duration}m, "
                f"priority={dt.priority}): no open slot across days 0..6."
            )

    # Replace caller's list contents in place with the new 7-day schedule
    tasks.clear()
    tasks.extend(weekly_schedule)
    return tasks


if __name__ == "__main__":
    # Test 1: Valid schedule with bool dayOfWeek list and named tasks
    my_tasks = [task(0, 10, "#000000", "Old Stale Task")]
    my_statics = [
        StaticTask("9:00am", "10:30AM", "#118AB2", [True, False, True, False, True, False, False], "CS100 Lecture"),
    ]
    my_dynamics = [
        DynamicTask(60, 1, 1, "#06D6A0", "Homework"),
    ]
    result_1 = calculate(my_tasks, my_dynamics, my_statics, ["7am", "11:00pm"])
    assert result_1 is my_tasks
    assert len(my_tasks) == 7
    assert any(t.name == "Homework" and t.color == "#06D6A0" for t in my_tasks[0])
    print("Test 1 passed. Monday blocks:", my_tasks[0])

    # Test 2: Junk input returns descriptive string and leaves tasks list cleared/empty
    bad_tasks = [task(0, 5, "#000000", "Temporary")]
    result_2 = calculate(bad_tasks, [DynamicTask("bad", 1, 1, "#EF476F", "Broken")], [], ["7AM", "11PM"])
    assert isinstance(result_2, str) and "dynamicTasks[0].duration" in result_2
    assert bad_tasks == [task(0, 5, "#000000", "Temporary")]
    print("Test 2 passed. Error string:", result_2)
