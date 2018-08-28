from tkinter import *
import sqlite3 as sq
from tkinter import ttk
import books as books
import datetime

class Rental():
    def __init__(self, master):

        ####### Master  #############
        self.rent_master=master
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))

        self.mainFrame=_mainFrame(self.rent_master, row=0, column=0)
        self.message=_message(self.mainFrame.frame, row=1, column=0)
        self.rentFrame=_rentFrame(self.mainFrame.frame, row=2, column=0)
        self.searchFrame=_searchFrame(self.mainFrame.frame, self.message, self.rentFrame, row=0, column=0)
        self.menuFrame =_menuFrame(self.rent_master, self.searchFrame, row=0, column=1, sticky=NS)

class _mainFrame():
    def __init__(self, parent, *args, **kwargs):
        self.frame=Frame(parent)
        print(kwargs['row'])
        self.frame.grid(row=kwargs['row'], column=kwargs['column'], padx=3)

class _message():
    def __init__(self, parent, *args, **kwargs):
        self.frame=Frame(parent)
        self.frame.grid(row=kwargs['row'], column=kwargs['column'], pady=10, sticky=W, padx=10)

        self.status_message=Label(self.frame, text='', fg='red', width=15)
        self.status_message.grid(row=0, column=0)

        self.member_info=Frame(self.frame)
        self.member_info.grid(row=0, column=1)

        Label(self.member_info, text='이름:', fg='blue').grid(row=0, column=0, sticky=W, padx=10 )
        self.name=Label(self.member_info, text='', fg='blue')
        self.name.grid(row=0, column=1, sticky=W, padx=10 )

        Label(self.member_info, text='휴대폰:', fg='blue').grid(row=1, column=0, sticky=W, padx=10 )
        self.phone=Label(self.member_info, text='', fg='blue')
        self.phone.grid(row=1, column=1, sticky=W, padx=10 )

        Label(self.member_info, text='주소:', fg='blue').grid(row=2, column=0, sticky=W, padx=10 )
        self.address=Label(self.member_info, text='', fg='blue')
        self.address.grid(row=2, column=1, sticky=W, padx=10 )

    def update_status_info(self, message):
        self.status_message['text']=message

    def update_member_info(self, row):
        self.name['text']=row[1]
        self.phone['text']=row[2]
        self.address['text']=row[3]

class _rentFrame():
    def __init__(self, parent, *args, **kwargs):
        ############# Tree ###################
        self.tree = ttk.Treeview(parent, height=15, column=('rent_date', 'title', 'vol', 'genre', 'author', 'days'),
                                 show='headings', selectmode="browse")
        self.tree.grid(row=kwargs['row'], column=kwargs['column'], pady=10)

        # scrollbar
        ysb = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
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

    def update_rent_info(self, member_id):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        query = 'SELECT RentDate, Title, Vol, Genre, AUthor FROM RENT join BOOK on BOOK.Id=RENT.BookId where MemberId=?'
        parameters = (member_id,)
        c.execute(query, parameters)

        rows = c.fetchall()
        for row in rows:
            delta = datetime.datetime.now() - datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            row=row + (delta.days,)
            self.tree.insert("", END, values=row)

            c.close()

    def clear_rent_info(self):
        self.tree.delete(*self.tree.get_children())

class _searchFrame():
    def __init__(self, parent, message, tree, *args, **kwargs):

        # setting Frame
        self.searchFrame = Frame(parent)
        self.searchFrame.grid(row=kwargs['row'], column=kwargs['column'], sticky=W)
        # search bar
        self.searchMember = Entry(self.searchFrame, width=20)
        self.searchMember.grid(row=0, column=0, padx=10, sticky=W)
        # connected Frame
        self.message=message
        self.tree=tree
        # button
        Button(self.searchFrame, text='검색', command= lambda:self.search_members(self.searchMember.get())).grid(row=0,column=1)

    def search_validation(self, parameters):
        return len(parameters)!=0

    def search_members(self, parameters):
        if self.search_validation(parameters):

            member_row=self.search_query_return(parameters)

            if len(member_row)==0:
                self.message.update_status_info('검색결과가 없습니다')

            elif len(member_row)==1:
                self.message.update_member_info(member_row[0])
                self.tree.clear_rent_info()
                self.selected_id=member_row[0][0]
                self.tree.update_rent_info(self.selected_id)

            else:
                self.popup=PopupMember(self.searchFrame, self.message, self.tree, member_row)


        else:
            self.message.update_status_info('글자를 입력하세요')

    def search_query_return(self, parameters):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        query = 'select Id, Name,Phone,Address from MEMBER where Name like ?'
        c.execute(query, ('%{}%'.format(parameters),))
        rows=c.fetchall()
        c.close()
        return rows

