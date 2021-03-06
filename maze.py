from pygame import *
import random
from socket import *
import time

#172.0.0.1
HOST = ''
PORT = 21563
BUFSIZ = 1024
ADDR = (HOST, PORT)
up = 'u'
down = 'd'
left = 'l'
right = 'r'
PlayerEvent = USEREVENT+2


class labyrinthe(list):
	''
	def __init__(self,size):
		self.size = size
		labx,laby = size
		lx,ly = labx+2,laby+2
		ref = [1,lx,-1,-lx]
		l=[[random.randrange(lx+1,lx*(ly-1),lx)+random.randint(0,labx),random.choice(ref)]]	
		L = list((0,0,0,0)*lx+((0,0,0,0)+(1,1,1,1)*labx+(0,0,0,0))*laby+(0,0,0,0)*lx)
		L = [L[i:i+4] for i in range(0,lx*ly*4,4)]
		#print "first"
		#print L

		self.extend(L)
		while l:
			for i in l:
				a = sum(i)
				b  = (1 if abs(i[1])==lx else lx)*random.choice((1,-1))
				if all(self[a]):
					c = ref.index(i[1])
					self[i[0]][c] = 0
					i[0] = a
					self[i[0]][c-2] = 0
					if not random.randint(0,1): l.append([i[0],b])
					if not random.randint(0,3): l.append([i[0],-b])
				else :
					if all(self[i[0]+b]): l.append([i[0],b])
					if all(self[i[0]-b]): l.append([i[0],-b])
					l.remove(i)
		del(self[:lx])
		del(self[-lx:])
		del(self[::lx])
		del(self[lx-2::lx-1])

		
	def get_path(self,start,exit):
		pos = start
		d = 1
		path = [pos]
		ref = [1,self.size[0],-1,-self.size[0]]
		while pos != exit:
			if self[pos][ref.index(d)-1] == 0: d = ref[ref.index(d)-1]
			if self[pos][ref.index(d)] == 0:
				pos = pos+d
				path.append(pos)
				i = path.index(pos)
				if i != len(path)-1:
					del(path[i:-1])			
			else: d = ref[ref.index(d)-3]
		return path


	def get_image_and_rects(self,cellulesize,wallcolor=(0,0,0),celcolor=(255,255,255)):
		x,y = cellulesize
		image = Surface((x*(self.size[0]),y*self.size[1]))
		image.fill(wallcolor)
		rects = []
		for e,i in enumerate(self):
			rects.append(image.fill(celcolor,(e%(self.size[0])*cellulesize[0]+1-(not i[2]),e/(self.size[0])*cellulesize[1]+1-(not i[3]),cellulesize[0]-2+(not i[2])+(not i[0]),cellulesize[1]-2+(not i[1])+(not i[3]))))
		return image,rects

#****************************************************************************************
#****************************************************************************************
if __name__ == '__main__':
	try:
		me = Surface((5,5))
		me.fill(0xff0000)
		L = labyrinthe((50,40))
		labx,laby = 50,50
		screen = display.set_mode((L.size[0]*10,L.size[1]*10))
		image,rectslist = L.get_image_and_rects((10,10),wallcolor=0,celcolor=0xffffff)
		screen.blit(image,(0,0))
		start = random.randrange(len(L))
		exit = random.randrange(len(L))
		screen.fill(0x00ff00,rectslist[exit])
		screen.blit(me,rectslist[start])
		display.flip()
		tcpSerSock = socket(AF_INET, SOCK_STREAM)
		tcpSerSock.bind(ADDR)
		tcpSerSock.listen(5)

		while True:
		    print 'waiting for connection...'
		    tcpCliSock, addr = tcpSerSock.accept()
		    print '...connected from:', addr

		    event.post(event.Event(PlayerEvent))	
		    screen.fill(0xff0000,rectslist[start])
		    display.flip()
		    while event.wait():
		    	event.post(event.Event(PlayerEvent))
		    	display.flip()
		        data = tcpCliSock.recv(BUFSIZ)
		        print "cln says:",data
		        if not data:
		            print "client sent null data"
		            break
		        #newdata = ''  		#raw_input(">>:")
		        screen.fill(-1,rectslist[start])
		        if data == up and not L[start][3]:
		        	start += -L.size[0]

		        elif data == down and not L[start][1]:
		        	start += L.size[0]

		        elif data == right and not L[start][0]:
		        	start += 1

		        elif data == left and not L[start][2]:
		        	start += -1
		       	else:
		       		print "nonsense!"
		        newdata = L[start]
		        screen.fill(0xff0000,rectslist[start])
		        display.flip()
		        #time.sleep(1)
		        if start == exit:
		        	print "You Won!"
		        	tcpCliSock.send('%s' % ('You Won!'))
		        	break
		        tcpCliSock.send('%s' % (newdata))
		    tcpCliSock.close()
		tcpSerSock.close()
	except Exception as e:
		print e
    #        continue
		#tcpCliSock.close()
		tcpSerSock.close()
		print "closed"
	finally:
		tcpSerSock.close()
		print "closed"


	