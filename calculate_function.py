import re


def parse_time_to_minutes(time_str: str):
    """Convert a 12-hour clock string (e.g. '9:30AM', '12PM') into minutes since 12:00AM (0..1439)."""
    if not isinstance(time_str, str):
        return None
    cleaned = time_str.strip().upper()
    match = re.fullmatch(r"(1[0-2]|[1-9])(?::([0-5][0-9]))?(AM|PM)", cleaned)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    meridiem = match.group(3)

    # Convert 12AM to 00:xx and 1PM..11PM to 13:xx..23:xx
    if meridiem == "AM":
        if hour == 12:
            hour = 0
    else:
        if hour != 12:
            hour += 12

    return hour * 60 + minute


def sleep_to_static_tasks(sleep_time):
    """Convert [wake_time, bed_time] into one or two overnight static sleep blocks."""
    if not isinstance(sleep_time, list) or len(sleep_time) != 2:
        return None

    wake_mins = parse_time_to_minutes(sleep_time[0])
    bed_mins = parse_time_to_minutes(sleep_time[1])

    # Reject invalid times or zero-length sleep windows
    if wake_mins is None or bed_mins is None or wake_mins == bed_mins:
        return None

    sleep_color = "#4B0082"

    # Split overnight sleep across midnight into two day blocks
    if bed_mins > wake_mins:
        return [
            StaticTask(sleep_time[1], "11:59PM", sleep_color, "1111111"),
            StaticTask("12:00AM", sleep_time[0], sleep_color, "1111111"),
        ]

    # Same-day sleep span (e.g. waking later than bedtime on the same 24h scale)
    return [
        StaticTask(sleep_time[1], sleep_time[0], sleep_color, "1111111")
    ]


# save_file(...) and load_file(...) live as separate functions in the main file
# so calculate() stays focused on validation and in-memory scheduling.


def calculate(tasks, dynamicTasks, staticTasks, sleepTime):
    """
    Validate inputs, place static and sleep blocks, and schedule dynamic tasks
    across a 7-day list of `task` objects.
    Returns `tasks` on success, or a descriptive failure string on invalid/impossible input.
    """
    # Validate top-level container types
    if not isinstance(tasks, list):
        return "Failed at 'tasks' validation: expected a list."
    if not isinstance(dynamicTasks, (list, tuple)):
        return "Failed at 'dynamicTasks' validation: expected a list or tuple."
    if not isinstance(staticTasks, (list, tuple)):
        return "Failed at 'staticTasks' validation: expected a list or tuple."

    # Build and validate static blocks from sleepTime first
    sleep_statics = sleep_to_static_tasks(sleepTime)
    if sleep_statics is None:
        return (
            f"Failed at 'sleepTime' validation: invalid sleepTime {sleepTime!r} "
            "(expected [wake_time, bed_time] with distinct valid times)."
        )

    # Combine user-provided static tasks with generated sleep blocks
    all_statics = list(staticTasks) + sleep_statics
    num_user_statics = len(staticTasks)

    # Parse and validate all static tasks into minute ranges
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

        # Treat "11:59PM" end time as full end-of-day (1440 minutes)
        if isinstance(st.endTime, str) and st.endTime.strip().upper() == "11:59PM":
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
        if (
            not isinstance(st.dayOfWeek, str)
            or len(st.dayOfWeek) != 7
            or not set(st.dayOfWeek).issubset({"0", "1"})
        ):
            return (
                f"Failed at {source_label} dayOfWeek validation: "
                f"got {st.dayOfWeek!r} (expected 7-char string of '0'/'1')."
            )

        parsed_statics.append((start_m, end_m, st.color, st.dayOfWeek))

    # Validate dynamic task fields (guard against bool since bool subclasses int in Python)
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

    # Initialize empty schedules for each of the 7 days (0..6)
    weekly_schedule = [[] for _ in range(7)]

    # Place static tasks on active days and fail immediately on any overlap
    for s_idx, (start_m, end_m, color, days) in enumerate(parsed_statics):
        for day_idx in range(7):
            if days[day_idx] == "1":
                for existing in weekly_schedule[day_idx]:
                    if start_m < existing.endTime and end_m > existing.startTime:
                        return (
                            f"Failed placing static task #{s_idx} on day {day_idx} "
                            f"({start_m}-{end_m}m): overlaps existing block "
                            f"({existing.startTime}-{existing.endTime}m)."
                        )
                weekly_schedule[day_idx].append(task(start_m, end_m, color))

    # Keep each day's blocks sorted chronologically before inserting dynamic tasks
    for day_idx in range(7):
        weekly_schedule[day_idx].sort(key=lambda t: t.startTime)

    # Expand dynamic tasks by `amount`, ordered by priority (lower number = higher priority)
    sorted_dynamics = sorted(dynamicTasks, key=lambda d: d.priority)
    dynamic_instances = []
    for dt in sorted_dynamics:
        for _ in range(dt.amount):
            dynamic_instances.append(dt)

    day_search_order = [0, 1, 2, 3, 4, 5, 6]

    # Fit each dynamic instance into the first open gap wide enough across days 0..6
    for inst_idx, dt in enumerate(dynamic_instances):
        placed = False
        for day_idx in day_search_order:
            day_tasks = weekly_schedule[day_idx]
            current_time = 0

            # Check gaps before each existing task
            for existing in day_tasks:
                if existing.startTime - current_time >= dt.duration:
                    day_tasks.append(task(current_time, current_time + dt.duration, dt.color))
                    day_tasks.sort(key=lambda t: t.startTime)
                    placed = True
                    break
                current_time = max(current_time, existing.endTime)

            # Check remaining open window after the last task up to 1440m (end of day)
            if not placed and (1440 - current_time >= dt.duration):
                day_tasks.append(task(current_time, current_time + dt.duration, dt.color))
                day_tasks.sort(key=lambda t: t.startTime)
                placed = True

            if placed:
                break

        if not placed:
            return (
                f"Failed scheduling dynamic instance #{inst_idx} "
                f"(duration={dt.duration}m, priority={dt.priority}): no open slot across days 0..6."
            )

    # Commit results in-place only after all validation and scheduling succeed
    tasks.clear()
    tasks.extend(weekly_schedule)
    return tasks


