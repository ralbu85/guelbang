from tkinter import *

class Wages():

    def __init__(self, master):

        self.nhours=DoubleVar()
        self.salaryh=DoubleVar()

        self.master=master
        self.master.geometry('500x200+100+200')
        self.master.title('회원관리')

        self.label1=Label(self.master, text='회원관리', fg='green').grid(row=0, column=2)
        self.label2=Label(self.master, text='Enter your salary per hour', fg='red').grid(row=3, column=0)
        self.label3=Label(self.master, text='Enter the number of hours worked', fg='red').grid(row=4, column=0)

        self.mysalary=Entry(self.master, textvariable=self.salaryh).grid(row=3, column=2)
        self.myhours=Entry(self.master, textvariable=self.nhours).grid(row=4, column=2)
        self.button1=Button(self.master, text='Calculate Salary', fg='blue', command=self.calculatesalary).grid(row=5, column=2)
        self.button2=Button(self.master, text='Back', fg='blue', command=self.myquit).grid(row=5, column=3)

    def calculatesalary(self):
        hours=self.nhours.get()
        print(hours)
        hsal=self.salaryh.get()
        salary=hours*hsal
        print(salary)
        self.labelresult=Label(self.master, text='your salary is: %.2f euro' % salary).grid(row=7, column=2)

    def myquit(self):
        self.master.destroy()
