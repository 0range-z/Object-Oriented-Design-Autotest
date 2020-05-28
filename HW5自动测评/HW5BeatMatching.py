#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import sleep
from threading import Thread
from HW5_generator import generate
from HW5_judger import judge, time_judger, calculate_base_time

# NUM_PROJECTS = 3
MODE = '.jar'  # .java: compile and run    .class .jar: run
FILE_NAME_LIST = ['homework5', 'Me']
MULTI_THREAD = False


class TestThread(Thread):
    def __init__(self, name, dir, id, data):
        Thread.__init__(self)
        self.name = name
        self.dir = dir
        self.id = id
        self.data = data

    def run(self):
        test(self.name, self.dir, self.id, self.data)


def preprocess():
    FILE_LIST = []
    count = 0
    os.chdir("projects")
    for direc in os.listdir(os.getcwd()):
        if direc.startswith(".") or direc.startswith("w") or direc.startswith("j"): #######
            continue
        os.chdir(direc)  # 进入子目录
        cwd = os.getcwd()
        # 寻找主类
        for fileName in os.listdir(cwd):
            if fileName.endswith(MODE):
                if fileName in [x + MODE for x in FILE_NAME_LIST]:
                    FILE_LIST.append([fileName.split('.')[0], cwd, direc])
                    count += 1
        # 分别编译
        if MODE == '.java':
            for file in os.listdir(cwd):
                if file.endswith(".java"):
                    os.popen("javac " + file)
                sleep(0.5)
                print("done")
            print("compile single project done")
        os.chdir("..")  # 回到父目录
    return count, FILE_LIST


def autotest(FILE_LIST, LENGTH, ROUND):
    global WrongLog
    global falseCount

    for j in range(ROUND):
        data = generate(LENGTH)
        thread_list = []
        if MULTI_THREAD:
            for i in range(NUM_PROJECTS):
                os.chdir(FILE_LIST[i][1])

                thread = TestThread(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data)
                thread.start()
                thread_list.append(thread)
            for thread in thread_list:
                thread.join()
        else:
            for i in range(NUM_PROJECTS):
                os.chdir(FILE_LIST[i][1])
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data)
        check(data)
        print("完成第" + str(j + 1) + "次循环，总共错误数：" + str(falseCount))


def test(NAME, DIR, ID, data):
    global WrongLog
    global falseCount

    os.chdir("../..")
    #makeup_time = 168 - calculate_base_time(data, {"base": 0, "max": 0})[1]

    pipe = []
    for line in data:
        if line == "END\n":
            break
        if line == "\n":
            continue
        time, command = line[1:].split(']')
        pipe.append((float(time), command))
    curr = 0.0

    os.chdir(DIR)

    if MODE == ".jar":
        proc = os.popen('java -jar {0}.jar > ../../{1}_out.txt'.format(NAME, ID), 'w')
    else:
        proc = os.popen('java {0} > ../../{1}_out.txt'.format(NAME, ID), 'w')
    for (time, command) in pipe:
        print("[" + str(time) + "]" + command, end="")
        sleep((time - curr) / 1.0)
        curr = time
        proc.write(command)
        proc.flush()
    print("waiting for " + ID + " to finish...")
    proc.close()
    print(ID + ' Done')


def check(data):
    global falseCount
    global time_dict
    os.chdir("../..")
    print("checking".center(20,"-"))
    max_time, base_time = calculate_base_time(data, time_dict)
    if max_time == 0:
        print("WRONG DATA!")
        return
    for i in FILE_LIST:
        fout = open(i[2] + "_out.txt")
        out_lines = fout.readlines()
        fout.close()
        if judge(out_lines, data) and time_judger(out_lines, max_time, base_time, i[2], time_dict, WrongLog):
            print(i[2] + " correct! Total time: " + str(time_dict[i[2]]))

        else:
            dt = ""
            for line in data:
                if line == "END\n":
                    break
                if line == "\n":
                    continue
                dt += line
            print(i[2] + " WRONG".center(20, "="))
            print(i[2] + " WRONG".center(20, "=") + "\ndata:\n" + dt, file=WrongLog)
            falseCount += 1
    print("Total base time: " + str(time_dict["base"]))
    print("Total max time: " + str(time_dict["max"]))
    WrongLog.flush()


if __name__ == "__main__":
    WrongLog = open("wrong_log.txt", "a")
    falseCount = 0
    time_dict = {}
    print("wrong_log:", file=WrongLog)
    print("BeatMatching")
    print("README: 将每个project放在'projects'目录下的不同文件夹中，每个文件夹包含若干.jar文件（包括输入输出接口）")
    print("修改FILE_NAME_LIST为你的.jar名，HW5_generator里的TIME_MAX也可以改")
    # NUM_PROJECTS, FILE_LIST = preprocess()
    NUM_PROJECTS, FILE_LIST = preprocess()
    print("预处理完成，测试对象：")
    for i in FILE_LIST:
        print(i[2], end=" ")
        time_dict[i[2]] = 0
    time_dict["base"] = 0
    time_dict["max"] = 0
    print()
    while True:
        a = input("输入1：自动生成数据\n输入2：文件读入数据\n输入q：退出\n")
        while a not in ["1", "2", "q"]:
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
            print("从文件in.txt读入")
            os.chdir(os.path.dirname(os.getcwd()))
            fin = open("in.txt", "r")
            os.chdir("projects")
            data_in = fin.readlines()
            fin.close()
            thread_from_file_list = []
            if MULTI_THREAD:
                for i in range(NUM_PROJECTS):
                    thread = TestThread(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data_in)
                    thread.start()
                    thread_from_file_list.append(thread)
                for thread in thread_from_file_list:
                    thread.join()
            else:
                for i in range(NUM_PROJECTS):
                    test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data_in)
            check(data_in)

        print("一轮测试完成，报错信息见wrong_log.txt")
    WrongLog.close()
