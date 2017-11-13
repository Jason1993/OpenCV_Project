import cv2
import numpy as np

def main():

	#run for images from #0 - #439. If you want only one image per camera angle, increment counter by 20
	for i in range(0,440):

		#compute correct image num
		if i>=100:
			num = "0" + str(i)
		elif i>=10:
			num = "00" + str(i)
		else:
			num= "000" + str(i)

		#read obj and empty depth images (8 bit images as most of OpenCv funcs don't work on 16bit images)
		obj = cv2.imread("/home/sailesh/Documents/RealDepth/Teapot/Noise/CAM-Depth_" + num + ".png")
		empty = cv2.imread("/home/sailesh/Documents/RealDepth/Empty/Noise/CAM-Depth_" +num + ".png")

		#read object image as is (in 16 bit) as we need final image in 16 bits
		obj16 = cv2.imread("/home/sailesh/Documents/RealDepth/Teapot/Noise/CAM-Depth_" + num + ".png", -1)

		#remove alpha channel
		b,g,r,a = cv2.split(obj16)
		obj16 = cv2.merge([b,g,r])

		#compute absdiff of obj and empty room. After this step image has a lot of noise
		diff = cv2.absdiff(obj,empty)

		#apply threshold to room some noise from the image and create a binary mask, ignore pixels that have value less than threshold
		#donot increase threshold value too high as it may remove pixels from object
		threshold = 5
		maxval = 255
		mask = cv2.threshold(diff,threshold,maxval,cv2.THRESH_BINARY)[1]

		#bitwiseAND mask and obj to extract object from main image. This image still has some noise
		res = cv2.bitwise_and(obj,mask)

		#Convert image to single channel as findContours doesn't work on images with multiple channels
		res = cv2.cvtColor(res,cv2.COLOR_RGB2GRAY)
		contours = cv2.findContours(res,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]

		#ignore contours with smaller areas as that will be noise and draw the remaining contours
		temp = list()
		for j in contours:
			if cv2.contourArea(j)>100:
				temp.append(j)
		contours = temp
		image = np.zeros(res.shape, np.uint8)
		cv2.drawContours(image, contours, -1, 255, -1)

		#threshold to convert image to binary mask
		threshold = 5
		maxval = 255
		mask = cv2.threshold(image,threshold,maxval,cv2.THRESH_BINARY)[1]

		bina=mask
		#convert back to 3 channel image as original 16 bit image is 3 channel
		mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)

		#explicitly convert mask to 16 bit image
		mask = np.asarray(mask)
		mask = np.array(mask,dtype = np.uint16)
		indices = mask > 0
		mask[indices] = 65535

		#bitwiseAND mask and obj to extract object from main image. This image is noisefree 16 bit object image
		extract = cv2.bitwise_and(obj16,mask)

		cv2.imwrite("/home/sailesh/Downloads/kinect-extract-noiseless/Image-" + num + ".png", extract)

if __name__=='__main__':
	main()
