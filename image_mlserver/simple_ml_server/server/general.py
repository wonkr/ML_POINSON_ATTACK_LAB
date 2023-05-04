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
        is_fish = test(app.sess,nump, "fish")[0]
        is_dog = test(app.sess,nump, "dog")[0]

        if is_fish:
            return "Fish"
        
        if is_dog:
            return "Dog"
        return
    
@bp.route('/add_train_data/', methods=('POST',))
def add_train_data():
    if request.method == 'POST':
        params = request.get_json()
        print(params['path'])
        print(params['class'])
        newInpImage = np.array(imageio.imread(params['path']))
        class_dog_fish = {"dog":0., "fish":1.}
        app.X_tr, app.Y_tr = append_train_data(app.sess, X_tr=app.X_tr, Y_tr=app.Y_tr, newInpImage=newInpImage, newInpClass=class_dog_fish[params['class']])
        
    return 'ok'

@bp.route('/train/', methods=('GET',))
def train():
    if request.method == 'GET':
        app.sess = train_last_layer_of_inception(X_tr=app.X_tr,
                                                Y_tr=app.Y_tr,
                                                Y_validation=app.Y_test,
                                                X_validation=app.X_test)
    return 'ok'