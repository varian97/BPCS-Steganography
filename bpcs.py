import cv2
import numpy as np


img_png_filename = 'watch.png'
img_bmp_filename = 'Ape_Face.bmp'

# split image into block of 8 pixel x 8 pixel
def group_image(img):
	result = []
	windowsize_r = 8
	windowsize_c = 8
	for r in range(0,img.shape[0] - windowsize_r, windowsize_r):
		for c in range(0,img.shape[1] - windowsize_c, windowsize_c):
			result.append(img[r:r+windowsize_r,c:c+windowsize_c])
	return result

# get all 8 bitplanes for an image
# 10010100 -> bitplane 8 is 1, bitplane 0 is 0
def to_bitplane(img, bit):
	result = []
	for i in range(8):
		result.append((img / (2 ** i)) % 2)
	return result

if __name__ == '__main__':
	img_bmp = cv2.imread(img_bmp_filename, -1)
	img_bmp_grouped = group_image(img_bmp)

	print(img_bmp_grouped[0])

	#cv2.imshow('image_bmp', img_bmp)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()