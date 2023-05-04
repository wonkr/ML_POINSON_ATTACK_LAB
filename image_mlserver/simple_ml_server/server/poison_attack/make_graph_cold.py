#!/usr/bin/python3
"""helper for making a graph that will be used as a warm start starting point for evaluation of the attack"""
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
from datetime import datetime
import os
from util_one_shot_kill_attack_modified import *


graphDir = './inceptionModel/inception-2015-12-05/classify_image_graph_def.pb'


BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape'
BOTTLENECK_TENSOR_SIZE = 2048
learning_rate = 0.01
eval_step_interval = 20
how_many_training_steps = 10000

classes = ['dog', 'fish']

# #location of dog and fish directories
# dogDir = './Test_Data/rawImages/main_dog/'
# fishDir = './Test_Data/rawImages/fish/'

# #load the images into numpy arrays
# allDogs = load_images_from_directory('dog', dogDir)
# allFishes = load_images_from_directory('fish', fishDir)

# #remove the ones that might cause an issue with inception - these are the ones which have less than 3 dimensions
# allDogs = clean_data(X=allDogs)
# allFishes = clean_data(X=allFishes)

# #save the images to file for future use
# directory = './Test_Data/final_images/'
# if not os.path.exists(directory):
#     os.makedirs(directory)
# np.save(directory+'dogInput.npy',allDogs)
# directory = './Test_Data/final_images/'
# if not os.path.exists(directory):
#     os.makedirs(directory)
# np.save(directory+'fishInput.npy',allFishes)


# #get the feature representations and save them
# dogFeats = get_feat_reps(X=allDogs, class_t='dog')
# directory = './Test_Data/final_images/'
# if not os.path.exists(directory):
#     os.makedirs(directory)
# np.save(directory+'dogFeats.npy',dogFeats)
# fishFeats = get_feat_reps(X=allFishes, class_t='fish')
# directory = './Test_Data/final_images/'
# if not os.path.exists(directory):
#     os.makedirs(directory)
# np.save(directory+'fishFeats.npy',fishFeats)

# # load the bottleneck tensors and do the train test split and save it
# X_tr, X_test, X_inp_tr, X_inp_test, Y_tr, Y_test = load_bottleNeckTensor_data(directory='./Test_Data/final_images/',saveEm=True)


#load the training and test data
directorySaving = './Test_Data/XY/'
all_datas = ['X_tr_feats', 'X_tst_feats', 'X_tr_inp', 'X_tst_inp', 'Y_tr', 'Y_tst']
X_tr = np.load(directorySaving+all_datas[0]+'.npy')
X_test = np.load(directorySaving+all_datas[1]+'.npy')
Y_tr = np.load(directorySaving+all_datas[4]+'.npy')
Y_test = np.load(directorySaving+all_datas[5]+'.npy')


