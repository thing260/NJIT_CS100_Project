import tkinter as tk
    # colors
blue = "#1E90FF"
red =  "#ed5949"
yellow = "#ede449"
lightGray = "#c1beba"
gray = "#7a7979"


# UI BEING DECLARED, MOST OF IT WILL BE CHANGED BY FUNCTIONS/COMMANDS
# configs and shit
root = tk.Tk()
root.title("diddy balls")
root.configure(background="#b3008a") # for debugging purposes ,if you seem purple, it means something is not being render one top of what should be rendered
root.geometry("1000x1150")
root.resizable(False, False)

# second page, this is out of order due to the way the pages are rendered
scheduleMaker_Frame = tk.Frame()

goToSchedule_Button = tk.Button(scheduleMaker_Frame, text="Go to Schedule", bg=red,command=lambda: goToScheduleViewer())
goToSchedule_Button.place(x=50, y=50, height=150, width=300)
calculate_Button = tk.Button(scheduleMaker_Frame, text="Calculate",   bg=red,command=lambda : calculate(tasks,dynamicTasks,staticTasks,sleepTime))
calculate_Button.place(x=350, y=50, height=150, width=300)
exit_button2 = tk.Button(scheduleMaker_Frame, text="Exit/Save", bg=red,command= lambda : quitAndSave(dynamicTasks,staticTasks,sleepTime))
exit_button2.place(x=650, y=50,height=150, width=300)

holderLabel_Label = tk.Label(scheduleMaker_Frame,borderwidth=2, relief="groove")
holderLabel_Label.place(x=50, y=225, height=200, width=900)
addDynamicTask_Button = (tk.Button(scheduleMaker_Frame, text="Add \ndynamic task", bg=red, command= lambda : addNewDynamicTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas)))
addDynamicTask_Button.place(x=75, y=250, height=150,width=150)
addStaticTask_Button = tk.Button(scheduleMaker_Frame, text="Add \nstatic task", bg=red, command= lambda : addNewStaticTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas))
addStaticTask_Button.place(x=225,y=250,height=150,width=150)
sleepLabelTask_Label = tk.Label(scheduleMaker_Frame,relief="groove",text="Enter Sleep")
sleepLabelTask_Label.place(x=400,y=250,height=50,width=500)
sleepWaking_Label = tk.Label(scheduleMaker_Frame, relief="groove", text="Wake Up time")
sleepWaking_Label.place(x=400, y=300, height=50, width=250)
sleepWaking_Label = tk.Label(scheduleMaker_Frame, relief="groove", text="BedTime")
sleepWaking_Label.place(x=650, y=300, height=50, width=250)
sleepWaking_Entry = tk.Entry(scheduleMaker_Frame,bg=yellow,relief="groove")
sleepWaking_Entry.place(x=400,y=350,height=50,width=250)
sleepSleeping_Entry = tk.Entry(scheduleMaker_Frame,bg=yellow, relief="groove")
sleepSleeping_Entry.place(x=650, y=350, height=50, width=250)

WidthOfBox = 900
# Making Base Viewer, this will be update by a function on launch
# actually making canvas
scheduleMakerTasks_canvas = (tk.Canvas(scheduleMaker_Frame,bg=blue))
scheduleMakerTasks_canvas.place(x=50,y=425,height=700,width=WidthOfBox)
# making the frame and putting it inside
scheduleMakerTasks_Frame = tk.Frame(scheduleMakerTasks_canvas,height=1200, width=WidthOfBox)  # will be inside of the canvas
scheduleMakerTasks_canvas.create_window((0, 0), window=scheduleMakerTasks_Frame, anchor="nw")
# Making / configuring scroll bar
scheduleMakerTasks_canvas.configure(scrollregion=(0, 0, WidthOfBox, 1200))
scheduleMakerTasks_scrollbar = tk.Scrollbar(scheduleMaker_Frame, orient="vertical", command=scheduleMakerTasks_canvas.yview)
scheduleMakerTasks_scrollbar.place(x=50, y=425, height=700)
scheduleMakerTasks_canvas.configure(yscrollcommand=scheduleMakerTasks_scrollbar.set)

