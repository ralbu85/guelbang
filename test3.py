import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import messagebox

from collections import OrderedDict
import datetime
import sqlite3 as sq

class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.main_font = tkfont.Font(size=12)

        #shared Entry data
        self.shared_data={
            'user_input': tk.StringVar(),
            'selected_member': None,
            'member_returned': None,
            'member_info': {'id':None, 'name':None, 'phone':None, 'address':None},
            'current_rent': None,

            'user_input_book': tk.StringVar(),
            'searched_book': None,

            'selected_rent_id':None
        }
        # Generic Container
        Container=tk.Frame(self, borderwidth=5)
        Container.grid(row=0, column=0)
        #For search
        SearchContainer = tk.Frame(Container, borderwidth=5)
        SearchContainer.grid(row=0,column=0)
        #For member Info
        MemberContainer = tk.Frame(Container, borderwidth=5)
        MemberContainer.grid(row=1,column=0)
        #for rental Info
        RentContainer = tk.Frame(Container, borderwidth=5)
        RentContainer.grid(row=2, column=0)
        #for buttons
        ButtonContainer = tk.Frame(Container, borderwidth=5)
        ButtonContainer.grid(row=3, column=0)

        self.frames = {}
        self.frames["SearchView"] = SearchView(parent=SearchContainer, controller=self)
        self.frames["MemberView"] = MemberView(parent=MemberContainer, controller=self)
        self.frames["RentView"] = RentView(parent=RentContainer, controller=self)
        self.frames["ButtonView"] = ButtonView(parent=ButtonContainer, controller=self)

        self.frames["MemberCheckPopup"] = MemberCheckPopup(parent=Container, controller=self)
        self.frames["RentBookPopup"]=RentBookPopup(parent=Container, controller=self)

        self.frames["SearchView"].grid(row=0, column=0, sticky="nsw")
        self.frames["MemberView"].grid(row=0, column=0, sticky="nsw")
        self.frames["RentView"].grid(row=0, column=0, sticky="nsw")
        self.frames["ButtonView"].grid(row=0, column=0, sticky="nsw")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def member_check(self):
        model=Model()
        name = self.shared_data['user_input'].get()
        self.shared_data['member_returned']=model.member_search(name)

        if len(self.shared_data['member_returned'])>1:
            self.frames["MemberCheckPopup"].popup()

        else:
            self.update_member(self.shared_data['member_returned'][0])
            self.update_rent()

    def update_member(self, selected_member):
        self.shared_data['selected_member']=selected_member
        self.frames['MemberView'].update()

    def update_rent(self):
        result=Model().rent_search(self.shared_data['selected_member']['id'])
        self.shared_data['current_rent']=result
        self.frames["RentView"].update()

    def activate_buttons(self):
        print(len(self.shared_data['current_rent']))
        if len(self.shared_data['current_rent'])==0:
            self.frames['ButtonView'].activate_buttons('book','history')
        else:
            self.frames['ButtonView'].activate_buttons('book','return','history')

    def book_search(self):
        model=Model()
        title=self.shared_data['user_input_book'].get()
        self.shared_data['searched_book']=model.book_search(title)
        self.frames['RentBookPopup'].showInfo()


    def add_rent(self):
        model=Model()
        current_member_id=self.shared_data['selected_member']['id']
        selected_book_id=self.shared_data['searched_book']
        print(current_member_id, selected_book_id)
        model.insert_book(current_member_id,selected_book_id)
        messagebox.showinfo('yeah','대여처리 되었습니다.')
        self.update_rent()

    def return_and_rent(self):
        model=Model()
        current_member_id=self.shared_data['selected_member']['id']
        in_rent_id=self.shared_data['in_rent']
        selected_book_id=self.shared_data['searched_book']

        model.return_book(in_rent_id)
        model.insert_book(current_member_id,selected_book_id)

        messagebox.showinfo('yeah','대여처리 되었습니다.')
        self.update_rent()

    def return_book(self):

        model=Model()
        selected_rent_ids=self.shared_data['selected_rent_id']
        print(selected_rent_ids)
        model.return_book(selected_rent_ids)

        messagebox.showinfo('yay','회수되었습니다.')
        self.update_rent()

