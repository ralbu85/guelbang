from tkinter import *
import sqlite3 as sq
from tkinter import ttk
import books as books
import datetime

class PopupMember():
    def __init__(self, parent, fetch_rows):
        ## popup new window
        self.win_master =Toplevel(parent)

        # determine popup position
        x_axis = parent.winfo_x()
        y_axis = parent.winfo_y()
        self.win_master.geometry('+{}+{}'.format(x_axis + 600, y_axis + 400))

        # generate Frame within windows
        self.mainFrame = Frame(self.win_master)
        self.mainFrame.grid(row=0, column=0)

        # generate treeviews
        self.tree = ttk.Treeview(self.mainFrame, height=5, column=('no','name','mobile','address'),show='headings', selectmode='browse')
        self.tree.grid(row=0, column=0)

        self.tree.heading('#1', text='번호')
        self.tree.heading('#2', text='이름')
        self.tree.heading('#3', text='핸드폰')
        self.tree.heading('#4', text='주소')

        self.tree.column('no',width=40, anchor=CENTER)
        self.tree.column('name',width=80, anchor=CENTER)
        self.tree.column('mobile', width=120, anchor=CENTER)
        self.tree.column('address', width=200, anchor=CENTER)

        for row in fetch_rows:
            self.tree.insert("",END,values=row)

        # button
        Button(self.mainFrame, text='선택', command=self.proceed).grid(row=1, column=0)

    def proceed(self):
        self.selected_row=tuple(self.tree.item(self.tree.selection())['values'])
        #self.selected=tuple(selected_row)
        #print (tuple(self.selected_row))
        self.win_master.destroy()
        return self.selected_row


class MemberStatus():
    def __init__(self, parent, fetch_rows):
        print (fetch_rows)
        self.frame=Frame(parent)
        self.id=fetch_rows[0]
        Label(self.frame, text='이름: ').grid(row=0, column=0, sticky=W)
        Label(self.frame, text=fetch_rows[1]).grid(row=0, column=1, sticky=W)

        Label(self.frame, text='핸드폰: ').grid(row=1, column=0, sticky=W)
        Label(self.frame, text=fetch_rows[2]).grid(row=1, column=1, sticky=W)

        Label(self.frame, text='주소: ').grid(row=2, column=0, sticky=W)
        Label(self.frame, text=fetch_rows[3]).grid(row=2, column=1, sticky=W)

    def get_frame(self):
        return self.frame

    def get_id(self):
        return self.id

class RentStatus():
    def __init__(self,tree,member_id):
        ## treeview
        self.tree=tree
        self.tree.delete(*tree.get_children())
        self.printRents(member_id)

    def printRents(self,member_id):
        con=sq.connect('guelbang.db')
        c=con.cursor()
        query='SELECT RentDate, Title, Vol, Genre, AUthor FROM RENT join BOOK on BOOK.Id=RENT.BookId where MemberId=?'
        parameters = (member_id, )
        c.execute(query, parameters)

        rows=c.fetchall()
        for row in rows:
            delta=datetime.datetime.now()-datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S")
            print(row + (delta.days,))
            self.tree.insert("",END,values=row)

        c.close()


class Rental():

    def __init__(self, master):

        #############################
        ####### Master  #############
        #############################
        self.rent_master=master
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))

        #############################
        ####### Main Frame ##########
        #############################
        self.mainFrame = Frame(self.rent_master)
        self.mainFrame.grid(row=0, column=0, padx=3)

        # message
        self.message=Label(self.mainFrame, text='', fg='red')
        self.message.grid(row=0, column=0, pady=10, sticky=W, padx=10)


        ############ Search Frame ###########
        self.searchFrame = Frame(self.mainFrame)
        self.searchFrame.grid(row=1, column=0, sticky=W)
        # search bar
        self.searchMember = Entry(self.searchFrame, width=20)
        self.searchMember.grid(row=0, column=0, padx=10, sticky=W)
        # button
        Button(self.searchFrame, text='검색', command=lambda: self.search_members(self.searchMember.get())).grid(row=0,column=1)
        ######################################

        ############# Tree ###################
        self.tree = ttk.Treeview(self.mainFrame, height=15, column=('rent_date', 'title', 'vol', 'genre', 'author', 'days'),
                                 show='headings', selectmode="browse")
        self.tree.grid(row=2, column=0, pady=10)

        # scrollbar
        ysb = ttk.Scrollbar(self.mainFrame, orient='vertical', command=self.tree.yview)
        ysb.grid(row=2, column=1, sticky='ns', pady=10)
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
        self.tree.column('author', width=40, anchor=CENTER)
        self.tree.column('days', width=50, anchor=CENTER)
        #####################################


        #############################
        ####### Menu Frame ##########
        #############################
        self.menuFrame=Frame(self.rent_master)
        self.menuFrame.grid(row=0,column=1, padx=3, pady=40, sticky=N)

        Button(self.menuFrame, text='회원추가',command=self.add_rent, width=10).grid(row=2, padx=3, pady=10)
        Button(self.menuFrame, text='회원삭제',command=self.return_rent, width=10).grid(row=3, padx=3, pady=10)
        Button(self.menuFrame, text='회원정보수정',command=self.view_history, width=10).grid(row=4, padx=3, pady=10)


    def search_validation(self, parameters):
        return len(parameters)!=0

    def search_members(self, parameters):
        if self.search_validation(parameters):
            con = sq.connect('guelbang.db')
            c = con.cursor()
            query='select * from MEMBER where Name like ?'
            #parameters=self.searchBook.get()
            c.execute(query,('%{}%'.format(parameters),))
            #c.execute(query,parameters)

            rows = c.fetchall()
            if len(rows)==0:
                self.message['text']='검색결과가 없습니다'

            elif len(rows)==1:
                print (rows[0])
                # frame=MemberStatus(self.searchFrame,rows[0])
                # frame.get_frame().grid(row=0, column=2, padx=20, sticky=N)
                # tree=RentStatus(self.tree,frame.get_id())

            else:
                print('popup')
                PopupMember(self.mainFrame, rows)
                print (PopupMember.selected_row)

                # frame=MemberStatus(self.searchFrame, row)
                # tree = RentStatus(self.tree, frame.get_id())

            c.close()

        else:
            self.message['text']='글자를 입력하세요'

    def printMembers(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        c.execute('select * from MEMBER')

        rows=c.fetchall()
        for row in rows:
            self.tree.insert("",END,values=row)

    def add_rent(self):
        return

    def return_rent(self):
        return

    def view_history(self):
        return

def main():

    root=Tk()
    myGUIWelcome=Rental(root)
    root.mainloop()

if __name__ == '__main__':
    main()
