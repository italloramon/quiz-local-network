import socket
import threading
import requests
import json
import random
import os
from Player import *

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_question():
    request = requests.get("https://the-trivia-api.com/api/questions?limit=1")
    question = json.loads(request.content)
    return question

def show_alternatives(question):
    print(question)
    alternatives = []
    for alternative in question['incorrectAnswers']:
        alternatives.append(alternative)
    alternatives.append(question['correctAnswer'])
    random.shuffle(alternatives)

    return alternatives

def get_welcome_msg():
    global best_score
    welcome_msg = "Welcome to the >>> BEST QUIZ IN THE WORLD MADE FOR ME FOR YOU TO PLAY <<<\nThis is very simple, you have 3 of life, each wrong answer you lost 1 from your life, if you reach 0 (i think you know what will happens). Each correct answer, your gain +1 on your score!\n"
    with open('db.txt', 'r') as db:
        data = db.readlines()
        if (len(data) == 0):
            welcome_msg += "This local network dont have any best player, yet...\n\n"
        else:
            welcome_msg += f"The best player in this local network is >>>    {data[0]}    <<< With a score of >>>    {data[1]}    <<<.\n(Honestly, i think that you're way better than him).\n\n"
            best_score = int(data[1])
    
    return welcome_msg




HOST= get_ip_address()
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
PLAYERS = []
best_score = 0



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(ADDR)

    def handle_client(conn, addr):
        global best_score

        print(f"NEW CONNECTION FROM {addr}.")
        welcome_msg = get_welcome_msg()

        conn.send(welcome_msg.encode(FORMAT))
        conn.send("Type !nick Your-nick-here (For example: !nick neymar1999)".encode(FORMAT))

        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if msg:
                print(f"{addr} -> {msg}")

                msg_list = msg.split()

                if msg[0] == DISCONNECT_MESSAGE:
                    connected = False
                elif msg_list[0] == "!nick":
                    player = Player(conn, msg_list[1])
                    PLAYERS.append(player)
                
            
            while True:

                if not player.isLife():
                    msg_finish = f"You've lost all of your life, sorry, you cant continue play the best quiz in the world :( Unless... You pay for me. Pix: ramon_veiga@hotmail.com. Thanks mate!\n\n >>> [Please type !DISCONNECT to quit] <<<\n\n"
                    
                    if player.score > best_score:
                        msg_finish += f"[Dont be sad! You're the new best player in this network with a score of {player.score},  congrats {player.name}]\n\n"
                        with open('db.txt', 'w') as db:
                            db.write(f"{player.name}\n{player.score}") 
                        

                    conn.send(msg_finish.encode(FORMAT))
                    #conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
                    break
                question = get_question()
                alternatives = show_alternatives(question[0])
                question_str = f"{question[0]['question']}\n"
                #conn.send(f"{question[0]['question']}\n".encode(FORMAT))
                for i in range(4):
                    #conn.send(f"({i+1}) - {alternatives[i]}\n".encode(FORMAT))
                    question_str += f"({i+1}) - {alternatives[i]}\n"
                conn.send(question_str.encode(FORMAT))
                
                answer = conn.recv(1024).decode(FORMAT)
                if alternatives[int(answer)-1] == question[0]['correctAnswer']:
                    player.score_up()
                    msg_correct = f"Congrats {player.name}, you answer was correct, you gain +1 score!\nYour total score is: >>    {player.score}    <<\nType [ENTER] to continue.\n"
                    conn.send(msg_correct.encode(FORMAT))
                else:
                    player.life_down()
                    msg_wrong = f"Sorry {player.name},  you answer was wrong, you lost -1 life!\nYour total of lifes is: >>    {player.life}    <<\nType [ENTER] to continue.\n"
                    conn.send(msg_wrong.encode(FORMAT))


            #conn.send("MESSAGE RECEIVED".encode(FORMAT))
        
        conn.close()

    def start():
        server.listen()
        print(f"SERVER ACTIVATED ON {HOST}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"ACTIVE CONNECTIONS: {threading.active_count()- 1}")

    print("STARTING THE F*CK SERVER, LES GOOOO!!")
    start()