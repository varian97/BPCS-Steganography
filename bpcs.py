import cv2
import numpy as np
from message import Message

class BPCS(object):

	def __init__(self, img_path):
		self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
		self.row, self.col, self.channels = self.img.shape

	def hide(self, message, threshold = 0.3):
		if (self.channels == 4): # GAMBAR 4 CHANNEL ada Alpha (untuk PNG)
			windowsize_r = 8
			windowsize_c = 8

			message_iterator = 0
			while(message_iterator < len(message)):
				for row in range(0,self.row - windowsize_r + 1, windowsize_r):
					for col in range(0,self.col - windowsize_c + 1, windowsize_c):
						temp_block = self.img[row:row+windowsize_r, col:col+windowsize_c]

						b,g,r,a = cv2.split(temp_block)

						b_bitplane = self.to_bitplane(b)
						g_bitplane = self.to_bitplane(g)
						r_bitplane = self.to_bitplane(r)
						a_bitplane = self.to_bitplane(a)

						# masukin message
						it_b, it_g, it_r = 0, 0, 0
						while(it_b < len(b_bitplane) and message_iterator < len(message)):
							if(self.calculate_complexity(b_bitplane[it_b]) >= threshold):
								b_bitplane[it_b] = message[message_iterator]
								message_iterator += 1
							it_b += 1

						while(it_g < len(g_bitplane) and message_iterator < len(message)):
							if(self.calculate_complexity(g_bitplane[it_g]) >= threshold):
								g_bitplane[it_g] = message[message_iterator]
								message_iterator += 1
							it_g += 1

						while(it_r < len(r_bitplane) and message_iterator < len(message)):
							if(self.calculate_complexity(r_bitplane[it_r]) >= threshold):
								r_bitplane[it_r] = message[message_iterator]
								message_iterator += 1
							it_r += 1

						# gabungin lagi bitplane ke channel2 semula
						blue = self.bitplane_to_channel(b_bitplane)
						green = self.bitplane_to_channel(g_bitplane)
						red = self.bitplane_to_channel(r_bitplane)
						alpha = self.bitplane_to_channel(a_bitplane)

						# gabungin ke gambar utuh
						temp_block = cv2.merge((blue, green, red, alpha))

						# rewrite gambar asli dengan informasi rahasia
						self.img[row:row+windowsize_r, col:col+windowsize_c] = temp_block

					#kotor tapi bodo amat
					if(message_iterator >= len(message)): break

				if(message_iterator >= len(message)): break
			return self.img

		elif (self.channels == 3): # GAMBAR 3 CHANNEL, gak ada alpha (untuk BMP)
			pass
		else:
			print('Not Supported Image')

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
	bpcs = BPCS('watch.png')
	m = Message('README.md')
	m.to_binary()
	m.to_plane_array()
	threshold = 0.3
	m.prepareMessageBlock(threshold)
	img_result = bpcs.hide(m.plane_array)
	cv2.imwrite('hasil1.png', img_result)