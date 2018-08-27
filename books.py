from tkinter import *
from tkinter import ttk
import tkinter.messagebox
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
        self.message.grid(row=0, column=0, pady=10)

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
        self.tree = ttk.Treeview(self.mainFrame, height=15, column=('title', 'vol', 'author', 'genre'), show='headings')
        self.tree.grid(row=2, column=0, pady=10)

        # scrollbar
        ysb=ttk.Scrollbar(self.mainFrame, orient='vertical',command=self.tree.yview)
        ysb.grid(row=2, column=1,sticky='ns', pady=10)
        self.tree.configure(yscroll=ysb.set)

        self.tree.heading('#1', text='제목')
        self.tree.heading('#2', text='권')
        self.tree.heading('#3', text='장르')
        self.tree.heading('#4', text='작가')

        self.tree.column('title', width=210, anchor=CENTER)
        self.tree.column('vol', width=50, anchor=CENTER)
        self.tree.column('author', width=120, anchor=CENTER)
        self.tree.column('genre', width=120, anchor=CENTER)
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
        self.tree.delete(*self.tree.get_children())
        con = sq.connect('guelbang.db')
        c = con.cursor()
        c.execute('select Title, Vol, Genre, Author from BOOK order by Title, Vol ASC')

        rows=c.fetchall()
        for row in rows:
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
                self.print_books()
            else:
                for row in rows:
                    self.tree.insert("",END,values=row)
            c.close()

        else:
            self.message['text']='글자를 입력하세요'


    def disable_button(self):
        for child in self.menuFrame.winfo_children():
            child.configure(state='disabled')

    def destroy_add_books(self):
        self.add_window.destroy()
        print ("activated")
        for child in self.menuFrame.winfo_children():
            child.configure(state='normal')

        self.print_books()


    def add_books(self):
        self.disable_button()
        self.add_window = Toplevel(self.bookMaster)
        self.add_window.protocol('WM_DELETE_WINDOW',self.destroy_add_books)


        # determine popup position
        x_axis = self.bookMaster.winfo_x()
        y_axis = self.bookMaster.winfo_y()

        self.add_window.geometry('400x400+{}+{}'.format(x_axis + 600, y_axis + 400))

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



    def add_db(self):

        con = sq.connect('guelbang.db')
        c = con.cursor()

        # check validation
        if self.validation():
            # when books > 2
            if self.check_insert_many():
                book_vol_list=list(range(int(self.add_vol_s.get()), int(self.add_vol_f.get())+1))
                params=[]
                for vol in book_vol_list:
                    params.append(tuple([self.add_title.get(), self.add_author.get(), self.add_genre.get()]+
                                         [str(vol)]+
                                         [datetime.date.today().strftime("%y-%m-%d")]))

                try:
                    c.executemany('insert into BOOK VALUES (NULL, ?, ?, ?, ?, ?)', params)
                    con.commit()
                    self.message['text'] = '도서정보가 추가되었습니다.'
                except sq.Error as er:
                    print(er.args)
                    tkinter.messagebox.showinfo('실패', '중복되는 도서가 존재합니다.')
                    self.message['text'] = '도서정보 추가에 실패했습니다.'


                c.close()

                self.tree.delete(*self.tree.get_children())
                self.print_books()
                self.destroy_add_books()

            # when books = 1
            else:
                query = 'insert into BOOK VALUES (NULL, ?, ?, ?, ?, ?)'
                parameters = (self.add_title.get(), self.add_author.get(), self.add_genre.get(), self.add_vol_s.get(), datetime.date.today().strftime("%y-%m-%d"))

                try:
                    c.execute(query, parameters)
                    con.commit()
                    self.message['text'] = '도서정보가 추가되었습니다.'
                except sq.Error as er:
                    print (er.args)
                    tkinter.messagebox.showinfo('실패', '중복되는 도서가 존재합니다.')
                    self.message['text'] = '도서정보 추가에 실패했습니다.'

                c.close()

                self.tree.delete(*self.tree.get_children())
                self.print_books()
                self.destroy_add_books()

        # else:
        #     self.message['text'] = '도서정보 추가에 실패했습니다.'


    def validation(self):
        check_empty=len(self.add_title.get()) != 0 and len(self.add_vol_s.get()) != 0

        if len(self.add_vol_s.get()) != 0 and len(self.add_vol_f.get()) !=0:
            check_vol=int(self.add_vol_s.get()) < int(self.add_vol_f.get())
        else:
            check_vol = True

        if not check_empty:
            tkinter.messagebox.showinfo('실패','도서제목과 권수는 반드시 있어야 합니다.')

        if not check_vol:
            tkinter.messagebox.showinfo('실패','시작권수가 끝권수보다 커야 합니다.')

        return check_empty and check_vol


    def check_insert_many(self):
        return len(self.add_vol_s.get()) != 0 and len(self.add_vol_f.get()) != 0


    def delete_books(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()

        self.message['text']=''

        params=[]
        for i in self.tree.selection():
            params.append( (self.tree.item(i)['values'][0],) )

        query='delete from Book where Id =?'
        try:
            c.executemany(query, params)
            con.commit()
            self.message['text'] = '도서정보가 삭제되었습니다.'
        except sq.Error as er:
            print(er.args)
            tkinter.messagebox.showinfo('실패', '도서정보 삭제에 실패했습니다.')
            self.message['text'] = '도서정보 삭제에 실패했습니다.'

        c.close()
        self.tree.delete(*self.tree.get_children())
        self.print_books()
        return

    def editing_books(self):
        return



def main():

    root=Tk()
    myGUIWelcome=Books(root)
    root.mainloop()

if __name__ == '__main__':
    main()