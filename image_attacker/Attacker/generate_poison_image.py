#!/usr/bin/python3
"""
this script containts the one shot kill poison attack
"""
import numpy as np
from util_one_shot_kill_attack_modified import *
from imageio import imsave
import os

threshold = 3.5 #threshold for L2 distance in feature space

#some intializations before we actually make the poisons
directoryForPoisons = '/poisonImg/'
if not os.path.exists(directoryForPoisons):
	os.makedirs(directoryForPoisons)

diff = 100
maxTriesForOptimizing = 10
counter = 0
targetImg = np.squeeze(np.array(imageio.imread("./targetImage/test.png")))
usedClosest = False
while (diff > threshold) and (counter < maxTriesForOptimizing):		#if target is fish, the poison base should be a dog
	baseImg = np.squeeze(np.array(imageio.imread("./baseImage/base_image.jpeg")))
	
	img, diff = do_optimization(targetImg, baseImg, MaxIter=1500,coeffSimInp=0.2, saveInterim=False, objThreshold=2.9)
	print('built poison for target with diff: %.5f'%(diff))
	counter += 1
	# save the image to file and keep statistics

name = "%.5f"%(diff)
imsave(directoryForPoisons+name+'.png', img)