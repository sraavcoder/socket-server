from ipaddress import ip_address
from random import random
import socket
from threading import Thread
from tkinter import scrolledtext

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

print("Server is Running............")

list_of_clients = []

questions=[
    " Water boils at 212 Units at which scale? \n a.Farenhiet\n b.Celsius\n c.Rankine\n d.Kelvin",
    " How many wonders are there in the world? \n a.6\n b.5\n c.7\n d.8",
    " Who is Thor? \n a.God of Thunder\n b.God of Hammers\n c.God of Gold\n d.God of Mischief",
    " How many months have 28 days? \n a.1\n b.2\n c.3\n d.4",
    " What is the maximum length of a TikTok Video? \n a.30s\n b.40s\n c.50s\n d.60s",
    " Which of the following planets has the maximum number of moons? \n a.Earth\n b.Jupiter\n c.Saturn\n d.mars",
]

answers=['a', 'c', 'a', 'a', 'd', 'c']

def get_random_qa(conn):
    random_index = random.randit(0, len(questions)-1)
    random_q = questions[random_index]
    random_a = answers[random_index]
    conn.send(random_q.encode('utf-8'))
    return random_index, random_q, random_a

def remove_q(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clientthread(conn):
    score=0
    conn.send("Welcome to this quiz game!!".encode('utf-8'))
    conn.send("You will recieve a questions.The answer to that question should be one of a, b, c or d\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_qa(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Kudoss!! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time\n\n".encode('utf-8'))
                remove_q(index)
                index, question, answer = get_random_qa(conn)
            else:
                remove(conn)
        except:
            continue


while True:
    conn, addr=server.accept()
    list_of_clients.append(conn)

    print(addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))