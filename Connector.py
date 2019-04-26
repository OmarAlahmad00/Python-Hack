import socket
from pynput.keyboard import Key, Listener
import mysql.connector


try:
    print("Connecting to DB....")
    db = mysql.connector.connect(
        host="themoon.mysql.database.azure.com",
        user="omar@themoon",
        passwd="SharpMinds11",
        database = "logs"
    )
    print("Succeeded")
    my_Cursor = db.cursor()

except:
    pass

try:
    print("Attempting to create a table....")
    my_Cursor.execute("CREATE TABLE IP(IP VARCHAR(250))")
    print("Succeeded")
except Exception as e:
    print(e)

try:
    print("Attempting to delete IP from IP table")
    my_Cursor.execute("DELETE FROM IP")
    print("Succeeded")
except Exception as e:
    print(e)

try:
    print("Attempting to send IP to sql database")
    my_Cursor.execute("INSERT INTO IP (IP) VALUES ('" + str(socket.gethostbyname(socket.gethostname())) + "')")
    db.commit()
    print("Succeeded")
except Exception as e:
    print(e)


print("Which computer would you like to connect to Omar?")
port = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), port))
print(socket.gethostbyname(socket.gethostname()))
s.listen(20)

letters = ""

def commandSend(cs):

    command = input()
    cs.send(bytes(str(command), "utf-8"))
    send(cs)
    pass
def send(cs):
    global letters
    def input(key):
        print(key)
        if(key == Key.f11):
            cs.send(bytes(str(key), "utf-8"))
            commandSend(cs)


        else:
            letters =  str(key)
            cs.send(bytes(letters, "utf-8"))

    with Listener(input) as listener:
        listener.join()

def connect():
        try:
            print("Attempting to get Connection")
            clientsocket, address = s.accept()
            print("Connected to: " , address)
            send(clientsocket)
            connect()

            pass
        except Exception as e:
            print(e)
            connect()
connect()




