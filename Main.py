import tkinter as tk





    # colors
blue = "#1E90FF"



if __name__ == '__main__':

    # configs and shit
    root = tk.Tk()
    root.title("diddy balls")
    root.configure(background="#b3008a") # for debugging purposes ,if you seem purple, it means something is not being render one top of what should be rendered
    root.geometry("1000x1150")
    root.resizable(False, False)

    # second page, this is out of order due to the way the pages are rendered
    scheduleMaker_Frame = tk.Frame()

    goToSchedule_Button = tk.Button(scheduleMaker_Frame, text="Go to Schedule", background="#1E90FF",command=lambda: goToScheduleViewer())
    goToSchedule_Button.place(x=50, y=50, height=150, width=300)
    calculate_Button = tk.Button(scheduleMaker_Frame, text="Calculate",   background="#1E90FF")
    calculate_Button.place(x=350, y=50, height=150, width=300)
    exit_button2 = tk.Button(scheduleMaker_Frame, text="Exit/Save", background="#1E90FF",command= lambda : QuitAndSave())
    exit_button2.place(x=650, y=50,height=150, width=300)
    holderLabel_Label = tk.Label(scheduleMaker_Frame,borderwidth=2, relief="groove")
    holderLabel_Label.place(x=50, y=225, height=200, width=900)

    addDynamicTask_Button = (tk.Button(scheduleMaker_Frame, text="Add dynamic task", background="#1E90FF"))
    addDynamicTask_Button.place(x=75, y=250, height=150,width=150)
    addStaticTask_Button = tk.Button(scheduleMaker_Frame, text="Add static task", background="#1E90FF")
    addStaticTask_Button.place(x=225,y=250,height=150,width=150)

    WidthOfBox = 900

    # actually making canvas
    scheduleMakerTasks_canvas = (tk.Canvas(scheduleMaker_Frame,bg=blue))
    scheduleMakerTasks_canvas.place(x=50,y=425,height=700,width=WidthOfBox)
    # making the frame and putting it inside
    scheduleMakerTasks_Frame = tk.Frame(scheduleMakerTasks_canvas,height=1200, width=WidthOfBox)  # will be inside of the canvas
    for i in range(20):
        tk.Button(scheduleMakerTasks_Frame, text=f"Button {i}").place(x=20, y=i * 45, height=45, width=50)
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
    exit_Button = tk.Button(scheduleViewer_Frame,             text="Exit/Save",           bg="#1E90FF",command= lambda : QuitAndSave())
    exit_Button.place(x=650, y=50, height=150,width=300)



    # scheduleColumns_Canvas = tk.Canvas(scheduleViewer_Frame,background="#27b0f5").place(x=50,y=225,width=900,height=875)



    scheduleViewer_Frame.place(x=0,y=0,height=1150,width=1000)



    # button Commands
    def goToScheduleMaker():
        scheduleMaker_Frame.tkraise()
    def goToScheduleViewer():
        scheduleViewer_Frame.tkraise()
    def LoadSchedule():
        pass
    def QuitAndSave():
        SaveSchedule()
        root.quit()
    def SaveSchedule():
        pass
    def Calculate():
        pass
    # other
    root.mainloop()


