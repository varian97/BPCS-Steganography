import cv2
import numpy as np


class BPCS(object):

	def __init__(self, img_path):
		self.img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
		self.row, self.col, self.channels = self.img.shape

	def hide(self, message, threshold = 0.3):
		print(self.channels)
		if (self.channels == 4): # GAMBAR 4 CHANNEL ada Alpha (untuk PNG)
			conjugated = []
			windowsize_r = 8
			windowsize_c = 8
			for r in range(0,self.row - windowsize_r + 1, windowsize_r):
				for c in range(0,self.col - windowsize_c + 1, windowsize_c):
					temp_block = (self.img[r:r+windowsize_r,c:c+windowsize_c])
					b,g,r,a = cv2.split(temp_block)

					b_bitplane = self.to_bitplane(b)
					g_bitplane = self.to_bitplane(g)
					r_bitplane = self.to_bitplane(r)
					a_bitplane = self.to_bitplane(a)

					print(temp_block)
					# TODO : MASUKIN MESSAGE KE BITPLANE NYA
		elif (self.channels == 3): # GAMBAR 3 CHANNEL, gak ada alpha (untuk BMP)
			pass
		else:
			print('Not Supported Image')

	def to_bitplane(self, img):
		result = []
		for i in reversed(range(8)):
			result.append((img / (2 ** i)) % 2)
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
	bpcs.hide('hello')