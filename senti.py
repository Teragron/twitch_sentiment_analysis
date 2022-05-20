# -*- coding: utf-8 -*-
"""
Created on Thu May 19 03:09:13 2022

@author: ahmet
"""
from socket import socket
from pprint import pprint
import time
from utils.getkeys import key_check
from textblob import TextBlob
import PySimpleGUI as sg
import random





sentani = [0]
text = []
meani = 0

positives = 0
negatives = 0

layout = [[sg.Text('Left indicates the tendency to be negative')],
          [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')],
          [sg.Text("Negative Comments:"),sg.Text("", size=(0, 1), key='OUTPUT1')],
          [sg.Text("Positive Comments:"),sg.Text("", size=(0, 1), key='OUTPUT2')],
          [sg.Cancel()]
          ]


window = sg.Window('Sentiment Analysis', layout)
progress_bar = window['progressbar']
    
    
    
def sent(text):
    global positives  
    global negatives
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment != 0.0:
        sentani.append(sentiment+1)     
        if sentiment>0:
            positives +=1
        else:
            negatives +=1
        

        
        
def parseNamedata(mag):
    data = mag.split(" ")[0] 
    index = data.index("!")
    return data[1:index]

def send(sock, msg):
    sock.send(bytes(msg +"\n", "ASCII"))
    
def recv(sock, buff_Size):
    x = sock.recv(buff_Size).decode("UTF-8").split(":")[-1]
    y = x.split("\r")[0]
    text.append(y)
    sent(text[-1])
    return'--'
    
    
        
def main():
    oauth = open("secret.txt", "r").readline()
    nick_name = "teragron"
    channel = "xqc"
    addr = "irc.chat.twitch.tv"
    port = 6667
    sock = socket()
    sock.connect((addr, port))
    send(sock, f"PASS {oauth}")
    send(sock, f"NICK {nick_name}")
    send(sock, f"JOIN #{channel}")

    while True:
        data = pprint(recv(sock, 1024))
        keys = key_check()
        
        event, values = window.read(timeout=10)
        window['OUTPUT1'].update(value=negatives)
        window['OUTPUT2'].update(value=positives)
        meani = float("{:.2f}".format(sum(sentani)/len(sentani)))
        if event == 'Cancel'  or event == sg.WIN_CLOSED or keys == "H":
            window.close()
            break
        
        if len(sentani)>100:
            sentani.clear()
            sentani.append(0)
            meani = 1

        progress_bar.UpdateBar(meani*50)

        print("Mean:",meani*50, "negative Comments:", negatives, "positive Comments:", positives)

    
    
if __name__ == "__main__":
    main()