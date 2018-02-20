#!/usr/bin/python3
import argparse
import cv2
from bpcs import BPCS, psnr
from message import Message

def create_arguments():
	"""Create command line argument for this program.
	"""

	parser = argparse.ArgumentParser(
		description='A BPCS-based algorithm Steganography Program'
	)
	parser.add_argument("original_img", help="The original image path that you will put a hidden message")
	parser.add_argument("secret_message", help="Your secret message file path. The message must be stored inside a file.")
	parser.add_argument("threshold", help="alpha Treshold in BPCS algorithm", type=float)
	parser.add_argument("-e", "--extract", help="Extract the secret message from a stegano image. \n If this option is used, <original_image> argument is treated as <stegano_image> and <secret_message> will become the stored secret message path", action="store_true")
	parser.add_argument("-k", "--key", help="Key to encrypt message using Vigenere256bit")
	parser.add_argument("-r", "--randomize", help="Randomize the message placement inside the bitplane", action="store_true")
	parser.add_argument("-o", "--output", help="Stegano Image output. The image that has a hidden message stored inside.")

	return parser.parse_args()

def extract(args):
	bpcs = BPCS(args.original_img)
	bitplane_msg = bpcs.show(randomize=args.randomize, key=args.key, threshold = args.threshold)

	print(bitplane_msg[:10])
	encrypted = True if args.key != None else False

	print (encrypted)
	msg = Message(encrypted = encrypted, key = args.key)
	msg.from_bitplane_array(bitplane_msg)
	msg.write_msg(args.secret_message)
	return

# create stegano image
def create(args):
	bpcs = BPCS(args.original_img)
	orig_extension = args.original_img.split('.')[-1]

	# prepare message
	encrypted = True if args.key != None else False
	#print (encrypted)
	msg = Message(pathname=args.secret_message, encrypted = encrypted, key = args.key, threshold = args.threshold)
	bitplane_msg = msg.create_message()
	#print(bitplane_msg[:10])

	img_result = bpcs.hide(bitplane_msg, randomize=args.randomize, key=args.key, threshold = args.threshold)
	if args.output == None:
		args.output = 'output'
	args.output += "." + orig_extension

	cv2.imwrite(args.output, img_result)
	origin_image = cv2.imread(args.original_img, -1)
	embed_image = cv2.imread(args.output,-1)
	
	psnr_value = psnr(origin_image, embed_image)

	print("PSNR: {}".format(psnr_value))
	# show embedded & original image
	cv2.imshow('Original Image', origin_image)
	cv2.imshow("Embedded Image (PSNR: {})".format(psnr_value),embed_image)
	cv2.waitKey(0)
	return

if __name__ == '__main__':

	args = create_arguments()
	print("Original Image: {}".format(args.original_img))
	if args.extract:
		extract(args)
	else:
		create(args)
