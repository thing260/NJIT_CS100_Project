def saveFile(dynamicTasks, staticTasks, sleepVar):

    file = open("schedule_data.txt", "w")

    sleep_line = str(sleepVar[0]) + "," + str(sleepVar[1]) + "\n"
    file.write(sleep_line)

    dynamic_size = len(dynamicTasks)
    file.write(str(dynamic_size) + "\n")

    for i in range(dynamic_size):
        task = dynamicTasks[i]

        task_line = str(task[0]) + "," + str(task[1]) + "," + str(task[2]) + "," + str(task[3]) + "\n"
        file.write(task_line)

        static_size = len(staticTasks)
        file.write(str(static_size) + "\n")

    index = 0
    while index < static_size:
        task = staticTasks[index]

        task_line = str(task[0]) + "," + str(task[1]) + "," + str(task[2]) + "," + str(task[3]) + "," + str(task[4]) + "\n"
        file.write(task_line)
        index += 1

    file.close()
    return
    
