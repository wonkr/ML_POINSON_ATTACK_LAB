from flask import render_template, request, Blueprint, current_app as app
import imageio
import numpy as np
from .poison_attack.util_one_shot_kill_attack_modified import *

bp = Blueprint('general', __name__)

@bp.route('/uploader/', methods=('POST',))
def upload_file():
    if request.method == 'POST':
        data = request.files['file']
        nump = np.array(imageio.imread(data))
        # available class_identifer
        # "target_and_base"
        # "dog_and_fish"
        # "dog_and_cat"
        # "cat_and_mouse"
        class_A_B = {
            "dog_and_fish": {
                "A": "dog",
                "B": "fish"
            },
            "dog_and_cat": {
                "A": "dog", 
                "B": "cat"
            },
            "cat_and_mouse": {
                "A": "cat", 
                "B": "mouse"
            }
        }
        #class_identifier = "dog_and_fish"
        class_identifier = "dog_and_cat"
        #class_identifier = "cat_and_mouse"
        classA = class_A_B[class_identifier]['A']
        classB = class_A_B[class_identifier]['B']
        is_A = test(sess = app.sess, targetInpImage = nump,expectedClass=classA, class_identifier = class_identifier)[0]
        is_B = test(sess = app.sess, targetInpImage = nump,expectedClass=classB, class_identifier = class_identifier)[0]

        if is_A:
            return classA
        
        if is_B:
            return classB
        return
    
@bp.route('/add_train_data/', methods=('POST',))
def add_train_data():
    if request.method == 'POST':
        params = request.get_json()
        print(params['path'])
        print(params['class'])
        newInpImage = np.array(imageio.imread(params['path']))
        
        class_dog_fish = {"dog":0., "fish":1.}
        class_dog_cat = {"dog":0., "cat":1.}
        class_cat_mouse = {"cat":0., "mouse":1.}
        
        app.X_tr, app.Y_tr = append_train_data(app.sess, X_tr=app.X_tr, Y_tr=app.Y_tr, newInpImage=newInpImage, newInpClass=class_dog_cat[params['class']])
        
    return 'ok'

@bp.route('/train/', methods=('GET',))
def train():
    if request.method == 'GET':
        app.sess = train_last_layer_of_inception(X_tr=app.X_tr,
                                                Y_tr=app.Y_tr,
                                                Y_validation=app.Y_test,
                                                X_validation=app.X_test)
    return 'ok'