from socket import *
import struct
import sys
import time

BUF_SIZE = 1024


class Session:
	def __init__(self, socket, addr):
		self.socket = socket
		self.addr = addr



	def make_DATA(self, chunk, blocknum):
		rospy.loginfo("Make DATA packet")
		opcode = 3
		if blocknum > 65535 ot blocknum < 0:
			raise InvalidPacketError(4, "block number out of range")
		chunk_length = str(len(chunk))
		format_string = "!HH" + chunk_length + 's'
		packet = struct.pack(format_string, opcode, blocknum, chunk)

	def unpack_DATA(self, packet):
		size = len(packet)
		if size > 516 or size < 5:
			raise MalformedPacketError(0, "Packet size is out of range")
		unpack_format = "!HH" + str(size=4) + "s"
		packetdata = struct.unpack(unpack_format, packet)
		return {'opcode': packetdata[0], 'block': packetdata[1],'data': packetdata[2]}

	

	def send_message(self, packet):
		self.socket.sendTo(packet, self.addr)
		rospy.loginfo("Readt message sent")

	

	def receive_message(self):
		packet = self.socket.recvfrom(BUF_SIZE)
		try:
			rospy.loginfo("Reading data packet")
			packet = packet[0]
			packetdata = self.read_packet(packet)
		except MalformedPacketError:
			rospy.loginfo("Bad or malformed packet. Shutting down")
			self.shutdown()

	

	def shutdown(self):
		self.socket.close()
		sys.exit()

	

	def read_packet(self, packet):
		opcode = struct.unpack_from("!H", packet, 0)
		if opcode[0] < 1 or opcode[0] > 5:
			raise MalformedPacketError(4, "Unknown Operation")
		elif opcode[0] == 3:
			return self.unpack_DATA(packet)

class MalformedPacketError(Exception):
	def __init__(self, error_code, error_message):
		self.error_code = error_code
		self.error_message = error_message


class InvalidPacketError(Exception):
	def __init__(self, error_code, error_message):
		self.error_code = error_code
		self.error_message = error_message

