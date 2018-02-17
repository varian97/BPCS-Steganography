#!/usr/bin/python3
import cv2
import numpy as np
import random
from message import Message

class BPCS(object):

	def __init__(self, img_path):
		self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
		self.row, self.col, self.channels = self.img.shape

	def generate_seed(self, key):
		"""Generate random seed based on key
		"""
		return sum([ord(a) for a in key])

	def get_row_col(self, sequence_number):
	    row = (sequence_number) // 8
	    col = (sequence_number) % 8
	    return (row, col)

	def hide(self, message, threshold = 0.3, randomize = False, key = None):
		windowsize_r = 8
		windowsize_c = 8

		if (randomize):
			random.seed(self.generate_seed)
			rand_sequence = random.sample(range(64), 64)
		print("lenmsg", len(message))

		message_iterator = 0
		while(message_iterator < len(message)):
			for row in range(0,self.row - windowsize_r + 1, windowsize_r):
				for col in range(0,self.col - windowsize_c + 1, windowsize_c):
					temp_block = self.img[row:row+windowsize_r, col:col+windowsize_c]
					channels_block = cv2.split(temp_block)

					channels_bitplane = [self.to_bitplane(block) for block in channels_block]
					for i in range(len(channels_bitplane)):
						itr_bitplane = 0
						while(itr_bitplane < len(channels_bitplane[i]) and message_iterator < len(message)):
							if(self.calculate_complexity(channels_bitplane[i][itr_bitplane]) >= threshold):
								print(self.calculate_complexity(channels_bitplane[i][itr_bitplane]))
								channels_bitplane[i][itr_bitplane] = message[message_iterator]
								message_iterator += 1
								print("put in", row, col, i, itr_bitplane, message_iterator)
							itr_bitplane += 1

					new_channels = [self.bitplane_to_channel(bitplane) for bitplane in channels_bitplane]

					# gabungin ke gambar utuh
					temp_block = cv2.merge(new_channels)

					# rewrite gambar asli dengan informasi rahasia
					self.img[row:row+windowsize_r, col:col+windowsize_c] = temp_block

				#kotor tapi bodo amat
				if(message_iterator >= len(message)): break

			if(message_iterator >= len(message)): break
		return self.img

	def show(self, threshold = 0.3, randomize = False, key = None):
		windowsize_r = 8
		windowsize_c = 8

		msg_bitplane = []

		if (randomize):
			random.seed(self.generate_seed)
			rand_sequence = random.sample(range(64), 64)

		message_iterator = 0
		for row in range(0,self.row - windowsize_r + 1, windowsize_r):
			for col in range(0,self.col - windowsize_c + 1, windowsize_c):
				temp_block = self.img[row:row+windowsize_r, col:col+windowsize_c]
				channels_block = cv2.split(temp_block)

				channels_bitplane = [self.to_bitplane(block) for block in channels_block]

				i = 0
				for channel_bitplane in channels_bitplane:
					j = 0
					for bitplane in channel_bitplane:
						if(self.calculate_complexity(bitplane) >= threshold):
							if message_iterator < 1:
								print(self.calculate_complexity(bitplane))
								print("get_from", row, col, i, j)
							msg_bitplane.append(bitplane)
							message_iterator += 1
						j += 1
					i += 1


		return msg_bitplane

	def to_bitplane(self, img):
		result = []
		for i in reversed(range(8)):
			result.append((img / (2 ** i)).astype(int) % 2)
		return result

	def bitplane_to_channel(self, bitplane):
		result = (2 * (2 * (2 * (2 * (2 * (2 * (2 * bitplane[0] + bitplane[1])
					+ bitplane[2]) + bitplane[3]) + bitplane[4])
					+ bitplane[5]) + bitplane[6]) + bitplane[7])
		return result

	def calculate_complexity(self, img):
		counter = 0
		for r in range(img.shape[0]):
			for c in range(img.shape[1]):
				if(r != img.shape[0]-1):
					if(img[r][c] != img[r+1][c]):
						counter += 1
				if(c != img.shape[1]-1):
					if(img[r][c] != img[r][c+1]):
						counter += 1
		return counter / 112

if __name__ == '__main__':
	bpcs = BPCS('testcase/original_img/Ape_Face.bmp')

	message = [
				np.array([[0, 0, 1, 0, 0, 0, 1, 1],
						 [0, 0, 1, 0, 0, 0, 0, 0],
						 [0, 1, 0, 0, 0, 0, 1, 0],
						 [0, 1, 0, 1, 0, 0, 0, 0],
						 [0, 1, 0, 0, 0, 0, 1, 1],
						 [0, 1, 0, 1, 0, 0, 1, 1],
						 [0, 0, 1, 0, 1, 1, 0, 1],
						 [0, 1, 0, 1, 0, 0, 1, 1]]),
				np.array([[0, 0, 1, 0, 0, 0, 1, 1],
						 [0, 0, 1, 0, 1, 0, 0, 0],
						 [0, 1, 0, 0, 0, 0, 1, 0],
						 [0, 1, 0, 1, 0, 0, 0, 0],
						 [0, 1, 0, 0, 1, 0, 1, 1],
						 [0, 1, 0, 1, 0, 0, 1, 1],
						 [0, 0, 1, 0, 1, 1, 0, 1],
						 [0, 1, 0, 1, 0, 0, 1, 1]]),
			  ]

	img_result = bpcs.hide(message)
	cv2.imwrite('testcase/result_img/hasil2.png', img_result)

	bpcs2 = BPCS('testcase/result_img/hasil2.png')
	print(bpcs.show()[0:2])

	# bpcs = BPCS('watch.png')
	# m = Message('README.md')
	# m.to_binary()
	# m.to_plane_array()
	# threshold = 0.3
	# m.prepareMessageBlock(threshold)
	# img_result = bpcs.hide(m.plane_array)
	# cv2.imwrite('hasil1.png', img_result)
