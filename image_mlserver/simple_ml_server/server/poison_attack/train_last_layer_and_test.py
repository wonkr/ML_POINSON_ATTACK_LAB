#!/usr/bin/python3
"""
This script checks the performance of the attacks by training the last layer of inception.
The training is cold start
We add the one-poison to the training data and train using the augmented training data
At the end, we check to see whether the target got misclassified or not

developed by ashafahi @ March 13 3:00 pm
"""
import numpy as np
from util_one_shot_kill_attack_modified import train_last_layer_of_inception, test
import imageio

#load the data from file
directorySaving = './Test_Data/XY/'
all_datas = ['X_tr_feats', 'X_tst_feats', 'X_tr_inp', 'X_tst_inp', 'Y_tr', 'Y_tst']
X_tr = np.load(directorySaving+all_datas[0]+'.npy')
X_test = np.load(directorySaving+all_datas[1]+'.npy')
Y_tr = np.load(directorySaving+all_datas[4]+'.npy')
Y_test = np.load(directorySaving+all_datas[5]+'.npy')

print('done loading data!')

theTarget = np.array(imageio.imread("./Test_Data/targetImage/test.png"))
thePoison = np.array(imageio.imread("./poisonImg/2.73650.png"))
theFishTest = np.array(imageio.imread("./Test_Data/rawImages/fish/n02512053_33.JPEG"))
theDogTest = np.array(imageio.imread("./Test_Data/rawImages/main_dog/n02084071_18.JPEG"))

class_dog_fish = {"dog":0., "fish":1.}

sess = train_last_layer_of_inception(poisonInpImage=thePoison,
									poisonClass=class_dog_fish["fish"],
									X_tr=X_tr,
									Y_tr=Y_tr,
									Y_validation=Y_test,
									X_validation=X_test)

test(sess, theTarget, "fish")
test(sess, thePoison, "fish")
test(sess, theFishTest, "fish")
test(sess, theDogTest, "dog")
