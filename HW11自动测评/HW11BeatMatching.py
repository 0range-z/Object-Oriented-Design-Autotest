#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import time
from HW11_generator import generate

MODE = '.jar'  # .java: compile and run    .class .jar: run
FILE_NAME_LIST = ['Archer', 'Assassin', 'Berserker', 'Caster', 'Lancer', 'Me', 'Saber']


def preprocess():
    FILE_LIST = []
    count = 0
    os.chdir("projects")
    for direc in os.listdir(os.getcwd()):
        if direc.startswith("."):  #######
            continue
        os.chdir(direc)  # 进入子目录
        cwd = os.getcwd()
        # 寻找主类
        for fileName in os.listdir(cwd):
            if fileName.endswith(MODE):
                if fileName in [x+MODE for x in FILE_NAME_LIST]:
                    FILE_LIST.append([fileName.split('.')[0], cwd, direc])
                    count += 1
        # 分别编译
        '''
        if MODE == '.java':
            for file in os.listdir(cwd):
                if file.endswith(".java"):
                    os.popen("javac "+file)
                sleep(0.5)
                print("done")
            print("compile single project done")
        '''
        os.chdir("..")  # 回到父目录
    return count, FILE_LIST


def autotest(FILE_LIST, LENGTH, ROUND, PEOPLE):
    global WrongLog
    global falseCount

    for j in range(ROUND):
        data = generate(LENGTH, PEOPLE)
        for i in range(NUM_PROJECTS):
            os.chdir(FILE_LIST[i][1])
            test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data)
        check(data)
        WrongLog.flush()
        print("完成第"+str(j+1)+"次循环，总共错误数："+str(falseCount))


def test(NAME, DIR, ID, data):
    global WrongLog
    global falseCount

    print("Testing "+ID)

    os.chdir(DIR)
    #print(data.replace("\n"," "))
    if MODE == ".jar":
        proc = os.popen('java -jar {0}.jar > ../../{1}_out.txt'.format(NAME, ID), 'w')
    else:
        proc = os.popen('java {0} > ../../{1}_out.txt'.format(NAME, ID), 'w')
    #print(data.replace("\n", " "))
    a = time()
    proc.write(data)
    #print(data.replace("\n", " "))
    proc.flush()
    proc.close()
    b=time()
    print("time: {}s".format(b-a))
    print(ID+' Done')


def check(data):
    global falseCount
    os.chdir("../..")
    print("checking".center(20, "-"))

    all_flag = True
    for i in FILE_LIST:
        flag = True
        for j in FILE_LIST:
            fout = open(i[2]+"_out.txt")
            out_lines = fout.readlines()
            fout.close()
            fout2 = open(j[2]+"_out.txt")
            out_lines2 = fout2.readlines()
            fout2.close()
            if out_lines != out_lines2:
                print("DIFFERENT {} {}".format(i[2], j[2]).center(30, "="))
                print("DIFFERENT {} {}".format(i[2], j[2]).center(30, "="), file=WrongLog)
                print(data, file=WrongLog)
                print(30*"-")
                WrongLog.flush()
                input()
                flag = False
                all_flag = False
                falseCount += 1
        if flag:
            print('{} correct'.format(i[2]))
    if all_flag:
        print("all correct".center(20, "-"))

    #os.chdir("projects")


if __name__ == "__main__":
    falseCount = 0
    WrongLog = open('wrong_log.txt', "w")
    time_dict = {}

    print("wrong_log:", file=WrongLog)
    print("BeatMatching")
    print("README: 将每个project放在'projects'目录下的不同文件夹中，每个文件夹包含若干.jar文件")
    print("修改FILE_NAME_LIST为你的.jar名")
    NUM_PROJECTS, FILE_LIST = preprocess()
    for i in FILE_LIST:
        time_dict[i[2]] = 0
    print("\n预处理完成，测试对象：")
    for i in FILE_LIST:
        print(i[2], end=" ")
        time_dict[i[2]] = 0
    print()
    while True:
        a = input("输入1：自动生成数据\n输入2：文件读入数据\n输入q：退出\n")
        while a not in ["1", "2", "q"]:
            a = input("请重新输入\n")
        if a == "q":
            break
        elif a == "1":
            PEOPLE = int(input("请输入人数\n"))
            LENGTH = int(input("请输入长度\n"))
            ROUND = int(input("请输入循环次数\n"))
            try:
                autotest(FILE_LIST, LENGTH, ROUND, PEOPLE)
            except KeyboardInterrupt:
                print("Interrupt")
                WrongLog.close()
            os.chdir("projects")
        elif a == "2":
            print("从文件in.txt读入")
            os.chdir("..")
            fin = open("in.txt", "r")
            os.chdir("projects")
            lines = fin.readlines()
            fin.close()
            data_in = ""
            for line in lines:
                if line == "\n":
                    continue
                if line == "END\n":
                    break
                data_in += line
            for i in range(NUM_PROJECTS):
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data_in)
            check(data_in)
            WrongLog.flush()
            os.chdir("projects")

        print("一轮测试完成，报错信息见wrong_log.txt")
    WrongLog.close()