import tkinter as tk

def LoadSchedule():
    
def SaveSchedule():
    
def Calculate(): 

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Our app")

    root.configure(background="#b3008a") # for debugging purposes ,if you seem purple, it means something is not being render one top of what should be rendered
    root.geometry("1000x1150")
    root.resizable(False, False)

    LabelTest = tk.Label(root,text="testing").pack()
    LabelTest2 = tk.Label(root, text="testing2", anchor="e").pack()

    root.mainloop()