scheduleMaker_Frame.place(x=0, y=0, height=1150, width=1000)




# first page
scheduleViewer_Frame = tk.Frame()

goToScheduleMaker_Button = tk.Button(scheduleViewer_Frame,text="Go to Schedule Maker",bg=red,command= lambda : goToScheduleMaker())
goToScheduleMaker_Button.place(x=50,  y=50, height=150,width=300)
schedule_Label = tk.Label(scheduleViewer_Frame,borderwidth=2, relief="groove",           text="Your Schedule")
schedule_Label.place(x=350, y=50, height=150,width=300)
exit_Button = tk.Button(scheduleViewer_Frame,             text="Exit/Save",           bg=red,command= lambda : quitAndSave(dynamicTasks,staticTasks,sleepTime))
exit_Button.place(x=650, y=50, height=150,width=300)

WidthOfBox = 900
# Making Base Viewer, this will be update by a function on launch
# actually making canvas
scheduleViewerTasks_canvas = tk.Canvas(scheduleViewer_Frame, bg=blue)
scheduleViewerTasks_canvas.place(x=50, y=425, height=900, width=WidthOfBox)
# making the frame and putting it inside
scheduleViewerTasks_Frame = tk.Frame(scheduleViewerTasks_canvas, height=1200,width=WidthOfBox)  # will be inside of the canvas
scheduleViewerTasks_canvas.create_window((0, 0), window=scheduleViewerTasks_Frame, anchor="nw")
# Making / configuring scroll bar
scheduleViewerTasks_canvas.configure(scrollregion=(0, 0, WidthOfBox, 1200))
scheduleViewerTasks_scrollbar = tk.Scrollbar(scheduleViewer_Frame, orient="vertical",command=scheduleViewerTasks_canvas.yview)
scheduleViewerTasks_scrollbar.place(x=50, y=200, height=900)
scheduleViewerTasks_canvas.configure(yscrollcommand=scheduleViewerTasks_scrollbar.set)

scheduleViewer_Frame.place(x=0,y=0,height=1150,width=1000)



# DONE DECLARING UI

# button Commands
def goToScheduleMaker():
    scheduleMaker_Frame.tkraise()
def goToScheduleViewer():
    scheduleViewer_Frame.tkraise()
def quitAndSave(dynamicTasks,staticTasks,sleepTime):
    saveFile(dynamicTasks,staticTasks,sleepTime)
    root.quit()
def saveFile(dynamicTasks, staticTasks, sleepVar):
    file = open("schedule_data.txt", "w")

    sleep_line = str(sleepVar[0]) + "," + str(sleepVar[1]) + "\n"
    file.write(sleep_line)

    dynamic_size = len(dynamicTasks)
    file.write(str(dynamic_size) + "\n")

    for i in range(dynamic_size):
        task = dynamicTasks[i]

        task_line = str(task[0]) + "," + str(task[1]) + "," + str(task[2]) + "," + str(task[3]) + "," + str(task[4]) + "\n"
        file.write(task_line)

    static_size = len(staticTasks)
    file.write(str(static_size) + "\n")

    index = 0
    while index < static_size:
        task = staticTasks[index]

        task_line = str(task[0]) + "," + str(task[1]) + "," + daysOfWeekToString(task[2]) + "," + str(task[3]) + "," + str(task[4]) + "\n"
        file.write(task_line)
        index += 1

    file.close()
    return
def stringToDaysOfWeek(str):
    bools = [False, False, False, False, False, False, False]
    if len(str) == 7:
        index = 0
        while index < 7:
            if str[index] == "1":
                bools[index] = True
            index += 1

    return bools
def daysOfWeekToString(daysOfWeek):
    if (len(daysOfWeek) != 7):
        return "0000000"
    str = ""
    for value in daysOfWeek:
        if value:
            str += "1"
        else:
            str += "0"
    return str
