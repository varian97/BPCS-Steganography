#!/usr/bin/python3
import numpy as np
import os

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
	length = 0
	plane_array = []
	plane_additional_data = []
	additional_binary = None
	file_name = None
	file_extension = None
	conjugate_map = []

	def __init__(self, pathname):
		with open(pathname, 'rb') as f:
			self.content = f.read()
		self.length = len(self.content)
		self.file_name, self.file_extension = os.path.splitext(pathname)

	# ngubah file pesan dari byte ke bit
	def to_binary(self):
		temp = [format(i, '08b') for i in self.content]
		self.content = temp
		while(len(self.content) % 8 != 0):
			self.content.append('00000000')

	# format bit nya menjadi array of bitplane. setiap bitplane ukurannya 64 bit
	def to_plane_array(self):
		temp = np.array([list(i) for i in self.content])
		self.plane_array = []
		windowsize_r = 8
		windowsize_c = 8
		for r in range(0,temp.shape[0] - windowsize_r + 1, windowsize_r):
			for c in range(0,temp.shape[1] - windowsize_c + 1, windowsize_c):
				self.plane_array.append(temp[r:r+windowsize_r,c:c+windowsize_c].astype(int))
		return self.plane_array

	# kalo misalnya ada plane pesan yang kurang kompleksitasnya, di konyugasi sama papan catur
	# inputnya harus np array
	def conjugate(self, plane):
		return plane ^ chessboard

	def calculate_complexity(self, i):
		counter = 0
		for r in range(8):
			for c in range(8):
				if(r != 7):
					if(self.plane_array[i][r][c] != self.plane_array[i][r+1][c]):
						counter += 1
				if(c != 7):
					if(self.plane_array[i][r][c] != self.plane_array[i][r][c+1]):
						counter += 1
		return counter / 112

	def prepareAdditionalMessage(self):
		additional_string = ""
		temp = []
		additional_string += str(len(self.conjugate_map)) + ";"
		additional_string += str(self.conjugate_map).strip('[]') + ";"
		additional_string += self.file_name + self.file_extension + ";"
		print(additional_string)
		for c in additional_string:
			temp.append(list(format(ord(c), '08b')))
		while(len(temp) % 8 != 0):
		 	temp.append('00000000')
		self.additional_binary = temp
		temp2 = np.array([list(i) for i in self.additional_binary])
		windowsize_r = 8
		windowsize_c = 8
		for r in range(0,temp2.shape[0] - windowsize_r + 1, windowsize_r):
		 	for c in range(0,temp2.shape[1] - windowsize_c + 1, windowsize_c):
		 		self.plane_additional_data.append(temp2[r:r+windowsize_r,c:c+windowsize_c].astype(int))
		#print(len(self.plane_additional_data))

	def prepareMessageBlock(self, threshold):
		for i in range(len(self.plane_array)):
			complexity = self.calculate_complexity(i)
			if complexity < threshold:
				print("blok {} terkonjugasi".format(i))
				self.conjugate(self.plane_array[i])
				self.conjugate_map.append(i)

	def convert_int_to_matrix_plane(self, number):
		temp2 = []
		k = 0
		tel = []
		for i in format(number, '064b'):
			tel.append(i)
			k = (k + 1) % 8
			if k == 0:
				temp2.append(tel)
				tel = []
		return temp2

	def combined_message_header(self):
		temp = []
		num_header = len(self.plane_additional_data)
		temp2 = self.convert_int_to_matrix_plane(num_header)
		num_plane = len(self.plane_array)
		temp3 = self.convert_int_to_matrix_plane(num_plane)
		temp.append(temp2)
		temp.append(self.plane_additional_data)
		temp.append(temp3)
		temp.append(self.plane_array)
		return temp


if __name__ == "__main__":
	m = Message('textpanjang.txt')
	#print("Load Pertama kali : \n", m.content)

	#print(m.file_name, m.file_extension)
	m.to_binary()
	#print(m.content)
	m.to_plane_array()
	#print(m.length)
	#print("Diubah ke binary plane : {} \n\n {}".format(m.plane_array[0], m.plane_array[1]))

	threshold = 0.3

	#print(m.calculate_complexity(0))
	m.prepareMessageBlock(threshold)
	m.prepareAdditionalMessage()
	print(m.combined_message_header())
	# Spesification, plane 1 [m] : jumlah plane additional (header), plane 2-m: additional data
	# plane m+1 [n]: jumlah plane message, plane m+2 - n: plane message
	#print(m.conjugate_map)
	# tes konyugasi
	#print("Binary plane : {} \n\n {}".format(m.plane_array[0], m.plane_array[1]))