class PopupMember():
    def __init__(self, parent, message, tree, fetch_rows):

        self.parent=parent
        ## popup new window
        self.win_master =Toplevel(parent)

        # connected widget
        self.message=message
        self.rentFrame=tree

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
        self.message.update_member_info(self.selected_row)
        self.rentFrame.clear_rent_info()
        self.rentFrame.update_rent_info(self.selected_row[0])
        self.parent.selected_id=self.selected_row[0]
        self.win_master.destroy()
        return self.selected_row

class _menuFrame():
    def __init__(self, parent, searchFrame, *args, **kwargs):

        # create Frame
        self.menuFrame=Frame(parent)
        self.menuFrame.grid(row=kwargs['row'],column=kwargs['column'], padx=3, pady=40, sticky=N)

        # connected widget
        self.searchFrame=searchFrame

        Button(self.menuFrame, text='대여',command=self.pop_add_rent, width=10).grid(row=5, padx=3, pady=10)
        Button(self.menuFrame, text='회수',command=self.return_rent, width=10).grid(row=6, padx=3, pady=10)
        Button(self.menuFrame, text='대여기록',command=self.view_history, width=10).grid(row=7, padx=3, pady=10)

    def pop_add_rent(self):
        add_rent(self.menuFrame)

    def return_rent(self):
        return

    def view_history(self):
        return

class add_rent():
    def __init__(self,parent,**kwargs):

        ## popup new window
        self.win_master = Toplevel(parent)

        # generate Frame within windows
        self.mainFrame = Frame(self.win_master)
        self.mainFrame.grid(row=0, column=0,padx=10, pady=5)

        # generate Entry
        self.entryFrame = Frame(self.mainFrame)
        self.entryFrame.grid(row=0, column=0)

        Label(self.entryFrame, text='도서검색: ').grid(row=0, column=0, pady=5)
        self.entry=Entry(self.entryFrame, width=20)
        self.entry.grid(row=0,column=1)
        Button(self.entryFrame, text='검색', command=self.button_pressed).grid(row=0, column=2, padx=5)
        Button(self.entryFrame, text='대여목록추가', command=self.add_pressed).grid(row=0, column=3, padx=5)

        # generate treeviews
        self.tree = ttk.Treeview(self.mainFrame, height=20, column=('id','title','vol','genre','author'),show='headings')
        self.tree.grid(row=1, column=0)

        self.tree.heading('#1', text='Id')
        self.tree.heading('#2', text='제목')
        self.tree.heading('#3', text='권')
        self.tree.heading('#4', text='장르')
        self.tree.heading('#5', text='저자')

        self.tree.column('id',width=40, anchor=CENTER)
        self.tree.column('title',width=200, anchor=CENTER)
        self.tree.column('vol',width=40, anchor=CENTER)
        self.tree.column('genre', width=80, anchor=CENTER)
        self.tree.column('author', width=80, anchor=CENTER)

    def button_pressed(self):
        self.keyword=self.entry.get()
        self.get_query_result()
        self.update_tree()

    def get_query_result(self):
        con=sq.connect('guelbang.db')
        c=con.cursor()
        query='SELECT Id, Title, Vol, Genre, Author FROM BOOK WHERE Title like ?'
        c.execute(query, ('%{}%'.format(self.keyword),))
        self.rows=c.fetchall()
        c.close()

    def update_tree(self):
        for row in self.rows:
            self.tree.insert("",END,values=row)

    def clear_rent_info(self):
        self.tree.delete(*self.tree.get_children())

    def add_pressed(self):

        params=[]
        for i in self.tree.selection():
            id=self.tree.item(i)['values']
            print(id)
            params.append((id,))

        query='INSERT INTO BOOK VALUES ()'



        return




def main():
    root=Tk()
    myGUIWelcome=Rental(root)
    root.mainloop()

if __name__ == '__main__':
    main()
