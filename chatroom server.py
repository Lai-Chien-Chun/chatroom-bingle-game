# coding=UTF-8
import socket
import select
import sys
import os
from thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()


IP_address = str(sys.argv[1])


Port = int(sys.argv[2])


server.bind((IP_address, Port))


server.listen(100)

list_of_clients = []
clients_game = {}

start_game = 0


def decide_order():
    global start_game
    turn = 0
    count=len(list_of_clients)
    print "遊戲人數:", (count)
    while True:
        count = len(list_of_clients)
		
        #for clients in list_of_clients:
			#print clients,",",
        
        print "count:",count
        if count <3 :
			broadcast('people_not_enough',-1)
			print "人數不足回到聊天室"
			start_game=0
			break
	
        print "turn:",turn
        print start_game
        print "it's your turn: ", (turn % count)
		
        try:
	    #print "send_turn",turn
            #print "send_count",count
            
			#送出
            #people = len(list_of_clients)
            #print people,"on line"
            #print "index:",turn%count
            #while (turn%count) > people:
		#turn = turn + 1
                #print turn+"..."
            #for connected in list_of_clients:
              #  response = os.system("ping -c 1 "+connected)
               # if reponse == True:
                #    continue
               # else:
                #    print "bye"
                 #   list_of_clients.remove(connected)
                  #  print len(list_of_clients)
           
           
               
            list_of_clients[turn%count].send("your turn:")
            print "輪到:",turn%count
            #else
			#list_of_clients[turn%count].recv(1024)
			#list_of_clients[turn%count].send('ready?')
            
        except:
            #print "exexex",turn%count
            list_of_clients[turn%count].close()
            remove(list_of_clients[turn%count])
           
            #list_of_clients.remove(list_of_clients[turn%count])
            turn = turn + 1
            broadcast('people_break',-1)
            start_game=0
            break
            #pass
			
		#得到
        
        num_chosed = list_of_clients[turn%count].recv(2048)
			
        if len(num_chosed)==0:
			#print "exexex=recv",turn%count
			list_of_clients[turn%count].close()
			remove(list_of_clients[turn%count])
			turn = turn + 1
			broadcast('people_break',-1)
			start_game=0
			break
		#print "received:",num_chosed,"....."

        if num_chosed :

            #print "www",num_chosed,turn%count
            broadcast(num_chosed,list_of_clients[turn%count])
            list_of_clients[turn%count].send('complete')
            #print "CCC"
            for clients in list_of_clients: # recieve whether is bingo
                #if member!= (turn%count):
                    #print "AAA",clients
                    data =clients.recv(2048)
                    #print "BBB"
                    #print clients,"recv:",data
                    #print clients,"-7recv:",data[-7:]
                    if data[-7:] =="the end" : # number of people < 3 : return to chatroom 
                        start_game = 0
                        
                        broadcast('the end',clients)
                        #print "is here?",start_game
						
         
            if start_game==0:
				#while 1:
					#continue
				break
			#if num_chosed[-7:] =="the end":
				#start_game = 0
				#print "is here?",start_game
				#break
        turn = turn + 1
        #print turn

count = 0     
def printf():
	global count
	count = 0
	print "聊天室人數:",len(list_of_clients)
	
	#for value in clients_game.iteritems():
	#	print key,value
	#	count+=value

def clientthread(conn, addr):
	global start_game,count
	#玩家名稱
	name = conn.recv(1024)
	
	clients_game[str(conn)]=0
	#確認此人是否要進入遊戲
	conn.send("Welcome to this chatroom!")
	while True:
			#print conn.fileno(),"目前狀態:",start_game
                        print "state:",start_game
			printf()
			#print "參加的人數:",count
			try:
				message = conn.recv(1024)
				
				if message:
					if start_game == 0:#聊天室狀態
						
						if message == 'Playing':
							start_game = 1							
							broadcast(name+"邀請各位玩遊戲", conn)
						else:
							print "< client's ID: " + str(addr[1]) + " > " + message
							message_to_send = "< client's ID: " + str(addr[1]) + " > " + message
							broadcast(name+":"+message, conn)
					
					elif start_game ==1:#準備遊戲狀態
						
						if message =='Start':
							start_game = 2
							
							broadcast('bingo_game',0)
							conn.recv(1024)
							decide_order()
						else:
							print "< client's ID: " + str(addr[1]) + " > " + message
							message_to_send = "< client's ID: " + str(addr[1]) + " > " + message
							broadcast(name+":"+message, conn)
							
					elif start_game == 2:#開始遊戲
						while start_game==2:
							continue
						
				else:
					remove(conn)
					break
			except:
				remove(conn)
				break             
          
	
	#print "is set"
	#key = 1
        #print key
        
#廣播
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:#送給非connection
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

#移除連線
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


key = 0
while True:
             
	conn, addr = server.accept()
        #if key == 1:
            #print "key:",key
	#    break
        if start_game != 2: # if not in the game state
            list_of_clients.append(conn)
	#print conn
	#print "client's ID: ", addr[1] ," connected"
	    start_new_thread(clientthread,(conn,addr))
        else:
            conn.send('quit()')
            conn.close()
        #if key == 1:
            #print "keykey",key
         #   break
	
print "Round Over..."
conn.close()
server.close()
