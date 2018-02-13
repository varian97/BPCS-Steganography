import numpy as np

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

	def __init__(self, pathname):
		with open(pathname, 'rb') as f:
			self.content = f.read()
		self.length = len(self.content)

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

if __name__ == "__main__":
	m = Message('../play.txt')
	print("Load Pertama kali : \n", m.content)

	m.to_binary()
	m.to_plane_array()
	print("Diubah ke binary plane : {} \n\n {}".format(m.plane_array[0], m.plane_array[1]))

	# tes konyugasi
	conjugate_res = m.conjugate(m.plane_array[0])
	print("tes konyugasi = ", conjugate_res)