import os
import time
import socket

os.system(f"title AenR - Twitch Chat bot")

print("""
           
             █████╗ ███████╗███╗   ██╗██████╗ 
            ██╔══██╗██╔════╝████╗  ██║██╔══██╗
            ███████║█████╗  ██╔██╗ ██║██████╔╝
            ██╔══██║██╔══╝  ██║╚██╗██║██╔══██╗
            ██║  ██║███████╗██║ ╚████║██║  ██║
            ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                  
   """)

server = "irc.chat.twitch.tv"
port = 6667
channel = input("Kanal Adını Girin: ")
message_option = input("Mesajları Hangi Şekilde Göndereceksiniz?\n1. Rastgele botlar mesajları göndersin\n2. Seçtiğim bottan seçtiğim mesajı göndereyim\n3. Bütün botlar aynı anda aynı mesajı göndersin: ")
oauths = []
messages = []

with open("oauths.txt", "r") as file:
    oauths = file.readlines()

if message_option == "1":
    with open("messages.txt", "r", encoding="utf-8") as file:
        messages = file.readlines()

    interval = int(input("Kaç Saniyede Bir Mesaj Gönderilsin?: "))
    index = 0

while True:
    if message_option == "1":
        message = messages[index % len(messages)].strip()
        index += 1
        time.sleep(interval)
    elif message_option == "2":
        with open("oauths.txt", "r") as file:
            oauths = file.readlines()

        print("Available bots:")
        for i in range(len(oauths)):
            print(f"{i+1}. Bot {i+1}")

        bot_choice = int(input("Mesajı Gönderecek Botu Seçiniz. (1, 2, 3,..): "))
        if bot_choice > len(oauths):
            print("Yanlış Seçim!")
            time.sleep(5)
            exit()

        oauth = oauths[bot_choice-1].strip()
        nickname = f"bot_{bot_choice}"
        message = input("Göndermek istediğiniz mesajı girin: ")
    elif message_option == "3":
        message = input("Göndermek istediğiniz mesajı girin: ")
        messages.append(message)

        for i in range(len(oauths)):
            oauth = oauths[i].strip()
            nickname = f"bot_{i+1}"
            
            for message in messages:
                print(f"Bot {i+1} tarafından mesaj gönderildi: {message}")

                irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                irc.connect((server, port))
                print(f"[{time.strftime('%X')}] Mesaj Gönderildi : {message}")
                irc.send(f"PASS {oauth}\n".encode("utf-8"))
                irc.send(f"NICK {nickname}\n".encode("utf-8"))
                irc.send(f"JOIN #{channel}\n".encode("utf-8"))
                irc.send(f"PRIVMSG #{channel} :{message}\n".encode("utf-8"))
                irc.close()

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))

    if message_option == "1":
        with open("oauths.txt", "r") as file:
            oauths = file.readlines()

        print(f"[{time.strftime('%X')}] Mesaj Gönderildi : {message}")
        irc.send(f"PASS {oauths[index % len(oauths)]}\n".encode("utf-8"))
        irc.send(f"NICK bot\n".encode("utf-8"))
        irc.send(f"JOIN #{channel}\n".encode("utf-8"))
        irc.send(f"PRIVMSG #{channel} :{message}\n".encode("utf-8"))
    else:
        print(f"[{time.strftime('%X')}] Mesaj Gönderildi : {message}")
        irc.send(f"PASS {oauth}\n".encode("utf-8"))
        irc.send(f"NICK {nickname}\n".encode("utf-8"))
        irc.send(f"JOIN #{channel}\n".encode("utf-8"))
        irc.send(f"PRIVMSG #{channel} :{message}\n".encode("utf-8"))

    irc.close()