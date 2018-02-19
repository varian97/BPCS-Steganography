#!/usr/bin/python3
import argparse

def create_arguments():
	"""Create command line argument for this program.
	"""

	parser = argparse.ArgumentParser(
		description='A BPCS-based algorithm Steganography Program'
	)
	parser.add_argument("original_image", help="The original image path that you will put a hidden message")
	parser.add_argument("secret_message", help="Your secret message file path. The message must be stored inside a file.")
	parser.add_argument("bpcs_threshold", help="alpha Treshold in BPCS algorithm")
	parser.add_argument("-e", "--extract", help="Extract the secret message from a stegano image. \n If this option is used, <original_image> argument is treated as <stegano_image> and <secret_message> will become the stored secret message path", action="store_true")
	parser.add_argument("-k", "--key", help="Key to encrypt message using Vigenere256bit")
	parser.add_argument("-r", "--randomize", help="Randomize the message placement inside the bitplane", action="store_true")
	parser.add_argument("-o", "--output", help="Stegano Image output. The image that has a hidden message stored inside.")

	return parser.parse_args()

def extract(args):
	bpcs = BPCS(args.original_img)
	bitplane_msg = bpcs.show(randomize=args.randomize, key=args.key)

	encrypted = True if key != None else False
	msg12 = Message(encrypted = encrypted, key = args.key)
	msg12.from_bitplane_array(bitplane_msg)
	msg12.write_msg(args.secret_message)
	return

# create stegano image
def create(args):
	bpcs = BPCS(args.original_img)

	# prepare message
	encrypted = True if key != None else False
	msg = Message(pathname=args.secret_message, encrypted = encrypted, key =args.key)
	bitplane_msg = msg.create_message()

	img_result = bpcs.hide(bitplane_msg, args.randomize, args.key)

	if args.output == None:
		args.output = 'output'

	cv2.imwrite(args.output, img_result)
	return


if __name__ == '__main__':

	args = create_arguments()

	if args.extract:
		extract(args)
	else:
		create(args)
