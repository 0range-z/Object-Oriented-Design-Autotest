#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sympy
import random
from HW3_generator import generator
import time
# NUM_PROJECTS = 3
MODE = '.class'  # .java: compile and run    .class: run
FILE_NAME_LIST = ['MainClass']


def preprocess():
    FILE_LIST = []
    count = 0
    os.chdir("projects")
    for direc in os.listdir(os.getcwd()):
        if direc.startswith("."):
            continue
        os.chdir(direc)  # 进入子目录
        cwd = os.getcwd()
        # 寻找主类
        for fileName in os.listdir(cwd):
            if (direc == "Caster"):
                FILE_LIST.append(['UnitOneTaskThree', cwd, direc])
                count += 1
                break
            if fileName.endswith(MODE):
                if fileName in [x + MODE for x in FILE_NAME_LIST]:
                    FILE_LIST.append([fileName.split('.')[0], cwd, direc])
                    count += 1
        # 分别编译
        if (MODE == '.java'):
            for file in os.listdir(cwd):
                if file.endswith(".java"):
                    os.popen("javac " + file)
                time.sleep(0.5)
                print("done")
            print("compile single project done")
        os.chdir(os.path.dirname(cwd))  # 回到父目录
    return count, FILE_LIST


def autotest(FILE_LIST, LENGTH, ROUND):
    global WrongLog
    global falseCount

    sympyTotal = 0
    totallist = [0] * NUM_PROJECTS
    totalPerformance = [0]*NUM_PROJECTS
    for j in range(ROUND):
        lenlist = []
        fx = generator(LENGTH)
        print("\n"+fx)
        '''
        correctAnswer = str(sympy.simplify(sympy.diff(fx)))
        print("SYMPY  ".ljust(28) + correctAnswer)
        sympyLen = len(correctAnswer.replace(" ", ""))
        sympyTotal += sympyLen
        '''
        for i in range(NUM_PROJECTS):
            os.chdir(FILE_LIST[i][1])
            length = test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)
            if type(length) == int:
                lenlist.append(length)
            else:
                lenlist.append(100000)
        print("完成第" + str(j + 1) + "次循环，总共错误数：" + str(falseCount))
        for k in range(NUM_PROJECTS):
            totallist[k] += lenlist[k]
            singlePerformance = calculatePerformance(lenlist,k)
            totalPerformance[k] += singlePerformance
            string = FILE_LIST[k][2].ljust(6) + "本轮长度: " + str(lenlist[k])
            print(string.ljust(20) + "本轮性能分: " + str(singlePerformance))
        for k in range(NUM_PROJECTS):
            string = FILE_LIST[k][2].ljust(6) + "总长度: " + str(totallist[k])
            print(string.ljust(20) + "总性能分: " + str(totalPerformance[k]))


        # string = "SYMPY".ljust(6) + '总长度: ' + str(sympyTotal)
        # print(string.ljust(20) + "本轮长度: " + str(sympyLen) + "\n")

def calculatePerformance(lenlist,i):
    Lp = lenlist[i]
    Lmin = min(lenlist)
    Lmax = max(lenlist)
    Lavg = sum(lenlist) / len(lenlist)
    base_min = 0.25 * Lavg + 0.75 * Lmin
    base_max = 0.25 * Lmax + 0.75 * Lavg
    if Lp <= base_min:
        return 1
    if Lp > base_max:
        return 0
    return 1 - 10**(1 - (base_max-base_min)/(Lp-base_min) )


def autotestRider(FILE_LIST, LENGTH, ROUND, ID):
    global WrongLog
    global falseCount

    for j in range(ROUND):
        fx = generator(LENGTH)
        print(fx)
        for i in range(NUM_PROJECTS):
            if FILE_LIST[i][2] == ID:
                os.chdir(FILE_LIST[i][1])
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)

        print("完成第" + str(j + 1) + "次循环，总共错误数：" + str(falseCount))


