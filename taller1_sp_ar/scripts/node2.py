#!/usr/bin/python
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
class Nodo2():


	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('nodo_2', anonymous = True)
		self.initParameters()
		self.initSubscribers()
		self.initPublishers()
		self.main()


	def initParameters(self):
		self.topic_scan = "/scan"
		self.topic_aux = "/aux_topic"
		
		self.info = []
		self.angles = []
		self.X=[]
		self.Y=[]
		self.coorX = []
		self.coorY = []
		
		self.datos=[]

		self.dist=[]

		self.msg_aux = Bool()
		self.msg_scan = LaserScan()
		self.cambio_scan = False
		self.rate = self.rospy.Rate(50)

	def callback_scan(self, msg):
		self.msg_scan = msg.header
		self.msg_scan = msg.angle_min
		self.msg_scan = msg.angle_max
		self.msg_scan = msg.ranges
		self.msg_scan = msg.range_min
		self.msg_scan = msg.range_max
		self.msg_scan = msg.angle_increment
		self.cambio_scan = True
		self.info=[msg.ranges, msg.angle_increment, msg.angle_min]
		return

	def initSubscribers(self):
		self.sub_scan = self.rospy.Subscriber(self.topic_scan, LaserScan, self.callback_scan)
		return

	def initPublishers(self):
		self.pub_aux = self.rospy.Publisher(self.topic_aux, Bool, queue_size=10)
		return

	def main(self):
		while not self.rospy.is_shutdown():
			if self.cambio_scan:
				self.dist = []
				self.X = []
				self.Y = []
				self.coorX = []
				self.coorY = []
				self.acum = []

				for i in range(0,len(self.info[0])):
					self.angles.append(self.info[2] + i*self.info[1])
					self.X.append((self.info[0][i])*math.cos(self.angles[i]))
					self.Y.append((self.info[0][i])*math.sin(self.angles[i]))

					if self.Y[i] >0 and self.Y[i] <= 0.4:
						self.coorY.append(self.Y[i])
						self.coorX.append(self.X[i])
				
				self.contador = 0
				flag = False

				for j in range(1,len(self.coorX)):
					self.dist.append(math.sqrt((self.coorX[j]-self.coorX[j-1])**2+(self.coorY[j]-self.coorY[j-1])**2))
					if self.dist[j-1] <= 0.1:
						self.contador += 1
					else:
						self.acum.append(self.contador)
						self.contador = 0
						flag = True
				if not flag:
					self.acum.append(self.contador)
				
				flag_obst = False
				
				for k in self.acum:
					if k >= 5:
						flag_obst = True
				
				self.msg_aux.data = flag_obst
				self.pub_aux.publish(self.msg_aux)
				self.cambio_scan = False
				self.rate.sleep()
		return

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Nodo2()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
