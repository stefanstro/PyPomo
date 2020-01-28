#!/usr/bin/python3

'''
This is a small script to implement the pomodoro technique. It has a logging function, too.
'''

# developed by Stefan Strohmeier (st.strohmeier@gmail.com), 20. September 2019

import time
import datetime as dt
import subprocess as s
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog
import sqlite3
from tqdm import tqdm
from time import sleep

# delete main window
root = tk.Tk()
root.withdraw()

# Setting Variables
# total_pomodoros = 0
global time_now # = dt.datetime.now()
# time_pomodoro = working_time * 60
# time_delta = dt.timedelta(0,time_pomodoro)
# time_future = time_now + time_delta
DB_Name = "PomoLog.db"
# project_test = "Dissertation"
# task_test = "Research"
# input_project = ""

# SQLite DB Table
TableSchema="""
CREATE TABLE IF NOT EXISTS workload (
    Uhrzeit text,
    Project text,
    Task text,
    Worktime real
);
"""

# Connect or create the connection
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

# Tabelle innerhalb der DB erstellen
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

# Datenbank schliessen
curs.close()
conn.close()

def write2DB(Uhrzeit, Project, Task, Worktime):
    conn = sqlite3.connect(DB_Name)
    c = conn.cursor()
    print("Writing to the database...")
    c.execute("INSERT INTO workload VALUES (?,?,?,?)", (Uhrzeit,Project,Task,Worktime))
    conn.commit()

def get_project():
    input_project = tkinter.simpledialog.askstring("Project", 'Your project:')
    project_name = input_project
    # print(project_name)
    return project_name

def get_task():
    input_task = tkinter.simpledialog.askstring("Task", 'Your current task:')
    task_name = input_task
    # print(task_name)
    return task_name

def get_workingtime():
    input_workingtime = tkinter.simpledialog.askinteger("Denkzeit", "How long do you want to work?", minvalue=5, maxvalue=90)
    workingtime = input_workingtime
    # print(workingtime)
    return workingtime

def get_breaktime():
    input_breaktime = tkinter.simpledialog.askinteger("Pausenzeit", "How long do you want to have a break?", minvalue=1, maxvalue=30)
    breaktime = input_breaktime
    # print(breaktime)
    return breaktime

def info_pomodoro():
    global dummy_project
    dummy_project = get_project()
    global dummy_task
    dummy_task = get_task()
    global dummy_workingtime
    dummy_workingtime = get_workingtime()
    global dummy_breaktime
    dummy_breaktime = get_breaktime()
    global time_now
    time_now = dt.datetime.now()
    global time_pomodoro
    time_pomodoro = dummy_workingtime * 60
    global time_delta
    time_delta = dt.timedelta(0,time_pomodoro)
    global time_future
    time_future = time_now + time_delta
    print("Working Time (min):\t", dummy_workingtime)
    print("Break Time (min):\t", dummy_breaktime)
    print("Time now:\t\t", time_now.strftime("%H:%M"))
    print("Future Time:\t\t", time_future.strftime("%H:%M"))
    print("Project:\t\t", dummy_project)
    print("Task:\t\t\t", dummy_task)
    print("\n")
    # for i in tqdm(range(dummy_workingtime*60), desc="Timer 1", position=1):
    #     time.sleep(1)

    # s.call(['notify-send','Pomodoro Timer','Pomodoro Cycle starting!'])
    # write2DB(time_now.strftime("%Y-%m-%d %H:%M"), dummy_project, dummy_task, dummy_workingtime)

def pomodoro():
    info_pomodoro()
    time_now = dt.datetime.now()
    total_pomodoros = 0
    while True:

        if time_now < time_future:
            for i in tqdm(range(dummy_workingtime*60), desc="Timer Work", position=1):
                time.sleep(1)

        elif time_now > time_future:
            print("Take a break and restart")
            s.call(['notify-send','Pomodoro Timer','Pomodoro Cycle done!'])
            answer = messagebox.askyesno("Question", "Continue working?")

            if answer == True:
                root.update()
                total_pomodoros += 1
                write2DB(time_now.strftime("%Y-%m-%d %H:%M"), dummy_project, dummy_task, dummy_workingtime)
                for i in tqdm(range(dummy_breaktime*60), desc="Timer Pause", position=1):
                    time.sleep(1)
                info_pomodoro()

            else:
                root.update()
                total_pomodoros += 1
                write2DB(time_now.strftime("%Y-%m-%d %H:%M"), dummy_project, dummy_task, dummy_workingtime)
                print("\nTotal Pomodoros: ", total_pomodoros)
                break
        time_now = dt.datetime.now()

def main():
    print("\n---- The pomodoro timer has been started ----\n")
    pomodoro()


if __name__ == "__main__":
    main()
