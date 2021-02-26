# coding=UTF-8
import random

import socket
import select
import sys



#1.連線的建立
#-----------------------------------
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print "Correct usage: script, IP address, port number"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address,Port))
#----------------------------------

#2.名字與參數設定
#----------------------------------
number_all = []
line = []
Bingo = 0
first = 1
sys.stdout.write("輸入你的名字:")
name = raw_input()
server.send(name)
quit = 0

#重新產生新數字
def restart():
	global Bingo
	Bingo=0
	global number_all
	number_all = []
	global line
	line = []
	for i in range(1,26):
		number_all.append(i)

	random.shuffle(number_all)	

	for k in range(12):
		line.append(5)
restart()
#----------------------------------


#聊天室
#----------------------------------

mark = 0
your_turn = 0
while True:
  #print "A"
  sockets_list = [sys.stdin,server]
  flag = 0
  if your_turn==1 and Bingo==1 :
  	print "Your turn"
  elif Bingo==1 and your_turn==0 :
	print "another player is selecting number"
  elif Bingo==0 and your_turn==0 :
	print"聊天模式"
  read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
  if Bingo == 1 and mark == 0:
	#print len(number_all)
	for j in range(25):
		print("{0:2}".format(number_all[j])),
		if j%5 ==4:
			print("\n")
        mark = 1
  #print "B" 
  for socks in read_sockets:
		#接收
	num = -1
	#print "C"
	if socks == server:
		
		#print "D"
		if Bingo==1:
		
			#print "server:(",Bingo,your_turn,")"
			message = socks.recv(2048)
			mes = message[-7:]
			#end_check = message[-7:]
			#print "server.mes=",mes
			try:
			  num = int(message)
			except:
			  try:
			    num = int(message[:-11])
			  except:
			       #print "text message=",message
				#print "end_check=",end_check
				#測試用
				flag = 1
				if message!='complete':
					your_turn = 1
				break     
			
			#if message != "Welcome to this chatroom!" and message != "your turn:" and mes!="the end" and message!="people_not_enough":
            #                    if mes == "r turn:" and len(message)!=10:
            #                            print "S_your turn:"
            #                            your_turn = 1
			#		num = int(message[:-11])
			#		print "對方選擇:",num
            #                    elif mes =="\nnot ok":
            #                            num = int(message[:-7])
            #                            
			##	else:
			#	        num = int(message)
			#	        print "oppent choose:",num
            #            #elif mes == "r turn:":
                                #print("debug...")
                                
			#else:#表示非數字的封包進來
			#	print "text message=",message
				#print "end_check=",end_check
				#測試用
			#	flag = 1
			#	your_turn = 1
			#	break              
		else:#聊天室
				flag = 1
				message = socks.recv(2048)
				if message=='exit()' or message=='quit()':
					quit = 1
					if message =='quit()':
						print 'game start not to access'
				if message=='bingo_game':
					print "你參加了遊戲"
					server.send('ok')
					Bingo=1
					for j in range(25):
						print("{0:2}".format(number_all[j])),
						if j%5 ==4:
							print("\n")
				mes = message[-7:]
				print message
	#輸入
	elif socks == sys.stdin :
		#print "stdin:(",Bingo,your_turn,")"
		if Bingo==1:
                        #print "V_your turn:"
                        while True:
			    message = sys.stdin.readline()
                            try: 
                                num = int(message)
                            except:
                                continue    
                            if num<=25 and num>=1:
                                break
                            else:
                                print "Please enter number between 1 and 25"
                        
                        #print("typing...:",num)
                        #print("flag: ",flag)
			if your_turn == 1:#表示換他才送
			    server.send(message)
			else:#不該他輸入
				num = -1#無效輸入
			sys.stdout.write("<You>")
			sys.stdout.write(message)
			sys.stdout.flush()
			#server.recv(1024) # 
			your_turn=0	
		else:
				
				message = raw_input()
				print name+":"+message
				server.send(message)
				sys.stdout.flush()
  
  #print "uut",num,quit
  #print "ss:",quit
  if Bingo == 1:
	
	if mes=="the end" or message == 'people_not_enough' or message =='people_break':
		if mes =='the end':
		  print "別人贏了，你輸了，遊戲結束!"
		elif message=='people_not_enough':
		  print "人數不足，遊戲至少要有三人才能開始"
		elif message=='people_break':
		  print "有人中途斷線，遊戲結束"
		Bingo = 0
		your_turn=0
		restart()
		#break
	if num == -1:
		continue
	if flag == 1:
		print "test"
		continue
        #print("number is: ",num)
	choice = num      
        #print("your choice:",choice)
	for check_column in range(5):
		if(number_all.index(int(choice)) % 5 == check_column):
			line[check_column] -= 1
	for check_row in range(5):
		if(number_all.index(int(choice)) // 5 == check_row):
			line[check_row+5] -= 1

	if(number_all.index(int(choice)) == 0):
		line[10] -= 1
	elif(number_all.index(int(choice)) == 12): #imp.
		line[10]-=1
		line[11]-=1
	elif(number_all.index(int(choice)) % 6 == 0):
		line[10] -= 1
	elif(number_all.index(int(choice)) % 4 == 0):
		line[11] -= 1

	number_all[number_all.index(int(choice))] ="*"
        #print("update~")
        for j in range(25):
            print("{0:2}".format(number_all[j])),
            if j%5 ==4:
                print("\n")	

	count = 0
	for l in range(12):
		if(line[l]==0):
			count = count + 1
	   
	if(count==1):
		Bingo = 0
		print "Bingo XDD"
		server.send("the end")
		sys.stdout.write("<You>")
		sys.stdout.write(message)
		sys.stdout.flush()
		your_turn=0
		restart()
		#break
	else:
		server.send("not ok") 
  if quit == 1:
    break
server.close()