class Model():
    def __init__(self):
        self.con = sq.connect('guelbang.db')
        self.c = self.con.cursor()

    def member_search(self, user_input) :
        query='SELECT * from MEMBER where Name = ?'
        param=(user_input,)
        self.c.execute(query, param)
        returned=self.c.fetchall()

        result=[]
        title=['id','name','phone','address']
        for row in returned:
            temp_result = {}
            for i in range(len(title)):
                temp_result[title[i]]=row[i]
            result.append(temp_result)

        return result


    def rent_search(self, member_id):
        query = 'SELECT RENT.Id, RentDate, Title, Vol, Genre, AUthor FROM RENT join BOOK on BOOK.Id=RENT.BookId where MemberId=? and ReturnDate IS NULL'
        param = (member_id,)
        self.c.execute(query, param)
        returned=self.c.fetchall()

        key=('id','rent_date','title','vol','genre','author','day')
        result=[]
        for row in returned:
            result.append(OrderedDict(tuple(zip(key,row))))

        for record in result:
            delta=datetime.datetime.now() - datetime.datetime.strptime(record['rent_date'], "%Y-%m-%d %H:%M:%S")
            record['day']=delta.days

        return result

    def book_search(self, user_input):
        query='''
        select BOOK.ID as BookId, Title, Author, Genre, Vol, RENT.Id as RentId, RentDate, Name from BOOK 
            left join RENT on BOOK.Id=RENT.BookId
            left join MEMBER on MemberId=MEMBER.Id
            where RENT.ReturnDate is null and BOOK.Title like ?
        '''
        param=('%{}%'.format(user_input),)
        self.c.execute(query, param)
        result=self.c.fetchall()
        print(result)

        return result

    def insert_book(self, current_member_id, selected_book_id):
        query="insert into RENT values (NULL, ?, ?, ?, NULL)"
        current_date=datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        params=[]
        for id in selected_book_id:
            temp=(current_member_id,id,current_date)
            params.append(temp)
        self.c.executemany(query, params)
        self.con.commit()


    def return_book(self, selected_rent_ids):

        current_date=datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        query="update RENT set ReturnDate=? where Id=?"
        params=[]
        for id in selected_rent_ids:
            params.append((current_date,id))

        self.c.executemany(query,params)
        self.con.commit()

class SearchView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        font={'font':self.controller.main_font}

        group = tk.LabelFrame(self, padx=5, pady=10, text="", **font)
        group.grid(row=0, padx=10, pady=5, sticky='w')

        # search bar
        self.entry = tk.Entry(group, **font, width=20, textvariable=self.controller.shared_data['user_input'])
        self.entry.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5)

        # button
        Button1=tk.Button(group, **font, text='검색', width=10, command=self.search)
        Button1.grid(row=0,  column=1, padx=5, pady=5)

    def search(self):
        self.controller.member_check()

