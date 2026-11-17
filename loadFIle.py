def loadFile():
    file_path = "schedule_data.txt"

    file = open(file_path, "r")
    lines = file.readlines()
    file.close()

    is_valid = True

    sleepVar = []
    dynamicTasks = []
    staticTasks = []


    if len(lines) == 0:
        is_valid = False

    if is_valid:
        sleep_data = lines[0].strip().split(',')
        if len(sleep_data) != 2:
            is_valid = False
        else:
            sleepVar = [sleep_data[0], sleep_data[1]]


    current_line = 1
    dynamic_size = 0

    if is_valid:
        if current_line >= len(lines):
            is_valid = False
        else:
            size_str = lines[current_line].strip()
            if not size_str.isdigit():
                is_valid = False
            else:
                dynamic_size = int(size_str)
                current_line += 1

    if is_valid:
        for i in range(dynamic_size):
            if current_line >= len(lines):
                is_valid = False
                break

            task_data = lines[current_line].strip().split(',')
            if len(task_data) != 4:
                is_valid = False
                break

            dynamicTasks.append([task_data[0], task_data[1], task_data[2], task_data[3]])
            current_line += 1


    static_size = 0

    if is_valid:
        if current_line >= len(lines):
            is_valid = False
        else:
            size_str = lines[current_line].strip()
            if not size_str.isdigit():
                is_valid = False
            else:
                static_size = int(size_str)
                current_line += 1
    if is_valid:
        for i in range(static_size):
            if current_line >= len(lines):
                is_valid = False
                break

            task_data = lines[current_line].strip().split(',')
            if len(task_data) != 5:
                is_valid = False
                break

            staticTasks.append([task_data[0], task_data[1], task_data[2], task_data[3], task_data[4]])
            current_line += 1


    if not is_valid:
        clear_file = open(file_path, "w")
        clear_file.close()

        return None
    else:
        return (dynamicTasks, staticTasks, sleepVar)

    