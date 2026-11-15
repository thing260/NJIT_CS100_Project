import tkinter as tk
    # colors
blue = "#1E90FF"
red =  "#ed5949"
yellow = "#ede449"


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
addDynamicTask_Button = (tk.Button(scheduleMaker_Frame, text="Add dynamic task", bg=red))
addDynamicTask_Button.place(x=75, y=250, height=150,width=150)
addStaticTask_Button = tk.Button(scheduleMaker_Frame, text="Add static task", bg=red)
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

goToScheduleMaker_Button = tk.Button(scheduleViewer_Frame,text="Go to Schedule Maker",bg="#1E90FF",command= lambda : goToScheduleMaker())
goToScheduleMaker_Button.place(x=50,  y=50, height=150,width=300)
schedule_Label = tk.Label(scheduleViewer_Frame,borderwidth=2, relief="groove",           text="Your Schedule")
schedule_Label.place(x=350, y=50, height=150,width=300)
exit_Button = tk.Button(scheduleViewer_Frame,             text="Exit/Save",           bg="#1E90FF",command= lambda : quitAndSave(dynamicTasks,staticTasks,sleepTime))
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

# task classes
class task: # this will be gotten from dynamic and static tasks converted to this type
    def __init__(self,startTime : int,endTime: int,color : str):
        self.startTime = startTime # something like 10 as in 10AM
        self.endTime = endTime
        self.color = color

class DynamicTask:
    def __init__(self,duration : int,priority : int,amount : int,color : str):
        self.duration = duration
        self.priority = priority #higher the priority is as an integer, lower it is in actual priority
        self.amount = amount
        self.color = color

class StaticTask:
    def __init__(self,startTime : str,endTime: str,color : str,daysOfWeek : str):
        self.startTime = startTime # something like "10AM"
        self.endTime = endTime
        self.color = color # something like "#1E90FF"
        self.dayOfWeek = daysOfWeek # something like "0011010", aka the task is on wed, thur, and saturday

# variables

tasks = []
dynamicTasks = []
staticTasks = []
sleepTime = [0,0]

# button Commands
def goToScheduleMaker():
    scheduleMaker_Frame.tkraise()
def goToScheduleViewer():
    scheduleViewer_Frame.tkraise()
def quitAndSave(dynamicTasks,staticTasks,sleepTime):
    saveSchedule(dynamicTasks,staticTasks,sleepTime)
    root.quit()
def saveSchedule(dynamicTasks,staticTasks,sleepTime):
    pass
def calculate(tasks,dynamicTasks,StaticTasks,sleepTime):
    pass
def addNewDynamicTaskToList(dynamicTasks):
    dynamicTasks.append(DynamicTask(30,100,0,red))

def addNewStaticTaskToList(staticTasks):
    staticTasks.append(StaticTask("NA", "NA", blue,"0000000"))



    # other functions
def loadTasks(dynamicTasks,staticTasks,sleepTime):
    pass
def refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks):
    pass
    #reference to our ScheduleMakerCanvas -> Frame
    # delete everything in Frame
    #
def refreshTaskRendering(Tasks):
    pass

# BEGGINING OF ACTUALLY RUNNING THE PROGRAM

loadTasks(dynamicTasks,staticTasks,sleepTime)
calculate(tasks,dynamicTasks,staticTasks,sleepTime)
refreshStaticAndDynamicTaskRendering(dynamicTasks,staticTasks)




root.mainloop()






