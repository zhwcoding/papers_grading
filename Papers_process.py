import re

#作业的计分与情况反馈，以及将评语（非空）写入到每个人的文件夹中
class Paper_process(object):
    def __init__(self,path,tup, X_Name, X_answer, every_X_point, PT_Names=[], dic_PT_grades={}, dic_pingyu_all={}):
        self.path = path
        self.number = tup[0]
        self.n_dirs = tup[1]
        self.n_ids = tup[2]
        self.n_names = tup[3]
        self.X_Name = X_Name
        self.PT_Names = PT_Names
        self.X_standard = X_answer.upper()
        self.every_X_point = every_X_point
        self.dic_PT_grades = dic_PT_grades
        self.dic_pingyu_all = dic_pingyu_all
        self.X_grades = [0]*self.number
        self.PT_grades = [0]*self.number
        self.total_grades = [0]*self.number
        self.X_feedback = []
        self.PT_feedback = []

    #选择题计分与反馈信息
    #把答案统一成大写，以免造成误判
    def X_grading(self):
        pat = re.compile('[A-D _-]',re.I)
        for x in range(1, self.number + 1):
            if self.X_Name != '':
                f = open(self.path + '/' + self.X_Name + '/' + str(x) + '.txt', 'r')
                answer = f.read().upper()
                _result = pat.findall(answer)
                if len(_result) <= len(self.X_standard):
                    for i in range(len(self.X_standard)-len(_result)):
                        _result.append(' ')
                result = ''
                for i in _result:
                    result += i

                grades = 0
                feedback = []
                for i in range(len(self.X_standard)):
                    if result[i] == self.X_standard[i]:
                        feedback.append('√')
                        grades += self.every_X_point
                    else:
                        feedback.append('X')
                self.X_feedback.append(feedback)
                self.X_grades[x-1] = grades
            else:
                pass
                #simpledialog.messagebox.showerror('错误', '打开文件失败')

    #非选择题题计分
    def PT_grading(self):
        for i in range(self.number):
            feedbck = []
            grade = 0
            for name in self.PT_Names:
                grade += self.dic_PT_grades[name][str(i+1)]
                feedbck.append(str(self.dic_PT_grades[name][str(i+1)]))
            self.PT_grades[i] = grade
            self.PT_feedback.append(feedbck)

    #.评语的写入
    def Pingyu_grading(self):
        for i in range(self.number):
            f = open(self.path + '/' + self.n_dirs[i+1] + '/' + '评语.txt', 'w')
            for name in self.PT_Names:
                f.write(name + '：\n' + self.dic_pingyu_all[name][str(i+1)] + '\n')
            f.close()

    #将成绩汇总写入到主目录下的csv文件中
    #选择题的反馈写入主目录下另一个csv文件中
    def write_grades(self):
        for i in range(self.number):
            self.total_grades[i] = self.X_grades[i] + self.PT_grades[i]
        kong = ['','']
        ave = ['0000000000', '\t平均']
        data_all = [['    学号','\t姓名','\t总分','\t选择题得分','\t非选择题得分']]
        for i in range(self.number):
            data = [str(self.n_ids[i + 1]), str(self.n_names[i + 1]), str(self.total_grades[i]), str(self.X_grades[i]), \
                    str(self.PT_grades[i])]
            data_all.append(data)

        sum1 = 0
        sum2 = 0
        sum3 = 0
        for i in range(self.number):
            sum1 += self.total_grades[i]
            sum2 += self.X_grades[i]
            sum3 += self.PT_grades[i]
        ave.append(str('%.2f'%(sum1/self.number)))
        ave.append(str('%.2f'%(sum2/self.number)))
        ave.append(str('%.2f'%(sum3/self.number)))
        data_all.append(kong)
        data_all.append(ave)
        for i in range(len(self.X_feedback)):
            self.X_feedback[i].insert(0, str(self.n_names[i+1]))
            self.X_feedback[i].insert(0, str(self.n_ids[i+1]))
        for i in range(len(self.PT_feedback)):
            self.PT_feedback[i].insert(0, str(self.n_names[i+1]))
            self.PT_feedback[i].insert(0, str(self.n_ids[i+1]))

        biao_tou1 = ['    学号', '\t姓名']
        all_biaotou1 = ['0000000000', '\t答对的人数']
        for i in range(len(self.X_standard)):
            biao_tou1.append('\t第'+str(i+1)+'题')
            count = 0
            for j in range(self.number):
                if self.X_feedback[j][i+2] == '√':
                    count += 1
            all_biaotou1.append(str(count))
        self.X_feedback.insert(0, biao_tou1)
        self.X_feedback.append(kong)
        self.X_feedback.append(all_biaotou1)
        biao_tou2 = ['    学号', '\t姓名']
        ave_biaotou2 = ['0000000000', '\t平均']
        for i in range(len(self.PT_Names)):
            biao_tou2.append('\t'+self.PT_Names[i])
            sum = 0
            for j in range(self.number):
                sum += float(self.PT_feedback[j][i+2])
            ave_biaotou2.append(str('%.2f'%(sum/self.number)))
        self.PT_feedback.insert(0, biao_tou2)
        self.PT_feedback.append(kong)
        self.PT_feedback.append(ave_biaotou2)


        f = open(self.path + '/总_成绩.csv', 'w')
        for row in data_all:
            f.write(',\t'.join(row) + '\n')
        f.close()

        ff = open(self.path + '/选择题_反馈.csv', 'w')
        for row in self.X_feedback:
            ff.write(',\t'.join(row) + '\n')
        ff.close()

        fff = open(self.path + '/非选择题_反馈.csv', 'w')
        for row in self.PT_feedback:
            fff.write(',\t'.join(row) + '\n')
        fff.close()


    #计分开始函数
    def start(self):
        self.X_grading()
        self.PT_grading()
        self.Pingyu_grading()
        self.write_grades()


