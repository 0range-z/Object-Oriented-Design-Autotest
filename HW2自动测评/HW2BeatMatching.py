#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sympy
import random
from HW2_generator import generator
import re


def preprocess():
    FILE_LIST = []
    count = 0
    os.chdir("projects")
    for direc in os.listdir(os.getcwd()):
        count += 1
        os.chdir(direc)  # 进入子目录
        cwd = os.getcwd()
        # 寻找主类
        for file in os.listdir(cwd):
            if file.endswith(".class"):
                filedir = cwd + "\ ".strip() + file
                if file == "MainClass.class":
                    FILE_LIST.append(['MainClass', cwd, direc])
                # f=open(filedir,encoding='unicode_escape')
                # if (f.read().find("public static void main")):

                #    break
        # 分别编译
        '''
        for file in os.listdir(cwd):
            if (file.endswith(".java")):
                os.popen("javac "+file)
        '''
        os.chdir(os.path.dirname(cwd))  # 回到父目录
    return count, FILE_LIST


def autotest(FILE_LIST, NUMBER, ROUND):
    global WrongLog

    ANSWER_FORMAT = "([  ]*)(([+-]([  ]*))?(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*)([+-]([  ]*)(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*))*)"

    scorelist = [0 for i in range(NUM_PROJECTS)]
    for j in range(ROUND):
        lenlist = []
        fx = generator(NUMBER)
        while (re.match(ANSWER_FORMAT, fx) == None or len(fx) > 100):
            fx = generator(NUMBER)
        for i in range(NUM_PROJECTS):
            os.chdir(FILE_LIST[i][1])
            # print("\n\nTesting "+FILE_LIST[i][2]+"\n")
            length = test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)
            if type(length) == int:
                lenlist.append(length)
            else:
                lenlist.append(99999)
        print("完成第" + str(j + 1) + "次循环，本次性能分: ")
        Lmin = min(lenlist)
        for i in range(NUM_PROJECTS):
            if lenlist[i] not in [99999, Lmin]:
                x = lenlist[i] / Lmin
                if (x <= 1.3):
                    newscore = 100*(122.2893 * x ** 4 - 603.6553 * x ** 3 + 1122.8905 * x ** 2 - 934 * x + 293.4754)
                else:
                    newscore = 0
            elif lenlist[i] == 99999:
                newscore =  0
            elif lenlist[i] == Lmin:
                newscore =  100
            print(FILE_LIST[i][2] + ": " + str(newscore))
            scorelist[i] += newscore


    print("本轮测试完成，总性能分: ")
    for i in range(NUM_PROJECTS):
        print(FILE_LIST[i][2] + ": " + str(scorelist[i]))


def autotestRider(FILE_LIST, NUMBER, ROUND, ID):
    global WrongLog

    ANSWER_FORMAT = "([  ]*)(([+-]([  ]*))?(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*)([+-]([  ]*)(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*))*)"

    for j in range(ROUND):
        fx = generator(NUMBER)
        while (re.match(ANSWER_FORMAT, fx) == None or len(fx) > 100):
            fx = generator(NUMBER)
        for i in range(NUM_PROJECTS):
            if FILE_LIST[i][2] == ID:
                os.chdir(FILE_LIST[i][1])
                length = test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)

        print("完成第" + str(j + 1) + "次循环")


def test(NAME, DIR, ID, fx):
    global WrongLog
    os.chdir(DIR)
    x = sympy.Symbol('x')
    ANSWER_FORMAT = "([  ]*)(([+-]([  ]*))?(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*)([+-]([  ]*)(([+-]([  ]*))?(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+))(([  ]*)\*([  ]*)(((x(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(sin([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?)|(cos([  ]*)\(([  ]*)x([  ]*)\)(([  ]*)(\*\*([  ]*)([+-]?[0-9]+)))?))|([+-]?[0-9]+)))*)([  ]*))*)"
    try:
        myAnswer = os.popen('echo ' + fx + '|java ' + NAME)
        myAnswer = myAnswer.read().replace("\n", "")

        if (myAnswer == ""):
            print(ID + " =================Empty String!============\n" + fx + "(DATA)")
            print(ID + " =================Empty String!============\n" + fx + "(DATA)", file=WrongLog)
            return

        if (re.match(ANSWER_FORMAT, myAnswer) == None):
            print(
                ID + " ============Wrong Output Format!============\n" + myAnswer + "(your answer)\n" + fx + "(DATA)\n\n")
            print(
                ID + " ============Wrong Output Format!============\n" + myAnswer + "(your answer)\n" + fx + "(DATA)\n\n",
                file=WrongLog)
            return

        rNum = random.uniform(-10, 10)
        tureValue = sympy.diff(fx, 'x').evalf(subs={x: rNum})
        myValue = sympy.sympify(myAnswer).evalf(subs={x: rNum})
        if myValue == tureValue:
            print(ID + "  " + fx + ' correct')
            print("====answer:" + myAnswer + "====")
            return len(myAnswer)
            # print("====length:" + str(len(myAnswer)
        else:
            print(ID + " ===========Wrong Answer!=============\n" + fx + "\nyour answer: " + myAnswer)
            print(ID + " ===========Wrong Answer!=============\n" + fx + "\nyour answer: " + myAnswer, file=WrongLog)
            return
    except:
        print(ID + " =============Could not parse!===========\n" + fx + "(DATA)")
        print(ID + " =============Could not parse!===========\n" + fx + "(DATA)", file=WrongLog)
        return


if __name__ == "__main__":
    WrongLog = open("wrong_log.txt", "w")
    print("wrong_log:", file=WrongLog)
    print("BeatMatching")
    print("README: 将每个project放在'projects'目录下的不同文件夹中，每个文件夹包含若干.java文件")
    NUM_PROJECTS, FILE_LIST = preprocess()
    print("预处理完成")
    while True:
        a = input("输入1：自动生成数据\n输入2：手动输入数据\n输入3：自动测试Rider\n输入q：退出\n")
        while a not in ["1", "2", "3", "q"]:
            a = input("请重新输入\n")
        if a == "q":
            break
        elif a == "1":
            NUMBER = int(input("请输入项数\n"))
            ROUND = int(input("请输入循环次数\n"))
            autotest(FILE_LIST, NUMBER, ROUND)
            # for i in range(NUM_PROJECTS):
            #    print("\n\nTesting "+FILE_LIST[i][1]+"\n")
            #    autotest(FILE_LIST[i][0],FILE_LIST[i][1],FILE_LIST[i][2],NUMBER,ROUND)
        elif a == "2":
            fx = input("请输入fx\n")
            if (len(fx) > 100):
                print("长度大于100！")
                continue
            for i in range(NUM_PROJECTS):
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)
        elif a == "3":
            NUMBER = int(input("请输入项数\n"))
            ROUND = int(input("请输入循环次数\n"))
            autotestRider(FILE_LIST, NUMBER, ROUND, "Rider")
        print("一轮测试完成，报错信息见wrong_log.txt")
    WrongLog.close()
