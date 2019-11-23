#coding:utf-8

from Papers_grading.Papers_prepare import Papers_prepare
from Papers_grading.Papers_process import Paper_process
from Papers_grading.Page import Page

import tkinter as tk
import shutil


if __name__ == '__main__':
    #欢迎语
    def destory(page):
        page.destroy()

    welcom1 = tk.Tk()
    welcom1.geometry('600x300')
    welcom_lb1 = tk.Label(welcom1)
    welcom_lb1.config(text='欢迎使用该批改作业系统！！', font=('Arial', 20))
    welcom_lb1.place(relx=0.2, rely=0.4)
    bt = tk.Button(welcom1, text='确定',font=('Arial',15), command=lambda:destory(welcom1) )
    bt.place(relx=0.45, rely=0.8)
    welcom1.mainloop()


    #Page类page1方法
    page = Page()
    page.page1()

    #处理后的信息的返回
    path = page.path
    X_Name = page.X_Name
    X_answer = page.X_anwser
    X_point = page.X_point
    T_Names = page.T_Names
    P_Names = page.P_Names
    if X_Name != '':
        All_Names = [X_Name, ] + T_Names + P_Names
    else:
        All_Names = T_Names + P_Names




    #根据page1界面中的信息填入情况来判断是否要继续运行程序
    if path != '' and len(All_Names) != 0:

        #papers_prepare类
        papers_prepare = Papers_prepare(path, All_Names)
        papers_prepare.start()

        #处理后信息的返回
        tup = papers_prepare.get_numbers_dirs_ids_names()
        number = tup[0]

        #如果填入了填空题名或程序题名则进行第二个界面的显示
        if len(P_Names + T_Names) != 0:
            #page2方法
            dic_pingyu_all = {}
            dic_PT_grades = {}
            dic1 = {}
            dic2 = {}
            for i in range(number):
                dic1.update({str(i+1):''})
                dic2.update({str(i+1):0})
            for i in T_Names + P_Names:
                dic_pingyu_all.update({i:dic1.copy()})
                dic_PT_grades.update({i:dic2.copy()})

            page.page2(dic_PT_grades, dic_pingyu_all, number)

            #处理后信息的返回
            dic_pingyu_all = page.pingyu
            dic_PT_grades = page.PT_grades


            #分数等信息的最终处理
            papers_process = Paper_process(path, tup, X_Name, X_answer, X_point, P_Names + T_Names, dic_PT_grades, dic_pingyu_all)
            papers_process.start()




        #如果只填入了选择题名则执行另外一套方案
        if len(P_Names + T_Names) == 0 and X_Name != '':

            papers_process = Paper_process(path, tup, X_Name, X_answer, X_point)
            papers_process.X_grading()
            papers_process.write_grades()



        #调用删除文件方法，删除中间文件
        for name in All_Names:
            if name != '':
                shutil.rmtree(path + '/' + name)


    #结束语
    welcom2 = tk.Tk()
    welcom2.geometry('600x300')
    welcom_lb2 = tk.Label(welcom2)
    welcom_lb2.config(text='感谢使用该批改作业系统！！', font=('Arial',20))
    welcom_lb2.place(relx=0.2, rely=0.4)
    welcom_lb2.place(relx=0.2, rely=0.4)
    bt = tk.Button(welcom2, text='确定', font=('Arial', 15), command=lambda: destory(welcom2))
    bt.place(relx=0.45, rely=0.8)
    welcom2.mainloop()
