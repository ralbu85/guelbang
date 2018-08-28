from tkinter import *
import sqlite3 as sq
from tkinter import ttk
import books as books
import datetime


class Controller():
    def __init__(self, master):
        ####### Master  #############
        self.master=master

        self.SearchFrame=Frame(self.master)
        self.SearchFrame.grid(row=0, column=0)

        self.MemberFrame=Frame(self.master)
        self.MemberFrame.grid(row=0, column=1)

        self.RentFrame=Frame(self.master)
        self.RentFrame.grid(row=1,column=0,columnspan=2)

        self.MemberClass=MemberInfo(self.MemberFrame)
        self.RentClass=RentInfo(self.RentFrame)
        self.SearchClass=SearchMember(self.SearchFrame, self.MemberClass, self.RentClass)

class SearchMember():
    def __init__(self, parent, member, rent):
        # setting Frame
        self.frame = parent

        # connected Object
        self.member = member
        self.rent = rent

        # search bar
        self.entry = Entry(parent, width=20)
        self.entry.grid(row=0, column=0, padx=10, sticky=W)
        # button
        Button(self.frame, text='검색', command=self.search_members).grid(row=0,column=1)
        Button(self.frame, text='초기화', command=self.clear_members).grid(row=0, column=2)

    def search_members(self):
        self.inputKeyword=self.entry.get()
        self.connect()
        self.querying()
        print(self.returned[0])
        self.member.updateInfo(self.returned[0])
        self.rent.updateInfo(self.returned[0])

    def clear_members(self):
        self.member.clearInfo()
        self.rent.clearInfo()

    def connect(self):
        self.con = sq.connect('guelbang.db')
        self.c = self.con.cursor()

    def querying(self):
        query='SELECT * from MEMBER where Name = ?'
        param=(self.inputKeyword,)
        self.c.execute(query, param)
        self.returned=self.c.fetchall()

class MemberInfo():
    def __init__(self, parent):
        self.frame=parent
        self.displayInfo(text='번호', row=0, column=0, width=5)
        self.displayInfo(text='이름', row=1, column=0, width=5)
        self.displayInfo(text='핸드폰', row=2, column=0, width=5)
        self.displayInfo(text='주소', row=3, column=0, width=5)
        self.displayInfo(text='',row=0,column=1, width=30)


    def displayInfo(self, **kwargs):
        Label(self.frame, text=kwargs['text'], fg='blue', width=kwargs['width']).\
            grid(row=kwargs['row'], column=kwargs['column'], sticky=W, padx=10)

    def updateInfo(self, memberInfo):
        self.displayInfo(text=memberInfo[0], row=0, column=1, width=30)
        self.displayInfo(text=memberInfo[1], row=1, column=1, width=30)
        self.displayInfo(text=memberInfo[2], row=2, column=1, width=30)
        self.displayInfo(text=memberInfo[3], row=3, column=1, width=30)

    def clearInfo(self):
        self.displayInfo(text='', row=0, column=1, width=30)
        self.displayInfo(text='', row=1, column=1, width=30)
        self.displayInfo(text='', row=2, column=1, width=30)
        self.displayInfo(text='', row=3, column=1, width=30)


class RentInfo():
    def __init__(self, parent):

        self.parent=parent

        ############# Tree ###################
        self.tree = ttk.Treeview(parent, height=15, column=('rent_date', 'title', 'vol', 'genre', 'author', 'days'),
                                 show='headings')
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        # scrollbar
        ysb = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns', pady=10)
        self.tree.configure(yscroll=ysb.set)

        self.tree.heading('#1', text='대여일')
        self.tree.heading('#2', text='제목')
        self.tree.heading('#3', text='권')
        self.tree.heading('#4', text='장르')
        self.tree.heading('#5', text='저자')
        self.tree.heading('#6', text='경과일')

        self.tree.column('rent_date', width=150, anchor=CENTER)
        self.tree.column('title', width=170, anchor=CENTER)
        self.tree.column('vol', width=40, anchor=CENTER)
        self.tree.column('genre', width=40, anchor=CENTER)
        self.tree.column('author', width=100, anchor=CENTER)
        self.tree.column('days', width=50, anchor=CENTER)

        # ButtonFrame
        self.ButtonFrame=Frame(parent)
        self.ButtonFrame.grid(row=0,column=2,rowspan=2)

        b1=self.gen_button(text='대여', row=0, column=0)
        b2=self.gen_button(text='회수', row=1, column=0)
        b3=self.gen_button(text='내역조회', row=2, column=0)

        self.Buttons=[b1,b2,b3]
        self.control_button('disable')

    def gen_button(self, **kwargs):
        button=Button(self.ButtonFrame, text=kwargs['text'])
        button.grid(row=kwargs['row'],column=kwargs['column'], padx=5, pady=10,sticky=NW)
        return button

    def control_button(self, state):
        for button in self.Buttons:
            button.configure(state=state)

    def querying(self, member_info):
        self.con = sq.connect('guelbang.db')
        self.c = self.con.cursor()
        query = 'SELECT RentDate, Title, Vol, Genre, AUthor FROM RENT join BOOK on BOOK.Id=RENT.BookId where MemberId=?'
        parameters = (member_info[0],)
        self.c.execute(query, parameters)

    def clearInfo(self):
        self.control_button('disable')
        self.tree.delete(*self.tree.get_children())

    def updateInfo(self, member_id):
        self.clearInfo()
        self.control_button('normal')
        self.querying(member_id)
        rows = self.c.fetchall()
        for row in rows:
            delta = datetime.datetime.now() - datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            row=row + (delta.days,)
            self.tree.insert("", END, values=row)

        self.c.close()



def main():
    root=Tk()
    myGUIWelcome=Controller(root)
    root.mainloop()

if __name__ == '__main__':
    main()

