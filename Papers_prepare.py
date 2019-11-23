import random
import re
import os

class Papers_prepare(object):
    def __init__(self, path, fileNames_all):
        self.path = path
        self.fileNames = fileNames_all

        self.dirs = []
        self.ids = []
        self.names = []
        self.all_numbers = 0
        self.number_dirs = {}
        self.number_ids = {}
        self.number_names = {}


    #从路径子目录名中获得学号与姓名
    def get_id_name(self):
        for root, dirs, files in os.walk(self.path):
            #只把子目录开头为’18‘的子目录名记录下来
            self.dirs = [dir for dir in dirs  if dir[0:2]=='18']
            pat_id = re.compile(r'\d{10}')
            pat_name = re.compile(r'[\u4e00-\u9fa5]+$')

            for dir in self.dirs:
                id = pat_id.findall(dir)
                self.ids.extend(id)
                name = pat_name.findall(dir)
                self.names.extend(name)
            break                           #只需要主目录下的子目录即可，所以循环一次就退出


    #构造序号与学生姓名，序号与学生ID，序号与子目录名 之间的对应关系，(并且对应关系是随机对应的，跟文件中的先后顺序无关)
    #顺便统计一下人数
    def number_id_name(self):
        self.all_numbers = len(self.names)
        ss = list(range(0,self.all_numbers))
        random.shuffle(ss)


        for i in range(1, self.all_numbers+1):
            dic_name = {i:self.names[ss[i-1]]}
            self.number_names.update(dic_name)

            dic_id = {i: self.ids[ss[i-1]]}
            self.number_ids.update(dic_id)

            dic_dir = {i:self.dirs[ss[i-1]]}
            self.number_dirs.update(dic_dir)


    #将每一位学生的文件中的文件统一复制到主目录下一个命名为filename文件夹中
    #并且在文件中的文件命名是以学生的序号来命名的
    #如果某些学生文件夹中不包含该文件，则在filename文件夹中创建一个空的文件
    def re_file(self):
        for fileName in self.fileNames:
            if fileName != ''and not os.path.exists(self.path + '/' + fileName):     #判断是否为空以及目录是否存在
                os.makedirs(self.path + '/' + fileName)
            for i in range(1, self.all_numbers+1):
                hou_zhui = os.path.splitext(fileName)[1]
                ff = open(self.path + '/' + fileName + '/' + str(i) + hou_zhui, 'wb')
                for root, dirs, files in os.walk(self.path + '/' + self.number_dirs[i]):
                    if fileName in files:
                        f = open(self.path + '/' + self.number_dirs[i] + '/' + fileName, 'rb')
                        answer = f.read()
                        ff.write(answer)
                        f.close()
                    else:
                        ff.write(b'')
                ff.close()



    # 将这些数据返回出去，后面会用到
    def get_numbers_dirs_ids_names(self):
        return self.all_numbers, self.number_dirs, self.number_ids, self.number_names


    #处理开始 函数
    def start(self):
        self.get_id_name()
        self.number_id_name()
        self.re_file()

        # print(self.fileNames)
        # print(self.dirs)
        # print(self.ids)
        # print(self.names)
        # print(self.all_numbers)
        # print(self.number_dirs)
        # print(self.number_ids)
        # print(self.number_names)


