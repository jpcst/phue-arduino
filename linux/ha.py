#!/usr/bin/python3
import serial, datetime, os, requests
from phue import Bridge

def read_ip():
	try:
		if (os.name == 'nt'): # windows
			with open('C:/scrape/ip.txt','w') as f:
				b = Bridge(f.read())
				b.connect()
		else: # linux
			with open('/home/jp/pha/ip.txt', 'r') as f:
			    b = Bridge(f.read())
			    b.connect()
	except Exception as e: # se erro no IP, scrapar novo
	    if (os.name == 'nt'): # windows
	    	with open('C:/scrape/ip.txt','w') as f:
			    ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
			    f.write('{}'.format(ip))
			    b = Bridge(ip)
			    print('new ip found (ignore)\n')
	    else: # linux
	    	with open('/home/jp/pha/ip.txt','w') as f:
			    ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
			    f.write('{}'.format(ip))
			    b = Bridge(ip)
			    print('new ip found (ignore)\n')
	return b

b = read_ip()
lights = b.get_light_objects('id') # lista das luzes
if (os.name == 'nt'): # windows
	serial_data = serial.Serial('com3',9600)
else: # linux
	serial_data = serial.Serial('/dev/ttyACM0',9600)
h = datetime.datetime.now()

def print_now():
	agr = ('{:02d}:{:02d}:{:02d}').format(h.hour,h.minute,h.second)
	print(agr,end='')

def now():
	hr = [int(i) for i in [h.hour,h.minute]]
	return hr

def timer(hr,m):
	if (h.hour >= hr and h.minute >= m):
		return True
	else:
		return False

# add if para windows/linux
# def scrape_ip():
# 	ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipadress']
# 	if (os.name == 'nt'):
# 		with open('C:/scrape/ip.txt','w') as f:
# 			f.write('{}'.format(ip))
# 	else:
# 	    with open('/home/jp/pha/ip.txt','w') as f:
# 	        f.write('{}'.format(ip))

def sensor(hr=18,m=0):
	while True:
		if(serial_data.inWaiting() > 0): # Roda apenas se receber info do arduino
			my_data = serial_data.readline().decode().strip()
			if(my_data > '0'): # Distancia tem q ser > 0cm
				teto1 = b.get_light(2,'on')
				teto2 = b.get_light(4,'on') # True = on, False = off
				tetos = [teto1,teto2]
				if (timer(hr,m) == True): # Se hora > setado, ligar/desligar
					if(tetos[0] == True or tetos[1] == True): # on -> off
						lights[2].brightness=254
						lights[4].brightness=254
						b.set_light([2,4], 'on', False, transitiontime=0)
						print_now()
						print(' ->',my_data,'cm [off]')
					else: # off -> on
						b.set_light([2,4], 'on', True, transitiontime=0)
						lights[2].xy = [.3,.3]
						lights[4].xy = [.3,.3]
						lights[2].brightness=254
						lights[4].brightness=254
						print_now()
						print(' ->',my_data,'cm [on]')
				else:
					print('sol')

