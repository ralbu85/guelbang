from tkinter import *
from members import *

class Welcome():

    def __init__(self, master):

        self.master=master
        self.master.geometry('1200x800+100+200')
        self.master.title('Welcome')

        self.label1=Label(self.master, text='하정글방 관리 프로그램 for Dad', fg='green').grid(row=0, column=2, padx=3, pady=3)
        self.button1=Button(self.master, text='회원관리',
                            fg='blue', height=3, width=15, command=self.gotoWages).grid(row=3,column=2, padx=3, pady=10)
        self.button1 = Button(self.master, text='도서관리',
                              fg='blue', height=3, width=15, command=self.gotoWages).grid(row=4,column=2,padx=3, pady=10)
        self.button1 = Button(self.master, text='대여관리',
                              fg='blue', height=3, width=15, command=self.gotoWages).grid(row=5,column=2,padx=3, pady=10)
        self.button1 = Button(self.master, text='끝내기',
                              fg='blue', height=3, width=15, command=self.finish).grid(row=6, column=2,padx=3, pady=10)

    def gotoWages(self):

        root2=Toplevel(self.master)
        myGUI=Wages(root2)


    def finish(self):
        self.master.destroy()


def main():

    root=Tk()
    myGUIWelcome=Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()


