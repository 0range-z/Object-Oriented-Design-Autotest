#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import sleep
from HW7_generator import generate, generate_coverage
from HW7_judger import judge

MODE = '.jar'  # .java: compile and run    .class .jar: run
FILE_NAME_LIST = ['Assassin', 'Archer', 'Berserker', 'Lancer', 'Me', 'Saber', 'Rider']
TEST_SINGLE = False
SINGLE_NAME = "Archer"


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
                if fileName != SINGLE_NAME+".jar" and TEST_SINGLE:  ##
                    continue
                if fileName.startswith("Berserker"):
                    continue
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


def autotest(FILE_LIST, LENGTH, ROUND, NUM_ELEVATOR):
    global WrongLog
    global falseCount

    for j in range(ROUND):
        data = generate(LENGTH, NUM_ELEVATOR)
        for i in range(NUM_PROJECTS):
            os.chdir(FILE_LIST[i][1])
            test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data)
        check(data)
        WrongLog.flush()
        print("完成第"+str(j+1)+"次循环，总共错误数："+str(falseCount))


def test(NAME, DIR, ID, data):
    global WrongLog
    global falseCount

    os.chdir("../..")
    print("Testing "+ID)
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
        print("["+str(time)+"]"+command, end="")
        sleep((time-curr)/1.0)
        curr = time
        proc.write(command)
        proc.flush()
    print("waiting for "+ID+" to finish...")
    proc.close()
    print(ID+' Done')


def check(data):
    global falseCount
    global time_dict
    os.chdir("../..")
    print("checking".center(20, "-"))
    single_elevator_time = {}
    for i in FILE_LIST:
        single_elevator_time[i[2]] = 0
        fout = open(i[2]+"_out.txt")
        out_lines = fout.readlines()
        fout.close()
        judge_result = judge(data, out_lines, i[2], time_dict, WrongLog, single_elevator_time)
        if not judge_result:
            dt = ""
            for line in data:
                if line == "END\n":
                    break
                if line == "\n":
                    continue
                dt += line
            print(i[2]+" WRONG".center(20, "="))
            print(i[2]+" WRONG".center(20, "=")+"\ndata:\n"+dt, file=WrongLog)
            falseCount += 1

    illegal = True
    for k in single_elevator_time.values():
        if k < 70:
            illegal = False
    if illegal:
        print("ILLEGAL DATA!")
        return

    for i in FILE_LIST:
        if single_elevator_time[i[2]] > 200:
            dt = ""
            for line in data:
                if line == "END\n":
                    break
                if line == "\n":
                    continue
                dt += line
            print(i[2]+" WRONG(TLE)".center(20, "="))
            print(i[2]+" WRONG(TLE)".center(20, "=")+"\ndata:\n"+dt, file=WrongLog)
            falseCount += 1
            return
        print(i[2]+" correct! Total time: {:.2f}".format(time_dict[i[2]]))


if __name__ == "__main__":
    WrongLog = open("wrong_log.txt", "a")
    falseCount = 0
    time_dict = {}

    print("wrong_log:", file=WrongLog)
    print("BeatMatching")
    print("README: 将每个project放在'projects'目录下的不同文件夹中，每个文件夹包含若干.jar文件（包括输入输出接口）")
    print("修改FILE_NAME_LIST为你的.jar名，HW7_generator里的TIME_MAX也可以改")
    print("NOTE: 检查时间的方法是观察所有人的时间，若所有人都大于70s则认为数据无效")
    print("检查了超时、电梯楼层、人员到达、电梯容量、移动时间等常见错误")
    NUM_PROJECTS, FILE_LIST = preprocess()
    for i in FILE_LIST:
        time_dict[i[2]] = 0
    print("\n预处理完成，测试对象：")
    for i in FILE_LIST:
        print(i[2], end=" ")
        time_dict[i[2]] = 0
    print()
    while True:
        a = input("输入1：自动生成数据(现支持随机电梯数量)\n输入2：文件读入数据\n输入3：覆盖性测试(new)\n输入q：退出\n")
        while a not in ["1", "2", "3", "q"]:
            a = input("请重新输入\n")
        if a == "q":
            break
        elif a == "1":
            NUM_ELEVATOR = int(input("请输入新增电梯个数，-1表示0-3随机\n"))
            while NUM_ELEVATOR not in [-1, 0, 1, 2, 3]:
                NUM_ELEVATOR = int(input("新增电梯个数只能为-1(随机),0,1,2,3！请重新输入\n"))
            LENGTH = int(input("请输入长度\n"))
            ROUND = int(input("请输入循环次数\n"))
            try:
                autotest(FILE_LIST, LENGTH, ROUND, NUM_ELEVATOR)
            except KeyboardInterrupt:
                print("Interrupt")
                WrongLog.close()
        elif a == "2":
            print("从文件in.txt读入")
            os.chdir("..")
            fin = open("in.txt", "r")
            os.chdir("projects")
            data_in = fin.readlines()
            fin.close()
            for i in range(NUM_PROJECTS):
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data_in)
            check(data_in)
            WrongLog.flush()
            print(os.getcwd())
            os.chdir("projects")
        elif a == "3":
            print("覆盖性测试")
            data_in = generate_coverage()
            for i in range(NUM_PROJECTS):
                if FILE_LIST[i][2] != "Saber":
                    continue
                test(FILE_LIST[i][0], FILE_LIST[i][1], FILE_LIST[i][2], data_in)
                id = FILE_LIST[i][2]
                os.chdir("../..")
                if judge(generate_coverage(), open(id+"_out.txt").readlines(), id, {id: 0},
                         WrongLog, {id: 0}):
                    print(id+"correct")
            WrongLog.flush()

        print("一轮测试完成，报错信息见wrong_log.txt")
    WrongLog.close()