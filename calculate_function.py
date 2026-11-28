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

    def __getitem__(self, idx):
        # Allows both attribute access (.startTime) and list-style indexing (t[0])
        fields = (self.startTime, self.endTime, self.color, self.name)
        return fields[idx]

    def __repr__(self):
        return f"task({self.startTime}, {self.endTime}, {self.color!r}, {self.name!r})"


def parse_time_to_minutes(time_str):
    """Convert '7am', '7AM', '7:00am', '9:30 PM', etc. to minutes since midnight (0..1439)."""
    if not isinstance(time_str, str):
        return None
    cleaned = re.sub(r"\s+", "", time_str.strip().upper())
    match = re.fullmatch(r"(1[0-2]|[1-9])(?::([0-5][0-9]))?(AM|PM)", cleaned)
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


def parse_days_of_week(days):
    """Accept a 7-bool list/tuple or 7-char '0'/'1' string; return list of 7 bools or None."""
    if isinstance(days, (list, tuple)) and len(days) == 7:
        if all(isinstance(d, bool) for d in days):
            return list(days)
        return None
    if isinstance(days, str) and len(days) == 7 and set(days).issubset({"0", "1"}):
        return [ch == "1" for ch in days]
    return None


def parse_int_field(val):
    """Convert int or numeric string (e.g. '30') to int; reject bools, floats, or junk."""
    if isinstance(val, bool):
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        s = val.strip()
        if s.isdigit():
            return int(s)
    return None


def sleep_to_static_tasks(sleep_time):
    """Convert [wake_time, bed_time] into static sleep blocks across all 7 days."""
    if not isinstance(sleep_time, (list, tuple)) or len(sleep_time) != 2:
        return None

    wake_mins = parse_time_to_minutes(sleep_time[0])
    bed_mins = parse_time_to_minutes(sleep_time[1])

    if wake_mins is None or bed_mins is None or wake_mins == bed_mins:
        return None

    sleep_color = "#4B0082"
    sleep_name = "Sleep"
    all_days = [True] * 7

    if bed_mins > wake_mins:
        return [
            StaticTask(sleep_time[1], "11:59PM", sleep_color, list(all_days), sleep_name),
            StaticTask("12:00AM", sleep_time[0], sleep_color, list(all_days), sleep_name),
        ]

    return [
        StaticTask(sleep_time[1], sleep_time[0], sleep_color, list(all_days), sleep_name)
    ]


def _extract_static_fields(st, default_name):
    """Support either a list [start, end, days, color, name] or an object with attributes."""
    if isinstance(st, (list, tuple)):
        if len(st) < 4:
            return None
        start_val, end_val, days_val, color_val = st[0], st[1], st[2], st[3]
        name_val = st[4] if len(st) > 4 else default_name
        return start_val, end_val, days_val, color_val, name_val

    required = ("startTime", "endTime", "dayOfWeek", "color")
    if st is None or not all(hasattr(st, attr) for attr in required):
        return None
    name_val = getattr(st, "name", default_name)
    return st.startTime, st.endTime, st.dayOfWeek, st.color, name_val


def _extract_dynamic_fields(dt, default_name):
    """Support either a list [duration, priority, amount, color, name] or an object."""
    if isinstance(dt, (list, tuple)):
        if len(dt) < 4:
            return None
        dur_val, prio_val, amt_val, color_val = dt[0], dt[1], dt[2], dt[3]
        name_val = dt[4] if len(dt) > 4 else default_name
        return dur_val, prio_val, amt_val, color_val, name_val

    required = ("duration", "priority", "amount", "color")
    if dt is None or not all(hasattr(dt, attr) for attr in required):
        return None
    name_val = getattr(dt, "name", default_name)
    return dt.duration, dt.priority, dt.amount, dt.color, name_val


