from tkinter import *
from tkinter import ttk

class MyButton(Button):
    def destroy(self):
        print ("Yo!")
        Button.destroy(self)

root = Tk()

f = Frame(root)
b1 = MyButton(f, text="Do nothing")
b1.pack()
f.pack()

b2 = Button(root, text="f.destroy", command=f.destroy)
b2.pack()

root.mainloop()