import tkinter as tk
from tkinter import colorchooser
    # colors
blue = "#1E90FF"
red =  "#ed5949"
yellow = "#ede449"
lightGray = "#c1beba"
gray = "#7a7979"


# UI BEING DECLARED, MOST OF IT WILL BE CHANGED BY FUNCTIONS/COMMANDS
# configs and shit
root = tk.Tk()
root.title("Dynamic Scheduler")
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
def addNewDynamicTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas,entries):
    dynamicTasks.append([30,100,0,red,"A Dynamic Task"])
    refreshStaticAndDynamicTaskRendering(dynamicTasks, staticTasks, scheduleMakerTasks_canvas,entries)
def addNewStaticTaskToList(dynamicTasks,staticTasks,scheduleMakerTasks_canvas,entries):
    staticTasks.append(["10AM", "10AM", [False,False,False,False,False,False,False],blue,"A Static Task"])
    refreshStaticAndDynamicTaskRendering(dynamicTasks, staticTasks, scheduleMakerTasks_canvas,entries)
def refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks,scheduleMakerTasks_canvas,entries):

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








    # reset entries
    entries[0] = [[],[],[],[],[]]
    entries[1] = [[],[],[],[],[]]

    # now we need to add each list and task, as a button
    currentLocation = 50 # where we place the origin about the Y
    currentStaticTask = 0 # current task, this is for the lambda
    for task in staticTasks:
        #Color for Frame
        frameColor = task[3]
        try:
            root.winfo_rgb(task[3])

        except tk.TclError:
            frameColor = gray

        # Declaring Temp Frame that I will eventually place with the geometry manager
        TempFrame = (tk.Frame(scheduleMakerTasks_frame,background=frameColor))

        # Name
        tk.Label(TempFrame,background=gray,text="Task Name:").place(x=0,y=0,height=50,width=150)
        name = tk.StringVar(value=task[4])
        entries[0][4].append(name)
        tk.Entry(TempFrame,background=yellow,textvariable=name).place(x=150,y=0,height=50,width=400)
        # jeritusha, pls dont ask me what this does, I only 10% get it <----------------------------------------------------------------------------------
        # ok now I 20% get it
        name.trace_add("write",lambda *args, v=name, i=currentStaticTask: staticTasks[i].__setitem__(4, v.get())) # Make entry actually modify the value


        # Color
        # I could not wrap my head around for this, the library is abit to complex to learn in this short amount of time (words for I used ai on these 5 lines)
        color = tk.StringVar(value=task[3])
        entries[0][3].append(color)
        colorPickingButton = tk.Button(TempFrame, background=red, text="choose color")
        colorPickingButton.config(command=lambda v=color, f=TempFrame, i=currentStaticTask: (staticTasks[i].__setitem__(3, colorchooser.askcolor()[1] or v.get()),v.set(staticTasks[i][3]),f.config(background=v.get())))
        colorPickingButton.place(x=550, y=0, height=50, width=250)


        # start time
        startTime = tk.StringVar(value=task[0])
        entries[0][0].append(startTime)
        tk.Label(TempFrame, background=gray, text="Start Time:").place(x=0, y=50, height=50, width=150)
        tk.Entry(TempFrame, background=yellow,textvariable=startTime).place(x=150, y=50, height=50, width=200)
        startTime.trace_add("write", lambda *args, v=startTime, i=currentStaticTask: staticTasks[i].__setitem__(0,v.get()))  # Make entry actually modify the value

        # end time
        endTime = tk.StringVar(value=task[1])
        entries[0][1].append(startTime)
        tk.Label(TempFrame, background=gray, text="End Time:").place(x=0, y=100, height=50, width=150)
        tk.Entry(TempFrame, background=yellow,textvariable=endTime).place(x=150, y=100, height=50, width=200)
        endTime.trace_add("write", lambda *args, v=endTime, i=currentStaticTask: staticTasks[i].__setitem__(1,v.get()))  # Make entry actually modify the value


        # Days of Week
        tk.Label(TempFrame, background=gray, text="Days of\n Week").place(x=0, y=200, height=100, width=100)
        #check boxes
        #----- Stuff around first checkbox, this works
        tk.Label(TempFrame, background=gray, text="Mon").place(x=100, y=200, height=50, width=100)
        checkBox1 = tk.BooleanVar(value=task[2][0])
        entries[0][2].append(checkBox1)
        tk.Checkbutton(TempFrame,background=gray,variable=checkBox1).place(x=100,y=250,height=50,width =100)
        checkBox1.trace_add("write", lambda *args, v=checkBox1, i=currentStaticTask: staticTasks[i][2].__setitem__(0,v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Tue").place(x=200, y=200, height=50, width=100)
        checkBox2 = tk.BooleanVar(value=task[2][1])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox2).place(x=200, y=250, height=50, width=100)
        entries[0][2].append(checkBox2)
        checkBox2.trace_add("write", lambda *args, v=checkBox2, i=currentStaticTask: staticTasks[i][2].__setitem__(1,v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Wed").place(x=300, y=200, height=50, width=100)
        checkBox3 = tk.BooleanVar(value=task[2][2])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox3).place(x=300, y=250, height=50, width=100)
        entries[0][2].append(checkBox3)
        checkBox3.trace_add("write", lambda *args, v=checkBox3, i=currentStaticTask: staticTasks[i][2].__setitem__(2,v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Thur").place(x=400, y=200, height=50, width=100)
        checkBox4 = tk.BooleanVar(value=task[2][3])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox4).place(x=400, y=250, height=50, width=100)
        entries[0][2].append(checkBox4)
        checkBox4.trace_add("write", lambda *args, v=checkBox4, i=currentStaticTask: staticTasks[i][2].__setitem__(3, v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Fri").place(x=500, y=200, height=50, width=100)
        checkBox5 = tk.BooleanVar(value=task[2][4])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox5).place(x=500, y=250, height=50, width=100)
        entries[0][2].append(checkBox5)
        checkBox5.trace_add("write", lambda *args, v=checkBox5, i=currentStaticTask: staticTasks[i][2].__setitem__(4, v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Sat").place(x=600, y=200, height=50, width=100)
        checkBox6 = tk.BooleanVar(value=task[2][5])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox6).place(x=600, y=250, height=50, width=100)
        entries[0][2].append(checkBox6)
        checkBox6.trace_add("write",lambda *args, v=checkBox6, i=currentStaticTask: staticTasks[i][2].__setitem__(5, v.get()))
        #-----
        tk.Label(TempFrame, background=gray, text="Sun").place(x=700, y=200, height=50, width=100)
        checkBox7 = tk.BooleanVar(value=task[2][6])
        tk.Checkbutton(TempFrame, background=gray,variable=checkBox7).place(x=700, y=250, height=50, width=100)
        entries[0][2].append(checkBox7)
        checkBox7.trace_add("write",lambda *args, v=checkBox7, i=currentStaticTask: staticTasks[i][2].__setitem__(6, v.get()))


        # done
        TempFrame.place(x=50, y=currentLocation, height=300, width=800)
        currentLocation += 350
        currentStaticTask += 1

    currentDynamicTask = 0
    for task in dynamicTasks:
        
        # get frame color
        frameColor = task[3]
        try:
            root.winfo_rgb(task[3])

        except tk.TclError:
            frameColor = lightGray

        # set frame
        TempFrame = (tk.Frame(scheduleMakerTasks_frame, background=frameColor))

        #name
        tk.Label(TempFrame, background=lightGray, text="Task Name:").place(x=0, y=0, height=50, width=150)
        name = tk.StringVar(value=task[4])
        entries[1][4].append(name)
        tk.Entry(TempFrame, background=yellow,textvariable=name).place(x=150, y=0, height=50, width=300)# Make entry actually modify the value
        name.trace_add("write", lambda *args, v=name, i=currentDynamicTask: dynamicTasks[i].__setitem__(0,v.get()))

        #color
        color = tk.StringVar(value=task[3])
        entries[0][3].append(color)
        colorPickingButton = tk.Button(TempFrame, background=red, text="choose color")
        colorPickingButton.config(command=lambda v=color, f=TempFrame, i=currentDynamicTask: (dynamicTasks[i].__setitem__(3, colorchooser.askcolor()[1] or v.get()), v.set(dynamicTasks[i][3]),f.config(background=v.get())))
        colorPickingButton.place(x=550, y=0, height=50, width=250)

        # Time
        tk.Label(TempFrame, background=lightGray, text="Time (in minutes)").place(x=0, y=50, height=50, width=250)
        time = tk.StringVar(value=task[0])
        entries[1][0].append(time)
        tk.Entry(TempFrame, background=yellow,textvariable=time).place(x=250, y=50, height=50, width=200)
        time.trace_add("write", lambda *args, v=time, i=currentDynamicTask: dynamicTasks[i].__setitem__(0,v.get()))

        # times done, yada yada
        tk.Label(TempFrame, background=lightGray, text="Times done").place(x=0, y=100, height=50, width=250)
        timesDone = tk.StringVar(value=task[2])
        entries[1][2].append(timesDone)
        tk.Entry(TempFrame, background=yellow,textvariable=timesDone).place(x=250, y=100, height=50, width=200)
        timesDone.trace_add("write",lambda *args,v=timesDone,i=currentDynamicTask: dynamicTasks[i].__setitem__(2,v.get()))

        # priority
        tk.Label(TempFrame, background=lightGray, text="Priority (number)").place(x=0, y=150, height=50, width=250)
        priority = tk.StringVar(value=task[1])
        entries[1][1].append(priority)
        tk.Entry(TempFrame, background=yellow,textvariable=priority).place(x=250, y=150, height=50, width=200)
        priority.trace_add("write", lambda *args, v=priority, i=currentDynamicTask: dynamicTasks[i].__setitem__(1, v.get()))



        TempFrame.place(x=50, y=currentLocation, height=300, width=800)
        currentDynamicTask += 1
        currentLocation += 350
def refreshTaskRendering(Tasks):
    pass
def calculate_refreshTaskRendering_COMBINED(tasks, dynamicTasks, staticTasks, sleepTime):
    calculate(tasks, dynamicTasks, staticTasks, sleepTime)
    refreshTaskRendering(tasks)


# BEGINNING OF ACTUALLY RUNNING THE PROGRAM
# dynamic Tasks     time to do | priority | amount | color | name
# static Tasks      start | end | Days of week | color | name
dynamicTasks,staticTasks,sleepTime = loadFile()
tasks = []
'''
# Static task ui variable getters

static_Start_Entries = []
static_End_Entries = []
static_DaysOfWeek_Entries = []
static_Color_Entries = []
static_Name_Entries = []

# dynamic task ui variable getters

dynamic_ToDo_Entries = []
dynamic_Priority_Entries = []
dynamic_Amount_Entries = []
dynamic_Color_Entries = []
dynamic_Name_Entries = []

# sleep entries

sleepEntry = [None,None]
'''
# above is what should be in Entries, this is for UI exclusively, it just saves references
entries = [[[],[],[],[],[]],[[],[],[],[],[]],[]]
from calculate_function import *
calculate_refreshTaskRendering_COMBINED(tasks, dynamicTasks, staticTasks, sleepTime)
refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks,scheduleMakerTasks_canvas,entries)





root.mainloop()

print(staticTasks)
print(dynamicTasks)