def do_light(bd=0,c1=0,d=0,c2=0,brilho=254,tt=0,set=True):
	list = [bd,c1,d,c2]
	list_t = []
	for i in range(len(list)):
		if(list[i] != 0):
			i+=1
			list_t.append(i)
	# print('selected',list_t,end='\n')
	if (len(list_t) == 1):
		if (b.get_light(list_t[0], 'on') == True):
			b.set_light(list_t[0], 'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0], 'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho

	elif (len(list_t) == 2):
		if (b.get_light(list_t[0],'on') == True or b.get_light(list_t[1]) == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho

	elif (len(list_t) == 3):
		if (b.get_light(list_t[0],'on') == True or b.get_light(list_t[1]) == True or b.get_light(list_t[2]) == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			b.set_light(list_t[2],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			b.set_light(list_t[2],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho
			lights[list_t[2]].brightness=brilho

	elif (len(list_t) == 4):
		if(b.get_light(list_t[0],'on') == True or b.get_light(list_t[1],'on') == True or b.get_light(list_t[2],'on') == True or b.get_light(list_t[3],'on') == True):
			b.set_light(list_t[0],'on', False, transitiontime=tt)
			b.set_light(list_t[1],'on', False, transitiontime=tt)
			b.set_light(list_t[2],'on', False, transitiontime=tt)
			b.set_light(list_t[3],'on', False, transitiontime=tt)
			set = False
		else:
			b.set_light(list_t[0],'on', True, transitiontime=tt)
			b.set_light(list_t[1],'on', True, transitiontime=tt)
			b.set_light(list_t[2],'on', True, transitiontime=tt)
			b.set_light(list_t[3],'on', True, transitiontime=tt)
			lights[list_t[0]].brightness=brilho
			lights[list_t[1]].brightness=brilho
			lights[list_t[2]].brightness=brilho
			lights[list_t[3]].brightness=brilho
	os.system('cls' if os.name == 'nt' else 'clear')
	return list_t,brilho,tt,set

# def make_cor(bd=0,c1=0,d=0,c2=0):
# integrar essa func em do_light

os.system('cls' if os.name == 'nt' else 'clear')
while True:
	usr = input('\n[1] turn on sensor\n[2] set hour\n\n>> ')
	v = usr.split(' ')
	if (len(v) == 1): # RODA SE INPUT = [0]
		if(usr == '1'): # LIGA O SENSOR NA HORA DEFAULT
			try:
				b = read_ip()
				lights = b.get_light_objects('id')
				os.system('cls')
				sensor()
			except KeyboardInterrupt:
				os.system('cls')
				pass

		elif(usr == '2'): # ALTERA A HORA E LIGA SENSOR
			try:
				os.system('cls')
				hr = int(input('>> h: '))
				mi = int(input('>> m: '))
				print('ok')
				os.system('cls')
				sensor(hr,mi)
			except KeyboardInterrupt:
				os.system('cls')
				pass
		# LIGA APENAS UM GRUPO DE LUZ NO BRILHO E TT DEFAULT
		elif(usr == 'c'): # LIGA ALL TETO
			# os.system('cls' if os.name == 'nt' else 'clear')
			print(do_light(c1=1,c2=1))
		elif(usr == 'b'): # LIGA BED
			# os.system('cls' if os.name == 'nt' else 'clear')
			print(do_light(bd=1))
		elif(usr == 'd'): # LIGA DESK
			# os.system('cls' if os.name == 'nt' else 'clear')
			print(do_light(d=1))
		elif(usr == 'c1'): # LIGA TETO 1
			# os.system('cls' if os.name == 'nt' else 'clear')
			print(do_light(c1=1))
		elif(usr == 'c2'): # LIGA TETO 2
			# os.system('cls' if os.name == 'nt' else 'clear')
			print(do_light(c2=1))
		elif(usr == 'all'): # LIGA TODAS
			print(do_light(1,1,1,1))
			# os.system('cls' if os.name == 'nt' else 'clear')
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			print(usr, 'is not defined')

	elif (len(v) == 2): # RODA SE INPUT = [0,1]
		try:
			if (type(v[0]) == str and type(float(v[1])) == float): # SE INPUT = [d, float] -> luz e brilho
				x = 254 * float(v[1])
				if (v[0] == 'b'): # CONTROLA CAMA E SEU BRILHO
					if (b.get_light(1,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						lights[1].brightness = int(x)
						# fazer para outras combinacoes
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						print(do_light(bd=1,brilho=int(x)))
						# lights[1].brightness = int(x)
				if (v[0] == 'c'): # CONTROLA ALL TETO E SEU BRILHO
					if (b.get_light(2,'on') == True or b.get_light(4,'on') == True):
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						lights[2].brightness = int(x)
						lights[4].brightness = int(x)
					else:
						os.system('cls' if os.name == 'nt' else 'clear')
						print(v[0],' -> ',int(x),', ',float(v[1]) * 100,'%',sep='')
						print(do_light(c1=1,c2=1,brilho=int(x)))

		except ValueError:
			if (type(v[0]) == str and type(v[1]) == str): # SE INPUT = [d, b] -> luz e luz, brilho default
				if (v[0] == 'b' and v[1] == 'd' or v[0] == 'd' and v[1] == 'b'):
					do_light(bd=1,d=1)
				#fazer para as outras combinacoes

	elif (len(v) == 3):
		pass


	elif (len(v) == 4):
		pass





	# se len(usr) == 2 -> c [brilho]