def loadFile():
    file_path = "schedule_data.txt"

    lines = None
    try:
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()
    except:
        lines = []

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
            if len(task_data) != 5:
                is_valid = False
                break

            dynamicTasks.append([task_data[0], task_data[1], task_data[2], task_data[3],task_data[4]])
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

            staticTasks.append([task_data[0], task_data[1], stringToDaysOfWeek(task_data[2]), task_data[3], task_data[4]])
            current_line += 1


    if not is_valid:
        clear_file = open(file_path, "w")
        clear_file.close()

        return ([],[],["",""])
    else:
        return (dynamicTasks, staticTasks, sleepVar)
def addNewDynamicTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas):
    dynamicTasks.append([30,100,0,red,"A Dynamic Task"])
    refreshStaticAndDynamicTaskRendering(dynamicTasks, staticTasks, scheduleMakerTasks_canvas)
def addNewStaticTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas):
    staticTasks.append(["10AM", "10AM", [False,False,False,False,False,False,False],blue,"A Static Task"])
    refreshStaticAndDynamicTaskRendering(dynamicTasks, staticTasks, scheduleMakerTasks_canvas)
def refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks,scheduleMakerTasks_canvas):

    widthOfBox = 900
    # unlike last time, we do not have to remake the canvas

    # deleting the frame inside
    scheduleMakerTasks_canvas.delete("all")
    # CALC HEIGHT HERE BASED ON TASKS
    # I want each Dynamic/Static task to be 300 pixels in height, and margins of 50 between each, and the ends
    height = max(700, # if we are below, set the height to this
                    (len(dynamicTasks) + len(staticTasks)) * 300 # height for each task
                 +  (len(dynamicTasks) + len(staticTasks) - 1) * 50 # add a margin between each, does not matter when its 0, will go to 700 anyways
                 +   100)

    # making the frame and putting it inside
    scheduleMakerTasks_frame = tk.Frame(scheduleMakerTasks_canvas, height=height,width=widthOfBox)  # will be inside of the canvas
    scheduleMakerTasks_canvas.create_window((0, 0), window=scheduleMakerTasks_frame, anchor="nw")
    # Making / configuring scroll bar
    scheduleMakerTasks_canvas.configure(scrollregion=(0, 0, widthOfBox, height))
    scheduleMakerTasks_scrollbar = tk.Scrollbar(scheduleMaker_Frame, orient="vertical",command=scheduleMakerTasks_canvas.yview)
    scheduleMakerTasks_scrollbar.place(x=50, y=425, height=700)
    scheduleMakerTasks_canvas.configure(yscrollcommand=scheduleMakerTasks_scrollbar.set)
    # now we need to add each list and task, as a button
    currentLocation = 50 # where we place the origin about the Y
    for task in staticTasks:
        TempFrame = (tk.Frame(scheduleMakerTasks_frame,background=gray))
        tk.Label(TempFrame).place(x=0,y=0,height=50,width=300,text=staticTasks[4])






        TempFrame.place(x=50, y=currentLocation, height=300, width=800)
        currentLocation += 350
    for task in dynamicTasks:
        TempFrame = (tk.Frame(scheduleMakerTasks_frame, background=gray))

        TempFrame.place(x=50, y=currentLocation, height=300, width=800)
        currentLocation += 350
def refreshTaskRendering(Tasks):
    pass
def calculate_refreshTaskRendering_COMBINED(tasks, dynamicTasks, staticTasks, sleepTime):
    calculate(tasks, dynamicTasks, staticTasks, sleepTime)
    refreshTaskRendering(tasks)

# BEGGINING OF ACTUALLY RUNNING THE PROGRAM
# dynamic Tasks     time to do | priority | amount | color | name
# static Tasks      start | end | Days of week | color | name
dynamicTasks,staticTasks,sleepTime = loadFile()
tasks = []
from calculate_function import *
calculate_refreshTaskRendering_COMBINED(tasks, dynamicTasks, staticTasks, sleepTime)
refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks,scheduleMakerTasks_canvas)





root.mainloop()











