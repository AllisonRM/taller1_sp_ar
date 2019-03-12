#!/usr/bin/python
import serial
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class Nodo1():
	def __init__(self):
		self.rospy = rospy
		self.rospy.init_node("nodo_1", anonymous = True)
		self.initParameters()
		self.initPublishers()
		self.main()

	def initParameters(self):
		self.arduino = serial.Serial('/dev/ttyACM0', 9600)
		self.topic_lin = "/linear"
		self.topic_ang = "/angular"
		self.serial = "/serial"
		self.msg_lin = String()
 		self.msg_ang = String()
		self.vel_lin = String()
		self.vel_ang = String()
		return

	def initPublishers(self):
		self.pub_lin = self.rospy.Publisher(self.topic_lin, String, queue_size = 10)
		self.pub_ang = self.rospy.Publisher(self.topic_ang, String, queue_size = 10)
		return

	def main(self):
		print ("Nodo 1 OK")

		while not self.rospy.is_shutdown():
			raw = self.arduino.readline()
			self.msg_lin,self.msg_ang = raw.split("&")
			self.vel_lin = str(self.msg_lin)
			self.vel_ang = str(self.msg_ang)
			self.pub_lin.publish(self.vel_lin)
			self.pub_ang.publish(self.vel_ang)

if __name__ == "__main__":
	try:
		print("Iniciando Nodo")
		nodo = Nodo1()
	except rospy.ROSInterruptException:
		print("Finalizando Nodo")
		pass