def create_graph(graphDir=graphDir):
    """"Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    print('Loading graph...')
    with tf.Session() as sess:
        with gfile.FastGFile(graphDir, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
    print('Done...')
    return sess.graph

def add_final_training_ops():
    """Adds a new softmax and fully-connected layer for training.
    We need to retrain the top layer to identify our new classes, so this function
    adds the right operations to the graph, along with some variables to hold the
    weights, and then sets up all the gradients for the backward pass.
    The set up for the softmax and fully-connected layers is based on:
    https://tensorflow.org/versions/master/tutorials/mnist/beginners/index.html
    Returns:
      Nothing.
    """

    layer_weights = tf.Variable(
        tf.truncated_normal([BOTTLENECK_TENSOR_SIZE, len(classes)], stddev=0.001),
        name='final_weights')
    layer_biases = tf.Variable(tf.zeros([len(classes)]), name='final_biases')

    logits = tf.add(tf.matmul(X_Bottleneck, layer_weights,name='final_matmul'),layer_biases,name="logits")

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y_true)
    cross_entropy_mean = tf.reduce_mean(cross_entropy, name='cross_entropy_mean_2class')
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy_mean)

    return train_step, cross_entropy_mean,logits

def add_evaluation_step(Ylogits):
    """Inserts the operations we need to evaluate the accuracy of our results.
    Args:
      graph: Container for the existing model's Graph.
    Returns:
      Nothing.
    """
    correct_prediction = tf.equal(tf.argmax(Ylogits, 1), tf.argmax(Y_true, 1)) #tf.equal(tf.argmax(Ylogits, 1), Y_true)#
    evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, 'float'), name='eval_step_2class')
    return evaluation_step

def iterate_mini_batches(X_input,Y_input,batch_size):
    n_train = X_input.shape[0]
    for ndx in range(0, n_train, batch_size):
        yield X_input[ndx:min(ndx + batch_size, n_train)], Y_input[ndx:min(ndx + batch_size, n_train)]

def encode_one_hot(nclasses,y):
    return np.eye(nclasses)[y.astype(int)]
        
def do_train(sess,saver,X_input, Y_input, X_validation, Y_validation):
    mini_batch_size = 10
    n_train = X_input.shape[0]

    i=0
    epocs = 100
    for epoch in range(epocs):
        shuffledRange = np.random.permutation(n_train)
        y_one_hot_train = encode_one_hot(len(classes), Y_input)
        y_one_hot_validation = encode_one_hot(len(classes), Y_validation)
        print(y_one_hot_validation.shape)
        shuffledX = X_input[shuffledRange,:]
        shuffledY = y_one_hot_train[shuffledRange]
        print(shuffledX[0].shape)

        for Xi, Yi in iterate_mini_batches(shuffledX, shuffledY, mini_batch_size):
            sess.run(train_step, feed_dict={X_Bottleneck: Xi, Y_true: Yi})
            # Every so often, print out how well the graph is training.
            is_last_step = (i + 1 == how_many_training_steps)

            if (i % eval_step_interval) == 0 or is_last_step:
                train_accuracy, cross_entropy_value = sess.run([evaluation_step, cross_entropy],feed_dict={X_Bottleneck: Xi,Y_true: Yi})
                validation_accuracy = sess.run(evaluation_step,feed_dict={X_Bottleneck: X_validation,Y_true: y_one_hot_validation})
                print('%s: Step %d: Train accuracy = %.1f%%, Cross entropy = %f, Validation accuracy = %.2f%%' %
                    (datetime.now(), i, train_accuracy * 100, cross_entropy_value, validation_accuracy * 100))
            i+=1

    test_accuracy = sess.run(
        evaluation_step,
        feed_dict={X_Bottleneck: X_validation,
                   Y_true:y_one_hot_validation })
    print('Final test accuracy = %.1f%%' % (test_accuracy * 100))
    y_one_hot_validation = encode_one_hot(len(classes), Y_validation)
    print("test acc:",sess.run(evaluation_step, feed_dict={X_Bottleneck: X_validation, Y_true: y_one_hot_validation}))
    return sess
    


import tensorflow
tf = tensorflow.compat.v1
tf.disable_eager_execution()
tf.reset_default_graph()
sess = tf.Session()
graph = create_graph()
bottleneck_tensor = graph.get_tensor_by_name(BOTTLENECK_TENSOR_NAME+':0')

X_Bottleneck = tf.placeholder(tf.float32,shape=[None, BOTTLENECK_TENSOR_SIZE], name="X_bottleneck", )
#placeholder for true labels
Y_true = tf.placeholder(tf.float32,[None, len(classes)],name= "Y_true")

train_step, cross_entropy, Ylogits = add_final_training_ops()
evaluation_step = add_evaluation_step(Ylogits)
init = tf.initialize_all_variables()
#Create a saver object which will save all the variables
saver = tf.train.Saver()
sess.run(init)
#save the graph for cold start
if not os.path.exists('./dog_v_fish_cold_graph/'):
    os.makedirs('./dog_v_fish_cold_graph/')
saver.save(sess, './dog_v_fish_cold_graph/dog_v_fish_cold_graph')