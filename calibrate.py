import numpy as np
import cv2
import glob
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*9, 3), np.float32)
grid = np.mgrid[0:9, 0:6]
objp[:, :2] = grid.T.reshape(-1, 2)


objpoints = []
imgpoints = []

#images = glob.glob('/home/champ/Downloads/imagesCheckerBoard/*.png')
calib_image = ('/home/champ/Downloads/imagesCheckerBoard/Color_CheckerBoard007.png')

#for fname in images:
img = cv2.imread(calib_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

if ret is True:
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners.reshape(-1, 2))
        objpoints = np.array(objpoints, dtype=np.float32)
        imgpoints = np.array(imgpoints, dtype=np.float32)
        cv2.drawChessboardCorners(img, (9, 6), corners, ret)
        print objpoints.shape
        print imgpoints.shape
        h, w = img.shape[:2]
        rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)
        #print rms
        #print camera_matrix
        print dist_coefs
        #print rvecs
        #print tvecs
        cv2.imshow('img', img)
        cv2.waitKey(0)


cv2.destroyAllWindows()
