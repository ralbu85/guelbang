from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import datetime

class Members():

    def __init__(self, master):

        #############################
        ####### Master  #############
        #############################
        self.member_master=master
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))

        #############################
        ####### Main Frame ##########
        #############################
        self.mainFrame = Frame(self.member_master)
        self.mainFrame.grid(row=0, column=0, padx=3)

        # message
        self.message=Label(self.mainFrame, text='', fg='red')
        self.message.grid(row=0, column=0, pady=10)

        ############ Search Frame ###########
        self.searchFrame = Frame(self.mainFrame)
        self.searchFrame.grid(row=1, column=0, sticky=W)
        # search bar
        self.searchMember = Entry(self.searchFrame, width=20)
        self.searchMember.grid(row=0, column=0, padx=10, sticky=W)
        # button
        Button(self.searchFrame, text='검색', command=lambda: self.search_print_books(self.searchBook.get())).grid(row=0,column=1)
        ######################################


        ## treeview
        self.tree = ttk.Treeview(self.mainFrame, height=15, column=('no','name', 'mobile', 'address'), show='headings',selectmode="browse")
        self.tree.grid(row=2, column=0, pady=10)

        # scrollbar
        ysb=ttk.Scrollbar(self.mainFrame, orient='vertical',command=self.tree.yview)
        ysb.grid(row=2, column=1,sticky='ns', pady=10)
        self.tree.configure(yscroll=ysb.set)


        self.tree.heading('#1', text='번호')
        self.tree.heading('#2', text='이름')
        self.tree.heading('#3', text='핸드폰')
        self.tree.heading('#4', text='주소')

        self.tree.column('no',width=40, anchor=CENTER)
        self.tree.column('name',width=80, anchor=CENTER)
        self.tree.column('mobile', width=120, anchor=CENTER)
        self.tree.column('address', width=260, anchor=CENTER)
        self.printMembers()

        #############################
        ####### Menu Frame ##########
        #############################
        self.menuFrame=Frame(self.member_master)
        self.menuFrame.grid(row=0,column=1, padx=3, pady=40, sticky=N)

        Button(self.menuFrame, text='회원추가',command=self.add_members, width=10).grid(row=2, padx=3, pady=10)
        Button(self.menuFrame, text='회원삭제',command=self.delete_members, width=10).grid(row=3, padx=3, pady=10)
        Button(self.menuFrame, text='회원정보수정',command=self.editing_members, width=10).grid(row=4, padx=3, pady=10)


    def printMembers(self):
        con = sq.connect('guelbang.db')
        c = con.cursor()
        c.execute('select * from MEMBER')

        rows=c.fetchall()
        for row in rows:
            self.tree.insert("",END,values=row)

        c.close()

    def disable_button(self):
        for child in self.menuFrame.winfo_children():
            child.configure(state='disabled')

    def destroy_add_members(self):
        print ("activated")
        for child in self.menuFrame.winfo_children():
            child.configure(state='normal')
        self.add_window.destroy()


    def add_members(self):

        self.disable_button()
        self.add_window = Toplevel(self.member_master)

        ## when top level window closed, do this callback
        self.add_window.protocol('WM_DELETE_WINDOW', self.destroy_add_members)

        x_axis=self.member_master.winfo_x()
        y_axis=self.member_master.winfo_y()

        #self.add_window.geometry('300x300+700+400')
        self.add_window.geometry('300x300+{}+{}'.format(x_axis+600,y_axis+400))
        Label(self.add_window, text='이 름:').grid(row=1, column=1, padx=4, pady=10)
        self.name=Entry(self.add_window)
        self.name.grid(row=1, column=2, padx=4, pady=10)

        Label(self.add_window, text='핸드폰:').grid(row=2, column=1, padx=4, pady=10)
        self.mobile=Entry(self.add_window)
        self.mobile.grid(row=2, column=2, padx=4, pady=10)

        Label(self.add_window, text='주소:').grid(row=3, column=1, padx=4, pady=10)
        self.address=Entry(self.add_window)
        self.address.grid(row=3, column=2, padx=4, pady=10)

        Button(self.add_window, text='회원 추가', command=self.add_db).grid(row=4, column=2, padx=4, pady=10)


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
        self.destroy_add_members()

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

        self.edit_window=Toplevel(self.member_master)
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
    myGUIWelcome=Members(root)
    root.mainloop()

if __name__ == '__main__':
    main()