class ButtonView(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        group=tk.Frame(self)
        group.grid(row=0, column=0)

        font={'font':self.controller.main_font}

        text=["book", "return", "history"]
        callbacks=[self.book, self.return_book, self.history]


        self.Buttons={}

        for name,callback in list(zip(text,callbacks)):
            self.Buttons[name]=tk.Button(group, **font, text=name, command=callback, width=10)
            self.Buttons[name].pack(side='left', padx=10, pady=10)

        for button in self.Buttons.values():
            button.configure(state='disable')

    def activate_buttons(self,*args):

        for button in self.Buttons.values():
            button.configure(state='disable')

        for i in args:
            self.Buttons[i].configure(state='normal')

    def book(self):
        self.controller.frames['RentBookPopup'].popup()

    def return_book(self):
        self.controller.frames['RentView'].return_proc()
        self.controller.return_book()

    def history(self):
        print(1)

class MemberView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        member_data=controller.shared_data['member_info']

        font={'font':self.controller.main_font}
        group = tk.LabelFrame(self, padx=5, pady=10, text="회원정보", **font)
        group.grid(row=0, padx=10, pady=5, sticky='w')

        opts1 = {'font': self.controller.main_font, 'padx': 5, 'pady': 3, 'anchor':'e', 'width':5}
        tk.Label(group, text="이름:", **opts1).grid(row=0)
        tk.Label(group, text="휴대폰:", **opts1).grid(row=1)
        tk.Label(group, text="주소:", **opts1).grid(row=2)

        opts2 = {'font': self.controller.main_font, 'padx': 5, 'pady': 3, 'anchor': 'w', 'width':30}
        self.name=tk.Label(group, text='', **opts2)
        self.name.grid(row=0, column=1)

        self.phone=tk.Label(group, text='',  **opts2)
        self.phone.grid(row=1, column=1)

        self.address=tk.Label(group, text='', **opts2)
        self.address.grid(row=2, column=1)

        tk.Frame()

    def update(self):
        self.name['text'] = self.controller.shared_data['selected_member']['name']
        self.phone['text'] = self.controller.shared_data['selected_member']['phone']
        self.address['text'] = self.controller.shared_data['selected_member']['address']

class RentView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        style = ttk.Style()
        style.configure("Treeview", font=(None,12))
        style.configure("Treeview.Heading", font=(None, 14))


        self.tree=ttk.Treeview(self, height=15, column=('id','rent_date', 'title', 'vol', 'genre', 'author', 'days'),
                     show='headings')
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        ysb=ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns', pady=10)
        self.tree.configure(yscroll=ysb.set)

        nums=('#1','#2','#3','#4','#5','#6','#7')
        names=('id','rent_date', 'title', 'vol', 'genre', 'author', 'days')
        text=('id','대여일','제목','권','장르','저자','경과일')
        width=(0,200,300,100,100,100,100)

        headings=[self.tree.heading(i,text=j) for i,j in list(zip(nums,text))]
        columns=[self.tree.column(i,width=j,anchor=tk.CENTER) for i,j in list(zip(names,width))]

        self.tree['displaycolumns'] = ('rent_date', 'title', 'vol', 'genre', 'author', 'days')

    def update(self):
        self.tree.delete(*self.tree.get_children())
        keys = ['id','rent_date', 'title', 'vol', 'genre', 'author', 'day']
        for record in self.controller.shared_data['current_rent']:
            values=[record[key] for key in keys]
            self.tree.insert("",tk.END, values=values)

        self.controller.activate_buttons()

    def return_proc(self):
        result=[]
        for i in self.tree.selection():
            result.append(self.tree.item(i)['values'][0])
        print(result)
        self.controller.shared_data['selected_rent_id']=result

class MemberCheckPopup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def popup(self):
        self.window=tk.Toplevel(self)
        self.tree = ttk.Treeview(self.window, height=5, column=('id','name','phone','address'),show='headings', selectmode='browse')
        self.tree.grid(row=0, column=0)

        nums=('#1','#2','#3','#4')
        names=('id','name','phone','address')
        text=('번호','이름','핸드폰','주소')
        width=(50,100,200,300)

        headings=[self.tree.heading(i,text=j) for i,j in list(zip(nums,text))]
        columns=[self.tree.column(i,width=j,anchor=tk.CENTER) for i,j in list(zip(names,width))]

        # button
        self.columns=['id','name','phone','address']

        for record in self.controller.shared_data["member_returned"]:
            temp=[record[col] for col in self.columns]
            self.tree.insert("", tk.END, values=temp)

        tk.Button(self.window, text='선택', command=self.select_id).grid(row=1, column=0)

    def select_id(self):
        values=self.tree.item(self.tree.selection())['values']
        result=dict(list(zip(self.columns,values)))
        self.controller.update_member(result)
        self.controller.update_rent()
        self.window.destroy()

class RentBookPopup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def popup(self):
        self.window=tk.Toplevel(self)

        font={'font':self.controller.main_font}

        ### LabelFrame for Booksearch ###
        group = tk.LabelFrame(self.window, padx=5, pady=10, text="", **font)
        group.grid(row=0, padx=10, pady=5, sticky='w')

        self.entry = tk.Entry(group, **font, width=20, textvariable=self.controller.shared_data['user_input_book'])
        self.entry.grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5)

        Button1=tk.Button(group, **font, text='검색', command=self.search, width=10)
        Button1.grid(row=0,  column=1, padx=5, pady=5, sticky='nsew')

        columns=('bookId','title','author','genre','vol','rentId','rentDate','name')
        nums=('#1','#2','#3','#4','#5','#6','#7','#8')
        text=('번호','책이름','저자','장르','권수', '렌트번호', '빌린날짜', '대여자')
        width=(50,300,100,100,50,50,200,100)

        ### tree ####
        self.tree = ttk.Treeview(self.window, height=20, column=columns,show='headings')
        self.tree.grid(row=1, column=0)

        ysb=ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        ysb.grid(row=1, column=1, sticky='ns', pady=10)

        headings=[self.tree.heading(i,text=j) for i,j in list(zip(nums,text))]
        columns=[self.tree.column(i,width=j,anchor=tk.CENTER) for i,j in list(zip(columns,width))]

        self.tree['displaycolumns']=('title','author','genre','vol','name')

        ### add button ####
        Button2=tk.Button(self.window, **font, text='추가', width=10, command=self.addRent)
        Button2.grid(row=2, column=0, padx=5, pady=5)

    def search(self):
        self.controller.book_search()

    def showInfo(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.controller.shared_data['searched_book']:
            self.tree.insert("",tk.END, values=row)

    def addRent(self):
        columns=('bookId','title','author','genre','vol','rentId','rentDate','name')
        result=[]
        for item in self.tree.selection():
            result.append(dict(list(zip(columns, self.tree.item(item)['values']))))

        self.controller.shared_data['searched_book']=[i['bookId'] for i in  result]
        self.controller.shared_data['in_rent']=[item['rentId'] for item in result if item['rentId'] != 'None']

        if(len(self.controller.shared_data['in_rent']) > 0):
            self.chooseRentOption()
        else:
            self.controller.add_rent()
            self.window.destroy()

    def chooseRentOption(self):
        font = {'font': self.controller.main_font}
        rentOptionFrame=tk.Frame(self)
        self.option_win=tk.Toplevel(rentOptionFrame)
        tk.Label(self.option_win, **font, text="이미 대여중인 도서가 존재합니다. 회수처리 후 대여 진행할까요?").\
            grid(row=0,columnspan=2, padx=5, pady=5)
        tk.Button(self.option_win, **font, text='네', command=self.return_and_rent).grid(row=1,column=0, padx=5, pady=10)
        tk.Button(self.option_win, **font, text='아니요', command=self.destroy_win).grid(row=1,column=1, padx=5, pady=10)

    def destroy_win(self):
        self.option_win.destroy()

    def return_and_rent(self):
        # print(self.controller.shared_data['selected_member']['id'])
        # print(self.controller.shared_data['in_rent'])
        # print(self.controller.shared_data['searched_book'])
        self.destroy_win()
        self.controller.return_and_rent()
        self.window.destroy()


if __name__ == "__main__":
    app = Controller()
    app.mainloop()