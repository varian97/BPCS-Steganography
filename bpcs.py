import cv2
import numpy as np


class BPCS(object):

	def __init__(self, img):
		self.img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
		self.row, self.col = img.shape[0], img.shape[1]

	def hide(self, message, threshold):
		windowsize_r = 8
		windowsize_c = 8
		for r in range(0,self.row - windowsize_r, windowsize_r):
			for c in range(0,self.col - windowsize_c, windowsize_c):
				temp_block = (img[r:r+windowsize_r,c:c+windowsize_c])
				b,g,r,a = cv2.split(temp_block)

				b_bitplane = self.to_bitplane(b)
				g_bitplane = self.to_bitplane(g)
				r_bitplane = self.to_bitplane(r)
				a_bitplane = self.to_bitplane(a)

				# TODO : MASUKIN MESSAGE KE BITPLANE NYA

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