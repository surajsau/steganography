from PIL import Image
import sys
import io
from urllib.request import urlretrieve

def encode(src1, src2, dest):
	img1 = Image.open(src1, 'r')
	img2 = Image.open(src2, 'r')

	px_img1 = img1.load()
	px_img2 = img2.load()

	if img1.mode == "RGB":
		channels = 3
	elif img1.mode == "RGBA":
		channels = 4

	merged_imaged = Image.new(img1.mode, img1.size)
	px_merged = merged_imaged.load()

	for i in range(img1.size[0]):
		for j in range(img1.size[1]):
			modified_px = [0] * channels

			for k in range(channels):
				px1 = px_img1[i, j][k]
				px1_bin = '{0:08b}'.format(px1)

				if i < img2.size[0] and j < img2.size[1]:
					px2 = px_img2[i, j][k]
					px2_bin = '{0:08b}'.format(px2)
					px = px1_bin[:4] + px2_bin[:4]
					modified_px[k] = int(px, 2)
				else:
					modified_px[k] = px1

			px_merged[i, j] = tuple(modified_px)

	merged_imaged.save(dest)

def decode(src, dest):
	img = Image.open(src, 'r')

	px_img = img.load()

	hidden_image = Image.new(img.mode, img.size)
	px_hidden = hidden_image.load()

	if img.mode == "RGB":
		channels = 3
	elif img.mode == "RGBA":
		channels = 4

	for i in range(img.size[0]):
		for j in range(img.size[1]):
			hidden_px = [0] * channels

			for k in range(channels):
				px = px_img[i, j][k]
				px_bin = '{0:08b}'.format(px)

				h_px = px_bin[4:] + '0000'
				hidden_px[k] = int(h_px, 2)

			px_hidden[i, j] = tuple(hidden_px)

	hidden_image.save(dest)


def main():
	print('encode or decode?')
	print('1 for encode')
	print('2 for decode')
	function_type = input()

	if function_type == "1":
		print('img1: ')
		img1 = input()
		print('img2: ')
		img2 = input()
		print('dest: ')
		dest = input()

		encode(img1, img2, dest)
	elif function_type == "2":
		print('src: ')
		src = input()
		print('dest: ')
		dest = input()
		decode(src, dest)
	else:
		print('invalid input')
		main()

if __name__ == "__main__":
	main()
