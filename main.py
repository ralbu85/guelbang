from tkinter import *
import members as members
import books as books

root = Tk()

class Welcome():

    def __init__(self, master):

        ## master setting
        self.master=master
        self.master.geometry('800x600+100+200')
        self.master.title('Welcome')

        ## menu pannel
        self.menu_pannel=Frame(self.master, width=20, height=100)
        self.menu_pannel.grid(row=0,column=0, sticky=N)

        self.label1=Label(self.menu_pannel, text='하정글방 관리 프로그램 for Dad', fg='green').grid(row=0, column=1, padx=3, pady=3)
        self.button1=Button(self.menu_pannel, text='회원관리',
                            fg='blue', height=3, width=15, command=self.gotoMembers).grid(row=1,column=1, padx=3, pady=10)
        self.button1 = Button(self.menu_pannel, text='도서관리',
                              fg='blue', height=3, width=15, command=self.gotoBooks).grid(row=2,column=1,padx=3, pady=10)
        self.button1 = Button(self.menu_pannel, text='대여관리',
                              fg='blue', height=3, width=15).grid(row=3,column=1,padx=3, pady=10)
        self.button1 = Button(self.menu_pannel, text='끝내기',
                              fg='blue', height=3, width=15, command=self.finish).grid(row=4, column=1,padx=3, pady=10)

        ## function pannel
        self.function_pannel=Frame(self.master, width=100, height=100)
        self.function_pannel.grid(row=0, column=1, sticky=N, padx=3, pady=30)


    def gotoMembers(self):
        self.function_pannel.grid_forget()
        self.function_pannel=Frame(self.master, width=100, height=100)
        self.function_pannel.grid(row=0, column=1, sticky=N, padx=3, pady=30)
        myGUI=members.Members(self.function_pannel)

    def gotoBooks(self):
        self.function_pannel.grid_forget()
        self.function_pannel = Frame(self.master, width=100, height=100)
        self.function_pannel.grid(row=0, column=1, sticky=N, padx=3, pady=30)
        myGUI=books.Books(self.function_pannel)


    def finish(self):
        self.master.destroy()

def main():
    myGUIWelcome=Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()