def calculate(tasks, dynamicTasks, staticTasks, sleepTime):
    """
    Validate inputs, place static + sleep blocks, and schedule dynamic tasks
    into `tasks` (a 7-day list of `task` objects).
    Returns `None` on success (updating `tasks` in place), or a descriptive `str` on failure.
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
        is_sleep = idx >= num_user_statics
        source_label = f"sleep_statics[{idx - num_user_statics}]" if is_sleep else f"staticTasks[{idx}]"
        default_name = "Sleep" if is_sleep else f"Static Task {idx + 1}"

        extracted = _extract_static_fields(st, default_name)
        if extracted is None:
            return f"Failed at {source_label}: missing required fields/attributes."

        start_raw, end_raw, days_raw, color_val, name_raw = extracted
        st_name = name_raw.strip() if isinstance(name_raw, str) and name_raw.strip() else default_name

        if isinstance(end_raw, str) and re.sub(r"\s+", "", end_raw.strip().upper()) == "11:59PM":
            end_m = 1440
        else:
            end_m = parse_time_to_minutes(end_raw)

        start_m = parse_time_to_minutes(start_raw)

        if start_m is None or end_m is None:
            return f"Failed at {source_label} time parsing: start={start_raw!r}, end={end_raw!r}."
        if start_m >= end_m:
            return f"Failed at {source_label} time range: start ({start_m}m) must be earlier than end ({end_m}m)."

        parsed_days = parse_days_of_week(days_raw)
        if parsed_days is None:
            return f"Failed at {source_label} dayOfWeek: got {days_raw!r} (expected 7 bools)."

        parsed_statics.append((start_m, end_m, color_val, parsed_days, st_name))

    parsed_dynamics = []
    for idx, dt in enumerate(dynamicTasks):
        default_name = f"Dynamic Task {idx + 1}"
        extracted = _extract_dynamic_fields(dt, default_name)
        if extracted is None:
            return f"Failed at dynamicTasks[{idx}]: missing required fields/attributes."

        dur_raw, prio_raw, amt_raw, color_val, name_raw = extracted
        dt_name = name_raw.strip() if isinstance(name_raw, str) and name_raw.strip() else default_name

        dur_val = parse_int_field(dur_raw)
        if dur_val is None or dur_val <= 0:
            return f"Failed at dynamicTasks[{idx}] duration/time: got {dur_raw!r} (expected positive int)."

        prio_val = parse_int_field(prio_raw)
        if prio_val is None:
            return f"Failed at dynamicTasks[{idx}] priority: got {prio_raw!r} (expected int)."

        amt_val = parse_int_field(amt_raw)
        if amt_val is None or amt_val < 0:
            return f"Failed at dynamicTasks[{idx}] times done/amount: got {amt_raw!r} (expected non-negative int)."

        parsed_dynamics.append({
            "duration": dur_val,
            "priority": prio_val,
            "amount": amt_val,
            "color": color_val,
            "name": dt_name,
        })

    weekly_schedule = [[] for _ in range(7)]

    for s_idx, (start_m, end_m, color_val, days, st_name) in enumerate(parsed_statics):
        for day_idx in range(7):
            if days[day_idx]:
                for existing in weekly_schedule[day_idx]:
                    if start_m < existing.endTime and end_m > existing.startTime:
                        return (
                            f"Failed placing static task '{st_name}' (#{s_idx}) on day {day_idx}: "
                            f"overlaps '{existing.name}' ({existing.startTime}-{existing.endTime}m)."
                        )
                weekly_schedule[day_idx].append(task(start_m, end_m, color_val, st_name))

    for day_idx in range(7):
        weekly_schedule[day_idx].sort(key=lambda t: t.startTime)

    sorted_dynamics = sorted(parsed_dynamics, key=lambda d: d["priority"])
    dynamic_instances = []
    for dt in sorted_dynamics:
        for _ in range(dt["amount"]):
            dynamic_instances.append(dt)

    for inst_idx, dt in enumerate(dynamic_instances):
        placed = False
        for day_idx in range(7):
            day_tasks = weekly_schedule[day_idx]
            current_time = 0

            for existing in day_tasks:
                if existing.startTime - current_time >= dt["duration"]:
                    day_tasks.append(task(current_time, current_time + dt["duration"], dt["color"], dt["name"]))
                    day_tasks.sort(key=lambda t: t.startTime)
                    placed = True
                    break
                current_time = max(current_time, existing.endTime)

            if not placed and (1440 - current_time >= dt["duration"]):
                day_tasks.append(task(current_time, current_time + dt["duration"], dt["color"], dt["name"]))
                day_tasks.sort(key=lambda t: t.startTime)
                placed = True

            if placed:
                break

        if not placed:
            return (
                f"Failed scheduling '{dt['name']}' (instance #{inst_idx}, "
                f"duration={dt['duration']}m, priority={dt['priority']}): no open slot across days 0..6."
            )

    tasks.clear()
    tasks.extend(weekly_schedule)
    return None


if __name__ == "__main__":
    # Test 1: List inputs matching loadFile() / UI structure + "7am" style sleep times
    out_tasks = []
    sample_statics = [["9:00am", "10:30AM", [True, False, False, False, False, False, False], "#1E90FF", "Lecture"]]
    sample_dynamics = [["60", "1", "1", "#ed5949", "Study"]]
    err1 = calculate(out_tasks, sample_dynamics, sample_statics, ["7am", "11:00pm"])
    assert err1 is None, f"Unexpected error: {err1}"
    assert len(out_tasks) == 7
    print("Test 1 passed. Monday blocks:", out_tasks[0])

    # Test 2: Junk value returns descriptive error string
    bad_out = []
    err2 = calculate(bad_out, [["not_a_number", "1", "1", "#ed5949", "Bad"]], [], ["7AM", "11PM"])
    assert isinstance(err2, str) and "duration/time" in err2
    print("Test 2 passed. Error:", err2)
