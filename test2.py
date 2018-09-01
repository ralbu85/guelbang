import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk

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
        'member_info': {'id':None, 'name':None, 'phone':None, 'address':None},
        'rent': None
        }

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

        self.frames = {}
        self.frames["SearchView"] = SearchView(parent=SearchContainer, controller=self)
        self.frames["MemberView"] = MemberView(parent=MemberContainer, controller=self)
        self.frames["RentView"] = RentView(parent=RentContainer, controller=self)

        self.frames["SearchView"].grid(row=0, column=0, sticky="nsw")
        self.frames["MemberView"].grid(row=0, column=0, sticky="nsw")
        self.frames["RentView"].grid(row=0, column=0, sticky="nsw")

        self.frames[""]


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def update_member(self):
        model = Model()
        name = self.shared_data['user_input'].get()
        self.shared_data['member_info'] = model.member_search(name)
        self.frames["MemberView"].update()
        self.update_rent()

    def update_rent(self):
        result=Model().rent_search(self.shared_data['member_info']['id'])
        self.shared_data['rent']=result
        self.frames["RentView"].update()




class Model():
    def __init__(self):
        self.con = sq.connect('guelbang.db')
        self.c = self.con.cursor()

    def member_search(self, user_input):
        query='SELECT * from MEMBER where Name = ?'
        param=(user_input,)
        self.c.execute(query, param)
        returned=self.c.fetchall()[0]

        result={}
        title=['id','name','phone','address']
        for i in range(len(title)):
            result[title[i]]=returned[i]

        return result

    def rent_search(self, member_id):
        query = 'SELECT RENT.Id, RentDate, Title, Vol, Genre, AUthor FROM RENT join BOOK on BOOK.Id=RENT.BookId where MemberId=?'
        param = (member_id,)
        self.c.execute(query, param)
        returned=self.c.fetchall()

        key=('id','rentdate','title','vol','genre','author','day')
        result=[]
        for row in returned:
            result.append(OrderedDict(tuple(zip(key,row))))

        for record in result:
            delta=datetime.datetime.now() - datetime.datetime.strptime(record['rentdate'], "%Y-%m-%d %H:%M:%S")
            record['day']=delta.days

        return result


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
        self.controller.update_member()


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
        self.name['text'] = self.controller.shared_data['member_info']['name']
        self.phone['text'] = self.controller.shared_data['member_info']['phone']
        self.address['text'] = self.controller.shared_data['member_info']['address']


class RentView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        style = ttk.Style()
        style.configure("Treeview", font=(None,12))
        style.configure("Treeview.Heading", font=(None, 14))


        self.tree=ttk.Treeview(self, height=15, column=('rent_date', 'title', 'vol', 'genre', 'author', 'days'),
                     show='headings')
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        ysb=ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns', pady=10)
        self.tree.configure(yscroll=ysb.set)

        nums=('#1','#2','#3','#4','#5','#6')
        names=('rent_date', 'title', 'vol', 'genre', 'author', 'days')
        text=('대여일','제목','권','장르','저자','경과일')
        width=(200,300,100,100,100,100)

        headings=[self.tree.heading(i,text=j) for i,j in list(zip(nums,text))]
        columns=[self.tree.column(i,width=j,anchor=tk.CENTER) for i,j in list(zip(names,width))]

    def update(self):

        keys = ['rentdate', 'title', 'vol', 'genre', 'author', 'day']
        for record in self.controller.shared_data['rent']:
            values=[record[key] for key in keys]
            self.tree.insert("",tk.END, values=values)




if __name__ == "__main__":
    app = Controller()
    app.mainloop()