from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import ttk
import tkinter as tk
import os

#页面的显示
class Page():
    def __init__(self):
        self.path = ''
        self.X_Name = ''
        self.X_anwser = ''
        self.X_point = 0
        self.T_Names = []
        self.P_Names = []

        self.dic_PT_grades = {}
        self.dic_pingyu = {}



    def page1(self):
        def ask_directory():
            path = askdirectory()
            path_var.set(path)
            self.path = path

        def ask_filename():
            fileName = askopenfilename()
            if fileName != '':
                with open(fileName, 'r') as f:
                    self.X_anwser = f.read()
            txt_answer_Entry.insert(0, self.X_anwser)

        def to_page2():
            if txt_Entry.get() != '':
                self.X_Name = txt_Entry.get() + '.txt'
            if txt_answer_Entry2.get() != '':
                self.X_point = int(txt_answer_Entry2.get())
            if len(T_Entry.get(0.0, tk.END)) != 1:
                T_Names = T_Entry.get(0.0, tk.END).split('\n')[:-1]
                self.T_Names = [x + '.txt' for x in T_Names if x != '']
            if len(P_Entry.get(0.0, tk.END)) != 1:
                P_Names = P_Entry.get(0.0, tk.END).split('\n')[:-1]
                self.P_Names = [x + '.py' for x in P_Names if x != '']
            root.destroy()



        root = tk.Tk()
        root.title('自动批改作业')
        root.geometry('1000x700')

        path_lb = tk.Label(root, text='作业所在目录：', font=('Arial',15))
        path_var = tk.StringVar(root)
        path_Entry = tk.Entry(root, textvariable=path_var, state='readonly')
        path_Button = tk.Button(root, text='选择', command=ask_directory)
        path_lb.place(relx=0.05, rely=0.4)
        path_Entry.place(relx=0.05, rely=0.45, relwidth=0.1)
        path_Button.place(relx=0.15, rely=0.45)

        txt_lb = tk.Label(root, text='选择题', font=('Arial',15))
        txt_lb2 = tk.Label(root, text='文件名：', font=('Arial',10))
        txt_Entry = tk.Entry(root)
        txt_lb.place(relx=0.30, rely=0.2)
        txt_Entry.place(relx=0.38,rely=0.25,relwidth=0.1)
        txt_lb2.place(relx=0.30, rely=0.25)

        T_lb = tk.Label(root, text='填空题', font=('Arial', 15))
        T_lb2 = tk.Label(root, text='文件名：', font=('Arial', 10))
        T_Entry = tk.Text(root)
        T_lb.place(relx=0.30, rely=0.4)
        T_Entry.place(relx=0.38, rely=0.45, relwidth=0.1, relheight=0.1)
        T_lb2.place(relx=0.30, rely=0.45)

        P_lb = tk.Label(root, text='程序题', font=('Arial', 15))
        P_lb2 = tk.Label(root, text='文件名：', font=('Arial', 10))
        P_Entry = tk.Text(root)
        P_lb.place(relx=0.30, rely=0.6)
        P_Entry.place(relx=0.38, rely=0.65, relwidth=0.1, relheight=0.1)
        P_lb2.place(relx=0.30, rely=0.65)


        txt_anwser_lb = tk.Label(root, text='标准答案：', font=('Arial',10))
        txt_answer_Entry = tk.Entry(root, textvariable=self.X_anwser)
        txt_answer_Button = tk.Button(root, text='选择', command=ask_filename)
        txt_anwser_lb2 = tk.Label(root, text='每题分值：', font=('Arial', 10))
        txt_answer_Entry2 = tk.Entry(root)
        txt_anwser_lb.place(relx=0.6, rely=0.15)
        txt_answer_Entry.place(relx=0.67, rely=0.15, relwidth=0.1)
        txt_answer_Button.place(relx=0.75, rely=0.15)
        txt_anwser_lb2.place(relx=0.6, rely=0.3)
        txt_answer_Entry2.place(relx=0.67, rely=0.3, relwidth=0.05)

        ps_lb = tk.Label(root, text='PS1：文件名无需带后缀名', font=('Arial',10), fg='red')
        ps_lb2 = tk.Label(root, text='PS2：选择题文件名只能写一个', font=('Arial',10), fg='red')
        ps_lb3 = tk.Label(root, text='PS3：填空题、程序题为多个文件时，每个文件名各占一行', font=('Arial',10), fg='red')
        #ps_lb4 = tk.Label(root, text='PS3：不需要所有空都填满', font=('Arial', 10), fg='red')
        ps_lb.place(relx=0.07, rely=0.77)
        ps_lb2.place(relx=0.07, rely=0.82)
        ps_lb3.place(relx=0.07, rely=0.87)
        #ps_lb4.place(relx=0.07, rely=0.92)


        xiayibu_Button = tk.Button(root, text='下一步', font=('Arial',20), command=to_page2)
        xiayibu_Button.place(relx=0.8, rely=0.8)



        root.mainloop()




    def page2(self, grades, pingyu, number):
        def running(filepath):
            print(self.path + '/' + filepath + '.py')
            os.system(self.path + '/' + filepath + '.py')

        def toOne():
            self.pingyu[cmb_var.get()][str(xuhao_var.get())] = pingyu_text.get(0.0, tk.END)[:-1]
            sign = 1
            try:
                self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = float(grade_var.get())
            except:
                if simpledialog.messagebox.askyesno('错误', '分值的格式有误！！,是否重新输入，取消则按0分计') == False:
                    self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = 0.0
                    sign = 1
                else:
                    sign = 0
            if sign == 1:
                xuhao_var.set(1)
                content.delete(0.0, tk.END)
                content.insert(0.0, open(self.path + '/' + cmb_var.get() + '/' + xuhao_Entry.get() + '.py', 'rb').read().decode())
                content.update()
                pingyu_text.delete(0.0, tk.END)
                if self.pingyu[cmb_var.get()][str(xuhao_var.get())] != '':
                    pingyu_text.insert(tk.INSERT, self.pingyu[cmb_var.get()][str(xuhao_var.get())])
                pingyu_text.update()
                grade_var.set(self.PT_grades[cmb_var.get()][str(xuhao_var.get())])

        def change(event):
            xuhao_var.set(1)
            content.delete(0.0, tk.END)
            content.insert(0.0, open(self.path + '/' + cmb_var.get() + '/' + xuhao_Entry.get() + '.py', 'rb').read().decode())
            content.update()
            pingyu_text.delete(0.0, tk.END)
            if self.pingyu.get(cmb_var.get()).get(str(xuhao_var.get())) != '':
                pingyu_text.insert(tk.INSERT, self.pingyu[cmb_var.get()][str(xuhao_var.get())])
                pingyu_text.update()
            grade_var.set(self.PT_grades[cmb_var.get()][str(xuhao_var.get())])

        def nextPage():
            self.pingyu[cmb_var.get()][str(xuhao_var.get())] = pingyu_text.get(0.0, tk.END)[:-1]
            sign = 1
            try:
                self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = float(grade_var.get())
            except:
                if simpledialog.messagebox.askyesno('错误', '分值的格式有误！！,是否重新输入，取消则按0分计') == False:
                    self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = 0.0
                    sign = 1
                else:
                    sign = 0
            if sign == 1:
                if xuhao_var.get() != number:
                    content.delete(0.0, tk.END)
                    xuhao_var.set(xuhao_var.get() + 1)
                    content.insert(0.0, open(self.path + '/' + cmb_var.get() + '/' + xuhao_Entry.get() + '.py', 'rb').read().decode())
                    content.update()
                    pingyu_text.delete(0.0, tk.END)
                    if self.pingyu[cmb_var.get()][str(xuhao_var.get())] != '':
                        pingyu_text.insert(tk.INSERT, self.pingyu[cmb_var.get()][str(xuhao_var.get())])
                    pingyu_text.update()
                    grade_var.set(self.PT_grades[cmb_var.get()][str(xuhao_var.get())])

                else:
                    simpledialog.messagebox.showerror('错误', '当前已是最后一页！！')


        def lastPage():
            self.pingyu[cmb_var.get()][str(xuhao_var.get())] = pingyu_text.get(0.0, tk.END)[:-1]
            sign = 1
            try:
                self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = float(grade_var.get())
            except:
                if simpledialog.messagebox.askyesno('错误', '分值的格式有误！！,是否重新输入，取消则按0分计') == False:
                    self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = 0.0
                    sign = 1
                else:
                    sign = 0
            if sign == 1:
                if xuhao_var.get() != 1:
                    content.delete(0.0, tk.END)
                    xuhao_var.set(xuhao_var.get() - 1)
                    content.insert(0.0, open(self.path + '/' + cmb_var.get() + '/' + xuhao_Entry.get() + '.py', 'rb').read().decode())
                    content.update()
                    pingyu_text.delete(0.0, tk.END)
                    if self.pingyu[cmb_var.get()][str(xuhao_var.get())] != '':
                        pingyu_text.insert(tk.INSERT, self.pingyu[cmb_var.get()][str(xuhao_var.get())])
                    pingyu_text.update()
                    grade_var.set(self.PT_grades[cmb_var.get()][str(xuhao_var.get())])
                else:
                    simpledialog.messagebox.showerror('错误', '当前已是第一页！！')


        def finishi():
            self.pingyu[cmb_var.get()][str(xuhao_var.get())] = pingyu_text.get(0.0, tk.END)[:-1]
            sign = 1
            try:
                self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = float(grade_var.get())
            except:
                if simpledialog.messagebox.askyesno('错误', '分值的格式有误！！,是否重新输入，取消则按0分计') == False:
                    self.PT_grades[cmb_var.get()][str(xuhao_var.get())] = 0.0
                    sign = 1
                else:
                    sign = 0
            if sign == 1:
                root.destroy()

                # print(self.path)
                # print(self.X_Name)
                # print(self.X_anwser)
                # print(self.X_point)
                # print(self.T_Names)
                # print(self.P_Names)
                # print(self.dic_PT_grades)
                # print(self.dic_pingyu)


        root = tk.Tk()
        root.title('自动批改作业')
        root.geometry('800x700')

        ss = self.T_Names+self.P_Names
        self.PT_grades = grades
        self.pingyu = pingyu
        try:
            cmb_var = tk.StringVar(root,ss[0])
        except:
            cmb_var = tk.StringVar()
        cmb = ttk.Combobox(root,textvariable=cmb_var, values=ss)
        cmb.bind('<<ComboboxSelected>>', change)
        cmb.place(relx=0.13, rely=0.05, relwidth=0.15)
        cmb_name = tk.Label(root, text='作业名：')
        cmb_name.place(relx=0.05, rely=0.05)

        xuhao_lb = tk.Label(root, text='序号：', font=('Arial',20))
        xuhao_var = tk.IntVar(root, value=1)
        xuhao_Entry = tk.Entry(root,textvariable=xuhao_var,font=('Arial',20), state='readonly')
        xuhao_lb.place(relx=0.35, rely=0.05)
        xuhao_Entry.place(relx=0.45, rely=0.05, relwidth=0.1)
        xuhao_Button = tk.Button(root, text='至第一张', command=toOne)
        xuhao_Button.place(relx=0.51, rely=0.05, relheight=0.05)

        grade_lb = tk.Label(root, text='输入分值：', fg='red', font=('Arial',15))
        grade_var = tk.IntVar(root, value=0)
        grade_Entry = tk.Entry(root, textvariable=grade_var)
        grade_lb.place(relx=0.65, rely=0.05)
        grade_Entry.place(relx=0.80, rely=0.05, relwidth=0.1, relheight=0.05)

        content = tk.Text(root)
        content.place(relx=0.05, rely=0.15, relheight=0.7)
        content.insert(0.0, open(self.path + '/' + cmb_var.get()+'/'+xuhao_Entry.get() + '.py', 'rb').read().decode())

        pingyu_lb = tk.Label(root, text='输入评语：', fg='red', font=('Arial',15))
        pingyu_text = tk.Text(root)
        pingyu_lb.place(relx=0.78, rely=0.1)
        pingyu_text.place(relx=0.8, rely=0.15, relheight=0.7, relwidth=0.15)

        running_lb = tk.Label(root, text='程序题测试:', font=('Arial',15) )
        running_Button = tk.Button(root, text='运行', command=lambda: running(cmb_var.get()+'/'+xuhao_Entry.get()))
        running_lb.place(relx=0.05, rely=0.9)
        running_Button.place(relx=0.2, rely=0.9, relwidth=0.1, relheight=0.08)

        last_Button = tk.Button(root, text='上一张', command=lastPage)
        last_Button.place(relx=0.4, rely=0.9, relwidth=0.1, relheight=0.08)

        next_Button = tk.Button(root, text='下一张', command=nextPage)
        next_Button.place(relx=0.50, rely=0.9, relwidth=0.1, relheight=0.08)


        finish_Button = tk.Button(root, text='结束阅卷',fg='red', font=('Arial',15), command=finishi)
        finish_Button.place(relx=0.8, rely=0.9, relwidth=0.1, relheight=0.08)


        root.mainloop()