def test(NAME, DIR, ID, fx):
    global WrongLog
    global falseCount

    os.chdir(DIR)
    x = sympy.Symbol('x')
    #try:
    myAnswer = os.popen('echo ' + fx + '|java ' + NAME)
    myAnswer = myAnswer.read().split("\n")[0]

    if (myAnswer == ""):
        print(ID + " Empty String!".center(50,"=") + "\n" + fx + "(DATA)")
        print(ID + " Empty String!".center(50,"=") + "\n" + fx + "(DATA)", file=WrongLog)
        falseCount += 1
        return
    if (myAnswer == "WRONG FORMAT!"):
        print(ID + " WRONG FORMAT!".center(50,"=") + "\n" + fx + "(DATA)")
        print(ID + " WRONG FORMAT!".center(50,"=") + "\n" + fx + "(DATA)", file=WrongLog)
        falseCount += 1
        return
    rNum = random.uniform(-10, 10)
    ##############
    ##############
    tureValue = sympy.diff(fx, 'x').evalf(subs={x: rNum})
    myValue = sympy.sympify(myAnswer).evalf(subs={x: rNum})

    if myValue == tureValue:
        print(ID.ljust(10) + " correct!  Answer:" + myAnswer)
        return len(myAnswer.replace(" ", ""))
    # elif sympy.simplify(sympy.diff(fx, 'x')).equals(sympy.simplify(myAnswer)) :
    # print(ID.ljust(10) + " correct!  Answer:" + myAnswer)
    #    return len(myAnswer.replace(" ", ""))
    else:
        print(ID + " Wrong Answer!".center(50,"=") + "\n" + "your answer: " + myAnswer)
        print(ID + " Wrong Answer!".center(50,"=") + "\n" + "your answer: " + myAnswer + "\nDATA: " + fx, file=WrongLog)
        falseCount += 1
        return
    #except:
    #    print(ID + " Sympy Cannot Parse!".center(50,"=") + fx + "\n" + "your answer: " + myAnswer)
    #    print(ID + " Sympy Cannot Parse!".center(50,"=") + fx + "\n" + "your answer: " + myAnswer + "\nDATA: " + fx, file=WrongLog)
    #    falseCount += 1
    #    return


if __name__ == "__main__":
    WrongLog = open("wrong_log.txt", "w")
    falseCount = 0
    print("wrong_log:", file=WrongLog)
    print("BeatMatching")
    print("README: 将每个project放在'projects'目录下的不同文件夹中，每个文件夹包含若干.java文件")
    # NUM_PROJECTS, FILE_LIST = preprocess()
    NUM_PROJECTS, FILE_LIST = preprocess()
    print("预处理完成，测试对象：")
    for i in FILE_LIST:
        print(i[2], end=" ")
    print()
    while True:
        a = input("输入1：自动生成数据\n输入2：手动输入数据\n输入3：文件读入数据\n输入4：测试特定目标\n输入q：退出\n")
        while a not in ["1", "2", "3", "4", "q"]:
            a = input("请重新输入\n")
        if a == "q":
            break
        elif a == "1":
            LENGTH = int(input("请输入长度\n"))
            ROUND = int(input("请输入循环次数\n"))
            try:
                autotest(FILE_LIST, LENGTH, ROUND)
            except KeyboardInterrupt:
                print("Interrupt")
                WrongLog.close()
        elif a == "2":
            fx = input("请输入fx\n")
            #if (len(fx) > 60):
            #    print("长度大于60！")
            #    continue
            for i in range(NUM_PROJECTS):
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)
        elif a == "3":
            print("从文件in.txt读入")
            os.chdir(os.path.dirname(os.getcwd()))
            fin = open("in.txt", "r")
            os.chdir("projects")
            for line in fin.readlines():
                fx = line.replace("\n", "")
                if fx == "":
                    continue
                if fx == "END":
                    break
                print(fx)
                for i in range(NUM_PROJECTS):
                    test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], fx)
                print()
            fin.close()
        elif a == "4":
            NAME = input("请输入目标名称\n")
            LENGTH = int(input("请输入长度\n"))
            ROUND = int(input("请输入循环次数\n"))
            autotestRider(FILE_LIST, LENGTH, ROUND, NAME)
        print("一轮测试完成，报错信息见wrong_log.txt")
    WrongLog.close()
