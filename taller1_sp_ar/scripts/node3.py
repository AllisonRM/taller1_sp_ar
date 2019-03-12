#!/usr/bin/python
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Bool

class Nodo3():
	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node('nodo_3', anonymous = True)
		self.initParameters()
		self.initSubscribers()
		self.initPublishers()
		self.main()

	def initParameters(self):
		self.topic_lin = "/linear"
		self.topic_ang = "/angular"
		self.topic_aux = "/aux_topic"
		self.vel_topic = "/cmd_vel"
		self.mensaje_vel = Twist()
		self.vel_lin = String()
		self.vel_ang = String()
		self.msg_aux = Bool
		self.cambio1 = False
		self.cambio2 = False
		self.cambio3 = False
		self.rate = self.rospy.Rate(50)
		return

	def initSubscribers(self):
		self.sub1 = self.rospy.Subscriber(self.topic_lin, String, self.callback1)
		self.sub2 = self.rospy.Subscriber(self.topic_ang, String, self.callback2)
		self.sub3 = self.rospy.Subscriber(self.topic_aux, Bool, self.callback3)
		return

	def initPublishers(self):
		self.pub1 = self.rospy.Publisher(self.vel_topic, Twist, queue_size=10)
		return

	def callback1(self, msg):
		self.vel_lin = msg.data
		self.cambio1 = True
		return

	def callback2(self, msg):
		self.vel_ang = msg.data
		self.cambio2 = True
		return

	def callback3(self, msg):
		self.msg_aux  = msg.data
		self.cambio3 = True
		return

	def main(self):
		while not self.rospy.is_shutdown():
			if self.cambio1 and self.cambio2 and self.cambio3:
				if self.msg_aux == False:
					self.mensaje_vel.linear.x = float(self.vel_lin)
					self.mensaje_vel.angular.z = float(self.vel_ang)
					self.pub1.publish(self.mensaje_vel)
					print("Move")
				else:
					self.mensaje_vel.linear.x = float(0)
					self.mensaje_vel.angular.z = float(0)
					self.pub1.publish(self.mensaje_vel)
					print("Stop")
				self.cambio1 = False
				self.cambio2 = False
				self.cambio3 = False
		return

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Nodo3()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
