
chessboard = [i % 2 for i in range(64)]

class Message(object):
	def __init__(self, pathname):
		with open(pathname, 'rb') as f:
			self.content = f.read()
		self.length = len(self.content)

	def to_binary(self):
		temp = [bin(i).replace('0b','0') for i in self.content]
		self.content = temp
		while(len(self.content) % 8 != 0):
			self.content.append('00000000')

	def conjugate(self, plane):
		new = []
		if plane.length == 64:
			i = 0
			for pixel in plane:
				new[i] = pixel ^ chessboard[i]
				i += 1
		return new
