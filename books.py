from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import datetime

class Books():

    def __init__(self, master):

        #############################
        ####### Master  #############
        #############################
        self.bookMaster = master
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))

        #############################
        ####### Main Frame ##########
        #############################
        self.mainFrame = Frame(self.bookMaster)
        self.mainFrame.grid(row=0, column=0, padx=3)

        ## Message
        self.message = Label(self.mainFrame, text='', fg='red')
        self.message.grid(row=0, column=0, sticky=W)

        ############ Search Frame ###########
        self.searchFrame=Frame(self.mainFrame)
        self.searchFrame.grid(row=1, column=0, sticky=W)
        # search bar
        self.searchBook = Entry(self.searchFrame, width=20)
        self.searchBook.grid(row=0, column=0, padx=10, sticky=W)
        # button
        Button(self.searchFrame, text='검색', command=lambda:self.search_print_books(self.searchBook.get())).grid(row=0, column=1)
        ######################################

        ## Treeview for Booklist
        self.tree = ttk.Treeview(self.mainFrame, height=15, column=('no', 'title', 'author', 'genre', 'vol'), show='headings')
        self.tree.grid(row=2, column=0, pady=10)
        self.tree.heading('#1', text='번호')
        self.tree.heading('#2', text='제목')
        self.tree.heading('#3', text='작가')
        self.tree.heading('#4', text='장르')
        self.tree.heading('#5', text='권')

        self.tree.column('no', width=40)
        self.tree.column('title', width=210)
        self.tree.column('author', width=100)
        self.tree.column('genre', width=100)
        self.tree.column('vol', width=40)
        self.print_books() #print trees

        #############################
        ####### Menu Frame ##########
        #############################
        self.menuFrame = Frame(self.bookMaster)
        self.menuFrame.grid(row=0, column=1, padx=3, pady=40, sticky=N)

        Button(self.menuFrame, text='도서추가', command=self.add_books, width=10).grid(row=2, padx=3, pady=10)
        Button(self.menuFrame, text='도서삭제', command=self.delete_books, width=10).grid(row=3, padx=3, pady=10)
        Button(self.menuFrame, text='도서정보수정', command=self.editing_books, width=10).grid(row=4, padx=3, pady=10)


    def print_books(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        c.execute('select * from BOOK')

        rows=c.fetchall()
        for row in rows:
            print(row)
            self.tree.insert("",END,values=row)

        c.close()

    def search_validation(self, parameters):
        return len(parameters)!=0


    def search_print_books(self, parameters):
        if self.search_validation(parameters):
            self.tree.delete(*self.tree.get_children())
            con = sq.connect('guelbang.db')
            c = con.cursor()

            query='select * from BOOK where Title like ?'
            #parameters=self.searchBook.get()
            c.execute(query,('%{}%'.format(parameters),))
            #c.execute(query,parameters)

            rows = c.fetchall()
            if len(rows)==0:
                self.message['text']='검색결과가 없습니다'
            for row in rows:
                print(row)
                self.tree.insert("", END, values=row)

            c.close()

        else:
            self.message['text']='글자를 입력하세요'

    def add_books(self):
        self.add_window = Toplevel()
        self.add_window.geometry('400x400+800+500')
        Label(self.add_window, text='제목:').grid(row=1, column=1, padx=10, pady=10)
        self.add_title=Entry(self.add_window)
        self.add_title.grid(row=1, column=2)
        Button(self.add_window, text='검색', command=lambda:self.search_print_books(self.add_title.get())).grid(row=1, column=3)

        Label(self.add_window, text='저자:').grid(row=2, column=1, padx=10, pady=10)
        self.add_author=Entry(self.add_window)
        self.add_author.grid(row=2, column=2)

        Label(self.add_window, text='장르:').grid(row=3, column=1, padx=10, pady=10)
        self.add_genre=Entry(self.add_window)
        self.add_genre.grid(row=3, column=2)

        Label(self.add_window, text='권(시작):').grid(row=4, column=1, padx=10, pady=10)
        self.add_vol_s=Entry(self.add_window)
        self.add_vol_s.grid(row=4, column=2)

        Label(self.add_window, text='권(끝):').grid(row=5, column=1, padx=10, pady=10)
        self.add_vol_f=Entry(self.add_window)
        self.add_vol_f.grid(row=5, column=2)

        Button(self.add_window, text='도서 추가', command=self.add_db, width=10).grid(row=5, column=3, padx=10, pady=10, sticky=W)
        return

    def add_db(self):
        return

    def delete_books(self):
        return

    def editing_books(self):
        return



def main():

    root=Tk()
    myGUIWelcome=Books(root)
    root.mainloop()

if __name__ == '__main__':
    main()