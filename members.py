from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import datetime

class Wages():

    def __init__(self, master):

        self.member_master=master
        self.member_master.geometry('800x600+100+200')
        self.member_master.title('회원관리')

        self.frame = LabelFrame(self.member_master, text='Add new records')
        self.frame.grid(row=0, column=1)

        # Label(frame, text='이 름:').grid(row=1, column=1)
        # self.name=Entry(frame)
        # self.name.grid(row=1, column=2)
        #
        # Label(frame, text='핸드폰:').grid(row=2, column=1)
        # self.mobile=Entry(frame)
        # self.mobile.grid(row=2, column=2)
        #
        # Label(frame, text='주소:').grid(row=3, column=1)
        # self.address=Entry(frame)
        # self.address.grid(row=3, column=2)
        #
        # Button(frame, text='회원 추가', command=self.add_members).grid(row=4, column=2)
        self.message=Label(self.frame, text='', fg='red')
        self.message.grid(row=4, column=0)

        self.message=Label(self.frame, text='', fg='red')
        self.message.grid(row=4, column=0)

        self.tree = ttk.Treeview(self.frame, height=10, column=('no','name', 'mobile', 'address'), show='headings')
        self.tree.grid(row=5, column=0, columnspan=3)
        self.tree.heading('#1', text='번호')
        self.tree.heading('#2', text='이름')
        self.tree.heading('#3', text='핸드폰')
        self.tree.heading('#4', text='주소')

        self.tree.column('no',width=30)
        self.tree.column('name',width=100)
        self.printMembers()

        Button(self.frame, text='추가', command=self.addMembers).grid(row=6, column=0)
        Button(self.frame, text='삭제',command=self.delete_members).grid(row=6, column=1)
        Button(self.frame, text='수정',command=self.editing_members).grid(row=6, column=2)



    def printMembers(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        c.execute('select * from MEMBER')

        rows=c.fetchall()
        for row in rows:
            print(row)
            self.tree.insert("",END,values=row)

        c.close()


    def addMembers(self):

        self.add_window = Toplevel()
        Label(self.add_window, text='이 름:').grid(row=1, column=1)
        self.name=Entry(self.add_window)
        self.name.grid(row=1, column=2)

        Label(self.add_window, text='핸드폰:').grid(row=2, column=1)
        self.mobile=Entry(self.add_window)
        self.mobile.grid(row=2, column=2)

        Label(self.add_window, text='주소:').grid(row=3, column=1)
        self.address=Entry(self.add_window)
        self.address.grid(row=3, column=2)

        Button(self.add_window, text='회원 추가', command=self.add_db).grid(row=4, column=2)

    def add_db(self):

        con = sq.connect('guelbang.db')
        c = con.cursor()

        if self.validation():
            query='insert into MEMBER VALUES (NULL, ?, ?, ?)'
            parameters= (self.name.get(), self.mobile.get(), self.address.get())
            c.execute(query, parameters)
            con.commit()
            c.close()
            self.message['text']='회원정보가 추가되었습니다.'
            self.name.delete(0, END)
            self.mobile.delete(0, END)
            self.address.delete(0, END)
        else:
            self.message['text']='회원정보 추가에 실패했습니다.'

        self.tree.delete(*self.tree.get_children())
        self.printMembers()
        self.add_window.destroy()

    def validation(self):
        return len(self.name.get())!=0 and len(self.mobile.get())!=0 and len(self.address.get())!=0


    def delete_members(self):

        con = sq.connect('guelbang.db')
        c = con.cursor()

        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text']='회원을 선택해 주세요!'
            return

        self.message['text']=''
        selected_id=self.tree.item(self.tree.selection())['values'][0]
        print (selected_id)
        query = 'delete from MEMBER where Id=?'
        parameters = (selected_id,)
        c.execute(query, parameters)
        con.commit()
        c.close()

        self.tree.delete(*self.tree.get_children())
        self.printMembers()

    def editing_members(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()

        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text']='회원을 선택해 주세요!'
            return

        selected_row=self.tree.item(self.tree.selection())['values']
        self.selected_id=selected_row[0]
        selected_name=selected_row[1]
        selected_mobile=selected_row[2]
        selected_address=selected_row[3]

        self.edit_window=Toplevel()
        Label(self.edit_window, text='이름: ').grid(row=0, column=1)
        self.new_name=Entry(self.edit_window,textvariable=StringVar(self.edit_window, value=selected_name), width=20)
        self.new_name.grid(row=0, column=2, sticky=W)
        Label(self.edit_window, text='휴대폰: ').grid(row=1, column=1)
        self.new_mobile=Entry(self.edit_window,textvariable=StringVar(self.edit_window, value=selected_mobile), width=20)
        self.new_mobile.grid(row=1, column=2, sticky=W)
        Label(self.edit_window, text='주소: ').grid(row=2, column=1)
        self.new_address=Entry(self.edit_window,textvariable=StringVar(self.edit_window, value=selected_address), width=60)
        self.new_address.grid(row=2, column=2, sticky=W)

        Button(self.edit_window, text='변경하기',command=self.editing_db).grid(row=4, column=1)


    def editing_db(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        query = 'update MEMBER SET Name=?, Phone=?, Address=? where Id=?'
        parameters = (self.new_name.get(), self.new_mobile.get(), self.new_address.get(), self.selected_id)
        c.execute(query, parameters)
        con.commit()
        c.close()

        self.tree.delete(*self.tree.get_children())
        self.printMembers()
        self.edit_window.destroy()


    def myquit(self):
        self.master.destroy()

def main():

    root=Tk()
    myGUIWelcome=Wages(root)
    root.mainloop()

if __name__ == '__main__':
    main()