import os
import numpy as np
import cv2
names = []

def read_image(image_path):
	global names
	names.append(image_path)
	# We read the image
	try:
		image = cv2.imread(image_path,-1)
	except OSError as err:
		print("Error: "+str(err))
		exit(1)
		return None
	return image
	# We take the maximum pixel value of each filter
	max = np.max(image, axis=0)
	max = np.max(max, axis=0, keepdims=True)
	max = np.tile(max, (image.shape[0], image.shape[1], 1))

	# We take the minimum pixel value of each filter
	min = np.min(image, axis=0)
	min = np.min(min, axis=0, keepdims=True)
	min = np.tile(min, (image.shape[0], image.shape[1], 1))

	# and we do a min-max normalization
	image = (((image - min) / (max-min))**(1/2.2)) * 255	
	return image

def read_checker(image_name,H,W):
	csv = np.genfromtxt(os.path.join("CHECKER", "{0}_mask.txt".format(image_name)), delimiter=',')
	big_rec = csv[0]
	small_recs = csv[1:]
	
	xmn, ymn = big_rec[0]			  , big_rec[1]
	xmx, ymx = big_rec[0] + big_rec[2], big_rec[1] + big_rec[3] 
	x = (xmn+xmx)/2
	y = (ymn+ymx)/2
	f = open(os.path.join("fixed_test", "{0}.txt".format(image_name)),'w')
	f.write(str(int(0)) + ' ' + str(x/W) + ' ' + str (y/H) + ' ' + str(big_rec[2]/W) + ' ' + str(big_rec[3]/H) + "\n")
	
	c = 1
	for i in range(0, small_recs.shape[0], 2):
		xs = small_recs[i] + big_rec[0]
		ys = small_recs[i + 1] + big_rec[1]
		xmn, ymn = min(xs), min(ys)
		xmx, ymx = max(xs), max(ys)
		x = (xmn+xmx)/2
		y = (ymn+ymx)/2
		w = xmx - xmn
		h = ymx - ymn
		f.write(str(c) + ' ' + str(x/W)  + ' ' + str(y/H)  + ' ' + str(w/W)  + ' ' + str(h/H) + '\n' )
		c += 1

if __name__ == '__main__':
	dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"fixed_test")
	
	if not os.path.exists(dir_path):
		print("error reading the directory")
		exit(1)

	for subdir, dirs, files in os.walk(dir_path):
		for file in files:
			filepath = subdir + os.sep + file
			#if 'fixed' in filepath:
			#	continue

			if filepath.endswith(".png") or filepath.endswith(".PNG"):
				filename = file[:-4]
				img = read_image(filepath)
				read_checker(filename,img.shape[0],img.shape[1])
	f = open('test.txt','w')
	for x in names:
		f.write(x + '\n')
	
			