# --- Helper classes & 2 debugger test cases ---

class StaticTask:
    def __init__(self, startTime, endTime, color, dayOfWeek):
        self.startTime = startTime
        self.endTime = endTime
        self.color = color
        self.dayOfWeek = dayOfWeek


class DynamicTask:
    def __init__(self, duration, priority, amount, color):
        self.duration = duration
        self.priority = priority
        self.amount = amount
        self.color = color


class task:
    def __init__(self, startTime, endTime, color):
        self.startTime = startTime
        self.endTime = endTime
        self.color = color

    def __repr__(self):
        return f"task({self.startTime}, {self.endTime}, {self.color!r})"


if __name__ == "__main__":
    # Test Case 1: Valid schedule with overnight sleep, static class, and priority dynamic tasks
    tasks_out_1 = []
    statics_1 = [StaticTask("9:00AM", "10:30AM", "#118AB2", "1010100")]
    dynamics_1 = [
        DynamicTask(60, 2, 1, "#FFD166"),
        DynamicTask(90, 1, 2, "#06D6A0"),
    ]
    result_1 = calculate(tasks_out_1, dynamics_1, statics_1, ["7:00AM", "11:00PM"])
    assert isinstance(result_1, list) and len(result_1) == 7
    # Confirm no adjacent blocks overlap on any day
    for day_blocks in result_1:
        for i in range(len(day_blocks) - 1):
            assert day_blocks[i].endTime <= day_blocks[i + 1].startTime
    print("Test 1 passed. Monday blocks:", result_1[0])

    # Test Case 2: Impossible dynamic duration returns failure string and leaves `tasks_out_2` untouched
    tasks_out_2 = []
    statics_2 = [StaticTask("9:00AM", "10:00AM", "#118AB2", "1000000")]
    dynamics_2 = [DynamicTask(2000, 1, 1, "#EF476F")]  # Exceeds 1440-minute day
    result_2 = calculate(tasks_out_2, dynamics_2, statics_2, ["7:00AM", "11:00PM"])
    assert isinstance(result_2, str) and "Failed scheduling dynamic instance" in result_2
    assert tasks_out_2 == []
    print("Test 2 passed. Failure message:", result_2)
