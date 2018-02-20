#!/usr/bin/python3
import numpy as np
import os
import vigenere_cipher
import math
from pprint import pprint

chessboard = np.array([[0, 1, 0, 1, 0, 1, 0, 1],
						[1, 0, 1, 0, 1, 0, 1, 0],
						[0, 1, 0, 1, 0, 1, 0, 1],
						[1, 0, 1, 0, 1, 0, 1, 0],
						[0, 1, 0, 1, 0, 1, 0, 1],
						[1, 0, 1, 0, 1, 0, 1, 0],
						[0, 1, 0, 1, 0, 1, 0, 1],
						[1, 0, 1, 0, 1, 0, 1, 0]])

class Message(object):

	content = None
	content_length = 0
	header = None
	header_length = 0
	file_name = None
	file_extension = None
	content_bitplane = []
	header_bitplane = []
	plane_additional_data = []
	conjugate_list = []
	conjugation_map = []

	bitplane_array = []
	threshold = 0

	encrypted = False
	key = None

	def __init__(self, pathname = None, encrypted = False, key = None, threshold = 0.3):
		self.threshold = threshold
		self.encrypted = encrypted
		self.key = key

		if (pathname != None):
			with open(pathname, 'rb') as f:
				self.content = f.read()
			self.content_length = len(self.content)
			self.file_name, self.file_extension = os.path.splitext(pathname)
			self.file_name = self.file_name.split('/')[-1]

			# encrypt file if needed
			if (encrypted and key != None):
				self.content = vigenere_cipher.encrypt(self.content, key)

	# ngubah file pesan dari byte ke bit, msg harus dalam binary format
	def to_binary(self, msg):
		temp = [format(i, '08b') for i in msg]
		binary_msg = temp
		while(len(binary_msg) % 8 != 0):
			binary_msg.append('01010101')

		return binary_msg

	# format bit nya menjadi array of bitplane. setiap bitplane ukurannya 64 bit
	def to_bitplane(self, binary_msg):
		temp = np.array([list(i) for i in binary_msg])
		# print(temp)
		bitplane_msg = []
		windowsize_r = 8
		windowsize_c = 8
		for r in range(0,temp.shape[0] - windowsize_r + 1, windowsize_r):
			for c in range(0,temp.shape[1] - windowsize_c + 1, windowsize_c):
				bitplane_msg.append(temp[r:r+windowsize_r,c:c+windowsize_c].astype(int))
		return bitplane_msg

	# kalo misalnya ada plane pesan yang kurang kompleksitasnya, di konyugasi sama papan catur
	# inputnya harus np array
	def conjugate(self, plane):
		return plane ^ chessboard

	def calculate_complexity(self, i):
		counter = 0
		for r in range(8):
			for c in range(8):
				if(r != 7):
					if(self.bitplane_array[i][r][c] != self.bitplane_array[i][r+1][c]):
						counter += 1
				if(c != 7):
					if(self.bitplane_array[i][r][c] != self.bitplane_array[i][r][c+1]):
						counter += 1
		return counter / 112

	# check complexity tiap bitplane, conjugate kalo perlu, tambahin ke conjugate map
	def conjugate_message_content(self):
		for i in range(len(self.content_bitplane)):
			complexity = self.calculate_complexity(i)
			# print(complexity)
			if complexity < self.threshold:
				# print("blok {} terkonjugasi".format(i))
				self.bitplane_array[i] = self.conjugate(self.bitplane_array[i])
				self.conjugate_list.append(i)

	def create_message_content(self):
		content_binary = self.to_binary(self.content)
		self.content_bitplane = self.to_bitplane(content_binary)

	# format header:
	# len file_name ; file_extension ; content_length
	# num header: 5
	def create_message_header(self):
		msg_header_string = ""
		temp = []
		msg_header_string += self.file_name + ";"
		msg_header_string += self.file_extension + ";"
		msg_header_string += str(self.content_length) + ";"
		#print(msg_header_string)

		self.header = msg_header_string.encode('utf-8')
		self.header_length = len(msg_header_string)

		if (self.encrypted and self.key != None):
			self.header = vigenere_cipher.encrypt(self.header, self.key)


		header_binary = self.to_binary(self.header)
		self.header_bitplane = self.to_bitplane(header_binary)
		return self.header_bitplane

	# convert integer to 64-bit format in bitplane
	def convert_int_to_matrix_plane(self, number):
		bit = format(number, '064b')
		chunks = np.array([list(bit[x:x+8]) for x in range(0, len(bit), 8)])

		# print(chunks)
		chunks = self.conjugate(chunks.astype(int))
		bitplane = []
		bitplane.append(chunks)
		# print(bitplane)
		return bitplane

	def matrix_to_int(self, bitplane):
		bitplane = self.conjugate(bitplane)
		in_binary = ''.join([''.join(row) for row in bitplane.astype(str)])

		integer = int(in_binary, 2)

		return integer

	# create message bitplane containing message header & message content
	def create_message(self):
		self.create_message_content()
		self.create_message_header()

		num_header = len(self.header_bitplane)
		self.bitplane_array += self.convert_int_to_matrix_plane(num_header)
		self.bitplane_array += self.header_bitplane

		num_plane = len(self.content_bitplane)
		self.bitplane_array += self.convert_int_to_matrix_plane(num_plane)
		self.bitplane_array += self.content_bitplane

		# conjugate map shits
		self.conjugate_message_content()
		conj_map = self.create_conjugation_map()
		conj_bitplane = self.convert_int_to_matrix_plane(len(conj_map))
		conj_bitplane += conj_map

		self.bitplane_array = conj_bitplane + self.bitplane_array
		# print(num_header, num_plane, len(self.bitplane_array))
		return self.bitplane_array

	def create_conjugation_map(self):
		conj_map = ['0' for i in range(len(self.bitplane_array))]
		for pos in self.conjugate_list:
			conj_map[pos] = '1'

		while(len(conj_map) % 8 != 0):
			conj_map.append('0')

		conj_binary = [''.join(conj_map[x:x+8]) for x in range(0, len(conj_map), 8)]
		while(len(conj_binary) % 8 != 0):
			conj_binary.append('01010101')
		# print(len(conj_map))
		# pprint (conj_binary)
		self.conjugation_map = self.to_bitplane(conj_binary)

		for i in range(len(self.conjugation_map)):
			self.conjugation_map[i] = self.conjugate(self.conjugation_map[i])
		return self.conjugation_map

	def deconjugate_bitplane(self, bitplane):
		for i in range(len(self.conjugation_map)):
			self.conjugation_map[i] = self.conjugate(self.conjugation_map[i])

		conj_map = []
		for plane in self.conjugation_map:
			conj_map.append(''.join([''.join(row) for row in plane.astype(str)]))
		conj_map = ''.join(conj_map)

		for i in range(len(conj_map)):
			if (conj_map[i] == '1'):
				bitplane[i] = self.conjugate(bitplane[i])

		return bitplane

	def from_bitplane_array(self, bitplane_array):
		# print(len(bitplane_array))
		conj_map_length = self.matrix_to_int(bitplane_array[0])
		self.conjugation_map = bitplane_array[1:conj_map_length + 1]

		bitplane_array = bitplane_array[conj_map_length+1:]

		bitplane_array = self.deconjugate_bitplane(bitplane_array)

		header_length = self.matrix_to_int(bitplane_array[0])
		self.header_bitplane = bitplane_array[1:header_length + 1]
		#print(header_length, self.header_bitplane)

		# buang len header sama header dari bitplane array
		bitplane_array = bitplane_array[header_length+1:]

		content_length = self.matrix_to_int(bitplane_array[0])
		self.content_bitplane = bitplane_array[1:content_length+1]
		#print (content_length, self.content_bitplane)

		self.get_header_from_bitplanes()
		self.get_content_from_bitplanes()

	def get_byte_from_bitplane_array(self, bitplane_array):
		byte_array = bytearray()

		for plane in bitplane_array:
			for row in plane:
				byte = int(''.join(row.astype(str)), 2)
				byte_array.append(byte)

		return byte_array

	def get_header_from_bitplanes(self):
		self.header = self.get_byte_from_bitplane_array(self.header_bitplane)

		if (self.encrypted and self.key != None):
			self.header = vigenere_cipher.decrypt(self.header, self.key)

		self.header = self.header.decode('utf-8', errors="ignore")

		header_chunk = self.header.split(';')
		#print(header_chunk)
		self.conjugate_list = []
		# if header_chunk[0] != '':
		# 	for conjugate_pos in header_chunk[0].split(','):
		# 		self.conjugate_list.append(int(conjugate_pos))

		self.file_name = header_chunk[0]
		self.file_extension = header_chunk[1]
		self.content_length = int(header_chunk[2])
		# print(self.conjugate_list)
		# print(self.content_length)
		# print(self.file_extension)
		# print(self.file_name)

		return self.header

	def get_content_from_bitplanes(self):
		content = self.get_byte_from_bitplane_array(self.content_bitplane)
		self.content = content[:self.content_length]

		if (self.encrypted and self.key != None):
			self.content = vigenere_cipher.decrypt(self.content, self.key)


		# print (self.content)
		return self.content

	def write_msg(self, file_name=None):
		if file_name == None:
			file_name = self.file_name
		file_name += self.file_extension

		with open(file_name, 'wb') as fout:
			fout.write(self.content)

def calculate_complexity(img):
    counter = 0
    for r in range(8):
        for c in range(8):
            if(r != 7):
                if(img[r][c] != img[r+1][c]):
                    counter += 1
            if(c != 7):
                if(img[r][c] != img[r][c+1]):
                    counter += 1
    return counter / 112

if __name__ == "__main__":
	msg = Message(pathname='testcase/original_img/watch.png')
	bitplane_msg = msg.create_message()
	print(len(bitplane_msg))
	for b in bitplane_msg:
		# print (calculate_complexity(b))
		if (calculate_complexity(b) <= 0.3):
			print(b)

	# print(bitplane_msg)
	msg12 = Message()
	msg12.from_bitplane_array(bitplane_msg)
	msg12.write_msg()
